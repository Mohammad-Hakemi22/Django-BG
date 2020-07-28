from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from web.models import Articles


class FieldsMixins():
    def dispatch(self, request, *args, **kwargs):
        self.fields = [
                'title', 'slug', 'category',
                'description', 'thumbnail', 'publish', 'is_special', 'status',
            ]
        if request.user.is_superuser:
            self.fields.append('author')
        return super().dispatch(request, *args, **kwargs)


class FormValidMixins():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'I':
                self.obj.status = 'D'
        return super().form_valid(form)


class AuthorAccessMixins():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Articles, pk=pk)
        if article.author == request.user and article.status in ['B', 'D'] or\
                request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("you can't see this page")


class SuperUserDeleteMixins():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("you can't see this page")


class AuthorsAccessMixins():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("account:profile")
        else:
            return redirect("account:login")
