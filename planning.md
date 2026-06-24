# TakeMeter Planning Document
## Project: World Cup 2026 Discourse Classifier

---

## Community Choice

I chose the r/soccer and r/WorldCup subreddits during the 2026 FIFA World Cup. This community is an excellent fit for a classification task because discourse varies enormously in quality — the same event (a goal, a referee decision, a team's performance) generates everything from detailed tactical breakdowns to pure emotional reactions to bold unsupported claims. The World Cup 2026 is currently ongoing, making the data fresh, abundant, and highly varied. Regular participants in this community clearly distinguish between posts that add insight and posts that are just venting or noise, making the label distinctions meaningful and grounded in real community norms.

---

## Label Taxonomy

### 1. `analysis`
**Definition:** The post makes a structured argument supported by specific evidence — statistics, tactical observations, historical comparisons, or player/team performance data. The claim could stand on its own even if you removed the opinion framing.

**Example 1:**
> "Morocco's defensive block has been elite this tournament — they've conceded only 2 goals in 5 matches, and both came from set pieces. Their mid-block sits at a 4-4-2 that cuts off central passing lanes effectively."

**Example 2:**
> "The US midfield is being exposed because they play too narrow. Compare their heat maps to 2022 — they've lost 30% more duels in wide areas, which is exactly where Argentina exploited them."

---

### 2. `hot_take`
**Definition:** A bold, confident opinion stated without supporting evidence or reasoning. The post asserts a strong claim but does not back it up with data, history, or tactical observation. The framing is declarative and often provocative.

**Example 1:**
> "Mbappe is finished. He's been invisible this entire tournament and France will crash out in the quarters."

**Example 2:**
> "Argentina is overrated and Messi only looks good because his teammates do all the work. Any top striker would have those numbers."

---

### 3. `reaction`
**Definition:** An immediate emotional response to a specific match event or result. The post expresses a feeling in the moment — excitement, frustration, disbelief — with little to no argument or claim being made.

**Example 1:**
> "WHAT A GOAL. I cannot believe what I just watched. This World Cup is absolutely insane."

**Example 2:**
> "That red card just ruined the whole match. I'm so done with VAR. Absolutely heartbroken for that team."

---

## Hard Edge Cases

### Anticipated Ambiguous Case
A post that provides one statistic alongside a strong emotional or provocative claim:

> "Mbappe is clearly the best player in this tournament — he has 4 goals in 4 games, nobody else is close."

**Which labels it could belong to:** `analysis` (cites a specific stat) or `hot_take` (bold declarative claim, minimal reasoning, stat is used for effect rather than as part of a structured argument).

**Decision rule:** If the post provides specific, verifiable evidence that supports the claim as part of a structured argument, label it `analysis`. If the evidence is a single cherry-picked stat used to sound credible rather than to genuinely reason through a claim, label it `hot_take`. A post needs more than one data point and some logical structure to qualify as `analysis`. The one-stat post above → `hot_take`.

### Additional Edge Cases Encountered During Annotation

**Difficult Example 1 — analysis vs. hot_take:**
> "Norway's 7 goals in Group I after 2 matches is joint-second highest in the tournament, behind only Germany's 9 goals in Group E. Their direct vertical play is bypassing midfield lines effectively and creating overloads in the box."

This post cites a real statistic and includes a tactical observation, which pulls toward `analysis`. However it only uses one data point and the tactical claim is brief rather than structured. Decision: labeled `analysis` because the combination of a verified stat and a tactical explanation clears the minimum bar for structured argument.

**Difficult Example 2 — hot_take vs. reaction:**
> "Scotland will always be Scotland. Great in qualifying, absolutely bottling it when it matters at tournament football."

The emotional frustration in this post feels like a `reaction`, but there is no specific match event being responded to — it is making a broad declarative claim about Scotland's identity as a tournament team. Decision: labeled `hot_take` because the core of the post is a pattern-based assertion, not an emotional response to a specific moment.

**Difficult Example 3 — hot_take vs. reaction:**
> "Senegal has more talent than half the European teams at this tournament and they're as good as eliminated. Disgraceful."

The word "Disgraceful" and the emotional tone suggest `reaction`, but the post's core is a bold unsupported claim comparing Senegal's talent to European teams — a classic hot take structure. Decision: labeled `hot_take` because the dominant content is an assertive claim, not a response to a specific match event.

## Data Collection Plan

- **Source:** Reddit — r/soccer and r/WorldCup public posts and comments during the 2026 FIFA World Cup
- **Method:** Manual collection by reading posts and copy-pasting into a CSV file. An LLM (Claude) will be used to pre-label batches of examples using the label definitions above, which I will then review and correct every single example before finalizing.
- **Target distribution:** ~70 examples per label (roughly equal thirds across `analysis`, `hot_take`, and `reaction`) — no label above 70% of the dataset
- **If a label is underrepresented:** Specifically search for posts of that type (e.g., search r/soccer for tactical discussion threads to find more `analysis` examples)
- **File format:** Single CSV with columns: `text`, `label`, `notes`
- **Split:** Handled automatically by the Colab notebook (70% train / 15% validation / 15% test)

---

## Evaluation Metrics

I will use the following metrics and report them for both the fine-tuned model and the baseline:

- **Overall accuracy:** Fraction of test examples correctly classified. Reported for both models for direct comparison.
- **Per-class F1 score:** Harmonic mean of precision and recall for each label. This is the right metric here because the task has 3 classes and F1 catches cases where the model is gaming accuracy by over-predicting one class.
- **Confusion matrix:** Shows exactly which label pairs the model confuses and in which direction — more informative than aggregate metrics alone.

Accuracy alone is insufficient because a model that predicts `hot_take` for everything could achieve high accuracy if that label dominates. Per-class F1 and the confusion matrix reveal whether the model is genuinely learning all three distinctions.

---

## Definition of Success

The fine-tuned model will be considered "good enough" for deployment in a real community tool if it meets all three of the following thresholds on the test set:

1. **Overall accuracy ≥ 0.75** (meaningfully above random chance of 0.33 for 3 classes)
2. **Per-class F1 ≥ 0.65 for every label** (no label is being systematically ignored)
3. **Fine-tuned model outperforms the zero-shot baseline** on both overall accuracy and average F1

If the model fails any of these, I will investigate label inconsistency, class imbalance, or insufficient training examples before considering it deployable.

---

## AI Tool Plan

### 1. Label Stress-Testing
I will provide Claude with my label definitions and edge case description and ask it to generate 10 posts that sit at the boundary between two labels — particularly between `analysis` and `hot_take`. If Claude produces posts I cannot cleanly classify, I will tighten my definitions before annotating 200 examples.

### 2. Annotation Assistance
I will use Claude to pre-label batches of collected posts using the exact label definitions from this document. I will review and correct every single pre-assigned label — I will not skim. Pre-labeled examples and my corrections will be disclosed in the AI usage section of the README.

### 3. Failure Pattern Analysis
After fine-tuning, I will paste my list of wrong predictions into Claude and ask it to identify common themes — label pairs confused, post length, sarcasm, ambiguous phrasing. I will verify every suggested pattern myself by re-reading the examples, and document what I confirmed, what I corrected, and what I discarded.

---

## Stretch Features Plan

### Deployed Interface (+1pt)
I will build a simple web interface (Gradio or HTML+JS) that accepts a new post as text input, runs it through the fine-tuned model, and displays the predicted label and confidence score. The interface code will be committed to the repo and documented in the README.

### Error Pattern Analysis (+1pt)
Beyond listing individual wrong predictions, I will identify a systematic pattern across errors — a specific label pair, post type, or distributional issue the model consistently struggles with — and support it with evidence from the full error set.


## Stretch Features Plan

### Deployed Interface  - COMPLETED
Built a Gradio web interface that accepts a new post as text input, runs it through the fine-tuned DistilBERT model, and displays the predicted label and confidence score with all three label probabilities. Interface code is committed at `interface/app.py`. Runs inside Google Colab after fine-tuning is complete.

### Error Pattern Analysis - COMPLETED
Identified a systematic pattern across all 6 errors: the model consistently misclassifies calm, observational reaction posts as hot_takes. All errors share the absence of emotional markers (ALL CAPS, exclamation marks) and a declarative sentence structure. Full analysis with supporting evidence is documented in the README evaluation report.
