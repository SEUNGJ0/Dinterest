from django.urls import path
from .Views.Pins_views import PinsListView, PinsDetailView
from .Views.Comments_views import CommentListView, CommentAllListView, CommentDetailView
from .Views.Likes_views import LikeListView, LikeAllListView, LikeDetailView
app_name = "App_Pins"

urlpatterns = [
    path('', PinsListView.as_view(), name='pins-list'),
    path('<int:pin_id>', PinsDetailView.as_view(), name='pins-detail'),

    path('<int:pin_id>/comments', CommentListView.as_view(), name="pin-comments"),
    path('comments/', CommentAllListView.as_view(), name='conmments-all'),
    path('comments/<int:comment_id>', CommentDetailView.as_view(), name='conmment-detail'),

    path('<int:pin_id>/likes', LikeListView.as_view(), name='pin-likes'),
    path('likes/', LikeAllListView.as_view(), name='likes-all'),
    path('likes/<int:like_id>', LikeDetailView.as_view(), name='like-detail')
]