from django.contrib import admin
from .models import *

# admin panel change header
admin.site.site_header = 'مدیریت BIGBUG'


# Register your models here.
def make_published_article(modeladmin, request, queryset):
    row_update = queryset.update(status='P')
    if row_update == 1:
        message = 'مقاله بروز شد'
    else:
        message = f'{row_update} مقاله بروز شد  '
    modeladmin.message_user(request, f'{message}')


def make_draft_article(modeladmin, request, queryset):
    row_update = queryset.update(status='D')
    if row_update == 1:
        message = 'مقاله بروز شد'
    else:
        message = f'{row_update} مقاله بروز شد  '
    modeladmin.message_user(request, f'{message}')


make_draft_article.short_description = 'منتشر کردن مقالات'
make_draft_article.short_description = 'پیش نویس کردن مقالات'


def make_published_category(modeladmin, request, queryset):
    row_update = queryset.update(status=True)
    if row_update == 1:
        message = 'دسته بندی بروز شد'
    else:
        message = f'{row_update} دسته بندی بروز شد  '
    modeladmin.message_user(request, f'{message}')


def make_draft_category(modeladmin, request, queryset):
    row_update = queryset.update(status=False)
    if row_update == 1:
        message = 'دسته بندی بروز شد'
    else:
        message = f'{row_update} دسته بندی بروز شد  '
    modeladmin.message_user(request, f'{message}')


make_published_category.short_description = 'نمایش دادن دسته بندی'
make_draft_category.short_description = 'نمایش ندادن دسته بندی'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'jpublish', 'status', 'category_to_str'
                    )
    list_filter = ('title', 'slug', 'publish', 'status'
                   )
    search_fields = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['status', '-publish']  # - nozoli
    actions = [make_published_article, make_draft_article]

    def category_to_str(self, obj):
        return ' ,'.join([category.title for category in obj.category.active()])

    category_to_str.short_description = 'دسته بندی'


admin.site.register(Articles, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_published_category, make_draft_category]


admin.site.register(Category, CategoryAdmin)
