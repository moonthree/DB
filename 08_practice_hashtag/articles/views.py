from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Article, Comment, Hashtag
from .forms import ArticleForm, CommentForm
from django import template

# Create your views here.
@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            #hashtag
            for word in article.content.split():
                # word : ex) 오늘 # 장고 # 많이 #힘들다
                if word.startswith('#'):
                    # 해쉬태그 테이블에 우선 새로운 데이터를 생성하고
                    # get_or_create -> 이미 db에 있다면 가져오고 아니면 만든다.
                    hashtag, created = Hashtag.objects.get_or_create(content=word)
                    # 방금 생성된 해쉬태그와 현재 게시글을 관계 지어준다.
                    # (article 과 hashtag의 중개 테이블에 관계르 생성하는 부분)
                    article.hashtags.add(hashtag)

            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@require_safe
def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm()
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


@require_POST
def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.is_authenticated:
        if request.user == article.user: 
            article.delete()
            return redirect('articles:index')
    return redirect('articles:detail', article.pk)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                #hashtag
                # update 에서는 hashtag 관꼐를 초기화 해줘야함
                # 기존의 해쉬태그도 수정
                article.hashtags.clear()
                for word in article.content.split():
                # word : ex) 오늘 # 장고 # 많이 #힘들다
                    if word.startswith('#'):
                        # 해쉬태그 테이블에 우선 새로운 데이터를 생성하고
                        hashtag, created = Hashtag.objects.get_or_create(content=word)
                        # 방금 생성된 해쉬태그와 현재 게시글을 관계 지어준다.
                        # (article 과 hashtag의 중개 테이블에 관계르 생성하는 부분)
                        article.hashtags.add(hashtag)
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
        return redirect('articles:detail', article.pk)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('articles:detail', article_pk)

    
@require_POST
def likes(request, article_pk):
    if request.user.is_authenticated:
        article = Article.objects.get(pk=article_pk)

        # 좋아요 추가할지 취소할지 무슨 기준으로 if문을 작성할까?
        # 현재 게시글에 좋아요를 누른 유저 목록에 현재 좋아요를 요청하는 유저가 있는지 없는지를 확인
        # if request.user in article.like_users.all():
        
        # 현재 게시글에 좋아요를 누른 유저중에 현재 좋아요를 요청하는 유저를 검색해서 존재하는지를 확인 
        if article.like_users.filter(pk=request.user.pk).exists():
            # 좋아요 취소 (remove)
            article.like_users.remove(request.user)
        else:
            # 좋아요 추가 (add)
            article.like_users.add(request.user)
        return redirect('articles:index')
    return redirect('accounts:login')

register = template.Library()

def hashtag(request, hash_pk):
    tag = get_object_or_404(Hashtag, pk=hash_pk)
    #articles = tag.articles_set.all()
    context = {
        'tag':tag,
    #   'articles': articles,
    }
    return render(request, 'articles/hashtag.html', context)
