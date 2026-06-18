from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task as TodoistTask

from shabbot.config import load_config
from shabbot.task import Task


def create_task(task: Task) -> TodoistTask:
    config = load_config()
    api = TodoistAPI(config.todoist_token)

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
