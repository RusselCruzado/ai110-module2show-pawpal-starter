from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_defaults_to_today_due_date():
    task = Task("Morning walk", 30, 3, "walk", "07:30")

    assert task.due_date == date.today()


def test_scheduler_mark_task_complete_creates_next_daily_task():
    owner = Owner(name="Alex", available_minutes_per_day=120)
    pet = Pet(name="Milo", species="dog", age=4)
    owner.add_pet(pet)

    task = Task(
        title="Morning walk",
        duration_minutes=30,
        priority=3,
        category="walk",
        time="07:30",
        frequency="daily",
        due_date=date.today(),
    )
    pet.add_task(task)

    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete(task)

    assert task.completed is True
    assert result is not None
    assert result.title == task.title
    assert result.completed is False
    assert result.due_date == date.today() + timedelta(days=1)
    assert result in pet.tasks


def test_task_can_be_marked_complete():
    task = Task("Morning walk", 30, 3, "walk", "07:30")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_pet_can_add_task():
    pet = Pet("Milo", "dog", 4)
    task = Task("Morning walk", 30, 3, "walk", "07:30")

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1