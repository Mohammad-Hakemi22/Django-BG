from django.http import Http404


class FieldsMixins():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = [
                'author', 'title', 'slug', 'category',
                'description', 'thumbnail', 'publish', 'status'
            ]
        elif request.user.is_author:
            self.fields = [
                'title', 'slug', 'category',
                'description', 'thumbnail', 'publish'
            ]
        else:
            raise Http404("you can't see this page")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixins():
    def form_valid(self, form):
        if self.request.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = 'D'
        return super().form_valid(form)
