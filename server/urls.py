from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', NewsListView.as_view(), name='home'),
    path('voting/detail/<int:pk>', VotingDetailView.as_view(), name='voting_detail'),
    path('vote/', vote_question, name='question_vote'),
    path('vote_like/<int:pk>', vote_like, name='vote_like'),
    path('create/news/<int:pk>', create_news_voting, name='create_news'),
    path('chat/<int:pk>', chat_detail, name='chat_detail'),
    path('chats/', chat_list, name='chats'),
    path('security/', security, name='security'),
    path('settings/', settings, name='settings'),
    path('profile/<int:pk>', profile, name='profile'),
    path('rubrics/', NewsRubListView.as_view(), name='rubrics'),
    path('delegats/', DelegatListView.as_view(), name='delegats'),
    path('createrubrics/', createrubrics, name='createrubrics'),
    path('deleterubrics/<int:pk>/', deleterubrics, name='deleterubrics'),
    path('news/detail/<int:pk>/', post1, name='news_detail'),
    path('post_list/<int:pk>/', post_list, name='post_list'),
    path('updatecomment/<int:pk>/', updatecomment, name='updatecomment'),
    path('deletecomment/<int:pk>/', deletecomment, name='deletecomment'),
    path('commentlist/', commentlist, name='commentlist'),
    path('register/', register, name='register'),
    path('logout/', logoutpage, name='logout'),
    path('login/', loginpage, name='login'),
    path('setnews/', set_news, name='setnews'),
    path('createchats/', createchats, name='createchats'),
    path('createnews/', createnews, name='createnews'),
    path('create_voting/<int:pk>', create_voting, name='create_voting'),
    path('add_questions/<int:pk>', add_questions, name='add_questions'),
    path('end_chat/<int:pk>', end_chat, name='end_chat'),
    path('voting_detail/<int:pk>', voting_detail, name='voting_detail'),
    path('resetPassword/', PasswordsChangeView.as_view(), name='resetPassword'),
    path('managment/', managment, name='managment'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='resetPassword2.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='reset_password_complete'),

]
