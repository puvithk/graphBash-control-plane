from yaml import MappingStartEvent
from .state import MainState , IntendClassifierResponse
from .utils.models import ChatLLM
from .prompts import INTEND_CLASSIFIER_PROMPT
llm = ChatLLM()


def intent_classifier(state : MainState) -> MainState:
    """
    This node is used to classify the intent of the query.
    This function uses the query and creates wht the intend of the query.
    """
    # Get the memory from the data 
    memory = state.get("memory" , "No previous memory")
    query = state.get("query" , "")
    # Based on the prevoius conversation decides the intend
    
    
    # Ask the LLM to classify the intent of the query

    response : IntendClassifierResponse = llm.invoke_with_structured_output(
        prompt=INTEND_CLASSIFIER_PROMPT.format(query=query , memory=memory),
        output_structure=IntendClassifierResponse
        )

    return {
            "intends" : response.intent,
            "needs_policy_evaluation" : response.needs_policy_evaluation
            }


def planner(state : MainState) -> MainState :
    """
    This node is used to plan the execution of the query.
    This function uses the query and creates a plan for the execution of the query.
    """

    return {
            "planner" : ["Check the CPU" , "Check the memeory" , "Check the temperature" , "Provide a summary"]
            }

def tool_selector(state : MainState) -> MainState :
    """
    This node is used to select the tools for the query.
    This function uses the query and creates a list of tools for the execution of the query.
    """
    return {
            "tools" : ["cpu_mcp" , "memory_mcp" , "temperature_mcp" , "summary_mcp"]
            }

def evaluate_policy(state : MainState) -> MainState :
    """
    This node is used to evaluate the policy of the query.
    This function uses the query and creates a list of tools for the execution of the query.
    """
    return {
            "policy_evaluation" : True
            }


def approval_node(state : MainState) -> MainState :
    """
    This node is used to approval of the query.
    This function uses the query and creates a list of tools for the execution of the query.
    """
    return {
            "is_approved" : True
            }

def excecution_engine(state : MainState) -> MainState :
    """
    This node is used to excecution of the query.
    This function uses the query and creates a list of tools for the execution of the query.
    """
    return {
            "is_excecuted" : True
            }
def response_generator(state: MainState) -> MainState :
    """

    This node is used to generate the response of the query.
    This function uses the query and creates a list of tools for the execution of the query.
    """
    return {
            "response" : "Summary of the linux system"
            }


def result_validator(state : MainState) -> MainState :
    """
    This node is used to validate the result of the query.
    This function uses the query and creates a list of tools for the execution of the query.
    """
    return {
            "is_validated" : True
            }