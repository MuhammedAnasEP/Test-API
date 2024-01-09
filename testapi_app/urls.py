from django.urls import path
from .views import TestExecutionView

urlpatterns = [
    path('tests/v1/execute/', TestExecutionView.as_view(), name='execute_test'),
]