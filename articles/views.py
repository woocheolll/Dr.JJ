from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, CommentForm
from .models import Review, Comment
from free.models import Freereview, Freecomment
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from django.db.models import Q
from django.core.paginator import Paginator


# from django.db.models import Q

# Create your views here.


def prof(request):
    pass
    return render(request, "articles/prof.html")


def thx(request):
    pass
    return render(request, "articles/thx.html")


def index(request):
    reviews = Review.objects.order_by("-pk")
    all_article = Review.objects.all()
    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(reviews, 6)
    page_obj = paginator.get_page(page)
    context = {
        "reviews": reviews,
        "all_article": all_article,
        "question_list": page_obj,
    }
    return render(request, "articles/index.html", context)


# @login_required
# def search(request):
#     search = request.GET.get("search")
#     if search:
#         reviews = Review.objects.filter(title__contains=search) | Review.objects.filter(
#             menu__contains=search
#         )
#         frees = Freereview.objects.filter(
#             title__contains=search
#         ) | Freereview.objects.filter(content__contains=search)
#         context = {"search": search, "reviews": reviews, "frees": frees}
#         return render(request, "articles/search.html", context)
#     else:
#         return redirect("articles:index")


@login_required
def search(request):
    all_data = Review.objects.order_by("-pk")
    search = request.GET.get("search", "")
    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(all_data, 6)
    page_obj = paginator.get_page(page)
    if search:
        search_list = all_data.filter(
            Q(title__icontains=search)
            | Q(menu__icontains=search)
            | Q(addr__icontains=search)
            # | Q(user__icontains=search) #FK라서 검색불가
        )
        paginator = Paginator(search_list, 6)  # 페이지당 3개씩 보여주기
        page_obj = paginator.get_page(page)
        context = {
            "search": search,
            "search_list": search_list,
            "question_list": page_obj,
        }
    else:
        context = {
            "search": search,
            "search_list": all_data,
            "question_list": page_obj,
        }

    return render(request, "articles/search.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        print(request.POST)
        print(form.is_valid)
        if form.is_valid():

            temp = form.save(commit=False)
            temp.user = request.user
            temp.save()
            return redirect("articles:index")
    else:
        form = ReviewForm()
    context = {
        "form": form,
    }

    return render(request, "articles/create.html", context)


@login_required
def detail(request, review_pk):
    grades = Comment.objects.aggregate(Avg("grade"))
    print(grades)
    review = Review.objects.get(pk=review_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = review
            comment.user = request.user
            comment.save()
        return redirect("articles:detail", review.pk)
    else:
        comment_form = CommentForm()
    context = {
        "comment_form": comment_form,
        "review": review,
        "comments": review.comment_set.all(),
        "grades": grades,
    }
    return render(
        request,
        "articles/detail.html",
        context,
    )


@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect("articles:detail", review.pk)
    else:
        review_form = ReviewForm(instance=review)
    context = {"review_form": review_form}

    return render(request, "articles/create.html", context)


@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect("articles:index")


@login_required
def comment_delete(request, comment_pk, review_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("articles:detail", review_pk)


@login_required
def like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    # 만약에 로그인한 유저가 이 글을 좋아요를 눌렀다면,
    # if review.like_users.filter(id=request.user.id).exists():
    if request.user in review.like_art_users.all():
        # 좋아요 삭제하고
        review.like_art_users.remove(request.user)

    else:
        # 좋아요 추가하고
        review.like_art_users.add(request.user)

    # 상세 페이지로 redirect

    data = {
        "like_cnt": review.like_art_users.count(),
    }

    return JsonResponse(data)


@login_required
def comment_create(request, pk):

    if request.method == "POST":
        review = Review.objects.get(pk=pk)
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.review = review
            for _ in range(6):
                if comment.grade == 0:
                    comment.credit = "F"
                    break
                elif comment.grade > 0 and comment.grade < 1.5:
                    comment.credit = "E+"
                    break
                elif comment.grade >= 1.5 and comment.grade < 2.5:
                    comment.credit = "D+"
                    break
                elif comment.grade >= 2.5 and comment.grade < 3.5:
                    comment.credit = "C+"
                    break
                elif comment.grade >= 3.5 and comment.grade < 4.5:
                    comment.credit = "B+"
                    break
                elif comment.grade >= 4.5:
                    comment.credit = "A+"
                    break

            comment.save()
        return redirect("articles:detail", pk)
    else:
        comment_form = CommentForm()
    context = {"comment_form": comment_form}

    return render(request, "articles/comment_create.html", context)


def comment_detail(request, comment_pk, review_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment_form = CommentForm()

    context = {
        "comment": comment,
        "comment_form": comment_form,
    }
    return render(request, "articles/comment_detail.html", context)


@login_required
def comment_update(request, review_pk, comment_pk):
    review = Review.objects.get(pk=review_pk)
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment.user = request.user
            comment.review = review
            comment.save()
            return redirect("articles:detail", review_pk)
    else:
        comment_form = CommentForm(instance=comment)
    context = {"comment_form": comment_form, "review": review, "comment": comment}
    return render(request, "articles/comment_create.html", context)


# # 우리가 만드는 맛집정보
# def admin_create(request):
#     if request.method == "POST":
#         form = ArticleForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("main:index")
#     else:
#         form = ArticleForm()
#     context = {
#         "form": form,
#     }
#     return render(request, "articles/admin_create.html", context)
