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
Yes.
- If yes, describe at least one change and why you made it.
I added time and frequency to Task. My original Task had no way to say when a task happens or how often, so the scheduler couldn't make a timed plan.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
It considers the time of each task, the owner's available minutes per day, task priority, whether a task is already completed, and whether it is due today or earlier. 
- How did you decide which constraints mattered most?
I decided the ower's available time matters most, a plan that doesn't fit the day isn't useful. Priority is only used to break ties between tasks that are scheduled at the same time. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
My scheduler only detects conflicts when two tasks are at the exact same time. It doesn't check whether tasks overlap based on how long they last.
- Why is that tradeoff reasonable for this scenario?
Exact-time conflicts are the most obvious mistakes, and checking for them keeps the code simple and easy to read. Checking overlapping durations would be more complicated than this app needs right now.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used the AI coding chat in VSCode for design brainstorming especially for the first UML diagram, generating code in agent mode which was useful making the class skeletons, and also draft tests. I also used it to review code and explain anything I didn't understand. 
- What kinds of prompts or questions were most helpful?
Specific prompts worked best, like naming the exact method, its inputs, and what it should return. I made sure that the code was also very readable. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When I asked for algorithm ideas, the AI suggested to use minutes instead of hour and minutes which I refused. 
- How did you evaluate or verify what the AI suggested?
I ran 'python main.py' a lot to see the output. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested sorting tasks and time, daily and weekly recurring tasks creating the next task with the right due date, conflict detection, a pet with no tasks, the daily time limit, and filtering by pet name and completion status. 
- Why were these tests important?
These behaviors that I tested is what made the scheduler useful to pet owners. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
I'm fairly confident. Every pytest passed. 
- What edge cases would you test next if you had more time?
I would test tasks that would overlap in duration. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The recurring and conflict warning were definitely very time consuming but when I was able to finish it, it was very satified with the time I put in. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
Detecting overlapping durations due to task times. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
Working with AI made me realize how fast it can write code, construct the skeletons, create UMLs, etc. even when I was confused, the AI wasn't. 
