from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS = ((0, "Draft"), (1, "Publish"))


class Region(models.Model):
    title = models.CharField(max_length=123)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Account(AbstractUser):
    email = models.EmailField(unique=True)
    birth_of_place = models.CharField(verbose_name=_('Место рождения'), max_length=50, blank=True, null=True)
    birth_of_date = models.DateField(verbose_name=_('Дата рождения'), blank=True, null=True)
    living_place = models.CharField(verbose_name=_('Место проживания'), max_length=80, blank=True, null=True)
    nation = models.CharField(verbose_name=_('Нация'), max_length=30, blank=True, null=True)
    occupation = models.CharField(verbose_name=_('Профессия'), max_length=50, blank=True, null=True)
    phone_number = models.IntegerField(verbose_name=_('Номер телефона'), blank=True, null=True)
    is_tor_aga = models.BooleanField(verbose_name=_('Тор Ага'), default=False)
    is_zam = models.BooleanField(verbose_name=_('Заместитель Тор Ага'), default=False)
    is_katchy = models.BooleanField(verbose_name=_('Катчы'), default=False)
    is_delegat = models.BooleanField(verbose_name=_('Делегат'), default=False)
    image = models.ImageField(verbose_name=_('Аватар'), upload_to='avatars/', blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name']


class Rubrics(models.Model):
    title = models.CharField(max_length=24, verbose_name='Название рубрики')
    content = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="blog_posts")
    rubric_id = models.ForeignKey(Rubrics, on_delete=models.CASCADE, verbose_name='Рубрика')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title


class Voting(models.Model):
    title = models.CharField(max_length=123)
    content = models.TextField()
    chat = models.OneToOneField('Chat', on_delete=models.CASCADE, related_name='voting_chat')

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=40)
    users = models.ManyToManyField(Account, related_name='users_votes', blank=True, null=True)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='questions_vote')

    def __str__(self):
        return self.title

    def get_total_votes(self):
        return self.users.count()


class News(models.Model):
    title = models.CharField(max_length=123)
    preview = models.CharField(max_length=244)
    content = models.TextField()
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='news/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_news', args=[self.pk])


class Chat(models.Model):
    title = models.CharField(
        max_length=123,
        verbose_name='Название',
        default='.',
        blank=True
    )
    description = models.TextField(
        default='.',
        blank=True
    )
    avatar = models.ImageField(
        upload_to='images/avatars/%Y/%m/%d/',
        verbose_name='Изображение',
        blank=True,
        null=True
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавление'
    )
    is_privat = models.BooleanField(
        default=False,
        blank=True
    )
    users = models.ManyToManyField(Account, related_name='chats_user')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-date']


class Message(models.Model):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )
    content = models.TextField(
        verbose_name='Сообщение'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавление'
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщении'


class QuestionMessage(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField()
    image = models.ImageField(upload_to='questionmessage/', blank=True, null=True)
    from_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_user_questions')
    created_date = models.DateTimeField(auto_now_add=True)
    to_user = models.ForeignKey(Account, related_name='to_user_questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос от товарища'
        verbose_name_plural = 'Вопросы от людей'
        ordering = ['-created_date']


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False, verbose_name='Active')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

