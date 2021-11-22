from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from core.models import Category
from core.serializers import CategorySerializer

from rest_framework import status

@api_view(['GET'])
def getCategories(request):
    categories = Category.objects.all()

    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCategory(request, pk):
    category = Category.objects.get(_id=pk)
    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createCategory(request):
    user = request.user

    category = Category.objects.create(
        user=user,
        name="Sample name",
        image="Sample image"
    )

    category.save()
    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def uploadImage(request):
    data = request.data

    category_id = data['category_id']
    category = Category.objects.get(_id=category_id)

    category.image = request.FILES.get('image')
    category.save()

    return Response('Image was uploaded')

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteCategory(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateCategory(request, pk):
    data = request.data
    category = Category.objects.get(_id=pk)

    category.name = data.get('name')

    category.save()
    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)