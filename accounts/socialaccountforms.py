from django.contrib.auth.models import Group, User

from allauth.socialaccount.forms import


class CustomSocialSignupForm(SignupForm):

    def save(self, request):
        user = super(CustomSocialSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        if not user.groups.filter(name='common').exists():
            common_group.user_set.add(user)

        return user


