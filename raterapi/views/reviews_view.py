from django.db import IntegrityError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from raterapi.models import Review, Game
from django.contrib.auth import get_user_model

User = get_user_model()

class ReviewsViewSet(ViewSet):
    """Review view set"""

    def create(self, request):
        """Handle POST operations with unique constraint check"""
        try:
            # Optional: Prevent duplicate before saving
            existing_review = Review.objects.filter(
                user=request.data["user"], game=request.data["game"]
            ).first()
            if existing_review:
                return Response(
                    {"detail": "You have already submitted a review for this game."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            review = Review()
            review.game = Game.objects.get(pk=request.data["game"])
            review.user = User.objects.get(pk=request.data["user"])
            review.content = request.data["content"]
            review.save()

            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            # Catch if unique_together constraint fails unexpectedly
            return Response(
                {"detail": "Duplicate review: you can only review a game once."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Game.DoesNotExist:
            return Response(
                {"detail": "Game not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single review"""
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response({'detail': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests"""
        try:
            review = Review.objects.get(pk=pk)
            review.content = request.data["content"]
            review.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({'detail': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """Handle DELETE requests"""
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist as ex:
            return Response({'detail': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'detail': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests for all reviews"""
        try:
            reviews = Review.objects.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for Review"""

    class Meta:
        model = Review
        fields = ('id', 'game', 'user', 'content', 'date_posted')
        depth = 1  # include nested game/user info
