from django.urls import path

from .views import MLModelDetailView, MLModelListView

urlpatterns = [
    path('', MLModelListView.as_view(), name='ml-model-list'),
    path('<int:pk>/', MLModelDetailView.as_view(), name='ml-model-detail'),
]
