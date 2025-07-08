from django.db import models

def user_directory_path(instance, filename):
    # Images will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.id}/{filename}'

class UploadedImage(models.Model):
    image = models.ImageField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
