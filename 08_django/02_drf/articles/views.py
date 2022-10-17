
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Article
from .serializers import ArticleListSerializer, ArticleSerializer
# model에서 Article import
# serializers에서 ArticleListSerializer import

# DRF에선 데코레이터가 필수적임
@api_view(['GET', 'POST'])
def article_list(request):
    # GET
    if request.method == 'GET':
        articles = Article.objects.all()

        # (articles, many=True)
        # ArticleListSerializer괄호 안에 serializer될 객체 'articles' 넣음
        # 그런데 단일객체가 아니니까 many=True
        serializer = ArticleListSerializer(articles, many=True)

        # RDF의 Response를 통해 리턴함
        return Response(serializer.data)

    # POST
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # save 성공시 201 리턴
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # save 실패시 400 리턴 -> raise_exception=True로 대체
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def article_delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


