from django import forms
from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin
from .models import Rubrics, Account, Comment, Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'news', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Account)
admin.site.register(Rubrics)
admin.site.register(Post)

# class NewsAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())
#
#     class Meta:
#         model = News
#         fields = '__all__'


# class NewsAdmin(admin.ModelAdmin):
#     form = NewsAdminForm


admin.site.register(Voting)
admin.site.register(Question)
# admin.site.register(News, NewsAdmin)
admin.site.register(Chat)
admin.site.register(Region)
admin.site.register(Message)


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('title', 'preview')
