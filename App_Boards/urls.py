from django.urls import path
from .Boards_views import BoardListView, BoardDetailView, IdeasListView, IdeasDetailView

app_name = "App_Boards"

urlpatterns = [
    path('', BoardListView.as_view() ,name='board-list'),
    path('<int:board_id>', BoardDetailView.as_view(), name='board-detail'),

    path('<int:board_id>/ideas', IdeasListView.as_view(), name='ideas-list'),
    path('ideas/<int:idea_id>', IdeasDetailView.as_view(), name='ideas-detail'),
]