from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner(name="Alex", available_minutes_per_day=120)
dog = Pet(name="Milo", species="dog", age=4)
cat = Pet(name="Luna", species="cat", age=2)
owner.add_pet(dog)
owner.add_pet(cat)

# Daily recurring task and other tasks for sorting/filtering and conflict detection.
daily_walk = Task(
    title="Morning walk",
    duration_minutes=30,
    priority=4,
    category="walk",
    time="07:30",
    frequency="daily",
    due_date=date.today(),
)
dog.add_task(daily_walk)

cat.add_task(
    Task(
        title="Lunch feeding",
        duration_minutes=10,
        priority=3,
        category="feeding",
        time="12:00",
        due_date=date.today(),
    )
)
dog.add_task(
    Task(
        title="Evening medication",
        duration_minutes=5,
        priority=5,
        category="medication",
        time="18:00",
        due_date=date.today(),
    )
)

cat.add_task(
    Task(
        title="Vet visit",
        duration_minutes=40,
        priority=5,
        category="vet",
        time="07:30",
        due_date=date.today(),
    )
)

scheduler = Scheduler(owner)

print("=== Sorting and filtering ===")
for task in scheduler.sort_by_time(owner.get_all_tasks()):
    pet_name = next(pet.name for pet in owner.pets if task in pet.tasks)
    print(f"{task.time} | {task.title} | {pet_name} | {task.duration_minutes} min")

print()
print("Filtered by pet name (Milo):")
for task in scheduler.filter_tasks(pet_name="Milo"):
    print(f"{task.time} | {task.title} | completed={task.completed}")

print()
print("Filtered by completion status (completed=False):")
for task in scheduler.filter_tasks(completed=False):
    print(f"{task.time} | {task.title} | completed={task.completed}")

print()
print("=== Conflict warning ===")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts")

print()
print("=== Recurring task demo ===")
new_task = scheduler.mark_task_complete(daily_walk)
print(f"New task due date: {new_task.due_date}")
print("Full task list:")
for pet in owner.pets:
    for task in pet.tasks:
        print(
            f"{pet.name} | {task.title} | {task.time} | "
            f"completed={task.completed} | due={task.due_date}"
        )

print()
print("=== Today's schedule ===")
for task in scheduler.generate_daily_plan():
    pet_name = next(pet.name for pet in owner.pets if task in pet.tasks)
    print(
        f"{task.time} | {task.title} | {pet_name} | "
        f"{task.duration_minutes} min | Priority {task.priority}"
    )

print()
print(scheduler.explain_plan())