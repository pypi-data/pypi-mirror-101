from typing import Any
from os.path import join, exists
from shutil import copy, move
import random
import string
import subprocess

from torch.nn import Module
from torch import save

from . import BaseModel
from deeploy.enums import ModelType


class PyTorchModel(BaseModel):

    __pytorch_model: Module
    __model_file_path: str

    def __init__(self, model_object: Any, pytorch_model_file_path: str, **kwargs) -> None:

        if not issubclass(type(model_object), Module):
            raise Exception('Not a valid PyTorch class')

        if not exists(pytorch_model_file_path):
            raise Exception('The Pytorch model file does not exist')

        if not (pytorch_model_file_path.endswith('.py') or pytorch_model_file_path.endswith('.ipynb')):
            raise Exception(
                'The Pytorch model file is not a supported file type. Use .py or .ipynb')

        self.__pytorch_model = model_object
        self.__model_file_path = pytorch_model_file_path
        return

    def save(self, local_folder_path: str) -> None:
        save(self.__pytorch_model.state_dict(),
             join(local_folder_path, 'model.pt'))

        if self.__model_file_path.endswith('.py'):
            copy(self.__model_file_path, local_folder_path)

        elif self.__model_file_path.endswith('.ipynb'):
            convert_command = "ipython nbconvert --to script %s" % self.__model_file_path

            process = subprocess.Popen(
                convert_command.split(), stdout=subprocess.PIPE)
            _, error = process.communicate()
            if error:
                raise Exception(error)
            copy(self.__model_file_path.replace(
                '.ipynb', '.py'), local_folder_path)

        return

    def get_model_type(self) -> ModelType:
        return ModelType.PYTORCH
