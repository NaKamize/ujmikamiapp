# Chatbot Arena — LLM Preference Prediction

## Overview

Entry to the Kaggle "LLM Classification Finetuning" competition (Chatbot Arena
human-preference prediction). Given a user prompt and two LLM-generated responses
(from models like `gpt-4-1106-preview`, `gpt-4-0613`), the task is to predict which
response a human rater preferred — a 3-class problem (`winner_model_a`,
`winner_model_b`, `winner_tie`) scored by log loss, over 57,481 labeled training
rows.

## Approach — hybrid stacking pipeline

1. **Text formatting**: prompt and both responses are wrapped in explicit anchor
   tokens (`[PROMPT_START]...[PROMPT_END]`, `[RESPONSE_A_START]...`,
   `[RESPONSE_B_START]...`), truncated to 120/180 words respectively, to help the
   transformer structurally separate the three segments.
2. **Deep model**: fine-tuned `microsoft/deberta-v3-large` (24 layers, ~874MB),
   tokenizer extended with the 6 custom anchor tokens. Trained with gradient
   checkpointing, gradient accumulation (effective batch 16), linear warmup, and a
   NaN/Inf-loss guard — a defensive fix for numerical instability encountered
   during fine-tuning on a memory-constrained Tesla T4.
3. **Test-time augmentation**: inference run twice per example (original order and
   with response_a/response_b swapped), probabilities averaged to cancel
   positional bias.
4. **Hand-engineered features**: length diffs/ratios, Jaccard similarity between
   prompt and each response, markdown/code-block counts, and counts of "AI-tell"
   phrases (e.g. "as an ai", "delve", "tapestry", "in conclusion") — explicitly
   targeting known LLM stylistic fingerprints as predictive signal.
5. **TF-IDF + SVD**: 1-2 gram TF-IDF (25k features) reduced to 64 components via
   TruncatedSVD, as a dense text-subspace feature.
6. **Meta-stacking ensemble**: SVD features + hand-engineered features + DeBERTa's
   out-of-fold TTA probabilities (~111 dims total) feed a 4-fold stack of XGBoost,
   LightGBM, and CatBoost (all GPU-accelerated), averaged across boosters and folds.
7. **Deployment resilience**: a separate inference-only notebook loads saved
   DeBERTa/GBDT artifacts from Kaggle Datasets, falling back to retraining any
   missing fold models on the fly.

## Results

Final Kaggle leaderboard: **rank 116/257, score 1.04331** (log loss, lower is
better). The DeBERTa-only baseline scored 1.0977 OOF log loss, so the GBDT
stacking layer meaningfully improved on the deep model alone. Solution history
shows iterative improvement: TF-IDF + chi-square baseline (rank 168/263) →
DistilBERT fine-tune (rank 112/257) → final DeBERTa-v3-large + GBDT stack
(rank 116/257) — with Gemma2-9B-it and various DistilBERT variants tried and
abandoned along the way (visible in `.gitignore` history).

## Tech stack

PyTorch 2.12 (CUDA), Hugging Face Transformers 4.46, XGBoost 3.2, LightGBM 4.6,
CatBoost 1.2 (all GPU-enabled), scikit-learn, pandas, joblib.

## Notable engineering decisions

Treating the fine-tuned transformer as a *feature generator* rather than the sole
predictor — its softmax probabilities become just 3 of ~111 meta-features blended
with shallow tabular/stylistic signals — is the core design idea, explicitly
described as a "hybrid ensemble blending deep text and tabular predictions."
