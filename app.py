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
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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

if st.session_state.owner.pets:
    with st.form("add_task_form"):
        selected_pet_index = st.selectbox(
            "Pet",
            options=range(len(st.session_state.owner.pets)),
            format_func=lambda index: st.session_state.owner.pets[index].name,
        )
        task_title = st.text_input("Task title", value="")
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority_label = st.selectbox("Priority", ["low", "medium", "high"])
        category = st.text_input("Category", value="feeding")
        task_time = st.time_input("Time", value=time(8, 0))
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted and task_title.strip():
        priority_values = {"low": 1, "medium": 2, "high": 3}
        task = Task(
            title=task_title.strip(),
            duration_minutes=int(duration),
            priority=priority_values[priority_label],
            category=category.strip(),
            time=task_time.strftime("%H:%M"),
        )
        st.session_state.owner.pets[selected_pet_index].add_task(task)

    for pet in st.session_state.owner.pets:
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
                    }
                    for task in pet.tasks
                ]
            )
        else:
            st.caption("No tasks added.")

st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    daily_plan = scheduler.generate_daily_plan()
    pet_names_by_task_id = {
        id(task): pet.name
        for pet in st.session_state.owner.pets
        for task in pet.tasks
    }

    st.markdown("### Today's Schedule")
    if daily_plan:
        for task in daily_plan:
            pet_name = pet_names_by_task_id[id(task)]
            st.write(
                f"{task.time} | {task.title} | {pet_name} | "
                f"{task.duration_minutes} min | Priority {task.priority}"
            )
    else:
        st.info("No tasks fit the daily schedule.")

    st.markdown("### Plan explanation")
    st.text(scheduler.explain_plan())
