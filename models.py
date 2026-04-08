from pydantic import BaseModel

class Observation(BaseModel):
    ticket: str

class Action(BaseModel):
    category: str
    urgency: str
    action: str
    response: str

class Reward(BaseModel):
    score: float