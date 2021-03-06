from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from embed_video.fields import EmbedVideoField
from autoslug import AutoSlugField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
            .filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    )
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = AutoSlugField(populate_from='title', unique_for_date='publish')
    subhead = models.CharField(max_length=250, verbose_name='Краткое описание', blank=True)

    author = models.ForeignKey(User,
                               related_name='blog_posts',
                               default=1,
                               verbose_name='Автор')
    body = RichTextUploadingField(blank=True,
                                  default='',
                                  config_name='awesome_ckeditor',
                                  verbose_name='Текст')
    publish = models.DateTimeField(default=timezone.now,
                                   verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Дата редактирования')
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft',
                              verbose_name='Статут публикации')
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager(blank=True)
    video = EmbedVideoField(blank=True,
                            verbose_name='Видео')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])
