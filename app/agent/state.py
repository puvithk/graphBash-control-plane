from pydantic import Field
from groq import BaseModel
from typing import TypedDict
class MainState(TypedDict):
    """
    This is the main state used in the Graph

    This contains all the required State which are reqiered by the agent 
    """

    query : str 

    intends :str

    planner : list[str]

    tools : list[str]

    response : str

    premission_neeed : list[str] #Can have multiple premission which should be taked 

    granted_premission : list[dict[str , bool]]

    route : str

    is_validated  : bool

    is_excecuted : bool 
    policy_evaluation : bool

    needs_policy_evaluation :bool 


class IntendClassifierResponse(BaseModel):
    intent : str = Field(description="Provide a summary of the system")
    needs_policy_evaluation : bool = Field(desc="Whether the query needs policy evaluation")
    reason : str = Field(description="Reason for the intent classification")

    
