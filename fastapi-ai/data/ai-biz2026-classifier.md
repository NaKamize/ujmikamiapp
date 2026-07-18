# AI-Biz2026 Fashion-MNIST Classifier

## Overview

Competition entry for the AI-Biz2026 workshop ("International Workshop: Artificial
Intelligence of and for Business," associated with JSAI-isAI 2026), Kaggle slug
`ai-biz-2026-spring-task-3`. The task: classify Fashion-MNIST grayscale images
(28×28) into 10 clothing categories (T-shirt/top, Trouser, Pullover, Dress, Coat,
Sandal, Shirt, Sneaker, Bag, Ankle boot) from 60,000 labeled training rows and
10,000 unlabeled test rows, distributed as flattened-pixel CSVs.

## Result

**3rd place out of 38 teams.** Public score 0.95440, private score 0.95560. On the
held-out 6,000-sample validation split, the final fused model reached **95.42%
accuracy** (base ensemble alone: 95.35%). The hardest confusion
cluster was T-shirt/Pullover/Coat/Shirt — Shirt had the lowest per-class F1 (0.8661),
while Trouser and Bag were near-perfect (F1 ≈ 0.9975).

## Approach

- **Base model**: a custom ResNet-with-Squeeze-Excitation network
  (`fmnist_resnet_se`, 2.8M parameters) trained natively on 28×28 grayscale input
  (no upscaling). Stem conv → 3 residual stages (64→128→256 filters) each ending
  in an SE block (GAP → FC(swish) → FC(sigmoid) → channel-wise multiply) → GAP →
  Dropout → 10-way softmax. Swish activation used throughout for smoother gradients.
- **Base ensemble**: 5 independently trained models (seeds 11, 23, 47, 59, 73),
  each on a 90/10 stratified split, softmax-averaged. AdamW (lr 2e-3, weight decay
  1e-4), `ReduceLROnPlateau` + `EarlyStopping`.
- **Augmentation**: on-the-fly `tf.data` pipeline with random translation, zoom,
  contrast, and a custom `RandomCutout` layer (8×8 zeroed patch) that forces the
  model to rely on global texture rather than one region.
- **Specialist sub-model**: a separate 4-class ResNet-SE trained only on the
  "shirt cluster" (T-shirt, Pullover, Coat, Shirt), 3 seeds, to specifically target
  the hardest confusion group.
- **Margin-based routing/fusion**: a validation sample is only re-scored by the
  specialist if the base ensemble's prediction falls in the shirt cluster **and**
  its top1–top2 softmax margin is below a tuned threshold (grid-searched:
  route_margin=0.08, blend weight=0.90) — deliberately conservative so the
  specialist doesn't disturb already-confident correct predictions (forcing all
  shirt-cluster predictions through the specialist added noise and was rejected).
- **Test-time augmentation**: 5 forward passes per model (1 clean + 4 augmented),
  probabilities averaged.

## Tech stack

TensorFlow/Keras 2.19, NumPy, pandas, scikit-learn, matplotlib/seaborn. Single
self-contained Kaggle notebook (no separate `src/` modules), run on dual Tesla T4
GPUs.

## What didn't work (documented negative results)

CBAM spatial attention (worse than SE-only), random rotation augmentation (slight
degradation), 8-pass TTA (no improvement over 5), EfficientNet transfer learning
(didn't beat the from-scratch ResNet), MixUp (no improvement), class-weight
boosting for the Shirt class (added noise), and a wider WideResNet variant (worse).
These negative results directly informed the final architecture: SE blocks over
attention variants, from-scratch training over transfer learning, and margin-gated
specialist routing over blanket re-scoring.
