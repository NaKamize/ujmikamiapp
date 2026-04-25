from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer


class ProjectListView(generics.ListAPIView):
    """GET /api/projects/ — returns all projects ordered by 'order' field."""
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.prefetch_related('tags', 'links').all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class ProjectDetailView(generics.RetrieveAPIView):
    """GET /api/projects/<id>/ — returns a single project."""
    serializer_class = ProjectSerializer
    queryset = Project.objects.prefetch_related('tags', 'links').all()
