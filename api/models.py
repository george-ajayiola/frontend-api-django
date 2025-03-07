import uuid
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    borrowed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="borrowed_books")
    return_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title
