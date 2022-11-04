from django.urls import path
from . import views


app_name = "articles"

urlpatterns = [
    # articles 게시글
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:review_pk>/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    # 검색
    path("search/", views.search, name="search"),
    # articles 댓글

    path(
        "<int:review_pk>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path("<int:review_pk>/like/", views.like, name="like"),

    path("<int:pk>/comments/", views.comment_create, name="comment_create"),
    path("<int:review_pk>/comments/<int:comment_pk>/comment_detail", views.comment_detail, name="comment_detail"),

]
