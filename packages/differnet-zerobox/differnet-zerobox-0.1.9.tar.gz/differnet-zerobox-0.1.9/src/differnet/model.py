import os
import torch
import torch.nn.functional as F
from torch import nn
from torchvision.models import alexnet

from differnet.freia_funcs import (
    permute_layer,
    glow_coupling_layer,
    F_fully_connected,
    ReversibleGraphNet,
    OutputNode,
    InputNode,
    Node,
)

from datetime import datetime
import matplotlib.pyplot as plt
import json


class DifferNet(nn.Module):
    def __init__(self, conf, name="default"):
        super(DifferNet, self).__init__()
        self.conf = conf
        self.name = name
        self.device = self.conf.get("device", "cpu")
        if self.device == "cuda":
            torch.cuda.set_device(self.conf.get("device_id"))
        self.weight_dir = conf.get("weight_dir", f"./work/{self.name}/weight")
        self.model_dir = conf.get("model_dir", f"./work/{self.name}/models")
        self.feature_extractor = alexnet(pretrained=True)
        self.nf = self.nf_head()

    def nf_head(self):
        input_dim = self.conf.get("n_feat")
        nodes = list()
        nodes.append(InputNode(input_dim, name="input"))
        for k in range(self.conf.get("n_coupling_blocks")):
            nodes.append(
                Node([nodes[-1].out0], permute_layer, {"seed": k}, name=f"permute_{k}")
            )
            nodes.append(
                Node(
                    [nodes[-1].out0],
                    glow_coupling_layer,
                    {
                        "clamp": self.conf.get("clamp_alpha"),
                        "F_class": F_fully_connected,
                        "F_args": {
                            "internal_size": self.conf.get("fc_internal"),
                            "dropout": self.conf.get("dropout"),
                        },
                    },
                    name=f"fc_{k}",
                )
            )
        nodes.append(OutputNode([nodes[-1].out0], name="output"))
        coder = ReversibleGraphNet(nodes)

        return coder

    def forward(self, x):
        y_cat = list()

        for s in range(self.conf.get("n_scales")):
            x_scaled = (
                F.interpolate(x, size=self.conf.get("img_size")[0] // (2 ** s))
                if s > 0
                else x
            )
            feat_s = self.feature_extractor.features(x_scaled)
            y_cat.append(torch.mean(feat_s, dim=(2, 3)))

        y = torch.cat(y_cat, dim=1)
        z = self.nf(y)
        return z

    def save_model(self, model, filename):
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
        torch.save(model, os.path.join(self.model_dir, filename))

    def load_model(self, filename):
        path = os.path.join(self.model_dir, filename)
        model = torch.load(path)
        return model

    def save_weights(self, model, filename):
        if not os.path.exists(self.weight_dir):
            os.makedirs(self.weight_dir)
        torch.save(model.state_dict(), os.path.join(self.weight_dir, filename))

    def load_weights(self, model, filename):
        path = os.path.join(self.weight_dir, filename)
        model.load_state_dict(torch.load(path))
        return model

    def save_parameters(self, model_parameters, filename):
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

        with open(os.path.join(self.model_dir, filename + ".json"), "w") as jsonfile:
            jsonfile.write(json.dumps(model_parameters, indent=4))

    def save_roc_plot(self, fpr, tpr, filename):
        plt.figure()
        lw = 2
        plt.figure(figsize=(10, 10))
        plt.plot(
            fpr.tolist(), tpr.tolist(), color="darkorange", lw=lw, label="ROC curve"
        )
        plt.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.0])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curve")
        plt.legend(loc="lower right")
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")
        # plt.savefig(MODEL_DIR + '/' +filename + '_ROC_' + dt_string + '.jpg')
        plt.savefig(self.model_dir + "/" + filename + "_ROC.jpg")
