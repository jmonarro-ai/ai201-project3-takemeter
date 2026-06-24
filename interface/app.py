# TakeMeter — Deployed Interface
# Run instructions:
#   1. Open the Colab notebook and run all cells through Section 3 (fine-tuning)
#   2. Add the cell below at the bottom of the notebook and run it
#   3. Click the public Gradio URL that appears

# Requirements: gradio, torch, transformers
# !pip install -q gradio

import gradio as gr
import torch
import numpy as np

def classify_post(text):
    if not text.strip():
        return "Please enter a post to classify."
    
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=256
    )
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    probs_np = probs.numpy()[0]
    
    pred_id = np.argmax(probs_np)
    pred_label = ID_TO_LABEL[pred_id]
    confidence = probs_np[pred_id]
    
    result = f"**Predicted Label:** {pred_label}\n\n"
    result += f"**Confidence:** {confidence:.1%}\n\n"
    result += "---\n\n**All scores:**\n"
    for i, label in ID_TO_LABEL.items():
        result += f"- {label}: {probs_np[i]:.1%}\n"
    
    return result

demo = gr.Interface(
    fn=classify_post,
    inputs=gr.Textbox(
        lines=4,
        placeholder="Paste a World Cup post here...",
        label="Post Text"
    ),
    outputs=gr.Markdown(label="Classification Result"),
    title="TakeMeter — World Cup 2026 Discourse Classifier",
    description="Classifies World Cup posts as **analysis**, **hot_take**, or **reaction** using a fine-tuned DistilBERT model.",
    examples=[
        ["Germany's goal difference of +7 after two Group E matches is extraordinary. Their high press has been relentless — opponents are averaging only 3 completed passes before losing the ball."],
        ["France has the most talented squad in the tournament and will still find a way to underperform in the knockout stages."],
        ["ARGENTINA STILL HAVEN'T CONCEDED. How are they doing this. I am in awe."],
        ["Morocco conceding only 1 goal in 2 matches. Their defensive organization is something special to watch."],
    ],
    allow_flagging="never"
)

demo.launch(share=True)
