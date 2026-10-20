import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from dotenv import load_dotenv

from graph import task_workflow
from database import save_tasks_to_json

load_dotenv()

app = FastAPI(title="AI Task Organizer")

# # Mount Static directory
# os.makedirs("static", exist_ok=True)
# app.mount("/static", StaticFiles(directory="static") if "StaticFiles" in globals() else None, name="static")

# Templates directory link karna
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Initial Page Load Route"""
    return templates.TemplateResponse(
        request, 
        "index.html", 
        {"tasks": None, "raw_input": ""}
    )


@app.post("/organize", response_class=HTMLResponse)
async def organize_tasks(request: Request, raw_input: str = Form(...)):
    """Form submit hone par LangGraph execute karke task render karna"""
    
    # LangGraph Workflow Invoke
    inputs = {"raw_input": raw_input}
    result = task_workflow.invoke(inputs)
    
    prioritized_tasks = result.get("prioritized_tasks", [])
    
    # Save output to JSON file
    if prioritized_tasks:
        save_tasks_to_json(prioritized_tasks)

    # Jinja2 template response (Updated Starlette/FastAPI compatible syntax)
    return templates.TemplateResponse(
        request, 
        "index.html", 
        {
            "tasks": prioritized_tasks, 
            "raw_input": raw_input
        }
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)