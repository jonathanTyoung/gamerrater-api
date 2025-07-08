from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Game, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class GamesView(ViewSet):
    """Game view set"""

    def create(self, request):
        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.year_released = request.data["year_released"]
        game.num_players = request.data["num_players"]
        game.est_playtime = request.data["est_playtime"]
        game.age_recommendation = request.data["age_recommendation"]
        
        # Automatically assign the creator as the logged-in user
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
        """Handle GET requests for single item"""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist:
            return Response({"reason": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests"""
        try:
            game = Game.objects.get(pk=pk)
            game.title = request.data["title"]
            game.description = request.data["description"]
            game.designer = request.data["designer"]
            game.year_released = request.data["year_released"]
            game.num_players = request.data["num_players"]
            game.est_playtime = request.data["est_playtime"]
            game.age_recommendation = request.data["age_recommendation"]
            # Do NOT update creator here - keep original creator
            # game.creator = game.creator  # no change

            game.save()

            if "categories" in request.data:
                game.categories.set(request.data["categories"])

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        except Game.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item"""
        try:
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests for all items"""
        try:
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')

class GameSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)  # This is the key line

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
            'categories',  # Make sure this is included
        )
