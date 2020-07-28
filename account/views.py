from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from web.models import Articles
from django.urls import reverse_lazy
from .mixins import FieldsMixins, FormValidMixins, AuthorAccessMixins, SuperUserDeleteMixins,AuthorsAccessMixins
from .models import User
from .forms import ProfileForm



class ArticleList(AuthorsAccessMixins, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Articles.objects.all()
        else:
            return Articles.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixins, FieldsMixins, FormValidMixins, CreateView):
    model = Articles
    template_name = "registration/article-create-update.html"


class ArticleUpdate(AuthorAccessMixins, FieldsMixins, FormValidMixins, UpdateView):
    model = Articles
    template_name = "registration/article-create-update.html"


class ArticleDelete(SuperUserDeleteMixins, DeleteView):
    model = Articles
    success_url = reverse_lazy('account:home')
    template_name = "registration/articles_confirm_delete.html"


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')
