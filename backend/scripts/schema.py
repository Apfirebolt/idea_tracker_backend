from pydantic import BaseModel


class ScriptBase(BaseModel):
    idea_id: int
    title: str
    script_content: str


class ScriptList(ScriptBase):
    id: int
    user_id: int