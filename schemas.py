from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field

# Single Task Model
class TaskItem(BaseModel):
    task: str = Field(description="The extracted task description")
    due_date: Optional[str] = Field(None, description="Extracted relative or exact due date/time")
    priority: Optional[str] = Field("Medium", description="Priority level: High, Medium, or Low")

# Model for Structured Output from Gemini
class ExtractedTasks(BaseModel):
    tasks: List[TaskItem]

# LangGraph State Model
class TaskGraphState(TypedDict):
    raw_input: str
    extracted_tasks: List[dict]
    prioritized_tasks: List[dict]
    final_output: str