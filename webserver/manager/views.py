from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, UpdateView
from django.contrib.auth import authenticate, login

from .forms import *
from .models import User, Config, Messenger

class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'manager/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/config')
        return render(request, 'manager/login.html', context)


class ConfigView(View):

    def get(self, request, *args, **kwargs):
        config_form = ConfigForm()
        return render(request, 'manager/bot_config.html', {'config_form': config_form})

    # def post(self, request, *args, **kwargs):
    #     form_search = BotUsersSearchForm(request.POST or None)
    #     if form_search.is_valid():
    #         search_id = form_search.cleaned_data['search_id']
    #         if search_id != '':
    #             if User.objects.filter(user_id=search_id).exists():
    #                 user_td = User.objects.get(user_id=search_id)
    #                 return render(request, 'manager/bot_users.html', {'form_search': form_search, 'user_td': user_td})
    #             else:
    #                 return render(request, 'manager/bot_users.html', {'form_search': form_search, 'error': "Пользователь не найден"})
    #     form_search = BotUsersSearchForm()
    #     users = User.objects.all()
    #     return render(request, 'manager/bot_users.html', {'form_search': form_search, 'users': users})


    # model = Config
    # template_name = 'manager/bot_config.html'
    # form_class = ConfigForm


class UsersView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        form_search = FindUserForm()
        return render(request, 'manager/bot_users.html', {'form_search': form_search, 'users': users})

    def post(self, request, *args, **kwargs):
        form_search = FindUserForm(request.POST or None)
        if form_search.is_valid():
            search_id = form_search.cleaned_data['search_id']
            if search_id != '':
                if User.objects.filter(user_id=search_id).exists():
                    user_td = User.objects.get(user_id=search_id)
                    return render(request, 'manager/bot_users.html', {'form_search': form_search, 'user_td': user_td})
                else:
                    return render(request, 'manager/bot_users.html', {'form_search': form_search, 'error': "Пользователь не найден"})
        form_search = FindUserForm()
        users = User.objects.all()
        return render(request, 'manager/bot_users.html', {'form_search': form_search, 'users': users})


@login_required()
def bot_config(request):
    form = ConfigForm()
    return render(request, 'manager/bot_config.html', {'form': form})


@login_required()
def bot_schemes(request):
    form = BotSchemesForm()
    return render(request, 'manager/bot_schemes.html', {'form': form})




@login_required()
def bot_users(request):
    users = User.objects.all()
    form_search = FindUserForm()
    return render(request, 'manager/bot_users.html', {'form_search': form_search, 'users': users})





@login_required()
def scheme(request):
    form = BotSchemeForm()
    return render(request, 'manager/bot_scheme.html', {'form': form})


@login_required()
def element(request):
    form = BotElementForm()
    return render(request, 'manager/bot_element.html', {'form': form})


@login_required()
def addition(request):
    form = BotAdditionForm()
    return render(request, 'manager/bot_addition.html', {'form': form})


@login_required()
def transition(request):
    form = BotTransitionForm()
    return render(request, 'manager/bot_transition.html', {'form': form})
