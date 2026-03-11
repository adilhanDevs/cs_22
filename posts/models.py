from django.db import models
from accounts.models import Account


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.FileField(upload_to="posts_images", blank=True, verbose_name="Картинка")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создание")
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="user_posts")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Like(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_likes", verbose_name="Аккаунт")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes", verbose_name="Пост")
    created_at = models.DateField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.account} - {self.post}"

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        unique_together = ("account", "post")
        # constraints = [models.UniqueConstraint(fields=["account", "post"], name="unique Like")]