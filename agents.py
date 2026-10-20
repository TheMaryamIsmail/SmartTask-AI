import os
from langchain_google_genai import ChatGoogleGenerativeAI
from schemas import ExtractedTasks, TaskGraphState
from dotenv import load_dotenv

# Load environment variables explicitly
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Initialize Gemini Model
llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=API_KEY
)

# Combined Node: Extract & Prioritize in a single fast Gemini call
def extract_and_prioritize_node(state: TaskGraphState) -> dict:
    raw_text = state["raw_input"]
    structured_llm = llm.with_structured_output(ExtractedTasks)
    
    prompt = f"""
    Analyze the following natural language text. Extract all distinct actionable tasks, find their due dates/deadlines (if any), and assign a priority level ('High', 'Medium', or 'Low') based on urgency.
    
    Text: '{raw_text}'
    """
    
    response = structured_llm.invoke(prompt)
    tasks_list = [t.model_dump() for t in response.tasks]
    
    return {
        "extracted_tasks": tasks_list,
        "prioritized_tasks": tasks_list
    }

# Node 3: Format Results
def format_results_node(state: TaskGraphState) -> dict:
    tasks = state["prioritized_tasks"]
    
    formatted_output = "📋 **Your Organized To-Do List:**\n" + "-"*35 + "\n"
    for idx, t in enumerate(tasks, 1):
        due = f" (Due: {t['due_date']})" if t.get('due_date') else ""
        formatted_output += f"{idx}. [{t['priority'].upper()}] {t['task']}{due}\n"
        
    return {"final_output": formatted_output}