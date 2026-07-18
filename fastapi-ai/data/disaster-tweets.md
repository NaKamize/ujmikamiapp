# Disaster Tweets Classification

## Overview

Entry for Kaggle's "NLP Getting Started" competition ("Real or Not? NLP with
Disaster Tweets"): binary classification of tweets (7,613 train / 3,263 test rows)
into real-disaster (target=1) vs. not (target=0), using tweet text plus optional
keyword/location fields.

## Approach — DeBERTa + gradient-boosted meta-stack

1. **Preprocessing**: lowercasing, URL/mention stripping, hashtag unpacking, HTML
   entity and emoji removal. The competition's `keyword` field is prepended to the
   tweet text as an explicit domain signal.
2. **Feature engineering**: ~30 hand-crafted features — uppercase/hashtag/mention/
   URL/punctuation counts, a fixed disaster-keyword list, Laplace-smoothed
   keyword "priors" (P(disaster|keyword)), elongated-word counts, and VADER
   sentiment scores (compound/pos/neg/neu).
3. **Confident Learning label cleaning**: a 3-fold, 2-epoch DeBERTa pre-scan flags
   and flips noisy labels where out-of-fold confidence strongly disagrees with the
   given label — 587 labels were flipped in the recorded run.
4. **Transformer backbone**: `microsoft/deberta-v3-base` with a custom pooling
   head (CLS token concatenated with mean-pooled token embeddings), 5-fold
   stratified CV, class-weighted cross-entropy with label smoothing, AdamW with
   linear warmup.
5. **Meta-classifier stacking**: 5-fold OOF transformer probabilities are combined
   with the 30 scaled engineered features into a 31-column meta matrix, feeding
   both XGBoost and LightGBM; the winner is picked by tuned F1 threshold on a
   held-out split.
6. **Optional augmentation** (back-translation EN→FR→EN via MarianMT, plus EDA-style
   synonym replacement/deletion/swap) exists in the pipeline but is disabled in the
   final configuration — it was found to shift the training distribution away from
   the test distribution and hurt the public leaderboard score despite looking
   good locally.

## Results

- DeBERTa backbone OOF F1 @0.5: **0.8603** on cleaned labels vs. 0.7643 on original
  (noisy) labels.
- Final meta-model (XGBoost, threshold 0.44) on held-out validation: **F1 0.8613,
  Precision 0.8489, Recall 0.8742, Accuracy 0.8791**.
- **Public Kaggle leaderboard: F1 0.81182, rank 414/855.**

## Tech stack

PyTorch, Hugging Face Transformers (DeBERTa-v3, MarianMT for back-translation),
XGBoost, LightGBM, scikit-learn, NLTK (VADER sentiment, WordNet), pandas/NumPy.
Single-notebook Kaggle project, CUDA-aware, tuned to run on a T4 GPU.

## Notable lessons (documented "what did not work well")

- Class-balancing via disaster-only augmentation shifted the train distribution
  away from the test distribution and hurt leaderboard score despite looking good
  in local validation.
- An early, weak 2-epoch confident-learning pre-scan flipped otherwise-valid
  labels — later tuned more conservatively (threshold 0.80).
- Dynamic per-fold class weighting under-weighted the disaster class and hurt
  recall.
- Feeding raw transformer probabilities directly into XGBoost (rather than as one
  input among independent engineered features) reduced model independence and
  made the blend less robust — this is why the final architecture keeps the
  meta-model trained on OOF probabilities *plus* separately engineered features
  rather than raw embeddings.
- Submission-safety asserts (no NaNs, binary-only targets, correct column order)
  are run before every `submission.csv` write.
