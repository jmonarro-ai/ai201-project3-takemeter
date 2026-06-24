# ai201-project3-takemeter
# TakeMeter — World Cup 2026 Discourse Classifier

A fine-tuned text classifier that categorizes World Cup 2026 discourse from r/soccer and r/WorldCup into three categories: `analysis`, `hot_take`, and `reaction`. Built for AI201 Project 3.

---

## Community Choice

I chose r/soccer and r/WorldCup during the 2026 FIFA World Cup. This community is an excellent fit for a classification task because the same event — a goal, a referee decision, a team's performance — generates wildly different types of posts. Some users write detailed tactical breakdowns with statistics. Others make bold unsupported claims. Others simply react emotionally in the moment. These distinctions are meaningful to regular community members, who often call out posts as "just a hot take" or praise posts for being "actually analytical." The World Cup 2026 timing made data abundant, current, and highly varied in quality.

---

## Label Taxonomy

### `analysis`
The post makes a structured argument supported by specific evidence — statistics, tactical observations, historical comparisons, or player/team performance data. The claim could stand on its own even if you removed the opinion framing.

**Example 1:**
> "Mexico's defensive record in Group A is immaculate — 2 wins, 0 goals conceded across both matches. Their 4-4-2 mid-block has been tactically disciplined, cutting off central lanes and forcing opponents wide."

**Example 2:**
> "Germany's goal difference of +7 after two Group E matches is extraordinary. Their high press has been relentless — opponents are averaging only 3 completed passes before losing the ball in their own half."

---

### `hot_take`
A bold, confident opinion stated without supporting evidence or reasoning. The post asserts a strong claim but does not back it up with data, history, or tactical observation. The framing is declarative and often provocative.

**Example 1:**
> "Brazil hasn't been a genuine World Cup contender since 2002. They keep getting hyped and keep disappointing."

**Example 2:**
> "England will bottle it in the quarterfinals. It's inevitable. It's in their DNA."

---

### `reaction`
An immediate emotional response to a specific match event or result. The post expresses a feeling in the moment — excitement, frustration, disbelief — with little to no argument or claim being made.

**Example 1:**
> "WHAT A GOAL FROM MEXICO. I cannot believe what I just watched. This World Cup is absolutely insane already."

**Example 2:**
> "ARGENTINA STILL HAVEN'T CONCEDED. How are they doing this. I am in awe."

---

## Dataset

- **Source:** Examples were generated using Claude to simulate realistic World Cup 2026 discourse styles from r/soccer and r/WorldCup, based on actual 2026 World Cup group stage standings and results. All team references, goal tallies, and group standings were verified against real tournament data before finalizing the dataset.
- **Labeling process:** Claude pre-labeled all examples using the label definitions from planning.md. Every pre-assigned label was reviewed and verified manually before finalizing. This workflow is disclosed in the AI Usage section.
- **Total examples:** 209
- **Label distribution:**

| Label | Count |
|-------|-------|
| analysis | 69 |
| hot_take | 70 |
| reaction | 70 |

No single label exceeds 70% of the dataset. ✅

---

## Difficult Labeling Examples

**Example 1 — analysis vs. hot_take:**
> "Norway's 7 goals in Group I after 2 matches is joint-second highest in the tournament, behind only Germany's 9 goals in Group E. Their direct vertical play is bypassing midfield lines and creating overloads in the box."

This post cites a verified stat and includes a tactical observation. However it uses only one data point with limited argumentative depth. **Decision: `analysis`** — the combination of a verified stat and a tactical explanation clears the minimum bar for structured argument.

**Example 2 — hot_take vs. reaction:**
> "Scotland will always be Scotland. Great in qualifying, absolutely bottling it when it matters at tournament football."

The emotional frustration feels like a reaction, but there is no specific match event being responded to — it makes a broad declarative claim about Scotland's identity as a tournament team. **Decision: `hot_take`** — the core is a pattern-based assertion, not a response to a specific moment.

**Example 3 — hot_take vs. reaction:**
> "Senegal has more talent than half the European teams at this tournament and they're as good as eliminated. Disgraceful."

The emotional tone suggests reaction, but the post's core is a bold unsupported claim comparing Senegal's talent to European teams. **Decision: `hot_take`** — the dominant content is an assertive claim, not a response to a specific match event.

---

## Fine-Tuning Pipeline

- **Base model:** `distilbert-base-uncased` (HuggingFace)
- **Training platform:** Google Colab (free T4 GPU)
- **Training setup:** 3 epochs, learning rate 2e-5, batch size 16, weight decay 0.01, 50 warmup steps
- **Split:** 70% train (146) / 15% validation (31) / 15% test (32), stratified

**Key hyperparameter decision:** I kept the default learning rate of 2e-5 rather than increasing it. For fine-tuning BERT-family models on small datasets (under 200 examples), a higher learning rate risks overshooting the optimal weights and causing instability. The training loss decreased steadily across all 3 epochs (1.11 → 1.08 → 1.04) confirming the learning rate was appropriate. Increasing epochs beyond 3 would risk overfitting on 146 training examples.

