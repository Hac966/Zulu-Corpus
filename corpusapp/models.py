from unittest.mock import DEFAULT

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .corpus_utils import process_and_update_corpus_text

# Create your models here.
STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Disapproved', 'Disapproved'),
)

class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    isizulu = models.CharField(max_length=10000)
    english = models.CharField(max_length=20000)
    extract = models.CharField(max_length=90000)
    isixhosa = models.CharField(max_length=2000, blank=True, null=True)
    isipedi = models.CharField(max_length=2000, blank=True, null=True)
    learn_more = models.URLField(max_length=200, default="")
    word_usage = models.CharField(max_length=200)
    commonly = models.CharField(max_length=200)
    word_frequency = models.IntegerField(default = 0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    word = models.IntegerField(default=0)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_entries',  # A way to access the entries a user likes: user.favorite_entries.all()
        blank=True
    )

    def __str__(self):
        return self.isizulu

    def save(self, *args, **kwargs):
        # We need to capture the text BEFORE the save and after the object is saved,
        # but since we are not passing 'self' to the utility, we can process here.
        sentence_text = self.isizulu

        # Call the original save method first
        super().save(*args, **kwargs)

        # CRITICAL: If this entry IS NOT a single word dictionary entry,
        # but a sentence entry, process it.
        if len(sentence_text.split()) > 1:
            process_and_update_corpus_text(sentence_text)

        # You may also want to process the word_usage field:
        # if self.word_usage:
        #     process_and_update_corpus_text(self.word_usage)

class CeremoniesBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    heading = models.CharField(max_length=200)
    extract = models.TextField(max_length=700, blank=True)
    learnMore = models.URLField(max_length=200, blank=True, null=True)
    picture = models.ImageField(upload_to='corpusapp/user/categories/ceremonies/')
    file = models.FileField(upload_to='corpusapp/user/categories/ceremonies/files', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.heading

class AttireBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    heading = models.CharField(max_length= 200)
    extract = models.TextField(max_length=700, blank=True)
    learnMore = models.URLField(max_length=200, blank=True, null=True)
    picture = models.ImageField(upload_to='corpusapp/user/categories/attire/')
    file = models.FileField(upload_to='corpusapp/user/categories/attire/files', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.heading

class CuisineBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    heading = models.CharField(max_length=200)
    extract = models.TextField(max_length=700, blank=True)
    learnMore = models.URLField(max_length=200, blank=True, null=True)
    picture = models.ImageField(upload_to='corpusapp/user/categories/cuisine/', blank=True, null=True)
    file = models.FileField(upload_to='corpusapp/user/categories/cuisine/files', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.heading

class HistoryBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    heading = models.CharField(max_length=200)
    extract = models.TextField(max_length=7000000, blank=True)
    picture = models.ImageField(upload_to='corpusapp/user/categories/history/images')
    file = models.FileField(upload_to='corpusapp/user/categories/history/files', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.heading

class QuizBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=900)
    answer = models.TextField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.question

class UserInfo(AbstractUser):
    pass

    def __str__(self):
        return self.username

class QuizScores(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)

    def __str__(self):
        # FIX: Access the 'username' attribute of the user object and combine it with the score.
        # This uses an f-string for a clear, readable output in the Django Admin.

        if self.user:
            return f'{self.user.username} - Score: {self.score}/{self.max_score}'
        else:
            # Handle the case where 'user' is null/blank (as per your model definition)
            return f'Anonymous User - Score: {self.score}/{self.max_score}'




