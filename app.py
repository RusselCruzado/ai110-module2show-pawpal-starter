from datetime import time

import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        available_minutes_per_day=120,
    )

st.title("🐾 PawPal+")

st.markdown(
    """
Plan pet care tasks, track completion, and build a schedule that fits your daily time budget.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
Add pets and their care tasks, then generate a daily plan with an explanation.
"""
    )

st.divider()

st.subheader("Pets")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age (years)", min_value=0, max_value=100, value=1)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted and pet_name.strip():
    st.session_state.owner.add_pet(
        Pet(name=pet_name.strip(), species=species, age=int(age))
    )

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"Name": pet.name, "Species": pet.species, "Age": pet.age}
            for pet in st.session_state.owner.pets
        ]
    )
else:
    st.info("No pets yet. Add a pet before creating tasks.")

st.divider()
st.subheader("Tasks")
owner = st.session_state.owner
scheduler = Scheduler(owner)

if owner.pets:
    with st.form("add_task_form"):
        selected_pet_index = st.selectbox(
            "Pet",
            options=range(len(owner.pets)),
            format_func=lambda index: owner.pets[index].name,
        )
        task_title = st.text_input("Task title", value="")
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority_label = st.selectbox("Priority", ["low", "medium", "high"])
        category = st.text_input("Category", value="feeding")
        task_time = st.time_input("Time", value=time(8, 0))
        frequency = st.selectbox("Repeat", ["daily", "weekly"])
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted and task_title.strip():
        priority_values = {"low": 1, "medium": 2, "high": 3}
        task = Task(
            title=task_title.strip(),
            duration_minutes=int(duration),
            priority=priority_values[priority_label],
            category=category.strip(),
            time=task_time.strftime("%H:%M"),
            frequency=frequency,
        )
        owner.pets[selected_pet_index].add_task(task)

    st.markdown("### Filter tasks")
    filter_columns = st.columns(2)
    with filter_columns[0]:
        selected_pet_name = st.selectbox(
            "Pet filter", ["All pets", *(pet.name for pet in owner.pets)]
        )
    with filter_columns[1]:
        selected_status = st.selectbox(
            "Status", ["All", "Pending", "Completed"]
        )

    completed_filter = {"All": None, "Pending": False, "Completed": True}[
        selected_status
    ]
    filtered_tasks = scheduler.filter_tasks(
        pet_name=None if selected_pet_name == "All pets" else selected_pet_name,
        completed=completed_filter,
    )
    filtered_tasks = scheduler.sort_by_time(filtered_tasks)
    pet_names_by_task_id = {
        id(task): pet.name for pet in owner.pets for task in pet.tasks
    }
    if filtered_tasks:
        st.table(
            [
                {
                    "Pet": pet_names_by_task_id[id(task)],
                    "Time": task.time,
                    "Title": task.title,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority,
                    "Category": task.category,
                    "Repeat": task.frequency,
                    "Due date": task.due_date,
                    "Status": "Completed" if task.completed else "Pending",
                }
                for task in filtered_tasks
            ]
        )
    else:
        st.info("No tasks match these filters.")

    st.markdown("### Tasks by pet")
    for pet in owner.pets:
        st.markdown(f"**{pet.name}'s tasks**")
        if pet.tasks:
            st.table(
                [
                    {
                        "Time": task.time,
                        "Title": task.title,
                        "Duration (min)": task.duration_minutes,
                        "Priority": task.priority,
                        "Category": task.category,
                        "Repeat": task.frequency,
                        "Due date": task.due_date,
                        "Status": "Completed" if task.completed else "Pending",
                    }
                    for task in scheduler.sort_by_time(pet.tasks)
                ]
            )
        else:
            st.caption("No tasks added.")

    st.markdown("### Complete a task")
    pending_tasks = scheduler.filter_tasks(completed=False)
    if pending_tasks:
        task_labels = {
            index: (
                f"{pet_names_by_task_id[id(task)]} | {task.time} | {task.title} "
                f"({task.frequency})"
            )
            for index, task in enumerate(pending_tasks)
        }
        selected_task_index = st.selectbox(
            "Pending task to complete",
            options=range(len(pending_tasks)),
            format_func=lambda index: task_labels[index],
        )
        if st.button("Mark complete"):
            completed_task = pending_tasks[selected_task_index]
            next_task = scheduler.mark_task_complete(completed_task)
            if next_task is not None:
                st.success(
                    f"Task marked complete. Next {next_task.frequency} task is due "
                    f"{next_task.due_date.isoformat()}."
                )
            else:
                st.success("Task marked complete.")
    else:
        st.caption("There are no pending tasks to complete.")
else:
    st.info("Add a pet before creating tasks.")

st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(f"{warning} Suggestion: move one of the tasks to a different time.")
    else:
        st.success("No scheduling conflicts.")

    daily_plan = scheduler.generate_daily_plan()

    st.markdown("### Today's Schedule")
    if daily_plan:
        st.table(
            [
                {
                    "Time": task.time,
                    "Task": task.title,
                    "Pet": pet_names_by_task_id[id(task)],
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority,
                }
                for task in daily_plan
            ]
        )
    else:
        st.info("No tasks fit the daily schedule.")

    st.markdown("### Plan explanation")
    st.text(scheduler.explain_plan())
