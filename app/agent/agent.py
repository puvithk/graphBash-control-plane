from .graph import workflow
from .state import MainState

def agent(query : str) -> MainState :
    """

    This function is used to run the agent.
    """
    return workflow.invoke({
        "query" : query
    })


if __name__ == "__main__":
    print(agent("What is the CPU temperature?"))