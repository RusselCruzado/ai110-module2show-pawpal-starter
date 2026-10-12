from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner(name="Alex", available_minutes_per_day=120)
dog = Pet(name="Milo", species="dog", age=4)
cat = Pet(name="Luna", species="cat", age=2)
owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(
    Task(
        title="Morning walk",
        duration_minutes=30,
        priority=4,
        category="walk",
        time="07:30",
    )
)
cat.add_task(
    Task(
        title="Lunch feeding",
        duration_minutes=10,
        priority=3,
        category="feeding",
        time="12:00",
    )
)
dog.add_task(
    Task(
        title="Evening medication",
        duration_minutes=5,
        priority=5,
        category="medication",
        time="18:00",
    )
)

scheduler = Scheduler(owner)
daily_plan = scheduler.generate_daily_plan()
pet_names_by_task_id = {
    id(task): pet.name for pet in owner.pets for task in pet.tasks
}

print("Today's Schedule")
for task in daily_plan:
    pet_name = pet_names_by_task_id[id(task)]
    print(
        f"{task.time} | {task.title} | {pet_name} | "
        f"{task.duration_minutes} min | Priority {task.priority}"
    )

print()
print(scheduler.explain_plan())