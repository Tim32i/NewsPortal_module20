from django.shortcuts import render, redirect

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.contrib.auth.models import User, Group
from app_NewsPortal_module20.models import Author
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm

def EditProfile(request):
    # редирект с /accounts/profile на UserProfileUpdateView

    return redirect(f'/accounts/{request.user.pk}/edit_profile')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    # редактирование профиля после аутентификации пользователя
    form_class = ProfileForm
    model = User
    template_name = 'account/profile_update.html'


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    # Добавление пользователя в группу Common, если он впервые регистрируется через провайдера
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=None)
        common_group = Group.objects.get(name='common')
        if not user.groups.filter(name='common').exists():
            common_group.user_set.add(user)

        return user

@login_required
def upgrade_to_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    if not Author.objects.filter(author_user=user).exists():
        author = Author.objects.create(author_user=user)
        author.upgrade_rating()
        author.save()
    return redirect('/')