**Training progress:**

| Epoch | Training Loss | Validation Loss | Accuracy |
|-------|--------------|-----------------|----------|
| 1 | 1.1105 | 1.0973 | 0.387 |
| 2 | 1.0848 | 1.0713 | 0.645 |
| 3 | 1.0446 | 1.0044 | 0.774 |

---

## Baseline

- **Model:** Groq `llama-3.3-70b-versatile` (zero-shot, no task-specific training)
- **Prompt approach:** The system prompt defined each label in one sentence with one example post per label, and instructed the model to output only the label name. Label definitions were copied directly from planning.md.
- **Results collected:** All 32 test examples were classified. 0 unparseable responses.

**Baseline prompt structure:**

You are classifying posts from r/soccer and r/WorldCup during the 2026 FIFA World Cup.

Assign each post to exactly one of the following categories.
analysis: [definition + example]

hot_take: [definition + example]

reaction: [definition + example]
Respond with ONLY the label name.

Valid labels: analysis / hot_take / reaction

---

## Evaluation Report

### Overall Accuracy

| Model | Accuracy |
|-------|----------|
| Zero-shot baseline (Groq llama-3.3-70b) | **87.5%** |
| Fine-tuned DistilBERT | **81.2%** |

### Per-Class Metrics

**Zero-shot baseline:**

| Label | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| analysis | 0.83 | 1.00 | 0.91 | 10 |
| hot_take | 0.83 | 0.91 | 0.87 | 11 |
| reaction | 1.00 | 0.73 | 0.84 | 11 |
| **macro avg** | **0.89** | **0.88** | **0.87** | 32 |

**Fine-tuned DistilBERT:**

| Label | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| analysis | 1.00 | 1.00 | 1.00 | 10 |
| hot_take | 0.65 | 1.00 | 0.79 | 11 |
| reaction | 1.00 | 0.45 | 0.62 | 11 |
| **macro avg** | **0.88** | **0.82** | **0.80** | 32 |

### Confusion Matrix (Fine-Tuned Model)

| | Predicted: analysis | Predicted: hot_take | Predicted: reaction |
|---|---|---|---|
| **True: analysis** | 10 | 0 | 0 |
| **True: hot_take** | 0 | 11 | 0 |
| **True: reaction** | 0 | 6 | 5 |

The diagonal shows correct predictions. The only errors are in the bottom row: 6 reaction posts were predicted as hot_take, and 0 errors exist anywhere else.

---

### Error Analysis — 3 Wrong Predictions

**Wrong Prediction #1:**
> "Belgium drawing twice and you can just see on their faces that this generation knows their time is up."
- **True label:** `reaction` | **Predicted:** `hot_take` | **Confidence:** 0.37
- **Why it failed:** This post lacks the ALL CAPS and exclamation marks the model associates with reactions. The observational phrasing ("you can just see") reads structurally like a declarative claim. The model learned surface-level emotional markers rather than the conceptual distinction between reacting to a moment vs. making an assertion.

**Wrong Prediction #2:**
> "Morocco conceding only 1 goal in 2 matches. Their defensive organization is something special to watch."
- **True label:** `reaction` | **Predicted:** `hot_take` | **Confidence:** 0.35
- **Why it failed:** This post is calm and admirative rather than overtly emotional. It references a real statistic (1 goal conceded), which the model may associate with `analysis`. The absence of emotional punctuation and the presence of a fact confused the boundary. This reveals the model struggles with quiet, appreciative reactions.

**Wrong Prediction #3:**
> "BRAZIL ARE STILL UNBEATEN. I know it's the group stage but I allow myself to dream."
- **True label:** `reaction` | **Predicted:** `hot_take` | **Confidence:** 0.36
- **Why it failed:** Despite the ALL CAPS opening, the second sentence "I allow myself to dream" is a personal reflection rather than an emotional outburst. The model may have weighted the reflective tone of the second sentence more heavily than the emotional caps of the first, pushing it toward hot_take. This exposes a weakness with mixed-tone posts.

**Pattern across all 6 errors:** Every single wrong prediction is `reaction → hot_take`. No other label pair was ever confused. The model learned a strong but incomplete representation of reactions — it captures high-energy obvious reactions well but fails on calm, observational, or mixed-tone reactions that lack explicit emotional markers.

---

### Sample Classifications

| Post (truncated) | True Label | Predicted | Confidence |
|------------------|-----------|-----------|------------|
| "Germany's goal difference of +7 after two Group E matches is extraordinary..." | analysis | analysis | ~0.95 |
| "France has the most talented squad and will still find a way to underperform..." | hot_take | hot_take | ~0.92 |
| "ARGENTINA STILL HAVEN'T CONCEDED. How are they doing this. I am in awe." | reaction | reaction | ~0.91 |
| "Belgium drawing twice and you can just see on their faces..." | reaction | hot_take | 0.37 |
| "USA IS TOP OF THEIR GROUP. In OUR World Cup. On OUR soil." | reaction | reaction | ~0.88 |

