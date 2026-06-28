from django.urls import path, include
from projects.views import WorkExperienceListView, ResearchPublicationsView

urlpatterns = [
    path('projects/', include('projects.urls')),
    path('ml-models/', include('ml_models.urls')),
    path('publications/', ResearchPublicationsView.as_view(), name='publication-list'),
    path('experiences/', WorkExperienceListView.as_view(), name='experience-list'),
]
