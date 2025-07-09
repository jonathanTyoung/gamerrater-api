from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Rating

class RatingsView(ViewSet):
    """Rating view set"""

    def create(self, request):
        """Handle POST to create or update a game rating"""
        game_id = request.data.get("game")
        score = request.data.get("rating")

        if not game_id or not score:
            return Response({"detail": "Game and rating are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for existing rating by this user
        existing_rating = Rating.objects.filter(game_id=game_id, user=request.user).first()
        if existing_rating:
            existing_rating.rating = score
            existing_rating.save()
            serializer = RatingSerializer(existing_rating)
            return Response(serializer.data, status=status.HTTP_200_OK)

        try:
            rating = Rating.objects.create(
                game_id=game_id,
                user=request.user,
                rating=score,
            )
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET for single rating"""
        try:
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        except Rating.DoesNotExist:
            return Response({"reason": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT to update a rating"""
        try:
            rating = Rating.objects.get(pk=pk)
            if rating.user != request.user:
                return Response({"detail": "Not your rating to update."}, status=status.HTTP_403_FORBIDDEN)

            rating.game_id = request.data.get("game", rating.game_id)
            rating.rating = request.data.get("rating", rating.rating)
            rating.save()

            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Rating.DoesNotExist:
            return Response({"detail": "Rating not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single rating"""
        try:
            rating = Rating.objects.get(pk=pk)
            if rating.user != request.user:
                return Response({"detail": "Not your rating to delete."}, status=status.HTTP_403_FORBIDDEN)
            rating.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Rating.DoesNotExist:
            return Response({'message': "Rating not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests for all ratings"""
        try:
            ratings = Rating.objects.all()
            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'game', 'user', 'rating')
        depth = 1
