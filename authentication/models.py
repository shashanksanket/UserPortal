from django.db import models
from django.contrib.auth.models import User


class FileUpload(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="files")
    date_uploaded=models.DateTimeField(auto_now=True)
    file_type=models.CharField(max_length=10,blank=True)
    file = models.FileField(upload_to="media")