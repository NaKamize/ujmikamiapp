"""
Management command to seed the database with ML model showcase entries.

Usage:
    python manage.py seed_ml_models
    python manage.py seed_ml_models --clear-only
"""

from django.core.management.base import BaseCommand

from ml_models.models import MLModel, MLModelLink

MODELS_DATA = [
    {
        'title': 'Chatbot Arena: DeBERTa-GBDT Hybrid Pipeline',
        'description': (
            'Advanced LLM preference prediction pipeline combining a fine-tuned '
            'DeBERTa-v3-large backbone with a GBDT-based meta-stacking architecture. '
            'Leverages test-time augmentation (TTA) and engineered structural '
            'features to improve classification robustness.'
        ),
        'category': 'nlp',
        'architecture': 'DeBERTa-v3-large + LightGBM/XGBoost/CatBoost Ensemble',
        'framework': 'PyTorch + HuggingFace Transformers + Scikit-Learn',
        'competition_name': 'LLM Classification Finetuning',
        'competition_url': 'https://www.kaggle.com/competitions/llm-classification-finetuning',
        'dataset_description': (
            'Chatbot Arena conversation turns; multi-class classification for '
            'model preference (model_a, model_b, tie).'
        ),
        'metrics': {
            'log_loss': 1.04331,
        },
        'rank': '108 / 253',
        'score': '1.04331',
        'order': 1,
        'links': [
            {'label': 'Competition Page', 'url': 'https://www.kaggle.com/competitions/llm-classification-finetuning'},
            {'label': 'DeBERTa Pipeline Notebook', 'url': 'https://github.com/NaKamize/chatbot_arena/blob/main/chatbot-arena.ipynb'},
            {'label': 'GitHub Repo', 'url': 'https://github.com/NaKamize/chatbot_arena'},
        ],
    },
    {
        'title': 'Disaster Tweets, NLP Classification',
        'description': (
            'Predict which tweets are about real disasters and which are not. '
            'Uses a DeBERTa-v3 transformer combined with an XGBoost classifier '
            'trained on hand-crafted linguistic features.'
        ),
        'category': 'nlp',
        'architecture': 'Microsoft DeBERTa-v3-base + XGBoost ensemble',
        'framework': 'PyTorch + HuggingFace Transformers + XGBoost',
        'competition_name': 'NLP with Disaster Tweets',
        'competition_url': 'https://www.kaggle.com/competitions/nlp-getting-started',
        'dataset_description': (
            'Twitter-style text samples labelled as disaster (1) or not (0). '
            'Features include raw tweet text and extracted metadata like hashtags, '
            'mentions, URLs, punctuation ratios, and sentiment polarity.'
        ),
        'metrics': {
            'best_threshold': 0.44,
            'ensemble_threshold': 0.44,
            'f1_score': 0.8613,
            'accuracy': 0.8791,
        },
        'rank': '355 / 727',
        'score': '0.8613',
        'order': 2,
        'links': [
            {'label': 'Competition Page', 'url': 'https://www.kaggle.com/competitions/nlp-getting-started'},
            {'label': 'DeBERTa+XGBoost Notebook', 'url': 'https://github.com/NaKamize/disaster-tweets/blob/main/disaster_tweets_deberta_xgboost.ipynb'},
            {'label': 'DistilBERT Notebook', 'url': 'https://github.com/NaKamize/disaster-tweets/blob/main/disaster_tweets_distilbert_trained.ipynb'},
            {'label': 'GitHub Repo', 'url': 'https://github.com/NaKamize/disaster-tweets'},
        ],
    },
    {
        "title": "Fashion-MNIST, Computer Vision Classification",
        "description": "AI-Biz2026 Spring Task 3 competition. Achieved a top-tier rank by classifying Fashion-MNIST images using a multi-seed ensemble of ResNet-style CNNs with Squeeze-and-Excitation (SE) channel attention blocks. The architecture is optimized for 28×28 native resolution, utilizing Test-Time Augmentation (TTA) and specialized training to improve texture-based discrimination.",
        "architecture": "ResNet-style CNN with SE blocks; 5-seed ensemble for variance reduction.",
        "framework": "TensorFlow / Keras",
        "competition_name": "AI-Biz2026 Fashion-MNIST Classification",
        "dataset_description": "Fashion-MNIST: 70,000 grayscale images (28×28) across 10 clothing categories.",
        "metrics": {
            "accuracy": 0.95560
        },
        "rank": "3 / 38",
        "order": 3,
        "links": [
            {'label': 'GitHub Repo', 'url': 'https://github.com/NaKamize/ai-biz2026-classifier'},
            {'label': 'Competition Page', 'url': 'https://www.kaggle.com/competitions/ai-biz-2026-spring-task-3/overview'}
        ]
    },
    {
        'title': '3-LC Multi-Vehicle Detection Challenge',
        'description': (
            'A computer vision challenge focused on multi-vehicle detection. '
            'The primary difficulty involved extensive data preprocessing and '
            'cleaning, though limited time prevented deep refinement of the '
            'dataset, which was the core focus of this competition.'
        ),
        'category': 'cv',
        'architecture': 'YOLO-based detection pipeline',
        'framework': 'PyTorch + Ultralytics',
        'competition_name': '3-LC Multi-Vehicle Detection Challenge',
        'competition_url': 'https://www.kaggle.com/competitions/3-lc-multi-vehicle-detection-challenge',
        'metrics': {
            'score': 0.81188,
        },
        'rank': '43 / 97',
        'order': 4,
        'links': [
            {'label': 'Competition Page', 'url': 'https://www.kaggle.com/competitions/3-lc-multi-vehicle-detection-challenge'},
            {'label': 'GitHub Repository', 'url': 'https://github.com/NaKamize/3lc-multi-vehicle-detecion'},
        ],
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with ML model showcase entries.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-only',
            action='store_true',
            help='Only clear existing entries, do not seed.',
        )

    def handle(self, *args, **options):
        if options['clear_only']:
            count = MLModel.objects.count()
            MLModel.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Cleared {count} ML model(s).'))
            return

        # Clear existing
        MLModel.objects.all().delete()
        self.stdout.write('Cleared existing ML models.')

        allowed_fields = {field.name for field in MLModel._meta.fields}

        for data in MODELS_DATA:
            links = data.pop('links', [])
            unknown_fields = [key for key in data.keys() if key not in allowed_fields]
            if unknown_fields:
                self.stdout.write(
                    self.style.WARNING(
                        f"Ignoring unknown fields for '{data.get('title', 'unknown')}': {', '.join(unknown_fields)}"
                    )
                )

            clean_data = {key: value for key, value in data.items() if key in allowed_fields}
            model = MLModel.objects.create(**clean_data)
            for link_data in links:
                MLModelLink.objects.create(model=model, **link_data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ {model.title}'))

        total = MLModel.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nSeeded {total} ML model(s).'))
