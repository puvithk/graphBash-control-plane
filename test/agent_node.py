import sys
from pathlib import Path

# Add project root to sys.path so the test script can run standalone
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agent.nodes import intent_classifier
from app.agent.state import MainState


def test_intent_classifier(query: str = "Why did my system got crashed?") -> dict:
    state: MainState = {
        "query": query,
        "memory": "No previous memory",
        "intends": "",
        "reason": "",
        "planner": [],
        "tools": [],
        "response": "",
        "premission_neeed": [],
        "granted_premission": [],
        "route": "",
        "is_validated": False,
        "is_excecuted": False,
        "policy_evaluation": False,
        "needs_policy_evaluation": False,
    }
    result = intent_classifier(state)
    assert result is not None
    assert "intend" in result
    print(result)
    return result


if __name__ == "__main__":
    test_intent_classifier("""Hello, good morning, how are you doing today?""")
    test_intent_classifier()