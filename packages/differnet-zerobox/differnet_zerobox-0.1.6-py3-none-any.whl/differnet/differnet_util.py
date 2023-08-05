from unicodedata import name
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from torchvision import datasets, transforms
from torch.autograd import Variable
from PIL import Image
import torch
import numpy as np
import scipy
import matplotlib.pyplot as plt
from operator import itemgetter
import cv2
import os
from datetime import datetime
import time
import gc
from tqdm import tqdm
from .multi_transform_loader import ImageFolderMultiTransform
from .default_conf import default_conf
from .model import DifferNet

# import logging
import logging

logger = logging.getLogger(__name__)


def TransformShow(name="img", wait=100):
    def transform_show(img):
        # path = "transform/"
        # now = datetime.now()
        # dt_string = now.strftime("%d%m%Y%H%M%S")
        # cv2.imwrite(path + 'all_transform_' + dt_string + '.jpg', np.array(img))
        # cv2.imshow(name, np.array(img))
        # cv2.waitKey(wait)
        return img

    return transform_show


def cropImage(conf: dict):
    def crop_image(img):
        TRANSFORM_DIR = os.path.join(conf.get("differnet_work_dir"), "transform")
        x, y, w, h = shrinkEdges(img.size, conf)
        rs = transforms.functional.crop(img, y, x, h, w)

        if not os.path.exists(TRANSFORM_DIR):
            os.makedirs(TRANSFORM_DIR)

        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")
        if conf.get("save_transformed_image", False):
            cv2.imwrite(
                os.path.join(TRANSFORM_DIR, "transform_" + dt_string + ".jpg"),
                np.array(rs),
            )
        return rs

    return crop_image


def shrinkEdges(img_size, conf: dict):
    width, height = img_size
    shrink_scale_top = conf.get("crop_top")
    shrink_scale_bot = conf.get("crop_bottom")
    shrink_scale_left = conf.get("crop_left")
    shrink_scale_right = conf.get("crop_right")
    left_reduction = shrink_scale_left * width
    right_reduction = shrink_scale_right * width
    top_reduction = shrink_scale_top * height
    bot_reduction = shrink_scale_bot * height
    new_height = int(height - top_reduction - bot_reduction)
    new_width = int(width - left_reduction - right_reduction)
    new_ul_x = int(left_reduction)
    new_ul_y = int(top_reduction)
    # print(
    #    f"shrinking {0, 0, width, height} to {new_ul_x, new_ul_y, new_width, new_height}"
    # )
    return new_ul_x, new_ul_y, new_width, new_height


class Score_Observer:
    """Keeps an eye on the current and highest score so far"""

    def __init__(self, name):
        self.name = name
        self.max_epoch = 0
        self.max_score = None
        self.last = None

    def update(self, score, epoch, print_score=False):
        self.last = score
        if epoch == 0 or score > self.max_score:
            self.max_score = score
            self.max_epoch = epoch
        if print_score:
            self.print_score()

    def print_score(self):
        print(
            "{:s}: \t last: {:.4f} \t max: {:.4f} \t epoch_max: {:d}".format(
                self.name, self.last, self.max_score, self.max_epoch
            )
        )


