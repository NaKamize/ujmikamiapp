from django.test import TestCase
from rest_framework.test import APIClient
from .models import MLModel, MLModelLink


class MLModelAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.model = MLModel.objects.create(
            title='Test Model',
            description='A test model',
            category='nlp',
            architecture='DistilBERT',
            framework='PyTorch',
            competition_name='Test Competition',
            metrics={'accuracy': 0.95},
            rank='1 / 10',
            score='0.95',
        )
        MLModelLink.objects.create(
            model=self.model,
            label='Notebook',
            url='https://example.com',
        )

    def test_list_ml_models(self):
        response = self.client.get('/api/ml-models/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_detail_ml_model(self):
        response = self.client.get(f'/api/ml-models/{self.model.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Test Model')
        self.assertEqual(response.json()['metrics']['accuracy'], 0.95)
        self.assertEqual(len(response.json()['links']), 1)