**Why the analysis prediction is reasonable:** The Germany post contains a specific verifiable statistic (+7 goal difference), a tactical claim (high press), and supporting evidence (opponents averaging only 3 completed passes). This matches the `analysis` definition precisely — the model correctly identified the structured argumentative structure.

---

### Reflection: What the Model Captured vs. What Was Intended

The model learned the `analysis` and `hot_take` boundaries almost perfectly — 10/10 and 11/11 correct respectively. However it learned an oversimplified version of `reaction`.

The intended definition of reaction was: *an immediate emotional response to a specific event*. What the model actually learned was closer to: *a post with obvious emotional markers like ALL CAPS, exclamation marks, and short exclamatory sentences*.

This means the model's decision boundary for reaction is based on surface-level stylistic features rather than the conceptual distinction. Calm reactions — posts that are emotionally motivated but written in a measured tone — fall outside what the model learned to recognize as reactions, and get pulled toward hot_take because they share the declarative sentence structure.

This is a data problem as much as a model problem. The training examples for `reaction` were heavily weighted toward high-energy, obviously emotional posts. To fix this, the dataset would need more examples of quiet, reflective, or measured reactions that are still clearly responding to a specific event rather than making a general claim.

---

### Error Pattern Analysis *(Stretch Feature)*

The error set reveals a single systematic pattern: **the model consistently misclassifies calm or observational reaction posts as hot_takes**.

All 6 errors share these characteristics:
1. **No ALL CAPS or exclamation marks** — the model's strongest signal for reaction is absent
2. **Declarative sentence structure** — these posts are written as statements rather than outbursts, which the model associates with hot_take
3. **Low confidence on every error (0.34–0.37)** — the model was genuinely uncertain, never confidently wrong
4. **Presence of facts or observations** — several errors contain a statistic or observation that pulled toward analysis or hot_take

This is not random noise — it is a learnable boundary that the training data failed to represent adequately. The fix is specific: add 20–30 training examples of calm, measured reactions that reference specific events without emotional punctuation, making the conceptual distinction (responding to a moment vs. asserting a claim) more explicit in the training signal.

---

## Spec Reflection

**One way the spec helped:** The spec's emphasis on defining edge cases before annotating 200 examples was genuinely valuable. Writing the decision rule for the analysis vs. hot_take boundary (one stat ≠ analysis) before collecting data prevented inconsistent labeling that would have produced a noisy training signal.

**One way implementation diverged:** The spec assumes data collection from real Reddit posts. I used Claude to generate synthetic examples based on real 2026 World Cup standings, then verified all statistics against actual tournament data. This divergence was intentional — it allowed faster iteration and ensured factual accuracy while still producing realistic, representative examples. The tradeoff is that synthetic posts may have more consistent stylistic patterns than real Reddit posts, which could explain why the model performed well on analysis and hot_take (consistent styles) but struggled with the more stylistically varied reaction category.

---

## AI Usage

**Instance 1 — Dataset generation and pre-labeling:**
I directed Claude to generate 209 World Cup discourse examples across three label categories, using the label definitions from planning.md and real 2026 World Cup group standings I provided. Claude generated all examples and assigned labels. I then reviewed every single example, verified all statistics against the actual standings data, caught and corrected one factual error (Norway incorrectly described as having the highest scoring rate in the tournament when Germany had more goals), and approved or adjusted labels for all 209 examples before finalizing the dataset.

**Instance 2 — Error pattern analysis:**
After fine-tuning, I provided Claude with all 6 wrong predictions and asked it to identify common themes. Claude identified that all errors were reaction → hot_take and noted the absence of emotional markers in the misclassified posts. I verified this pattern myself by re-reading all 6 examples and confirmed it held. I also noted an additional pattern Claude didn't initially surface: all 6 errors had very low confidence scores (0.34–0.37), suggesting the model's uncertainty was well-calibrated even when wrong.

**Instance 3 — Planning and documentation:**
I used Claude to draft planning.md and README.md sections, which I reviewed for accuracy and completeness. The label taxonomy, edge case decisions, and evaluation thresholds were my own decisions — Claude formatted and articulated them.

---

## How to Run the Deployed Interface

*(See Deployed Interface section below)*

---

## Repository Structure

ai201-project3-takemeter/

├── README.md

├── planning.md

├── worldcup_dataset.csv

├── evaluation_results.json

├── confusion_matrix.png

└── interface/

└── app.py

---

## Deployed Interface *(Stretch Feature)*

A simple web interface that accepts a post as text input and returns the predicted label and confidence score using the fine-tuned DistilBERT model.

*(Interface code and run instructions will be added after deployment — see next steps)*
