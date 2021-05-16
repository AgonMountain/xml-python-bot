from django.forms import ModelForm, TextInput
from .models import *
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе.')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError(f'Неверный пароль.')

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class BotConfigForm(forms.Form):
    token = forms.CharField(max_length=40, required='required', label='Токен')
#
#
# class BotUsersForm(forms.Form):
#     search_id = forms.CharField(max_length=40, required='required', label='ID пользователя')
#
#
# class BotUsersTableForm(forms.Form):
#     tr_number = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Номер')
#     tr_id = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='ID пользователя')
#     tr_scheme = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Имя схемы')
#     tr_element = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Имя элемента')
#
#
# class BotSchemesForm(forms.Form):
#     tr_number = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Номер')
#     tr_scheme = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Имя схемы')
#     tr_elements_number = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Количество элементов')
#
#
# class BotSchemeForm(forms.Form):
#     name = forms.CharField(max_length=40, required='required', label='Имя ветки')
#
#
# class BotElementForm(forms.Form):
#     name = forms.CharField(max_length=40, required='required', label='Имя элемента')
#     text = forms.CharField(max_length=40, required='required', label='Текст элемента')
#
#
# class BotAdditionForm(forms.Form):
#     text = forms.CharField(max_length=40, required='required', label='Текст / Условие дополнения')
#     link = forms.MultipleChoiceField(choices=(('1', 'один'), ('2', 'два'), ('3', 'три')))
#
#
# class BotTransitionForm(forms.Form):
#     text = forms.CharField(max_length=40, required='required', label='Текст / Условие перехода')
#
