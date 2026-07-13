from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Task as TodoistTask

from shabbot.task_parser import Task


class TodoistError(Exception):
    pass


class TodoistClient:
    def __init__(self, token: str) -> None:
        self._token = token

    async def create_task(self, task: Task) -> TodoistTask:
        parts: list[str] = []

        if task.description:
            parts.append(task.description)

        if task.location:
            parts.append(f"📍 {task.location}")

        if task.raw_text and task.raw_text != task.summary:
            parts.append(f"🎙 {task.raw_text}")

        description: str | None = None
        if parts:
            description = "\n\n".join(parts)

        try:
            async with TodoistAPIAsync(self._token) as api:
                return await api.add_task(
                    content=task.summary,
                    description=description,
                    due_string="today",
                )
        except Exception as e:
            raise TodoistError(str(e)) from e
