from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class Author(models.Model):
    # Связь «один к одному» с встроенной моделью пользователей User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Рейтинг пользователя
    rating = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.user}'

    # Метод update_rating() модели Author, который обновляет рейтинг
    # текущего автора (метод принимает в качестве аргумента только self)
    def update_rating(self):
        # Cуммарный рейтинг каждой статьи автора умножается на 3
        posts_rating = self.post_set.aggregate(pr=Coalesce(Sum('rating'), 0)).get('pr')
        # Cуммарный рейтинг всех комментариев автора
        comments_rating = self.user.comment_set.aggregate(cr=Coalesce(Sum('rating'), 0)).get('cr')
        # Суммарный рейтинг всех комментариев к статьям автора
        posts_comments_rating = self.post_set.aggregate(pcr=Coalesce(Sum('rating'), 0)).get('pcr')

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()

class Category(models.Model):
    # Категории новостей/статей
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name.title()

class Post(models.Model):
    # выбор типа поста
    article = 'AR'
    news = 'NE'
    POSTS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    # Cвязь «один ко многим» с моделью Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Поле с выбором — «статья» или «новость»
    type = models.CharField(max_length=2, choices=POSTS, default=news)
    # Автоматически добавляемые дата и время создания
    created_date = models.DateTimeField(auto_now_add=True)
    # Cвязь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory)
    post = models.ManyToManyField(Category, through="PostCategory")
    # Заголовок статьи/новости
    title = models.CharField(max_length=255)
    # Текст статьи/новости
    text = models.TextField()
    # Рейтинг статьи/новости
    rating = models.IntegerField(default=0)

    # Метод like, который увеличивает рейтинг поста на единицу
    def like(self):
        self.rating += 1
        self.save()

    # Метод dislike, который уменьшает рейтинг поста на единицу
    def dislike(self):
        self.rating -= 1
        self.save()

    # Метод preview() модели Post, который возвращает начало статьи
    # (предварительный просмотр) длиной 124 символа и добавляет
    # многоточие в конце
    def preview(self):
        small_text = self.text[:124] + '...'
        return small_text

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('separate_news', args=[str(self.id)])


class PostCategory(models.Model):
    # Связь «один ко многим» с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Связь «один ко многим» с моделью Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    # Связь «один ко многим» с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Связь «один ко многим» со встроенной моделью User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Текст комментария
    text = models.TextField()
    # Дата и время создания комментария
    created_date = models.DateTimeField(auto_now_add=True)
    # Рейтинг комментария
    rating = models.IntegerField(default=0)

    # Метод like, который увеличивает рейтинг комментария на единицу
    def like(self):
        self.rating += 1
        self.save()

    # Метод dislike, который уменьшает рейтинг комментария на единицу
    def dislike(self):
        self.rating -= 1
        self.save()


