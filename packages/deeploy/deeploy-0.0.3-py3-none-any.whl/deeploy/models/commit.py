from pydantic import BaseModel

from deeploy.common import to_lower_camel


class Commit(BaseModel):
    id: str
    branch_name: str
    commit: str
    upload_method: int
    s3_link: str
    status: int
    created_at: str
    updated_at: str

    class Config:
        alias_generator = to_lower_camel
