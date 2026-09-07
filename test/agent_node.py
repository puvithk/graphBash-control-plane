from app.agent.nodes import intent_classifier
from app.agent.state import MainState



def test_intent_classifier(query : str = "Why did my system got crashed?" ) -> None:
    state : MainState = {
        "query" : query ,
        "memory" : "No previous memory",
        "intent" : "" ,
        "reason" : "" ,
        "planner" : [],
        "tools" : [],
        "response" : "",
        "premission_neeed" : [],
        "granted_premission" : [],
        "route" : "",
        "is_validated" : False,
        "is_excecuted" : False,
        "policy_evaluation" : False,
        "needs_policy_evaluation" : False
    }
    state = intent_classifier(state)
    print(state)


if __name__ == "__main__":
    test_intent_classifier("""Hello, good morning, how are you doing today?""") 
    test_intent_classifier()