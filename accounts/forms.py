from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import Group, User
from django import forms


class BasicSignupForm(SignupForm):
    # добавления пользователя в группу Common при первой регистрации

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]