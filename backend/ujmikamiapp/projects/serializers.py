from rest_framework import serializers
from .models import Project, ProjectLink, Tag, WorkExperience, WorkExperienceTechnology, Publication


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProjectLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = ['id', 'label', 'url']


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    links = ProjectLinkSerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'category', 'category_display',
            'tags', 'links', 'image', 'stat', 'order', 'created_at',
        ]


class WorkExperienceTechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperienceTechnology
        fields = ['label']


class WorkExperienceSerializer(serializers.ModelSerializer):
    technologies = WorkExperienceTechnologySerializer(many=True, read_only=True)

    class Meta:
        model = WorkExperience
        fields = [
            'id', 'company', 'role', 'period', 'location',
            'description', 'current', 'order', 'technologies',
        ]


class ResearchPublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = [
            'title', 'authors', 'project', 'badge',
            'subtitle', 'venue', 'description', 'links'
        ]
