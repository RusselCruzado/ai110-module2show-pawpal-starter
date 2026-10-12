from pawpal_system import Pet, Task


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