from langgraph.graph import END, START, StateGraph

from .nodes import (
    excecution_engine,
    intent_classifier,
    planner,
    response_generator,
    result_validator,
    tool_selector,
)
from .state import MainState

graph = StateGraph(MainState)


graph.add_node("intent_classifier" , intent_classifier)
graph.add_node("planner" , planner)
graph.add_node("tool_selector" , tool_selector)
graph.add_node("response_generator" , response_generator)
graph.add_node("excecution_engine" , excecution_engine)
graph.add_node("result_validator" , result_validator)


graph.add_edge(START , "intent_classifier")
graph.add_edge("intent_classifier" , "planner")
graph.add_edge("planner" , "tool_selector")
graph.add_edge("tool_selector" , "excecution_engine")
graph.add_edge("excecution_engine" , "response_generator")
graph.add_edge("response_generator" , "result_validator")
graph.add_edge("result_validator" , END)



workflow = graph.compile()
