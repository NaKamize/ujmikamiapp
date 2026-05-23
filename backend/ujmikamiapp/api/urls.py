from django.urls import path, include
from projects.views import WorkExperienceListView

urlpatterns = [
    path('projects/', include('projects.urls')),
    path('ml-models/', include('ml_models.urls')),
    path('experiences/', WorkExperienceListView.as_view(), name='experience-list'),
]
