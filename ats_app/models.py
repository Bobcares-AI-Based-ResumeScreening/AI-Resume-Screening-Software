from django.db import models

class ResumeUpload(models.Model):
    resume = models.FileField(upload_to='uploads/')
