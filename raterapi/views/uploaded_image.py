import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from raterapi.models import Game
from raterapi.models import GamePicture

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_game_picture(request):
    try:
        format, imgstr = request.data["game_image"].split(";base64,")
        ext = format.split("/")[-1]
        file_name = f'{request.data["game_id"]}-{uuid.uuid4()}.{ext}'
        data = ContentFile(base64.b64decode(imgstr), name=file_name)

        game = Game.objects.get(pk=request.data["game_id"])
        picture = GamePicture(game=game)
        picture.action_pic = data
        picture.save()

        return Response({"message": "Image uploaded successfully."}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
