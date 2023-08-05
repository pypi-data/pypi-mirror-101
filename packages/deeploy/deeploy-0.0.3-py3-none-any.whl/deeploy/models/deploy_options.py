from typing import Optional, List, Any

from pydantic import BaseModel

from deeploy.enums import PredictionMethod


class DeployOptions(BaseModel):
    """Class that contains the options for deploying a model

    Attributes:
        name (str): name of the deployment
        model_serverless (bool, optional): whether to deploy the model in 
            a serverless fashion. Defaults to False
        explainer_serverless (bool, optional): whether to deploy the model in 
            a serverless fashion. Defaults to False
        method (PredictionMethod, optional): which prediction function to use. Only applicable
            to sklearn and xgboost models. Defaults to 'predict'
        description (str, optional): the description of the deployment
        example_input (List, optional): list of example input parameters for the model
        example_output (List, optional): list of example output for the model
        model_class_name (str, optional): the name of the class containing the 
            PyTorch model.
    """
    name: str
    model_serverless = False
    explainer_serverless = False
    method = PredictionMethod.PREDICT
    description: Optional[str]
    example_input: Optional[List[Any]]
    example_output: Optional[List[Any]]
    model_class_name: Optional[str]
    pytorch_model_file_path: Optional[str]
