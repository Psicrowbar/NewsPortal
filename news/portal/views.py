from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Post, PostCategory,BaseRegisterForm, Author,Category
from .forms import ProductForm
from .filters import PostFilter
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .tasks import send_email_task
@login_required
def upgrade_me(request):
    Author.objects.get_or_create(user=request.user)
    authors_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        authors_group.user_set.add(request.user)
    return redirect('/news/')
class ProtectedView(LoginRequiredMixin, TemplateView):

    template_name = 'protected_page.html'
class PostList(ListView):
    model = Post
    ordering = 'post_date'
    template_name = 'articles.html'
    context_object_name = 'post_news'
    paginate_by = 10

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  #вписываем фильтр в контекст
        context['categories'] = PostCategory.objects.all()
        context['form'] = ProductForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый пост
            form.save()

        return super().get(request, *args, **kwargs)


class PostDetail(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'post_detail'
    queryset = Post.objects.all()


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    permission_required = ('portal.add.post')
    template_name = 'article_add.html'
    form_class = ProductForm
    success_url = '/news/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        send_email_task.delay(post.pk)
        return super().form_valid(form)
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    template_name = 'article_edit.html'
    permission_required = ('portal.update.post')
    form_class = ProductForm
    success_url = '/news/'
    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте редактирования
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления поста
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    queryset = Post.objects.all()
    success_url = '/products/'
    context_object_name = 'article'


class PostSearch(ListView):   #поиск поста
    model = Post
    template_name = 'article_search.html'
    context_object_name = 'post_news'
    paginate_by = 10

    def get_queryset(self):  # получаем обычный запрос
        queryset = super().get_queryset()  # используем наш класс фильтрации
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        return context

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category).order_by('-post_date')
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
    message = 'вы подписались на категорию: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'вы отписались от категории: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})