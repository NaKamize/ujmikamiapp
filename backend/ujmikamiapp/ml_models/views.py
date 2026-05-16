from rest_framework import generics
from .models import MLModel
from .serializers import MLModelSerializer


class MLModelListView(generics.ListAPIView):
    """GET /api/ml-models/ — returns all ML models ordered by 'order' field."""
    serializer_class = MLModelSerializer
    queryset = MLModel.objects.prefetch_related('links').all()


class MLModelDetailView(generics.RetrieveAPIView):
    """GET /api/ml-models/<id>/ — returns a single ML model."""
    serializer_class = MLModelSerializer
    queryset = MLModel.objects.prefetch_related('links').all()
