from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from .models import Author, Post, PostCategory, Category, Comment
from .forms import PostForm
from .filters import NewsFilter

from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class NewsListView(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(type_post='N')


class NewsFilteredListView(ListView):
    model = Post
    ordering = 'time_create'
    template_name = 'newsFiltered.html'
    context_object_name = 'posts'

    paginate_by = 2
    def get_queryset(self):
        queryset = Post.objects.filter(type_post__exact='N')
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class ArticleListView(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(type_post='A')


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post_categories_id = PostCategory.objects.filter(post=self.object).values('category')
        context['categories'] = Category.objects.filter(id__in=post_categories_id)
        return context


class NewsCreateView(FormView):

    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    def form_valid(self, form):
        post_title = form.cleaned_data['post_title']
        post_content = form.cleaned_data['post_content']
        author = form.cleaned_data['author']
        categories = form.cleaned_data['post_category']
        type_post = 'N'
        post_new = Post.objects.create(type_post=type_post,
                                       post_title=post_title,
                                       post_content=post_content,
                                       author=author
                                       )
        post_new.save()

        categories_list_id = Category.objects.filter(pk__in=categories).values('id')
        for category_id in categories_list_id:
            post_new.post_category.add(category_id['id'])                   # срабатывает m2m_changed
        post_new.save()


        if form.is_valid():
            return HttpResponseRedirect(f'/news/{post_new.pk}')


class ArticleCreateView(FormView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post_title = form.cleaned_data['post_title']
        post_content = form.cleaned_data['post_content']
        author = form.cleaned_data['author']
        categories = form.cleaned_data['post_category']
        type_post = 'A'
        post_new = Post.objects.create(type_post=type_post,
                                   post_title=post_title,
                                   post_content=post_content,
                                   author=author
                                   )
        post_new.save()

        categories_list_id = Category.objects.filter(pk__in=categories).values('id')
        for category_id in categories_list_id:
            post_new.post_category.add(category_id['id'])                     # срабатывает m2m_changed
        post_new.save()

        if form.is_valid():
            return HttpResponseRedirect(f'/articles/{post_new.pk}')


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_update.html'

    def form_valid(self, form):
        post_title = form.cleaned_data['post_title']
        post_content = form.cleaned_data['post_content']
        author = form.cleaned_data['author']
        categories = form.cleaned_data['post_category']
        type_post = 'N'
        post_updated = self.object
        post_updated.type_post=type_post
        post_updated.post_title=post_title
        post_updated.post_content=post_content
        post_updated.author=author
        post_updated.save()

        category_list = Category.objects.filter(pk__in=categories)

        PostCategory.objects.filter(post=post_updated).delete()   # удаляем все предыдущие категории

        # в цикле добавляем новые категории, при этом m2m_changed не срабатывает, т.к. поле manytomany
        # (post_updated.post_category) не затрагивается.

        for category in category_list:
            post_category = PostCategory.objects.create(post=post_updated, category=category)
            post_category.save()

        if form.is_valid():
            return HttpResponseRedirect(f'/news/{post_updated.pk}')\


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_update.html'

    def form_valid(self, form):
        post_title = form.cleaned_data['post_title']
        post_content = form.cleaned_data['post_content']
        author = form.cleaned_data['author']
        categories = form.cleaned_data['post_category']
        type_post = 'A'
        post_updated = self.object
        post_updated.type_post = type_post
        post_updated.post_title = post_title
        post_updated.post_content = post_content
        post_updated.author = author
        post_updated.save()

        category_list = Category.objects.filter(pk__in=categories)

        PostCategory.objects.filter(post=post_updated).delete()           # удаляем все предыдущие категории

        # в цикле добавляем новые категории, при этом m2m_changed не срабатывает, т.к. поле manytomany
        # (post_updated.post_category) не затрагивается.

        for category in category_list:
            post_category = PostCategory.objects.create(post=post_updated, category=category)
            post_category.save()

        if form.is_valid():
            return HttpResponseRedirect(f'/news/{post_updated.pk}')


class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('articles_list')