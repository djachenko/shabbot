import os

from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task as TodoistTask

from shabbot.task import Task


def create_task(task: Task) -> TodoistTask:
    api = TodoistAPI(os.environ["TODOIST_TOKEN"])

    parts: list[str] = []

    if task.description:
        parts.append(task.description)
    if task.location:
        parts.append(f"📍 {task.location}")
    if task.raw_text and task.raw_text != task.summary:
        parts.append(f"🎙 {task.raw_text}")

    return api.add_task(
        content=task.summary,
        description="\n\n".join(parts) if parts else None,
        due_string="today",
    )
