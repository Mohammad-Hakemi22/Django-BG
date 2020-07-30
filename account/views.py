from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from web.models import Articles
from django.urls import reverse_lazy
from .mixins import (
    FieldsMixins,
    FormValidMixins,
    AuthorAccessMixins,
    SuperUserDeleteMixins,
    AuthorsAccessMixins)
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


class Register(CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('لینک فعال سازی به ایمیل شما ارسال شد <a href="{% url "/login" %}">ورود</a>')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('اکانت شما با موفقیت فعال شد <a href="{% url "login" %}">ورود</a>')
    else:
        return HttpResponse('لینک فعال سازی نامعتبر است')
