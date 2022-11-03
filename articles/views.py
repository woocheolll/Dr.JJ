from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, CommentForm
from .models import Review, Comment
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



# from django.db.models import Q

# Create your views here.


def index(request):
    reviews = Review.objects.order_by("-pk")
    context = {"reviews": reviews}
    return render(request, "articles/index.html", context)


def search(request):
    search = request.GET.get("search")
    if search:
        reviews = Review.objects.filter(title__contains=search) | Review.objects.filter(
            content__contains=search
        )
        context = {
            "search": search,
            "reviews": reviews,
        }
        return render(request, "articles/search.html", context)
    else:
        return redirect("articles:index")


def create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        print(request.POST)
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


def detail(request, review_pk):
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
    }
    return render(
        request,
        "articles/detail.html",
        context,
    )


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

    return render(request, "articles/update.html", context)


def delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect("articles:index")


@login_required
def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = review
        comment.user = request.user
        comment.save()
    return redirect("articles:detail", review.pk)


@login_required
def comment_delete(request, comment_pk, review_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("articles:detail", review_pk)


@login_required
def comment_update(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    data = {"comment_content": comment.content}

    return JsonResponse(data)


@login_required
def comment_update_complete(request, review_pk, comment_pk):
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
def like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
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
