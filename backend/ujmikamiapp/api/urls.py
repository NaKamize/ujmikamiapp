from django.urls import path, include

urlpatterns = [
    path('projects/', include('projects.urls')),
    path('ml-models/', include('ml_models.urls')),
]
