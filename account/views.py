from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView
from web.models import Articles


class ArticleList(LoginRequiredMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Articles.objects.all()
        else:
            return Articles.objects.filter(author=self.request.user)

class ArticleCreate(LoginRequiredMixin, CreateView):
    model=Articles
    fields=['author','title','slug','category','description','thumbnail','publish','status']
    template_name="registration/article-create-update.html"