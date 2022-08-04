from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('password'), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_('confirm password'), widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save(using=self._db)
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text=_('you can change password using <a href="../password/">this link</a>'))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'bio', 'location', 'image', 'last_login')
