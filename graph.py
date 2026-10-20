from langgraph.graph import StateGraph, END
from schemas import TaskGraphState
from agents import extract_and_prioritize_node, format_results_node

# Workflow graph build karna
builder = StateGraph(TaskGraphState)

# Nodes add karna
builder.add_node("extract_and_prioritize", extract_and_prioritize_node)
builder.add_node("format_results", format_results_node)

# Edges connect karna
builder.set_entry_point("extract_and_prioritize")
builder.add_edge("extract_and_prioritize", "format_results")
builder.add_edge("format_results", END)

# Graph compile karna
task_workflow = builder.compile()