from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Category


class CategoriesView(ViewSet):
    """ViewSet for handling Category operations"""

    def list(self, request):
        """GET all categories"""
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """GET a single category"""
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """POST a new category"""
        try:
            category = Category(label=request.data["label"])
            category.save()
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'reason': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """PUT an existing category"""
        try:
            category = Category.objects.get(pk=pk)
            category.label = request.data["label"]
            category.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """DELETE a category"""
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for Category"""
    
    class Meta:
        model = Category
        fields = ['id', 'label']