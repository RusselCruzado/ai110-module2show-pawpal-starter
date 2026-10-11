from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int
    category: str
    completed: bool

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's care list."""
        pass

    def remove_task(self, title: str) -> None:
        """Remove the task with the given title."""
        pass


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care list."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks belonging to this owner's pets."""
        pass


class Scheduler:
    owner: Owner

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for the given owner."""
        self.owner = owner

    def generate_daily_plan(self) -> list[Task]:
        """Generate a daily care plan for the owner."""
        pass

    def explain_plan(self) -> str:
        """Explain the generated daily care plan."""
        pass