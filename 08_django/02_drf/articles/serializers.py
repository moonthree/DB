# rest_framework = drf 이름
from rest_framework import serializers
from .models import Article

# 이름에 리스트가 들어가는 이유는
# 이 클래스는 게시글의 목록(쿼리셋)의 json을 줄 것이므로
class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title', 'content',)


# 단일 게시글 정보를 담은 json을 줄 것
class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'
