from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
CHARS_TO_OUTPUT = 15


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follows",
                             verbose_name="Подписчик"
                             )
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="following",
                                  verbose_name="Автор"
                                  )

    def __str__(self):
        return f"{self.user} подписан на {self.following}"

    class Meta:
        unique_together = ("user", "following",)


class Group(models.Model):
    title = models.CharField("Имя", max_length=200)
    slug = models.SlugField("Адрес", unique=True)
    description = models.TextField("Описание")

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, blank=True,
                              null=True, on_delete=models.SET_NULL,
                              related_name="posts",
                              verbose_name="Сообщество")
    image = models.ImageField(
        upload_to="posts/", null=True, blank=True)

    def __str__(self):
        return self.text[:CHARS_TO_OUTPUT]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
