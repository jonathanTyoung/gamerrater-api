from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Game, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class GamesView(ViewSet):
    """Game view set"""

    def list(self, request):
        """Handle GET requests for all games"""
        try:
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST requests to create a new game"""
        game = Game()
        game.title = request.data.get("title")
        game.description = request.data.get("description")
        game.designer = request.data.get("designer")
        game.year_released = request.data.get("year_released")
        game.num_players = request.data.get("num_players")
        game.est_playtime = request.data.get("est_playtime")
        game.age_recommendation = request.data.get("age_recommendation")
        
        game.creator = request.user
        
        try:
            game.save()
            if "categories" in request.data:
                game.categories.set(request.data["categories"])
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game by pk"""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist:
            return Response({"reason": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests to update a game"""
        try:
            game = Game.objects.get(pk=pk)
            if game.creator != request.user:
                return Response({"detail": "You do not have permission to edit this game."}, status=status.HTTP_403_FORBIDDEN)

            # Update fields
            game.title = request.data.get("title")
            game.description = request.data.get("description")
            game.designer = request.data.get("designer")
            game.year_released = request.data.get("year_released")
            game.num_players = request.data.get("num_players")
            game.est_playtime = request.data.get("est_playtime")
            game.age_recommendation = request.data.get("age_recommendation")

            game.save()

            if "categories" in request.data:
                game.categories.set(request.data["categories"])

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests to delete a game"""
        try:
            game = Game.objects.get(pk=pk)
            if game.creator != request.user:
                return Response({"detail": "You do not have permission to delete this game."}, status=status.HTTP_403_FORBIDDEN)
            game.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')


class GameSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Game
        fields = (
            'id',
            'title',
            'description',
            'designer',
            'year_released',
            'num_players',
            'est_playtime',
            'age_recommendation',
            'creator',
            'categories',
        )
