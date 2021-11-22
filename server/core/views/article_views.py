from django.shortcuts import render
from django.db.models import F

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.models import Article, Category, Comment
from core.serializers import ArticleSerializer, CategorySerializer

from rest_framework import status


@api_view(['GET'])
def getArticles(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    articles = Article.objects.filter(
        title_icontains=query).order_by('createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(articles, 8)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ArticleSerializer(articles, many=True)
    return Response({'articles': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getArticleById(request, pk):
    article = Article.objects.filter(_id=pk).update(views=F('views')+1)
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getTopArticle(request, pk):
    articles = Article.objects.all().order_by('-views')[0:5]
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getNewsArticle(request, pk):
    articles = Article.objects.all().order_by('-createdAt')[0:5]
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getHotArticle(request, pk):
    articles = Article.objects.all().order_by('-numComments')[0:5]
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)
