from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Articles, Category
from account.models import User
from django.core.paginator import Paginator
from account.mixins import AuthorAccessMixins


# Create your views here.
class Articlelist(ListView):
    queryset = Articles.objects.published()
    paginate_by = 1


# def home(request, page=1):
#     article_list = Articles.objects.published()
#     paginator = Paginator(article_list, 1)
#     articles = paginator.get_page(page)
#     context = {
#         'articles': articles,
#     }
#     return render(request, 'web/home.html', context)

class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        queryset = get_object_or_404(Articles.objects.published(), slug=slug)
        return queryset



class ArticlePreview(AuthorAccessMixins,DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        queryset = get_object_or_404(Articles, pk=pk)
        return queryset

# def detail(request, slug):
#     # article = Articles.objects.get(slug=slug)
#     context = {
#         'article': get_object_or_404(Articles.objects.published(), slug=slug)}
#     return render(request, 'web/detail.html', context)


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     article_list = category.articles.published()
#     paginator = Paginator(article_list, 1)
#     articles = paginator.get_page(page)
#     context = {
#         'category': category,
#         'articles': articles
#     }
#     return render(request, 'web/category.html', context)


class Categorylist(ListView):
    paginate_by = 1
    template_name = 'web/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class Authorlist(ListView):
    paginate_by = 1
    template_name = 'web/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
