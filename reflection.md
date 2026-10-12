# PawPal+ Project Reflection

## 1. System Design

Three core actions:
1. A user can enter their info and add one or more pets (name, species, age).
2. A user can add or edit care tasks for a pet, with at least a duration and a priority (walks, feeding, meds, and so on).
3. A user can generate a daily plan that fits their available time and see why each task was chosen or skipped.

**a. Initial design**

- Briefly describe your initial UML design.
My initial design has four classes. Owner stores the user’s name, daily time budget, and preferences, and holds their pets. Pet stores basic pet info and owns a list of care tasks. Task represents a single care activity with a duration, priority, and category, and tracks whether it’s done. Scheduler is the “brain”: it takes an owner, gathers all tasks across their pets, and builds a daily plan that fits the available time, then explains its choices. I separated data (Owner, Pet, Task) from logic (Scheduler) so the scheduling rules can change without touching the data classes.
- What classes did you include, and what responsibilities did you assign to each?
  - Owner: stores the user's name, daily time budget, and preferences,
    and holds their pets. It can add a pet and gather all tasks across
    every pet.
  - Pet: stores basic info (name, species, age) and owns a list of care
    tasks. It can add or remove tasks.
  - Task: represents a single care activity, such as a walk or feeding.
    It tracks a title, duration, priority, and category, and whether it's
    completed.
  - Scheduler: the "brain" of the app. It takes an Owner, collects all
    their tasks, builds a daily plan that fits the available time and
    priorities, and explains its choices.

**b. Design changes**

- Did your design change during implementation?
No.
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
