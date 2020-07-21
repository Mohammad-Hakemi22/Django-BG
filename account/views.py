from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView,UpdateView
from web.models import Articles
from .mixins import FieldsMixins, FormValidMixins,AuthorAccessMixins


class ArticleList(LoginRequiredMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Articles.objects.all()
        else:
            return Articles.objects.filter(author=self.request.user)


class ArticleCreate(LoginRequiredMixin, FieldsMixins, FormValidMixins, CreateView):
    model = Articles
    template_name = "registration/article-create-update.html"


class ArticleUpdate(AuthorAccessMixins, FieldsMixins, FormValidMixins, UpdateView):
    model = Articles
    template_name = "registration/article-create-update.html"
