import numpy as np
import json
from art.estimators.classification import PyTorchClassifier, KerasClassifier
import torch
from .troj_dataset import TrojDataLoader, TrojDataset
import tensorflow as tf
from . import array_utils
from . import TrojEpsilon
import sys


"""
I imagine this class is like a session, it stores all the stuff we'd need to access frequently, collating it into one class
for now will store the client instance with key infod
also dataset information


Session:
    Methods:
        create_troj_dataset:
            initializes the dataframe
        create_attack:
            initializes the attack target using the model as input
        run_troj_test(test_loader, loss):
        
"""


class TrojSession:
    def __init__(self):
        super().__init__()
        # thing that makes requests to the troj api
        self.client = None
        # dataframe with the user's testing data
        self.dataset = None
        self.dataframe = None
        # dataloader made from the dataset
        self.dataloader = None
        self.adv_classifier = None
        self.attacker = None
        self.model = None
        self.loss_func = None

    def create_troj_dataset(self, image_folder_path, annotation_file=None):
        ds = TrojDataset()
        if annotation_file == None:
            ds.CreateDF(image_folder_path)
        else:
            ds.CreateDF(image_folder_path, annotation_file)

        self.dataset = ds
        self.dataframe = ds.dataframe

    def create_troj_dataloader(self, transforms=None):
        if self.dataset != None:
            self.dataloader = TrojDataLoader(
                self.dataset.dataframe,
                self.dataset.data_structure,
                self.dataset.root_folder,
                transforms=transforms,
            )

        else:
            return "error"



    def CreateClassifierInstance(
        self, model, input_shape, num_classes, loss_func=None
    ):
        print(type(model))
        model_type = type(model)
        if issubclass(model_type, torch.nn.Module):
            if loss_func is not None:
                # ensure model is in eval mode, not sure how to check that rn
                self.classifier = PyTorchClassifier(
                    model, loss_func, input_shape, num_classes
                )
            else:
                print("Pass in loss function with pytorch classifier!")

        elif issubclass(model_type, tf.keras.Model):
            # ensure model is compiled tensorflow
            if True:
                self.classifier = KerasClassifier(model)

    def MakeAttacker(self, learnining_rate=0.01, eps_steps=0.05, max_halving = 10,
                 max_doubling = 10, num_iters=15, batch_size=128, norm=np.inf, k=5):
        self.attacker = TrojEpsilon.TrojEpsAttack(self.classifier,  learnining_rate=learnining_rate, eps_steps=eps_steps,
                                                  max_halving = max_halving, max_doubling = max_doubling,
                                                  num_iters=num_iters, batch_size=batch_size,
                                                  norm=norm, k=k)

    def attack(self, data, target, index, device=None):
        
        """
        This will work for pytorch, tensorflow has no device
        """
        # index = index.numpy()
        # send data and target to cpu, convert to numpy
        data = np.ascontiguousarray(data.astype(np.float32))
        preds = self.classifier.predict(data)
        preds = np.argmax(preds, axis=1)
        self.classifier._reduce_labels = False
        
        test_loss = self.classifier.loss(data, target, reduction='none')
        self.classifier._reduce_labels = True
        adv_x = self.attacker.generate(data, target)
        adv_preds = self.classifier.predict(adv_x)
        self.classifier._reduce_labels = False
        adv_loss = self.classifier.loss(adv_x, target, reduction='none')
        perturbation = array_utils.compute_Lp_distance(data, adv_x)
        # generate the adversarial image using the data numpy array and label numpy array
        self._log_to_dataframe(
            index, perturbation, test_loss, adv_loss, preds, adv_preds
        )

    def _log_to_dataframe(
        self, index, perturbation, test_loss, adv_loss, prediction, adv_preds
    ):
        # want to write a function to add all this shit at once, can we obfuscate it in a simple way?
        self.dataset.dataframe.loc[index, "Linf_perts"] = perturbation
        self.dataset.dataframe.loc[index, "Loss"] = test_loss
        self.dataset.dataframe.loc[index, "Adversarial_Loss"] = adv_loss
        self.dataset.dataframe.loc[index, "prediction"] = prediction
        self.dataset.dataframe.loc[index, "Adversarial_prediction"] = np.argmax(
            adv_preds, axis=1
        )

    def create_project(self, project_name: str):
        return self.client.create_project(project_name)

    def create_dataset(self, project_name: str, dataset_name: str):
        return self.client.create_dataset(project_name, dataset_name)

    """
    TODO: 
    Look into setting proj/dataset name in the client class as a 'current project/dataset'
        so it can just be pulled in automatically instead of sending them in
    Maybe?
    """

    def upload_dataframe(self, project_name: str, dataset_name: str):
        self.dataset.dataframe = self.dataset.dataframe.dropna()
        # import sys
        # self.dataset.dataframe = self.dataset.dataframe[self.dataset.dataframe["stage"] == "train"] 
        jsonified_df = json.loads(self.dataset.dataframe.to_json(orient="index"))
        print(sys.getsizeof(jsonified_df))

        # Saves the dataframe as a .json file locally, just for testing purposes
        # with open("data.json", "w") as f:
        #     json.dump(jsonified_df, f)

        return self.client.upload_df_results(project_name, dataset_name, jsonified_df)
