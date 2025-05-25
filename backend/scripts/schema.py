from pydantic import BaseModel


class ScriptBase(BaseModel):
    id: int | None = None
    idea_id: int
    title: str
    script_content: str


class ScriptList(ScriptBase):
    user_id: int