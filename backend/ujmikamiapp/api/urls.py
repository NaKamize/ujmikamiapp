from django.urls import include, path

from projects.views import AboutItemView, ResearchPublicationsView, WorkExperienceListView

urlpatterns = [
    path('projects/', include('projects.urls')),
    path('ml-models/', include('ml_models.urls')),
    path('publications/', ResearchPublicationsView.as_view(), name='publication-list'),
    path('experiences/', WorkExperienceListView.as_view(), name='experience-list'),
    path('about/', AboutItemView.as_view(), name='aboutme-list')
]
