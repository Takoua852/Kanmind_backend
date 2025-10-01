from django.urls import path
from .views import BoardListView, BoardDetailView, EmailCheckView
"""
API endpoints for boards and user email checks.

Endpoints:

1. /boards/           - GET: list boards, POST: create board
2. /boards/<pk>/      - GET: retrieve board, PUT/PATCH: update, DELETE: delete board
3. /email-check/      - GET: check if user exists by email
"""
urlpatterns = [
    path('boards/', BoardListView.as_view(), name='board-list'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('email-check/', EmailCheckView.as_view(), name='email-check')
]
