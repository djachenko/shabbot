from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Task as TodoistTask

from shabbot.task import Task


async def create_task(task: Task, todoist_token: str) -> TodoistTask:
    parts: list[str] = []

    if task.description:
        parts.append(task.description)
    if task.location:
        parts.append(f"📍 {task.location}")
    if task.raw_text and task.raw_text != task.summary:
        parts.append(f"🎙 {task.raw_text}")

    async with TodoistAPIAsync(todoist_token) as api:
        return await api.add_task(
            content=task.summary,
            description="\n\n".join(parts) if parts else None,
            due_string="today",
        )
