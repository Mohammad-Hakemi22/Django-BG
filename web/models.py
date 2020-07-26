from django.db import models
from django.utils import timezone
from extensions.utils import jalali_converter
from django.utils.html import format_html
from account.models import User
from django.urls import reverse


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
        ('D', 'پیش نویس'),      #draft
        ('P', 'منتشر شده'),     #publish
        ('I', 'در حال بررسی'),  #investigation
        ('B', 'تایید نشده'),    #back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles',
                               verbose_name='نویسنده')
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
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')
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

    def category_to_str(self):
        return ' ,'.join([category.title for category in self.category.active()])

    def get_absolute_url(self):
        return reverse('account:home')

    category_to_str.short_description = 'دسته بندی'
    thumbnail_tag.short_description = 'تصویر پست'
    objects = ArticleManager()
