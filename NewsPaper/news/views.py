from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('profile')


class PostList(ListView):
    model = Post
    ordering = '-created_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'separate_news.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'separate_news'

class PostSearch(ListView):
    model = Post
    ordering = '-created_date'
    template_name = 'search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

# Представление для создания новости
class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    # Разработанная форма
    form_class = PostForm
    # Модель новости
    model = Post
    # Шаблон страницы
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/create/':
            post.type = 'AR'
        post.save()
        return super().form_valid(form)

# Представление для редактирования новости
class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    # Разработанная форма
    form_class = PostForm
    # Модель новости
    model = Post
    # Шаблон страницы
    template_name = 'news_edit.html'

# Представление для удаления новости
class NewsDelete(DeleteView):
    # Модель новости
    model = Post
    # Шаблон страницы
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')

# Представление для создания статьи
class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    # Разработанная форма
    form_class = PostForm
    # Модель новости
    model = Post
    # Шаблон страницы
    template_name = 'articles_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        return super().form_valid(form)

# Представление для редактирования статьи
class ArticlesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    # Разработанная форма
    form_class = PostForm
    # Модель новости
    model = Post
    # Шаблон страницы
    template_name = 'articles_edit.html'

# Представление для удаления статьи
class ArticlesDelete(DeleteView):
    # Модель новости
    model = Post
    # Шаблон страницы
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('news')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-created_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
