from pydantic import BaseModel


class ScriptBase(BaseModel):
    idea_id: int
    script_content: str


class ScriptList(ScriptBase):
    id: int
    user_id: int