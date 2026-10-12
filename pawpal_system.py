from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int
    category: str
    time: str
    frequency: str = "daily"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's care list."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove the first task matching the title, if present."""
        for index, task in enumerate(self.tasks):
            if task.title == title:
                del self.tasks[index]
                return


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks belonging to this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    owner: Owner

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for the given owner."""
        self.owner = owner

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return a copy of the task list sorted by the HH:MM time value."""
        return sorted(tasks, key=lambda task: task.time)

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[Task]:
        """Return all owner tasks filtered by pet name and completion status when provided."""
        tasks = self.owner.get_all_tasks()

        if pet_name is not None:
            tasks = [
                task
                for pet in self.owner.pets
                if pet.name == pet_name
                for task in pet.tasks
            ]

        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]

        return tasks

    def mark_task_complete(self, task: Task) -> Task | None:
        """Mark a task complete and create the next recurring instance for daily or weekly tasks."""
        for pet in self.owner.pets:
            if task in pet.tasks:
                task.mark_complete()

                if task.frequency == "daily":
                    next_task = Task(
                        title=task.title,
                        duration_minutes=task.duration_minutes,
                        priority=task.priority,
                        category=task.category,
                        time=task.time,
                        frequency=task.frequency,
                        completed=False,
                        due_date=task.due_date + timedelta(days=1),
                    )
                    pet.add_task(next_task)
                    return next_task

                if task.frequency == "weekly":
                    next_task = Task(
                        title=task.title,
                        duration_minutes=task.duration_minutes,
                        priority=task.priority,
                        category=task.category,
                        time=task.time,
                        frequency=task.frequency,
                        completed=False,
                        due_date=task.due_date + timedelta(weeks=1),
                    )
                    pet.add_task(next_task)
                    return next_task

                return None

        return None

    def detect_conflicts(self) -> list[str]:
        """Return warning strings for pending tasks that share the same exact time."""
        today = date.today()
        tasks_by_time: dict[str, list[tuple[str, Task]]] = {}

        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.completed or task.due_date > today:
                    continue
                tasks_by_time.setdefault(task.time, []).append((pet.name, task))

        warnings: list[str] = []
        for time_value, entries in tasks_by_time.items():
            if len(entries) < 2:
                continue

            task_labels = [f"'{task.title}' ({pet_name})" for pet_name, task in entries]
            if len(task_labels) == 2:
                message = (
                    f"Warning: {task_labels[0]} and {task_labels[1]} are both "
                    f"scheduled at {time_value}."
                )
            else:
                message = (
                    f"Warning: {', '.join(task_labels[:-1])}, and {task_labels[-1]} "
                    f"are both scheduled at {time_value}."
                )
            warnings.append(message)

        return warnings

    def generate_daily_plan(self) -> list[Task]:
        """Build today's schedule by selecting due tasks that fit within the owner's daily time limit."""
        today = date.today()
        pending_tasks = sorted(
            (
                task
                for task in self.owner.get_all_tasks()
                if not task.completed and task.due_date <= today
            ),
            key=lambda task: (task.time, -task.priority),
        )
        plan = []
        remaining_minutes = self.owner.available_minutes_per_day

        for task in pending_tasks:
            if task.duration_minutes <= remaining_minutes:
                plan.append(task)
                remaining_minutes -= task.duration_minutes

        return plan

    def explain_plan(self) -> str:
        """Explain which tasks were included, skipped, and excluded from today's plan."""
        today = date.today()
        all_tasks = [
            task for task in self.owner.get_all_tasks() if task.due_date <= today
        ]
        completed_count = sum(task.completed for task in all_tasks)
        pending_tasks = sorted(
            (task for task in all_tasks if not task.completed),
            key=lambda task: (task.time, -task.priority),
        )
        remaining_minutes = self.owner.available_minutes_per_day
        included = []
        skipped = []

        for task in pending_tasks:
            if task.duration_minutes <= remaining_minutes:
                remaining_minutes -= task.duration_minutes
                included.append(
                    f"- {task.time} {task.title} ({task.duration_minutes} min, "
                    f"priority {task.priority}): fits the remaining daily time."
                )
            else:
                skipped.append(
                    f"- {task.time} {task.title} ({task.duration_minutes} min, "
                    f"priority {task.priority}): needs more than the "
                    f"{remaining_minutes} min remaining."
                )

        lines = [
            f"Daily plan: {self.owner.available_minutes_per_day} minutes available.",
            f"Completed tasks excluded: {completed_count}.",
            "Included tasks:",
            *(included or ["- None."]),
            "Skipped because they did not fit:",
            *(skipped or ["- None."]),
        ]
        return "\n".join(lines)