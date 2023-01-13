from django.db import models
from django.db.models import Count

from account.models import Author


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'News {self.id}- {self.author.user.username}'

    def get_status(self):
        statuses = NewsStatus.objects.filter(news=self).values('status__name').annotate(count=Count('status'))
        result = {}
        for i in statuses:
            result[i['status__name']] = i['count']

        return result


class Comment(models.Model):
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment {self.id}- {self.author.user.username}'

    def get_status(self):
        statuses = CommentStatus.objects.filter(comment=self).values('status__name').annotate(count=Count('status'))
        result = {}
        for i in statuses:
            result[i['status__name']] = i['count']

        return result


class Status(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=50, unique=True)


class NewsStatus(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.SET_DEFAULT, default=1)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['author', 'news']

    def __str__(self):
        return f'{self.news.id} - {self.author.id} - {self.status}'


class CommentStatus(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.SET_DEFAULT, default=1)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['author', 'comment']

    def __str__(self):
        return f'{self.comment.id} - {self.author.id} - {self.status}'










