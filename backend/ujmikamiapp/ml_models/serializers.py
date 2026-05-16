from rest_framework import serializers
from .models import MLModel, MLModelLink


class MLModelLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModelLink
        fields = ['id', 'label', 'url']


class MLModelSerializer(serializers.ModelSerializer):
    links = MLModelLinkSerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = MLModel
        fields = [
            'id', 'title', 'description', 'category', 'category_display',
            'architecture', 'framework',
            'competition_name', 'competition_url', 'dataset_description',
            'metrics', 'rank', 'score',
            'image', 'links', 'order', 'created_at',
        ]
