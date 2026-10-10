# Product experience pulse

**Survey ID:** `product-experience-pulse`  
**Version:** 1.0.0  
**Audience:** People who attempted the target task in the product within the past 7 days.  
**Estimated time:** 3 minutes

> **Purpose:** Measure task outcome and perceived ease for a recent product task so the team can identify experience regressions and diagnostic follow-up needs.

## Before you begin

Participation is voluntary. You may skip optional questions or stop at any time.

## Your recent experience

### 1. What happened the last time you tried to complete this task?

`ID: task_outcome` · `single_choice` · Required

- ○ I completed it [completed]
- ○ I completed part of it [partial]
- ○ I did not complete it [not_completed]
- ○ I am not sure [not_sure]

**Rationale:** Establishes the behavioral outcome for the focal episode.
**Construct:** self-reported task outcome
**Analysis use:** Report completion distribution and use it to interpret ease.

### 2. How easy or difficult was it to complete as much of the task as you did?

`ID: task_ease` · `rating` · Required

Scale: 1 to 7 in steps of 1
Anchors: 1 = Very difficult; 4 = Neither easy nor difficult; 7 = Very easy

**Rationale:** Measures perceived ease for the same focal episode.
**Construct:** perceived task ease
**Analysis use:** Primary experience metric; report the full distribution and compare by task outcome.

### 3. What was the main obstacle, if any?

`ID: main_obstacle` · `single_choice` · Optional

- ○ No obstacle [none] (exclusive)
- ○ I could not find what I needed [could_not_find]
- ○ The instructions were unclear [instructions]
- ○ Something did not work as expected [technical]
- ○ I did not have the information I needed [information]
- ○ It took more time than I had [time]
- ○ Another obstacle [other]

**Rationale:** Provides a structured diagnostic for the primary outcome.
**Construct:** primary task obstacle
**Analysis use:** Report shares among respondents who encountered an obstacle and compare with ease.

### 4. What is one change that would have made this task easier?

`ID: improvement` · `textarea` · Optional

`[Long response]`

**Rationale:** Collects focused diagnostic detail without requiring a long response.
**Construct:** suggested task improvement
**Analysis use:** Code themes and connect them to outcome and ease; do not treat theme counts as population prevalence without context.

## Close

### 5. May the research team invite you to a separate follow-up study?

`ID: future_research` · `single_choice` · Optional

- ○ Yes [yes]
- ○ No [no]
- ○ Not sure [not_sure]

**Rationale:** Obtains permission for future contact without collecting contact data in this survey.
**Construct:** follow-up permission
**Analysis use:** Use only with an approved external contact linkage process.

## Thank you

Thank you for sharing your experience.
