# predictor.py

import numpy as np
from model_loader import infer, tokenizer, MAX_LENGTH


def compute_breakdown_scores(text):
    tokens = [t.lower() for t in text.split() if t.isalpha() or t.isalnum()]
    n = max(1, len(tokens))

    trigrams = [' '.join(tokens[i:i+3]) for i in range(max(0, n-2))]
    repetition = 1 - (len(set(trigrams)) / max(1, len(trigrams)))

    types = len(set(tokens))
    ttr = types / n
    vocab_richness = 1 - ttr

    sentences = [s.strip() for s in text.replace('?', '.').replace('!', '.').split('.') if s.strip()]
    if len(sentences) <= 1:
        synt_var = 0.0
    else:
        lens = [len(s.split()) for s in sentences]
        synt_var = 1 - (np.std(lens) / (np.mean(lens) + 1e-6))

    return {
        "repetition": round(np.clip(repetition, 0, 1) * 100, 2),
        "vocab_richness": round(np.clip(vocab_richness, 0, 1) * 100, 2),
        "syntactic_variation": round(np.clip(synt_var, 0, 1) * 100, 2)
    }

def verdict_from_prob(prob):
    score = round(prob * 100, 2)
    if score >= 70:
        return score, "Likely AI-Generated", "High", "red"
    elif score >= 40:
        return score, "Mixed/Uncertain", "Medium", "yellow"
    else:
        return score, "Likely Human-Created", "Low", "green"

def analyze_text(text: str):
    enc = tokenizer(
        [text],
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="tf"
    )

    outputs = infer(
        input_ids=enc["input_ids"],
        attention_mask=enc["attention_mask"]
    )

    raw_output = float(outputs[list(outputs.keys())[0]][0][0])


    # Convert safely to float and clamp
    prob_ai = float(np.clip(raw_output, 0.0, 1.0))

    score, verdict, confidence, badge_color = verdict_from_prob(prob_ai)
    breakdown = compute_breakdown_scores(text)

    return {
        "overall_ai_score": score,
        "overall_human_score": round(100 - score, 2),
        "verdict": verdict,
        "confidence": confidence,
        "badge_color": badge_color,
        
        "breakdown": {
            "Perplexity_proxy_Repetition": breakdown["repetition"],
            "Vocabulary_Richness_proxy": breakdown["vocab_richness"],
            "Syntactic_Variation_proxy": breakdown["syntactic_variation"]
        },
        "model_note": "This result is based on a probabilistic AI-vs-human classifier trained on multiple datasets.",


        "limitations": [
            "This system cannot guarantee 100% accuracy and should not be used as the only source to judge content authenticity ",
            "Text written by humans with very formal or repetitive style may sometimes appear AI-generated.",
            "AI-generated text that is heavily edited by humans may not be detected correctly.",
            "This tool does not identify which AI tool was used, only the likelihood of AI involvement."
        ]
    }
