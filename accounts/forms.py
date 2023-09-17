from django.contrib.auth.forms import UserCreationForm

from accounts.models import UserAccount


class AdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserAccount
        fields = UserCreationForm.Meta.fields
