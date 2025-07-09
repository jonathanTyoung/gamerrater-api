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
        """GET all games"""
        try:
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(str(ex))

    def retrieve(self, request, pk=None):
        """GET single game by ID"""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist:
            return Response({"reason": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """POST new game"""
        try:
            game = Game.objects.create(
                title=request.data.get("title"),
                description=request.data.get("description"),
                designer=request.data.get("designer"),
                year_released=request.data.get("year_released"),
                num_players=request.data.get("num_players"),
                est_playtime=request.data.get("est_playtime"),
                age_recommendation=request.data.get("age_recommendation"),
                creator=request.user,
            )
            if "categories" in request.data:
                game.categories.set(request.data["categories"])
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """PUT update game"""
        try:
            game = Game.objects.get(pk=pk)
            if game.creator != request.user:
                return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

            for field in [
                "title", "description", "designer", "year_released",
                "num_players", "est_playtime", "age_recommendation"
            ]:
                setattr(game, field, request.data.get(field))

            game.save()

            if "categories" in request.data:
                game.categories.set(request.data["categories"])

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(str(ex))

    def destroy(self, request, pk=None):
        """DELETE game"""
        try:
            game = Game.objects.get(pk=pk)
            if game.creator != request.user:
                return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

            game.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------- SERIALIZERS ----------

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')


class GameSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    average_rating = serializers.FloatField(read_only=True)

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
            'average_rating',
        )
