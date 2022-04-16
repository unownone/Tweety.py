from pydantic import BaseModel

class StartComment(BaseModel):
    tags: list[str]
    scripts: list[str]
    nums: int