from django.db import models
from django.utils import timezone
from extensions.utils import jalali_converter
from django.utils.html import format_html


# create my manager
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='P')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children', verbose_name='زیر دسته')
    title = models.CharField(max_length=300, verbose_name='عنوان دسته بندی')
    slug = models.CharField(max_length=100, unique=True, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='نمایش داده شود')
    position = models.IntegerField(verbose_name='موقعیت')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['-parent__id', 'position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Articles(models.Model):
    STATUS_CHOICES = (
        ('D', 'پیش نویس'),
        ('P', 'منتشر شده')
    )
    title = models.CharField(max_length=300, verbose_name='عنوان')
    slug = models.CharField(max_length=100, unique=True,
                            verbose_name='آدرس مقاله')
    category = models.ManyToManyField('Category', verbose_name='دسته بندی', related_name='articles')
    description = models.TextField(verbose_name='محتوا')
    thumbnail = models.ImageField(
        upload_to='images', verbose_name='تصویر مقاله')
    publish = models.DateTimeField(
        default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']

    def jpublish(self):
        return jalali_converter(self.publish)

    def __str__(self):
        return self.title

    jpublish.short_description = 'زمان انتشار'

    def thumbnail_tag(self):
        return format_html(
            "<img src='{}' height=80 width=120 style='border-radius: 10px;' >".format(self.thumbnail.url))

    thumbnail_tag.short_description = 'تصویر پست'
    objects = ArticleManager()
