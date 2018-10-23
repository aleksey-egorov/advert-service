from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField('Название', max_length=255)
    content = models.TextField('Текст')
    date = models.DateField('Дата')
    preview = models.TextField('Аннотация')
    alias = models.CharField('Алиас', max_length=255, unique=True)
    small_image = models.ImageField(null=True, blank=True, upload_to='articles/')
    big_image = models.ImageField(null=True, blank=True, upload_to='articles/')
    tags = models.ManyToManyField('main.Tag')
    active = models.BooleanField('Активность', default=False, null=True, blank=True)

    def tag_list(self):
        return ', '.join([tag.name for tag in self.tags.all()])