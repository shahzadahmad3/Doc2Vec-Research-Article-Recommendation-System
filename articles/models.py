from django.db import models

class Article(models.Model):
    paper_id = models.CharField(max_length=100, unique=True)
    paper_title = models.CharField(max_length=255)
    author_keywords = models.TextField()
    abstract = models.TextField()
    area = models.CharField(max_length=255)
    embedding = models.JSONField(null=True, blank=True)  # stores Doc2Vec vector as list[float]

    def __str__(self):
        return f"{self.paper_title} ({self.paper_id})"
