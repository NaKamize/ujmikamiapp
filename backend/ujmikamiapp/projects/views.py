from rest_framework import generics
from .models import Project, WorkExperience, Publication
from .serializers import ProjectSerializer, WorkExperienceSerializer, ResearchPublicationSerializer


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


class WorkExperienceListView(generics.ListAPIView):
    """GET /api/experiences/ — returns all work experiences ordered by 'order' field."""
    serializer_class = WorkExperienceSerializer
    queryset = WorkExperience.objects.prefetch_related('technologies').all()


class ResearchPublicationsView(generics.ListAPIView):
    """GET /api/publications/ - returns all research and publications."""
    serializer_class = ResearchPublicationSerializer
    queryset = Publication.objects.all()
