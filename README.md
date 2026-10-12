# PawPal+

PawPal+ is a Streamlit app for organizing pet care tasks and generating a daily plan within an owner's available time.

## Scenario

A busy pet owner can use PawPal+ to keep care tasks organized and build a daily plan. Each task records its title, duration, priority, category, time, recurrence frequency, completion status, and due date.

## Features

- Sort tasks by time with `Scheduler.sort_by_time()`.
- Filter tasks by pet name and completion status with `Scheduler.filter_tasks()`.
- Create daily or weekly recurring tasks when marking a task complete with `Scheduler.mark_task_complete()`.
- Detect pending tasks scheduled at the exact same time with `Scheduler.detect_conflicts()`.
- Build a daily plan within the owner's available time and explain the selection with `Scheduler.generate_daily_plan()` and `Scheduler.explain_plan()`.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

Start the interactive Streamlit app with:

```bash
streamlit run app.py
```

Run the command-line scheduling example with `python main.py`.

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The tests cover sorting, daily and weekly recurring tasks, conflict detection (including no conflict), empty pets, daily time-budget boundaries (exact fit and one minute over), and filtering by pet name and completion status.

```
collected 12 items

tests\test_pawpal.py ............                                                                  [100%]

12 passed in 0.06s
```

**Confidence Level:** ★★★★☆ (4 out of 5 stars). The tests cover core scheduling behavior and key edge cases, though they do not cover the full Streamlit interface.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting | `Scheduler.sort_by_time()` | Sorts tasks by their `time` value using `sorted(..., key=lambda task: task.time)`. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name and/or completion status; `None` leaves that filter off. |
| Conflict detection | `Scheduler.detect_conflicts()` | Checks pending tasks for the exact same `HH:MM` time and returns warnings instead of crashing. |
| Recurring tasks | `Scheduler.mark_task_complete()` | For daily and weekly tasks, marks the current task complete and creates a new instance with the next `due_date`. |

## Demo Walkthrough

1. Run `streamlit run app.py` and add a pet in the Pets section.
2. Select that pet and add tasks with a title, duration, priority, category, time, and daily or weekly recurrence.
3. Use the task filters to view all pets or one pet, and all, pending, or completed tasks. Per-pet task tables are sorted by time.
4. Select a pending task and choose **Mark complete**. Daily and weekly tasks create their next instance, and the app displays its due date.
5. Choose **Generate schedule** to see exact-time conflict warnings or confirmation that there are none, followed by today's plan and its explanation.

For example, add Milo, schedule a morning walk and an evening medication, then generate the schedule to see today's selected tasks and why they fit the available time. Set two pending tasks to the same time to see a conflict warning.

The command-line demo exercises sorting, filtering, conflict detection, daily recurrence, and plan generation. Its output from `python main.py` is:

```text
=== Sorting and filtering ===
07:30 | Morning walk | Milo | 30 min
07:30 | Vet visit | Luna | 40 min
12:00 | Lunch feeding | Luna | 10 min
18:00 | Evening medication | Milo | 5 min

Filtered by pet name (Milo):
07:30 | Morning walk | completed=False
18:00 | Evening medication | completed=False

Filtered by completion status (completed=False):
07:30 | Morning walk | completed=False
18:00 | Evening medication | completed=False
12:00 | Lunch feeding | completed=False
07:30 | Vet visit | completed=False

=== Conflict warning ===
Warning: 'Morning walk' (Milo) and 'Vet visit' (Luna) are both scheduled at 07:30.

=== Recurring task demo ===
New task due date: 2026-10-12
Full task list:
Milo | Morning walk | 07:30 | completed=True | due=2026-10-11
Milo | Evening medication | 18:00 | completed=False | due=2026-10-11
Milo | Morning walk | 07:30 | completed=False | due=2026-10-12
Luna | Lunch feeding | 12:00 | completed=False | due=2026-10-11
Luna | Vet visit | 07:30 | completed=False | due=2026-10-11

=== Today's schedule ===
07:30 | Vet visit | Luna | 40 min | Priority 5
12:00 | Lunch feeding | Luna | 10 min | Priority 3
18:00 | Evening medication | Milo | 5 min | Priority 5

Daily plan: 120 minutes available.
Completed tasks excluded: 1.
Included tasks:
- 07:30 Vet visit (40 min, priority 5): fits the remaining daily time.
- 12:00 Lunch feeding (10 min, priority 3): fits the remaining daily time.
- 18:00 Evening medication (5 min, priority 5): fits the remaining daily time.
Skipped because they did not fit:
- None.
```
