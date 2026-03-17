# Likes and Comments Changes

## Что изменено

Я привел лайки и комментарии к той же схеме, что и создание постов: через DRF validation и обработку `request.user` на сервере.

Основная идея:

- не передавать `account` с клиента
- брать пользователя из `request.user`
- валидировать входящие данные через сериализаторы
- возвращать `400`, если данные невалидны

## Измененные файлы

### `posts/views.py`

Что изменилось:

- в `PostListAPIView.post()` используется `request.data.copy()`
- `user` подставляется с сервера: `request.user.id`
- если сериализатор невалиден, возвращается `400`
- `LikeAPIView` теперь валидирует только поле `post`
- лайк ставится или снимается для текущего авторизованного пользователя

Ключевая логика:

```python
class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = PostCreateSerializer(data=data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

```python
class LikeAPIView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = LikeToggleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        post = serializer.validated_data['post']
        like_obj = Like.objects.filter(post=post, account=request.user).first()

        if not like_obj:
            Like.objects.create(post=post, account=request.user)
        else:
            like_obj.delete()
            return Response({"message": "Like was delete"}, status=status.HTTP_200_OK)

        return Response({"message": "Like was created"}, status=status.HTTP_201_CREATED)
```

### `posts/serializers.py`

Что добавилось:

- отдельный сериализатор `LikeToggleSerializer`
- он принимает только `post`
- `post` валидируется как существующий объект `Post`

```python
class LikeToggleSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
```

### `comments/views.py`

Что добавилось:

- `CommentListCreateAPIView`
- для `POST` используется `CommentCreateSerializer`
- комментарий создается от `request.user`
- доступ только для авторизованных пользователей

```python
class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.select_related('account', 'post').all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        comment = serializer.save(account=request.user)
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
```

### `comments/serializers.py`

Что добавилось:

- `CommentCreateSerializer`
- валидация текста комментария
- пустой или состоящий только из пробелов текст не проходит

```python
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'post']

    def validate_text(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Comment text cannot be empty.')
        return value
```

### `comments/urls.py`

Добавлен маршрут комментариев:

```python
urlpatterns = [
    path('', CommentListCreateAPIView.as_view(), name='comment-list'),
]
```

### `blog/urls.py`

Подключен общий API маршрут комментариев:

```python
api_urlpatterns = [
    path('', include('posts.urls')),
    path('accounts/', include('accounts.urls')),
    path('comments/', include('comments.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

## Какие теперь запросы отправлять

### Поставить или убрать лайк

`POST /api/likes`

Тело:

```json
{
  "post": 1
}
```

Поведение:

- если лайка нет, он создается
- если лайк уже есть, он удаляется

### Создать комментарий

`POST /api/comments/`

Тело:

```json
{
  "post": 1,
  "text": "Мой комментарий"
}
```

## Что это дает

- клиент больше не может подменять `account`
- логика лайков и комментариев стала одинаковой по стилю
- входящие данные валидируются через сериализаторы
- ошибки возвращаются корректно через `400 Bad Request`
- API стало проще использовать на фронте

## Проверка

После изменений проект проверялся командой:

```bash
python3 manage.py check
```

Результат: `System check identified no issues (0 silenced).`