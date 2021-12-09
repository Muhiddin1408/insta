from django.urls import path

from .views import (
    ImageViewSet,
    CreateImageViewSet,
    CreateCommentView,
    CommentView,
    UserView,
    UpdateView,
    login,
    RegisterView,
    ImageIdComment,
    UserImageView,
    AddFollower,
    LocationView

)

urlpatterns = [
    path('user/', UserView.as_view()),
    path('userimage/', UserImageView.as_view()),
    # path('image/', ImageViewSet.as_view()),
    path('image/create/', CreateImageViewSet.as_view()),
    path('imageidcomment/', ImageIdComment.as_view()),
    # path('comment/', CommentView.as_view()),
    path('comment/create/', CreateCommentView.as_view()),
    path('user/<int:pk>/', UpdateView.as_view()),
    path('login/', login),
    path('register/', RegisterView.as_view()),
    path('follow/', AddFollower.as_view()),
    path('location/', LocationView.as_view()),

]
