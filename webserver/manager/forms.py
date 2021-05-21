from django.forms import ModelForm, TextInput
from django import forms
from django.contrib.auth.models import User
from .models import User as MyUser
from .models import Config, Messenger

class LoginForm(ModelForm):

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


class ConfigForm(ModelForm):
    messenger = Messenger.objects.get(name='telegram')
    config = Config.objects.get(messenger=messenger.id)


    token = forms.CharField(max_length=100, required=True, label='Токен',
                    widget=forms.TextInput(attrs={'placeholder': 'токен'}), initial=config.token)
    is_on = forms.CharField(max_length=100, label='Бот включен',
                    widget=forms.CheckboxInput(), initial=config.is_on)


    class Meta:
        model = Config
        fields = ['token', 'is_on']


class FindUserForm(ModelForm):

    search_id = forms.CharField(max_length=40, required=False, label='ID пользователя',
                    widget=forms.TextInput(attrs={'placeholder': 'все пользователи'}))

    class Meta:
        model = MyUser
        fields = ['search_id']




class BotSchemesForm(forms.Form):
    tr_number = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Номер')
    tr_scheme = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Имя схемы')
    tr_elements_number = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Количество элементов')


class BotSchemeForm(forms.Form):
    name = forms.CharField(max_length=40, required='required', label='Имя ветки')


class BotElementForm(forms.Form):
    name = forms.CharField(max_length=40, required='required', label='Имя элемента')
    text = forms.CharField(max_length=40, required='required', label='Текст элемента')


class BotAdditionForm(forms.Form):
    text = forms.CharField(max_length=40, required='required', label='Текст / Условие дополнения')
    link = forms.MultipleChoiceField(choices=(('1', 'один'), ('2', 'два'), ('3', 'три')))


class BotTransitionForm(forms.Form):
    text = forms.CharField(max_length=40, required='required', label='Текст / Условие перехода')

