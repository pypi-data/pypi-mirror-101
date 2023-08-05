from typing import List, Optional

from pydantic import BaseModel

from .commit import Commit
from deeploy.common import to_lower_camel


class Repository(BaseModel):
    id: str
    name: str
    status: int
    is_archived: bool
    workspace_id: str
    is_public: Optional[bool]
    git_ssh_pull_link: str
    created_at: str
    updated_at: str
    commits: List[Commit]

    class Config:
        alias_generator = to_lower_camel
