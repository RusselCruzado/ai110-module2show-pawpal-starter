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


def test_scheduler_sort_by_time_returns_chronological_order():
    # Checks that tasks added out of order are sorted chronologically.
    scheduler = Scheduler(Owner("Alex", 120))
    late_task = Task("Evening walk", 30, 2, "walk", "18:00")
    early_task = Task("Breakfast", 10, 1, "food", "07:00")

    assert scheduler.sort_by_time([late_task, early_task]) == [early_task, late_task]


def test_scheduler_daily_recurrence_is_due_tomorrow():
    # Checks that completing a daily task creates an incomplete task due tomorrow.
    owner = Owner("Alex", 120)
    pet = Pet("Milo", "dog", 4)
    task = Task("Morning walk", 30, 3, "walk", "07:30", frequency="daily")
    owner.add_pet(pet)
    pet.add_task(task)

    next_task = Scheduler(owner).mark_task_complete(task)

    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_scheduler_weekly_recurrence_is_due_next_week():
    # Checks that completing a weekly task creates its next instance one week later.
    owner = Owner("Alex", 120)
    pet = Pet("Milo", "dog", 4)
    task = Task("Grooming", 45, 2, "grooming", "10:00", frequency="weekly")
    owner.add_pet(pet)
    pet.add_task(task)

    next_task = Scheduler(owner).mark_task_complete(task)

    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == date.today() + timedelta(weeks=1)


def test_scheduler_detects_conflict_at_same_time():
    # Checks that two pending tasks at the same time produce a warning.
    owner = Owner("Alex", 120)
    first_pet = Pet("Milo", "dog", 4)
    second_pet = Pet("Luna", "cat", 2)
    first_pet.add_task(Task("Walk", 30, 2, "walk", "08:00"))
    second_pet.add_task(Task("Breakfast", 10, 1, "food", "08:00"))
    owner.add_pet(first_pet)
    owner.add_pet(second_pet)

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "scheduled at 08:00" in warnings[0]


def test_scheduler_has_no_conflict_at_different_times():
    # Checks that pending tasks at different times produce no warnings.
    owner = Owner("Alex", 120)
    pet = Pet("Milo", "dog", 4)
    pet.add_task(Task("Breakfast", 10, 1, "food", "08:00"))
    pet.add_task(Task("Walk", 30, 2, "walk", "09:00"))
    owner.add_pet(pet)

    assert Scheduler(owner).detect_conflicts() == []


def test_scheduler_empty_pet_has_empty_plan_and_no_conflicts():
    # Checks that a pet with no tasks yields an empty plan and no warnings.
    owner = Owner("Alex", 120)
    owner.add_pet(Pet("Milo", "dog", 4))
    scheduler = Scheduler(owner)

    assert scheduler.generate_daily_plan() == []
    assert scheduler.detect_conflicts() == []


def test_scheduler_daily_plan_respects_exact_time_budget():
    # Checks that a task fitting exactly is included and one minute over is skipped.
    owner = Owner("Alex", 10)
    pet = Pet("Milo", "dog", 4)
    fits = Task("Breakfast", 10, 2, "food", "08:00")
    too_long = Task("Walk", 11, 1, "walk", "09:00")
    pet.add_task(fits)
    pet.add_task(too_long)
    owner.add_pet(pet)

    assert Scheduler(owner).generate_daily_plan() == [fits]


def test_scheduler_filter_tasks_by_pet_and_completion_status():
    # Checks that pet-name and completion filters return only matching tasks.
    owner = Owner("Alex", 120)
    milo = Pet("Milo", "dog", 4)
    luna = Pet("Luna", "cat", 2)
    milo_task = Task("Walk", 30, 2, "walk", "08:00")
    luna_task = Task("Breakfast", 10, 1, "food", "07:00")
    milo_task.mark_complete()
    milo.add_task(milo_task)
    luna.add_task(luna_task)
    owner.add_pet(milo)
    owner.add_pet(luna)
    scheduler = Scheduler(owner)

    assert scheduler.filter_tasks(pet_name="Milo") == [milo_task]
    assert scheduler.filter_tasks(completed=False) == [luna_task]