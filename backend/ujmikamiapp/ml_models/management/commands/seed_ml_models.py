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
        'title': 'Chatbot Arena — LLM Preference Classification',
        'description': (
            'Finetune LLMs to predict human preference using Chatbot Arena '
            'conversations. Implemented a fine-tuned DistilBERT baseline and '
            'a TF-IDF + chi-square feature selection baseline for comparison.'
        ),
        'category': 'nlp',
        'architecture': 'DistilBERT (distilbert-base-uncased)',
        'framework': 'PyTorch + HuggingFace Transformers',
        'competition_name': 'LLM Classification Finetuning',
        'competition_url': 'https://www.kaggle.com/competitions/llm-classification-finetuning',
        'dataset_description': (
            'Conversation turns with prompt, response_a, and response_b text. '
            'Multi-class classification: model_a wins, model_b wins, or tie.'
        ),
        'metrics': {
            'log_loss': 1.04331,
        },
        'rank': '124 / 281',
        'score': '1.04331',
        'order': 1,
        'links': [
            {'label': 'Competition Page', 'url': 'https://www.kaggle.com/competitions/llm-classification-finetuning'},
            {'label': 'DistilBERT Notebook', 'url': 'https://github.com/NaKamize/chatbot_arena/blob/main/distilbert_preference_model/distil-bert.ipynb'},
            {'label': 'TF-IDF Baseline Notebook', 'url': 'https://github.com/NaKamize/chatbot_arena/blob/main/td-idf-log-reg-baseline.ipynb'},
            {'label': 'GitHub Repo', 'url': 'https://github.com/NaKamize/chatbot_arena'},
        ],
    },
    {
        'title': 'Disaster Tweets — NLP Classification',
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
            'best_threshold': 0.86,
            'ensemble_threshold': 0.84,
        },
        'rank': '355 / 727',
        'score': '',
        'order': 2,
        'links': [
            {'label': 'Competition Page', 'url': 'https://www.kaggle.com/competitions/nlp-getting-started'},
            {'label': 'DeBERTa+XGBoost Notebook', 'url': 'https://github.com/NaKamize/disaster-tweets/blob/main/disaster_tweets_deberta_xgboost.ipynb'},
            {'label': 'DistilBERT Notebook', 'url': 'https://github.com/NaKamize/disaster-tweets/blob/main/disaster_tweets_distilbert_trained.ipynb'},
            {'label': 'GitHub Repo', 'url': 'https://github.com/NaKamize/disaster-tweets'},
        ],
    },
    {
        'title': 'Fashion-MNIST — Computer Vision Classification',
        'description': (
            'AI-Biz2026 Spring Task 3 competition. Classify Fashion-MNIST images '
            'into 10 clothing categories using a multi-seed ensemble of ResNet-style '
            'CNNs with a specialist model for confused classes.'
        ),
        'category': 'cv',
        'architecture': 'ResNet-style CNN (grayscale) + specialist ensemble',
        'framework': 'TensorFlow / Keras',
        'competition_name': 'AI-Biz2026 Fashion-MNIST Classification',
        'competition_url': 'https://www.kaggle.com/competitions/ai-biz-2026-spring-task-3',
        'dataset_description': (
            'Fashion-MNIST: 70,000 grayscale images (28×28) across 10 classes: '
            'T-shirt/top, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, '
            'Bag, Ankle boot. 60k train / 10k test split in CSV format.'
        ),
        'metrics': {
            'accuracy': 0.94220,
        },
        'rank': '5 / 27',
        'score': '0.94220',
        'order': 3,
        'links': [
            {'label': 'Competition Page', 'url': 'https://www.kaggle.com/competitions/ai-biz-2026-spring-task-3'},
            {'label': 'Colab Notebook (main pipeline)', 'url': 'https://colab.research.google.com/drive/1r6s5XDZGa_L8_YHZZ0MZgjth9-kxHdvX?usp=drive_link'},
            {'label': 'GitHub Repo', 'url': 'https://github.com/NaKamize/AIBiz-2026-spring'},
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

        for data in MODELS_DATA:
            links = data.pop('links', [])
            model = MLModel.objects.create(**data)
            for link_data in links:
                MLModelLink.objects.create(model=model, **link_data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ {model.title}'))

        total = MLModel.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nSeeded {total} ML model(s).'))
