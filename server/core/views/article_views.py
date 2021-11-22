from django.shortcuts import render
from django.db.models import F

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.models import Article, Comment
from core.serializers import ArticleSerializer

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


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createArticle(request):
    user = request.user
    data = request.data

    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    image = data.get('image')
    body = data.get('body')

    article = Article.objects.create(
        user=user,
        title=title,
        description=description,
        category=category,
        image=image,
        body=body,
    )

    article.save()
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteArticle(request, pk):
    article = Article.objects.get(id=pk)
    article.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def uploadImage(request):
    data = request.data

    article_id = data['article_id']
    article = Article.objects.get(_id=article_id)

    article.image = request.FILES.get('image')
    article.save()

    return Response('Image was uploaded')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def updateArticle(request, pk):
    data = request.data
    article = Article.objects.get(_id=pk)

    article.title = data.get('title')
    article.description = data.get('description')
    article.category = data.get('category')
    article.body = data.get('body')

    article.save()
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createComment(request, pk):
    user = request.user
    article = Article.objects.get(_id=pk)
    data = request.data

    comment = Comment.objects.create(
        user=user,
        article=article,
        name=user.first_name,
        body=data['body']
    )

    comments = article.comment_set.all()
    article.numComments = len(comments)

    article.save()
    return Response('Comment Added')
