from django.shortcuts import render, redirect, reverse
from .models import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import *
from .filters import UserFilterForm, NewsFilterForm
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.views import generic


class NewsListView(generic.ListView):
    template_name = 'indexActive.html'
    model = Voting
    queryset = News.objects.all()
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['register_form'] = UserRegisterForm
        print(context['register_form'])
        print('orin')
        context['rubrics'] = Rubrics.objects.all()
        context['text'] = _('Dastan')
        context['login_form'] = AuthenticationForm
        return context


class VotingDetailView(generic.DetailView):
    template_name = 'index.html'
    model = Voting
    context_object_name = 'voting'


@login_required(login_url='login')
def vote_question(request):
    question = get_object_or_404(Question, id=request.POST.get('question_id'))
    for i in question.voting.questions_vote.all():
        if request.user in i.users.all():
            question.users.remove(request.user)
            break

    else:
        question.users.add(request.user)
    return redirect(reverse('chat_detail', args=[str(question.voting.chat.id)]))


@login_required()
def create_news_voting(request, pk):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        das = form.save(commit=False)
        das.voting = get_object_or_404(Voting, id=pk)
        a = das.save()
        return redirect(das.get_absolute_url())
    form = NewsForm
    return render(request, 'create_news.html', {'form': form})


def chat_detail(request, pk):
    chat = get_object_or_404(Chat, id=pk)
    messages = Message.objects.filter(chat=chat)
    return render(request, 'chat_detail.html', {'chat': chat, 'messages': messages})


def chat_list(request):
    chats = Chat.objects.filter(users__id__exact=request.user.id)
    return render(request, 'chats.html', {'chats': chats})


def security(request):
    return render(request, 'security.html')


def profile(request, pk):
    account = get_object_or_404(Account, id=pk)
    return render(request, 'profile.html', {'account': account, 'chats': Chat.objects.filter(is_active=True)})


class DelegatListView(generic.ListView):
    model = Account
    queryset = Account.objects.filter(is_delegat=True)
    context_object_name = 'delegats'
    template_name = 'delegats.html'
    filter_class = UserFilterForm
    paginate_by = 10

    def get_queryset(self):
        query = Account.objects.filter(is_delegat=True)
        filter = UserFilterForm(self.request.GET, queryset=query)
        query = filter.qs
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DelegatListView, self).get_context_data(**kwargs)
        context['filter'] = UserFilterForm().form
        print('yes')
        context['regions'] = Region.objects.all()
        context['chats'] = Chat.objects.filter(is_active=True)
        print(context['filter'])
        return context


def delegats(request):
    users = Account.objects.all()
    return render(request, 'delegats.html', {'users': users})


def settings(request):
    form = UserUpdateForm(instance=request.user)
    if request.method == "POST":
        print('post')
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        print(form.errors)
    return render(request, 'settings.html', {'form': form})


def register(request):
    print('kirdi')
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('/')
        print(form.errors)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserRegisterForm()
    # return render(request=request, template_name="indexActive.html", context={"register_form": form})
    return redirect('/')


def loginpage(request):
    if request.method == "POST":
        print('login')
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print('valid')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('/')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            print(form.errors)
            messages.error(request, "Invalid email or password.")
    form = AuthenticationForm()
    return redirect('/')


def logoutpage(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(reverse('home'))


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')
    template_name = 'resetPassword.html'


def indexActive(request):
    print(Account.objects.all())
    rubrics = Rubrics.objects.all().order_by('-id')
    trans = _('привет')
    context = {'trans': trans, 'rubrics': rubrics, 'register_form': UserRegisterForm, 'login_form': AuthenticationForm}
    return render(request, 'indexActive.html', context)


def post_list(request, pk):
    post = Post.objects.filter(status=1, id=pk).order_by("-created_on")

    context = {'post_list': post}
    return render(request, template_name='post_list.html', context=context)

@login_required(login_url='login')
def createrubrics(request):
    form = RubricForm()
    if request.method == 'POST':
        form = RubricForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form = request.user
            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, 'createrubrics.html', context)


def deleterubrics(request, pk):
    teach = get_object_or_404(Rubrics, id=pk)
    teach.delete()
    return redirect('index')


def post1(request, pk):
    template_name = 'post1.html'
    news = get_object_or_404(News, id=pk)
    comments = news.comments.filter(active=True)
    new_comment = None
    paginator = Paginator(comments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'comments': comments,
                                           'news': news,
                                           'page_obj': page_obj,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def commentlist(request):
    if request.user.is_superuser:
        comment_list = Comment.objects.filter(active=False)

        context = {'comment_list': comment_list}
        return render(request, 'commentlist.html', context)
    return HttpResponse('Impossible to go ahead!')


def updatecomment(request, pk):
    if request.user.is_superuser:
        data = get_object_or_404(Comment, id=pk)
        form = Comment_mode_Form(instance=data)

        if request.method == "POST":
            form = Comment_mode_Form(request.POST, instance=data)
            if form.is_valid():
                form.save()
                return redirect('commentlist')
        context = {
            "form": form
        }
        return render(request, 'updatecomment.html', context)
    return HttpResponse('Imposible to ahead')


def deletecomment(pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.delete()
    return redirect('index')


def rubrics(request):
    rubrics = Rubrics.objects.all().order_by('-id')

    context = {'rubrics': rubrics}
    return render(request, 'rubrics.html', context)


class NewsRubListView(generic.ListView):
    model = News
    queryset = News.objects.all()
    context_object_name = 'news'
    template_name = 'rubrics.html'
    filter_class = NewsFilterForm
    paginate_by = 10

    def get_queryset(self):
        query = Account.objects.filter(is_delegat=True)
        filter = NewsFilterForm(self.request.GET, queryset=query)
        query = filter.qs
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsRubListView, self).get_context_data(**kwargs)
        context['filter'] = NewsFilterForm().form
        print('yes')
        context['rubrics'] = Rubrics.objects.all()
        context['chats'] = Chat.objects.filter(is_active=True)
        print(context['filter'])
        return context


def set_news(request):
    return render(request, 'new/setNews.html')



def createnews(request):
    if request.user.is_superuser:
        form = NewsForm()
        if request.method == 'POST':
            form = NewsForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/')

        context = {'form': form}

        return render(request, 'createnews.html', context)
    return HttpResponse('Impossible to enter page!')


def createchats(request):
    if request.user.is_superuser:
        form = ChatCreateForm()
        if request.method == 'POST':
            form = ChatCreateForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/')

        context = {'form': form}

        return render(request, 'createchats.html', context)
    return HttpResponse('Impossible to enter page!')