class DiffernetUtil(object):
    def __init__(self, conf: dict, model_name: str) -> None:
        super().__init__()
        self.model_name = model_name
        # load conf
        self._loadConf(dt=conf)
        self.work_folder = self.conf.get("differnet_work_dir", "./work")
        self.tranform_folder = os.path.join(self.work_folder, model_name, "transform")
        self.gradient_map_dir = os.path.join(self.work_folder, model_name, "gradient")
        self.model_dir = os.path.join(self.work_folder, model_name, "model")
        self.weight_dir = os.path.join(self.work_folder, model_name, "weight")
        self.train_dir = os.path.join(self.work_folder, self.model_name, "train")
        self.validate_dir = os.path.join(self.work_folder, self.model_name, "validate")
        self.test_dir = os.path.join(self.work_folder, self.model_name, "test")

        self.conf["model_dir"] = self.model_dir
        self.conf["weight_dir"] = self.model_dir

        # device
        self.device = self.conf.get("device", "cpu")
        if self.device == "cuda":
            torch.cuda.set_device(self.conf.get("device_id"))

        # self.class_perm = list()
        self.transform_train = self._initTransForm()

        # preload model
        self.model = None

    # def _target_transform(self, target):
    #     return self.class_perm[target]

    def _loadConf(self, dt: dict):
        self.conf = {}
        for key in default_conf.keys():
            self.conf[key] = default_conf.get(key)

        for key in dt.keys():
            self.conf[key] = dt.get(key)

    def _initTransForm(self):
        augmentative_transforms = []
        if self.conf.get("transf_rotations"):
            augmentative_transforms += [
                transforms.RandomRotation(self.conf.get("rotation_degree"))
            ]

        if (
            self.conf.get("transf_brightness") > 0.0
            or self.conf.get("transf_contrast") > 0.0
            or self.conf.get("transf_saturation") > 0.0
        ):
            augmentative_transforms += [
                transforms.ColorJitter(
                    brightness=self.conf.get("transf_brightness"),
                    contrast=self.conf.get("transf_contrast"),
                    saturation=self.conf.get("transf_saturation"),
                )
            ]

        tfs = (
            [cropImage(self.conf), transforms.Resize(self.conf.get("img_size"))]
            + augmentative_transforms
            + [
                TransformShow("Transformed Image", 10),
                transforms.ToTensor(),
                transforms.Normalize(
                    self.conf.get("norm_mean"), self.conf.get("norm_std")
                ),
            ]
        )

        transform_train = transforms.Compose(tfs)
        return transform_train

    def load_datasets(self, with_validateset: bool):
        """
        work_folder/model_name/train/any_filename.png
        work_folder/model_name/train/another_filename.tif
        work_folder/model_name/train/xyz.png
        work_folder/model_name/validate/good/any_filename.png
        work_folder/model_name/validate/bad/any_filename.png
        """

        data_dir_train = self.train_dir
        data_dir_validate = self.validate_dir
        # data_dir_test = os.path.join(self.work_folder, category_id, "test")
        def target_transform(target):
            return class_perm[target]

        if with_validateset:
            classes = os.listdir(data_dir_validate)
        else:
            classes = os.listdir(data_dir_train)

        if "good" not in classes:
            print(
                'There should exist a subdirectory "good". Read the doc of this function for further information.'
            )
            exit()
        classes.sort()
        class_perm = list()
        class_idx = 1
        for cl in classes:
            if cl == "good":
                class_perm.append(0)
            else:
                class_perm.append(class_idx)
                class_idx += 1

        trainset = None
        validateset = None

        trainset = ImageFolderMultiTransform(
            conf=self.conf,
            root=data_dir_train,
            transform=self.transform_train,
            n_transforms=self.conf.get("n_transforms"),
        )

        if with_validateset:
            validateset = ImageFolderMultiTransform(
                conf=self.conf,
                root=data_dir_validate,
                transform=self.transform_train,
                target_transform=target_transform,
                n_transforms=self.conf.get("n_transforms_test"),
            )

        return trainset, validateset

    def load_testsets(self):
        """
        work_folder/model_name/test/good/any_filename.png
        work_folder/model_name/test/bad/another_filename.tif
        work_folder/model_name/test/bad/xyz.png
        """

        data_dir_test = self.test_dir

        def target_transform(target):
            return class_perm[target]

        classes = os.listdir(data_dir_test)
        if "good" not in classes:
            print(
                'There should exist a subdirectory "good". Read the doc of this function for further information.'
            )
            exit()
        classes.sort()
        class_perm = list()
        class_idx = 1
        for cl in classes:
            if cl == "good":
                class_perm.append(0)
            else:
                class_perm.append(class_idx)
                class_idx += 1

        testset = ImageFolderMultiTransform(
            conf=self.conf,
            root=data_dir_test,
            transform=self.transform_train,
            target_transform=target_transform,
            n_transforms=self.conf.get("n_transforms_test"),
        )

        return testset

    def make_dataloaders(self, trainset, validateset):
        trainloader = torch.utils.data.DataLoader(
            trainset,
            pin_memory=True,
            batch_size=self.conf.get("batch_size"),
            shuffle=True,
            drop_last=False,
        )

        validateloader = None

        if validateset is not None:
            validateloader = torch.utils.data.DataLoader(
                validateset,
                pin_memory=True,
                batch_size=self.conf.get("batch_size"),
                shuffle=True,
                drop_last=False,
            )

        return trainloader, validateloader

    def make_testloaders(self, testset):
        testloader = torch.utils.data.DataLoader(
            testset,
            pin_memory=True,
            batch_size=self.conf.get("batch_size_test"),
            shuffle=False,
            drop_last=False,
        )
        return testloader

    def _preprocess_batch(self, data):
        """move data to device and reshape image"""
        inputs, labels = data
        # print(f"begin: size of inputs={inputs.size()}")
        inputs, labels = inputs.to(self.conf.get("device")), labels.to(
            self.conf.get("device")
        )

        # print(f"to: size of inputs={inputs.size()}")
        inputs = inputs.view(-1, *inputs.shape[-3:])
        # print(f"view: size of inputs={inputs.size()}")
        return inputs, labels

    def _get_loss(self, z, jac):
        """check equation 4 of the paper why this makes sense - oh and just ignore the scaling here"""
        return torch.mean(0.5 * torch.sum(z ** 2, dim=(1,)) - jac) / z.shape[1]

    def _t2np(self, tensor):
        """pytorch tensor -> numpy array"""
        return tensor.cpu().data.numpy() if tensor is not None else None

    def train(self, train_loader, validate_loader=None):
        model = DifferNet(self.conf, name=self.model_name)
        model_parameters = None
        optimizer = torch.optim.Adam(
            [{"params": model.nf.parameters()}],
            lr=self.conf.get("lr_init"),
            betas=(0.8, 0.8),
            eps=1e-04,
            weight_decay=1e-5,
        )
        model.to(self.conf.get("device"))

        # todo: learning rate
        score_obs = Score_Observer("AUROC")

        for epoch in range(self.conf.get("meta_epochs")):

            # train some epochs
            model.train()
            if self.conf.get("verbose"):
                print(f"\nTrain epoch {epoch}")
            for sub_epoch in range(self.conf.get("sub_epochs")):
                train_loss = list()
                for i, data in enumerate(
                    tqdm(train_loader, disable=self.conf.get("hide_tqdm_bar"))
                ):
                    optimizer.zero_grad()
                    inputs, labels = self._preprocess_batch(data)
                    # move to device and reshape
                    z = model(inputs)
                    loss = self._get_loss(z, model.nf.jacobian(run_forward=False))
                    train_loss.append(self._t2np(loss))
                    loss.backward()
                    optimizer.step()

                mean_train_loss = np.mean(train_loss)
                if self.conf.get("verbose"):
                    print(
                        "Epoch: {:d}.{:d} \t train loss: {:.4f}".format(
                            epoch, sub_epoch, mean_train_loss
                        )
                    )

            if not (validate_loader is None):
                # evaluate
                model.eval()
                if self.conf.get("verbose"):
                    print("\nCompute loss and scores on validate set:")
                test_loss = list()
                test_z = list()
                test_labels = list()
                with torch.no_grad():
                    for i, data in enumerate(
                        tqdm(validate_loader, disable=self.conf.get("hide_tqdm_bar"))
                    ):
                        inputs, labels = self._preprocess_batch(data)
                        z = model(inputs)
                        loss = self._get_loss(z, model.nf.jacobian(run_forward=False))
                        test_z.append(z)
                        test_loss.append(self._t2np(loss))
                        test_labels.append(self._t2np(labels))

                test_loss = np.mean(np.array(test_loss))

                test_labels = np.concatenate(test_labels)
                is_anomaly = np.array([0 if l == 0 else 1 for l in test_labels])

                z_grouped = torch.cat(test_z, dim=0).view(
                    -1, self.conf.get("n_transforms_test"), self.conf.get("n_feat")
                )
                anomaly_score = self._t2np(torch.mean(z_grouped ** 2, dim=(-2, -1)))
                AUROC = roc_auc_score(is_anomaly, anomaly_score)
                score_obs.update(
                    AUROC,
                    epoch,
                    print_score=self.conf.get("verbose")
                    or epoch == self.conf.get("meta_epochs") - 1,
                )

                fpr, tpr, thresholds = roc_curve(is_anomaly, anomaly_score)
                model_parameters = {}
                model_parameters["fpr"] = fpr.tolist()
                model_parameters["tpr"] = tpr.tolist()
                model_parameters["thresholds"] = thresholds.tolist()
                model_parameters["AUROC"] = AUROC

                if epoch == self.conf.get("meta_epochs") - 1:
                    model.save_parameters(model_parameters, self.model_name)
                    model.save_roc_plot(
                        fpr, tpr, self.model_name + "_{:.4f}".format(AUROC)
                    )

                if self.conf.get("verbose"):
                    print(
                        "Epoch: {:d} \t validate_loss: {:.4f}".format(epoch, test_loss)
                    )

                    # compare is_anomaly and anomaly_score
                    np.set_printoptions(precision=2, suppress=True)
                    print("is_anomaly:    ", is_anomaly)
                    print("anomaly_score: ", anomaly_score)
                    print("fpr:           ", fpr)
                    print("tpr:           ", tpr)
                    print("thresholds:    ", thresholds)

        if self.conf.get("grad_map_viz") and not (validate_loader is None):
            self.export_gradient_maps(model, validate_loader, optimizer, 1)

        if self.conf.get("save_model"):
            model.to("cpu")
            model.save_model(model, self.model_name + ".pth")
            model.save_weights(model, self.model_name + ".weights.pth")

        return model, model_parameters

    def train_model(self, with_validateset=True):
        train_set, validate_set = self.load_datasets(with_validateset)
        train_loader, validate_loader = self.make_dataloaders(train_set, validate_set)

        time_start = time.time()
        model, model_parameters = self.train(train_loader, validate_loader)

        time_end = time.time()
        time_c = time_end - time_start  # 运行所花时间
        logger.debug(f"Train time cost: {time_c} s")

        # free memory
        del train_set
        del validate_set
        del train_loader
        del validate_loader

        gc.collect()
        torch.cuda.empty_cache()

    def _test_model_noparameterjson(self, model, test_loader, target_threshold=10):
        print("Running test")
        optimizer = torch.optim.Adam(
            model.nf.parameters(),
            lr=self.conf.get("lr_init"),
            betas=(0.8, 0.8),
            eps=1e-04,
            weight_decay=1e-5,
        )
        model.to(self.conf.get("device"))
        model.eval()
        if self.conf.get("verbose"):
            print("\nCompute loss and scores on test set:")
        test_z = list()
        test_labels = list()
        predictions = []
        with torch.no_grad():
            for i, data in enumerate(test_loader):
                inputs, labels = self._preprocess_batch(data)
                if self.conf.get("frame_name_is_given"):
                    frame = int(
                        test_loader.dataset.imgs[i][0]
                        .split("frame", 1)[1]
                        .split("-")[0]
                    )
                frame = i
                # print(f"i={i}: frame#={frame}, labels={labels.cpu().numpy()[0]}, size of inputs={inputs.size()}")
                predictions.append(
                    [
                        frame,
                        test_loader.dataset.imgs[i][0],
                        labels.cpu().numpy()[0],
                        0,
                        0,
                    ]
                )
                z = model(inputs)
                test_z.append(z)
                test_labels.append(self._t2np(labels))

        test_labels = np.concatenate(test_labels)
        is_anomaly = np.array([0 if l == 0 else 1 for l in test_labels])

        z_grouped = torch.cat(test_z, dim=0).view(
            -1, self.conf.get("n_transforms_test"), self.conf.get("n_feat")
        )
        anomaly_score = self._t2np(torch.mean(z_grouped ** 2, dim=(-2, -1)))
        AUROC = roc_auc_score(is_anomaly, anomaly_score)
        fpr, tpr, thresholds = roc_curve(is_anomaly, anomaly_score)
        model.save_roc_plot(fpr, tpr, self.model_name + "_{:.4f}_test".format(AUROC))

        is_anomaly_detected = []
        i = 0
        for l in anomaly_score:
            predictions[i][4] = l
            if l < target_threshold:
                is_anomaly_detected.append(0)
                predictions[i][3] = 0
            else:
                is_anomaly_detected.append(1)
                predictions[i][3] = 1
            i += 1
        predictions = sorted(predictions, key=itemgetter(0))

        # calculate test accuracy
        error_count = 0
        for i in range(len(is_anomaly)):
            if is_anomaly[i] != is_anomaly_detected[i]:
                error_count += 1

        test_accuracy = 1 - float(error_count) / len(is_anomaly)

        for i in range(len(predictions)):
            msg = "frame: " + str(i) + ". "
            if predictions[i][3] == 1:
                msg += "prediction: defective. "
            else:
                msg += "prediction: good. "

            if predictions[i][2] == 1:
                msg += "ground truth: defective. "
            else:
                msg += "ground truth: good. "

            msg += "anomaly score: " + str(round(predictions[i][4], 4)) + ". "
            msg += "threshold: " + str(round(target_threshold, 4)) + ". "
            msg += "accuracy: " + str(round(test_accuracy * 100, 2)) + "%"

            print(msg)

        # print(f"test_labels={test_labels}, is_anomaly={is_anomaly},anomaly_score={anomaly_score},is_anomaly_detected={is_anomaly_detected}")
        print(
            f"target_tpr={self.conf.get('target_tpr')}, target_threshold={target_threshold}, test_accuracy={test_accuracy}"
        )
        if self.conf.get("grad_map_viz"):
            print("saving gradient maps...")
            self.export_gradient_maps(model, test_loader, optimizer, -1)

    def _test_model(self, model, model_parameters, test_loader):
        print("Running test")
        optimizer = torch.optim.Adam(
            model.nf.parameters(),
            lr=self.conf.get("lr_init"),
            betas=(0.8, 0.8),
            eps=1e-04,
            weight_decay=1e-5,
        )
        model.to(self.conf.get("device"))
        model.eval()
        if self.conf.get("verbose"):
            print("\nCompute loss and scores on test set:")
        test_z = list()
        test_labels = list()
        predictions = []
        with torch.no_grad():
            for i, data in enumerate(test_loader):
                inputs, labels = self._preprocess_batch(data)
                if self.conf.get("frame_name_is_given"):
                    frame = int(
                        test_loader.dataset.imgs[i][0]
                        .split("frame", 1)[1]
                        .split("-")[0]
                    )
                frame = i
                # print(f"i={i}: frame#={frame}, labels={labels.cpu().numpy()[0]}, size of inputs={inputs.size()}")
                predictions.append(
                    [
                        frame,
                        test_loader.dataset.imgs[i][0],
                        labels.cpu().numpy()[0],
                        0,
                        0,
                    ]
                )
                z = model(inputs)
                test_z.append(z)
                test_labels.append(self._t2np(labels))

        test_labels = np.concatenate(test_labels)
        is_anomaly = np.array([0 if l == 0 else 1 for l in test_labels])

        z_grouped = torch.cat(test_z, dim=0).view(
            -1, self.conf.get("n_transforms_test"), self.conf.get("n_feat")
        )
        anomaly_score = self._t2np(torch.mean(z_grouped ** 2, dim=(-2, -1)))
        AUROC = roc_auc_score(is_anomaly, anomaly_score)
        fpr, tpr, thresholds = roc_curve(is_anomaly, anomaly_score)
        model.save_roc_plot(fpr, tpr, self.model_name + "_{:.4f}_test".format(AUROC))

        for i in range(len(model_parameters["tpr"])):
            if model_parameters["tpr"][i] > self.conf.get("target_tpr"):
                target_threshold = model_parameters["thresholds"][i]
                break

        is_anomaly_detected = []
        i = 0
        for l in anomaly_score:
            predictions[i][4] = l
            if l < target_threshold:
                is_anomaly_detected.append(0)
                predictions[i][3] = 0
            else:
                is_anomaly_detected.append(1)
                predictions[i][3] = 1
            i += 1
        predictions = sorted(predictions, key=itemgetter(0))

        # calculate test accuracy
        error_count = 0
        for i in range(len(is_anomaly)):
            if is_anomaly[i] != is_anomaly_detected[i]:
                error_count += 1

        test_accuracy = 1 - float(error_count) / len(is_anomaly)

        for i in range(len(predictions)):
            msg = "frame: " + str(i) + ". "
            if predictions[i][3] == 1:
                msg += "prediction: defective. "
            else:
                msg += "prediction: good. "

            if predictions[i][2] == 1:
                msg += "ground truth: defective. "
            else:
                msg += "ground truth: good. "

            msg += "anomaly score: " + str(round(predictions[i][4], 4)) + ". "
            msg += "threshold: " + str(round(target_threshold, 4)) + ". "
            msg += "accuracy: " + str(round(test_accuracy * 100, 2)) + "%"

            print(msg)

        # print(f"test_labels={test_labels}, is_anomaly={is_anomaly},anomaly_score={anomaly_score},is_anomaly_detected={is_anomaly_detected}")
        print(
            f"target_tpr={self.conf.get('target_tpr')}, target_threshold={target_threshold}, test_accuracy={test_accuracy}"
        )
        if self.conf.get("grad_map_viz"):
            print("saving gradient maps...")
            self.export_gradient_maps(model, test_loader, optimizer, -1)

        # visualize the prediction result
        if self.conf.get("visualization"):
            for i in range(len(predictions)):
                # load file path
                file_path = predictions[i][1]
                idx = file_path.index("video")
                file_path = file_path[:idx] + "original-" + file_path[idx:]
                file_path = file_path.replace("test\\test", "zerobox-2010-1-original")

                # rotate and resize image
                img = cv2.imread(file_path)
                img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
                img = cv2.resize(img, (600, 900))

                # display prediction on each frame
                font = cv2.FONT_HERSHEY_DUPLEX
                font_size = 0.65
                pos_x = 330
                if predictions[i][3] == 1:
                    img = cv2.putText(
                        img,
                        "prediction: defective",
                        (pos_x, 810),
                        font,
                        font_size,
                        (0, 0, 255),
                        1,
                        cv2.LINE_AA,
                    )
                else:
                    img = cv2.putText(
                        img,
                        "prediction: good",
                        (pos_x, 810),
                        font,
                        font_size,
                        (0, 255, 0),
                        1,
                        cv2.LINE_AA,
                    )

                if predictions[i][2] == 1:
                    img = cv2.putText(
                        img,
                        "ground truth: defective",
                        (pos_x, 830),
                        font,
                        font_size,
                        (0, 0, 255),
                        1,
                        cv2.LINE_AA,
                    )
                else:
                    img = cv2.putText(
                        img,
                        "ground truth: good",
                        (pos_x, 830),
                        font,
                        font_size,
                        (0, 255, 0),
                        1,
                        cv2.LINE_AA,
                    )

                img = cv2.putText(
                    img,
                    "anomaly score: " + str(round(predictions[i][4], 4)),
                    (pos_x, 850),
                    font,
                    font_size,
                    (0, 255, 0),
                    1,
                    cv2.LINE_AA,
                )
                img = cv2.putText(
                    img,
                    "threshold: " + str(round(target_threshold, 4)),
                    (pos_x, 870),
                    font,
                    font_size,
                    (0, 255, 0),
                    1,
                    cv2.LINE_AA,
                )
                img = cv2.putText(
                    img,
                    "accuracy: " + str(round(test_accuracy * 100, 2)) + "%",
                    (pos_x, 890),
                    font,
                    font_size,
                    (0, 255, 0),
                    1,
                    cv2.LINE_AA,
                )
                # show results
                cv2.imshow("window", img)
                cv2.waitKey(220)

    def test_model(self):
        test_set = self.load_testsets()
        test_loader = self.make_testloaders(test_set)

        model = torch.load(
            os.path.join(self.model_dir, self.model_name + ".pth"),
            map_location=torch.device("cpu"),
        )
        # changed logic for test with only test_anormaly_target parameter from conf default 10
        time_start = time.time()
        self._test_model_noparameterjson(
            model,
            test_loader,
            target_threshold=self.conf.get("test_anormaly_target"),
        )
        time_end = time.time()
        time_c = time_end - time_start

        # Logic to test with model-name.json
        # model_parameters = None
        # parfile = os.path.join(self.model_dir, self.model_name + ".json")
        # if os.path.exists(parfile):
        #     with open(parfile) as jsonfile:
        #         model_parameters = json.load(jsonfile)

        #     time_start = time.time()
        #     self._test_model(model, model_parameters, test_loader)
        #     time_end = time.time()
        #     time_c = time_end - time_start
        # else:
        #     time_start = time.time()
        #     self._test_model_noparameterjson(
        #         model,
        #         test_loader,
        #         target_threshold=self.conf.get("test_anormaly_target"),
        #     )
        #     time_end = time.time()
        #     time_c = time_end - time_start
        print("testing time cost: {:f} s".format(time_c))

        # free memory
        del test_set
        del test_loader

        gc.collect()
        torch.cuda.empty_cache()

    def _save_gradient_imgs(self, inputs, grad, cnt):
        export_dir = self.gradient_map_dir
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        for g in range(grad.shape[0]):
            normed_grad = (grad[g] - np.min(grad[g])) / (
                np.max(grad[g]) - np.min(grad[g])
            )
            orig_image = inputs[g]
            for image, file_suffix in [
                (normed_grad, "_gradient_map.png"),
                (orig_image, "_orig.png"),
            ]:
                plt.clf()
                plt.imshow(image)
                plt.axis("off")
                plt.savefig(
                    os.path.join(export_dir, str(cnt) + file_suffix),
                    bbox_inches="tight",
                    pad_inches=0,
                )
            cnt += 1
        return cnt

    def export_gradient_maps(self, model, testloader, optimizer, n_batches=1):
        plt.figure(figsize=(10, 10))
        testloader.dataset.get_fixed = False
        cnt = 0
        degrees = (
            -1
            * np.arange(self.conf.get("n_transforms_test"))
            * 360.0
            / self.conf.get("n_transforms_test")
        )

        # TODO n batches
        for i, data in enumerate(
            tqdm(testloader, disable=self.conf.get("hide_tqdm_bar"))
        ):
            optimizer.zero_grad()
            inputs, labels = self._preprocess_batch(data)
            inputs = Variable(inputs, requires_grad=True)

            emb = model(inputs)
            loss = self._get_loss(emb, model.nf.jacobian(run_forward=False))
            loss.backward()

            grad = inputs.grad.view(
                -1, self.conf.get("n_transforms_test"), *inputs.shape[-3:]
            )
            grad = grad[labels >= 0]
            if grad.shape[0] == 0:
                continue
            grad = self._t2np(grad)

            inputs = inputs.view(
                -1, self.conf.get("n_transforms_test"), *inputs.shape[-3:]
            )[:, 0]
            inputs = np.transpose(self._t2np(inputs[labels >= 0]), [0, 2, 3, 1])
            inputs_unnormed = np.clip(
                inputs * self.conf.get("norm_std") + self.conf.get("norm_mean"), 0, 1
            )

            for i_item in range(self.conf.get("n_transforms_test")):
                old_shape = grad[:, i_item].shape
                img = np.reshape(grad[:, i_item], [-1, *grad.shape[-2:]])
                img = np.transpose(img, [1, 2, 0])
                img = np.transpose(
                    scipy.ndimage.rotate(img, degrees[i_item], reshape=False), [2, 0, 1]
                )
                img = scipy.ndimage.gaussian_filter(img, (0, 3, 3))
                grad[:, i_item] = np.reshape(img, old_shape)

            grad = np.reshape(grad, [grad.shape[0], -1, *grad.shape[-2:]])
            grad_img = np.mean(np.abs(grad), axis=1)
            grad_img_sq = grad_img ** 2

            cnt = self._save_gradient_imgs(inputs_unnormed, grad_img_sq, cnt)

            if i == n_batches:
                break

        plt.close()
        testloader.dataset.get_fixed = False

    # def defectDetectOnProductOnly(self, productImage, differnetModel):
    #     img_detect_result = None
    #     defectBoxes = []
    #     findDefect, _ = self.defectDetectionDifferNet(
    #         differnetModel.model, differnetModel.anomaly_threshold, productImage
    #     )
    #     img_detect_result = productImage
    #     # Differnet does not know where the defect is: use the whole
    #     height, width, _ = productImage.shape
    #     if findDefect:
    #         defectBoxes = [
    #             (0, 0, width, height)
    #         ]  # We don't know the defect box using differnet
    #     else:
    #         defectBoxes = []

    #     return findDefect, img_detect_result, defectBoxes

    def _loadTestInputsFromImageWithFixedRotation(self, sample):
        """
        input:
            sample: PIL Image object
        return:
            samples: list of torch tensors after transformations, including rotations
        """

        # 1. Define the transformations
        augmentative_transforms = []
        if self.conf.get("transf_rotations"):
            augmentative_transforms += [
                transforms.RandomRotation(self.conf.get("rotation_degree"))
            ]

        if (
            self.conf.get("transf_brightness") > 0.0
            or self.conf.get("transf_contrast") > 0.0
            or self.conf.get("transf_saturation") > 0.0
        ):
            augmentative_transforms += [
                transforms.ColorJitter(
                    brightness=self.conf.get("transf_brightness"),
                    contrast=self.conf.get("transf_contrast"),
                    saturation=self.conf.get("transf_saturation"),
                )
            ]

        tfs = (
            [cropImage(self.conf), transforms.Resize(self.conf.get("img_size"))]
            + augmentative_transforms
            + [
                transforms.ToTensor(),
                transforms.Normalize(
                    self.conf.get("norm_mean"), self.conf.get("norm_std")
                ),
            ]
        )

        # 2.  transfrom from a single sample to a set of samples
        samples = list()

        for _ in range(self.conf.get("n_transforms_test")):
            samples.append(transforms.Compose(tfs)(sample))

        samples = torch.stack(samples, dim=0)

        return samples

    def load_model(self):
        # 1. load model
        self.model = torch.load(
            os.path.join(self.model_dir, self.model_name + ".pth"),
            # map_location=torch.device("cpu"),
        )
        self.model.to(self.device)
        self.model.eval()

    def detect(self, cv2image, anomaly_threshold=10):
        findDefect = False
        # 1. load model
        if self.model is None:
            self.load_model()

        # 2. convert cv2image to pillow image
        # no rotating, it is the caller's job to convert it
        # cv2image = cv2.rotate(cv2image, cv2.ROTATE_90_CLOCKWISE)
        imgRGB = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(
            imgRGB
        )  # PIL Image type: such as <PIL.Image.Image image mode=RGB size=454x823 at 0x23DA6A260D0>

        inputs = self._loadTestInputsFromImageWithFixedRotation(pil_image)

        # this sets the first dimension which is size c.n_transforms_test: not really any change
        inputs = inputs.view(-1, *inputs.shape[-3:])
        inputs = Variable(inputs, requires_grad=False)  # This result is deterministic
        inputs = inputs.to(self.device)  # to work with both GPU and CPU

        # 2. detect
        with torch.no_grad():
            z = self.model(inputs)

        anomaly_score = self._t2np(torch.mean(z ** 2, dim=(-2, -1)))
        if anomaly_score > anomaly_threshold:
            findDefect = True

        # no need to loss, reduce compute
        # loss = self._get_loss(z, model.nf.jacobian(run_forward=False))
        # loss.backward()
        logger.info(
            f"Detection: anomaly_score={anomaly_score}, findDefect={findDefect}"
        )

        return findDefect