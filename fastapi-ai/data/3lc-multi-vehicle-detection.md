# 3LC Multi-Vehicle Detection

## Overview

A Kaggle competition solution for multi-class vehicle detection on the UA-DETRAC
traffic-surveillance dataset. The task is to detect and classify vehicles into four
classes — truck, car, van, bus — in traffic-camera footage, using a 10,000-image
subset (`ua_detrac_10k`) split into 7,852 train, 982 validation, and 982 test images
with YOLO-format labels. The competition rules lock the model architecture to
YOLOv8n trained **from scratch** (no pretrained/COCO weights allowed), and this
constraint is hard-enforced in code via `_assert_yolov8n_only()` and
`_reject_pretrained_config()`, which raise `SystemExit` if violated.

## Approach

- **Model**: YOLOv8n (Ultralytics), instantiated from `yolov8n.yaml` (architecture
  only, no pretrained weights) — 3,006,428 parameters, 73 fused layers, 8.1 GFLOPs.
- **Experiment tracking**: 3LC (`tlc` / `tlc_ultralytics` packages) — a dataset
  versioning and experiment platform. `register_tables.py` converts YOLO-format
  splits into versioned 3LC "Tables," which supported dashboard-driven label
  corrections (the val table had 413 bounding-box edits, the train table 3,826
  value edits, tracked via `tables_used.txt`).
- **Pipeline**: `verify_setup.py` (environment checks) → `register_tables.py` →
  `train.py` (trains via `tlc_ultralytics`, computes 3D UMAP image embeddings for
  the dashboard) → `predict.py` (batch inference to `submission.csv`) →
  `sweep_val_thresholds.py` (grid search over confidence 0.05–0.25 × IoU 0.55–0.70
  to find the best mAP50 operating point).
- **Training config**: 100 epochs, batch 32, image size 640, AdamW optimizer,
  lr0 0.01, warmup 5 epochs, label smoothing 0.1, weight decay 0.0005, seed 42,
  mosaic/mixup/copy-paste augmentation.
- **Engineering workaround**: a custom compatibility shim
  (`_apply_ultralytics_83_compat`) monkey-patches the 3LC validator because newer
  Ultralytics versions return detections as a dict instead of the Nx6 tensor the
  3LC validator expects — a concrete integration bug diagnosed and patched around.
- Two selectable inference pipelines: `memory` (chunked, GPU-resident, default —
  avoids disk I/O spikes on ~8GB GPUs) or `txt` (standard Ultralytics export style).

## Results

Seven training runs (`yolov8n_baseline` through `baseline7`) were logged. The best
run (`baseline7`, 100 epochs, 1.21 hours on an RTX 5070 Ti Laptop GPU, 12GB) achieved
on the 982-image validation set (12,018 instances):

- **Overall: Precision 0.966, Recall 0.802, mAP50 0.877, mAP50-95 0.767**
- car: mAP50 0.920 · bus: mAP50 0.901 · van: mAP50 0.848 · truck: mAP50 0.840
- Training-set mAP50 0.989 / mAP50-95 0.933 — the train/val gap suggests some
  overfitting typical of small-dataset from-scratch training.
- Inference speed: ~2.0ms per image on GPU. Final chosen inference config: conf 0.1,
  IoU 0.55.

## Tech stack

Python 3.13, PyTorch 2.12 (CUDA 13.0), Ultralytics 8.4.6, `3lc-ultralytics` /
`tlc` (dataset versioning + embeddings), `umap-learn`, scikit-learn, PyYAML.

## Notable decisions

- Fully config-driven: no hardcoded paths/hyperparameters, everything routes
  through `config.yaml`.
- Fail-fast dependency checks (e.g. `_check_umap()`) before long training runs,
  to avoid crashing only after training completes.
- Idempotent table registration to avoid duplicating 3LC datasets across reruns.
- Threshold tuning treated as a separate optimization step from training via a
  dedicated post-hoc grid search script.
- Reproducibility enforced via a fixed seed (42) applied across Python, NumPy,
  Torch, and CUDA.
