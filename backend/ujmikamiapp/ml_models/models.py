from django.db import models


class MLModel(models.Model):
    CATEGORY_CHOICES = [
        ('nlp', 'NLP & Text'),
        ('cv', 'Computer Vision'),
        ('tabular', 'Tabular / Classic ML'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')

    # Model technical details
    architecture = models.CharField(max_length=200, blank=True, help_text='e.g. DistilBERT, DeBERTa-v3, ResNet')
    framework = models.CharField(max_length=100, blank=True, help_text='e.g. PyTorch, TensorFlow, scikit-learn')

    # Competition info
    competition_name = models.CharField(max_length=200, blank=True)
    competition_url = models.URLField(blank=True)
    dataset_description = models.TextField(blank=True)

    # Performance — stored as JSON: {"accuracy": 0.94, "f1": 0.91, ...}
    metrics = models.JSONField(default=dict, blank=True)

    # Leaderboard results
    rank = models.CharField(max_length=50, blank=True, help_text='Leaderboard rank, e.g. "112 / 257"')
    score = models.CharField(max_length=50, blank=True, help_text='Leaderboard score')

    # Visual / file
    image = models.ImageField(upload_to='ml_models/', blank=True, null=True)

    # Ordering & metadata
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower = first)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'ML Model'
        verbose_name_plural = 'ML Models'

    def __str__(self):
        return self.title


class MLModelLink(models.Model):
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='links')
    label = models.CharField(max_length=100)
    url = models.URLField()

    class Meta:
        verbose_name = 'ML Model Link'
        verbose_name_plural = 'ML Model Links'

    def __str__(self):
        return f'{self.model.title} — {self.label}'
