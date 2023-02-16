from django.shortcuts import render, redirect, reverse
from .models import *
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import *
from .filters import UserFilterForm, NewsFilterForm, ChatFilterForm
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
    model = News
    queryset = News.objects.all()
    context_object_name = 'news'
    paginate_by = 10

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


@login_required(login_url='login')
def vote_like(request, pk):
    news = get_object_or_404(News, id=pk)

    if request.user in news.likes.all():
        news.likes.remove(request.user)
    else:
        news.likes.add(request.user)
    return redirect(reverse('news_detail', args=[str(news.id)]))


@login_required()
def create_news_voting(request, pk):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
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


@login_required()
def chat_list(request):
    chats = Chat.objects.filter(users__id__exact=request.user.id, is_active=True)
    filter = ChatFilterForm(request.GET, queryset=chats)
    chats = filter.qs
    return render(request, 'chats.html', {'chats': chats, 'filterchat': filter})


@login_required()
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


@login_required()
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

@login_required()
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


@login_required()
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
    print('das')
    comment_form = CommentForm
    context = {'comments': comments, 'news': news, 'page_obj': page_obj, 'new_comment': new_comment,
               'comment_form': comment_form, 'questions': []}
    total = 0
    if news.voting:
        for i in news.voting.questions_vote.all():
            total += i.get_total_votes()
        print(total)
        total_procent = 100 // total
        print(total_procent)
        for i in news.voting.questions_vote.all():
            context['questions'].append({'title': i.title, 'procent': i.get_total_votes() * total_procent, 'users': i.users, 'total_votes': i.get_total_votes()})
        print(context)
        context['total'] = total
    return render(request, template_name, context)


@permission_required('is_superuser')
def commentlist(request):
    if request.user.is_superuser:
        comment_list = Comment.objects.filter(active=False)

        context = {'comment_list': comment_list}
        return render(request, 'commentlist.html', context)
    return HttpResponse('Impossible to go ahead!')


@login_required()
def updatecomment(request, pk):
    if request.user.is_superuser:
        data = get_object_or_404(Comment, id=pk)
        data.active = True
        print('da')
        data.save()

        return redirect(reverse('commentlist'))
    return HttpResponse('Imposible to ahead')


def deletecomment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.delete()
    return redirect(reverse('commentlist'))


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
        query = News.objects.all()
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



@permission_required('is_superuser')
def createnews(request):
    if request.user.is_superuser:
        form = NewsForm()
        if request.method == 'POST':
            form = NewsForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/')

        context = {'form': form}

        return render(request, 'create_news.html', context)
    return HttpResponse('Impossible to enter page!')


@permission_required('is_superuser')
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


@permission_required('is_superuser')
def create_voting(request, pk):
    chat = get_object_or_404(Chat, id=pk)
    if request.method == 'POST':
        form = VotingForm(request.POST)
        das = form.save(commit=False)
        das.chat = chat
        das.save()
        return redirect(reverse('chat_detail', args=[pk]))
    form = VotingForm
    return render(request, 'add_voting.html', {'form': form, 'chat': chat})


@permission_required('is_superuser')
def add_questions(request, pk):
    voting = get_object_or_404(Voting, id=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        das = form.save(commit=False)
        das.voting = voting
        das.save()
        return redirect(reverse('chat_detail', args=[voting.chat.id]))
    form = VotingForm
    return render(request, 'add_voting.html', {'form': form, 'chat': voting})


@permission_required('is_superuser')
def end_chat(request, pk):
    chat = get_object_or_404(Chat, id=pk)
    chat.is_active = False
    chat.save()
    return redirect(reverse('chat_detail', args=[chat.id]))


@login_required()
def voting_detail(request, pk):
    voting = get_object_or_404(Voting, id=pk)
    return render(request, 'voting_detail.html', {'voting': voting})


@permission_required('is_superuser')
def create_news(request, pk):
    chat = get_object_or_404(Chat, id=pk)
    form = NewsForm
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES).save(commit=False)
        form.voting = chat.voting
        form.save()
        return redirect(reverse('news_detail', args=[form.id]))
    return render(request, 'create_news.html', {'form': form, 'chat': chat})



def managment(request):
    return render(request, 'managment.html')
