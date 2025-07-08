from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Rating

class RatingsView(ViewSet):
    """Rating view set"""

    def create(self, request):
        """Handle POST operations"""
        rating = Rating()
        rating.game_id = request.data["game"]
        rating.user_id = request.data["user"]
        rating.value = request.data["value"]

        try:
            rating.save()
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item"""
        try:
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests"""
        try:
            rating = Rating.objects.get(pk=pk)
            rating.game_id = request.data["game"]
            rating.user_id = request.data["user"]
            rating.value = request.data["value"]
            rating.save()
        except Rating.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item"""
        try:
            rating = Rating.objects.get(pk=pk)
            rating.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Rating.DoesNotExist as ex:
            return Response({'message': str(ex)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests for all items"""
        try:
            ratings = Rating.objects.all()
            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Rating
        fields = (
            'id',
            'game',
            'user',
            'value',
        )