from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm, ReviewForm
from .models import Comment, Review
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    reviews = Review.objects.order_by("-pk")
    page = request.GET.get("page", "1")
    paginator = Paginator(reviews, 5)
    page_obj = paginator.get_page(page)
    context = {"reviews": reviews, "question_list": page_obj}
    return render(request, "free/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("free:detail", review.pk)
    else:
        review_form = ReviewForm()
    context = {"review_form": review_form}

    return render(request, "free/create.html", context)


def detail(request, free_pk):
    review = Review.objects.get(pk=free_pk)
    comment_form = CommentForm()
    context = {
        "review": review,
        "comment_form": comment_form,
        "comments": review.comment_set.all(),
    }

    return render(request, "free/detail.html", context)


def update(request, free_pk):
    review = Review.objects.get(pk=free_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect("free:detail", review.pk)
    else:
        review_form = ReviewForm(instance=review)
    context = {"free_form": review_form}

    return render(request, "free/update.html", context)


def delete(request, free_pk):
    review = Review.objects.get(pk=free_pk)
    review.delete()
    return redirect("free:index")


@login_required
def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.free = review
        comment.user = request.user
        comment.save()
    return redirect("free:detail", review.pk)


@login_required
def comment_delete(request, comment_pk, review_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("free:detail", review_pk)


@login_required
def comment_update(request, free_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    data = {"comment_content": comment.content}

    return JsonResponse(data)


@login_required
def comment_update_complete(request, free_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment_form = CommentForm(request.POST, instance=comment)

    if comment_form.is_valid():
        comment = comment_form.save()

        data = {
            "comment_content": comment.content,
        }

        return JsonResponse(data)

    data = {
        "comment_content": comment.content,
    }

    return JsonResponse(data)


@login_required
def like(request, free_pk):
    review = get_object_or_404(Review, pk=free_pk)
    # 만약에 로그인한 유저가 이 글을 좋아요를 눌렀다면,
    # if review.like_users.filter(id=request.user.id).exists():
    if request.user in review.like_users.all():
        # 좋아요 삭제하고
        review.like_users.remove(request.user)

    else:
        # 좋아요 추가하고
        review.like_users.add(request.user)

    # 상세 페이지로 redirect

    data = {
        "like_cnt": review.like_users.count(),
    }

    return JsonResponse(data)


def search(request):
    all_data = Review.objects.order_by("-pk")
    search = request.GET.get("search", "")
    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(all_data, 5)
    page_obj = paginator.get_page(page)
    if search:
        search_list = all_data.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            # | Q(user__icontains=search) #FK라서 검색불가
        )
        paginator = Paginator(search_list, 5)  # 페이지당 3개씩 보여주기
        page_obj = paginator.get_page(page)
        context = {
            "search_list": search_list,
            "question_list": page_obj,
        }
    else:
        context = {
            "search_list": all_data,
            "question_list": page_obj,
        }

    return render(request, "free/search.html", context)
