from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int
    category: str
    time: str
    frequency: str = "daily"
    completed: bool = False

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

    def generate_daily_plan(self) -> list[Task]:
        """Select incomplete tasks by time and priority within the daily time limit."""
        pending_tasks = sorted(
            (task for task in self.owner.get_all_tasks() if not task.completed),
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
        """Describe included tasks, time-limit skips, and completed tasks excluded."""
        all_tasks = self.owner.get_all_tasks()
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