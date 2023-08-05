from typing import Optional, List, Any

from pydantic import BaseModel

from deeploy.enums import ModelType, ExplainerType, PredictionMethod


class CreateDeployment(BaseModel):
    """
    """
    repository_id: str
    name: str
    description: Optional[str]
    example_input: Optional[List[Any]]
    example_output: Optional[Any]
    model_type: ModelType
    model_class_name: Optional[str]
    method: Optional[PredictionMethod] = PredictionMethod.PREDICT
    model_serverless: Optional[bool] = False
    explainer_type: ExplainerType
    explainer_serverless: Optional[bool] = False
    branch_name: str
    commit_sha: str

    def to_request_body(self):
        return {
            'repositoryId': self.repository_id,
            'name': self.name,
            'description': self.description,
            'exampleInput': self.example_input,
            'exampleOutput': self.example_output,
            'modelType': self.model_type.value,
            'modelClassName': self.model_class_name,
            'method': self.method.value,
            'modelServerless': self.model_serverless,
            'explainerType': self.explainer_type.value,
            'explainerServerless': self.explainer_serverless,
            'branchName': self.branch_name,
            'commitSHA': self.commit_sha,
        }
