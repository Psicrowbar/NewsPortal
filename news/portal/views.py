from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, PostCategory
from .forms import ProductForm
from .filters import PostFilter


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


class PostDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'post_detail'
    queryset = Post.objects.all()


class PostCreateView(CreateView):
    template_name = 'article_add.html'
    form_class = ProductForm
    success_url = '/products/'

class PostUpdateView(UpdateView):
    template_name = 'article_edit.html'
    form_class = ProductForm
    success_url = '/products/'
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