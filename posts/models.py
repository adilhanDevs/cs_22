from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.FileField(upload_to="posts_images", blank=True, verbose_name="Картинка")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"