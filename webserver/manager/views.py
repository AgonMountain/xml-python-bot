from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, UpdateView
from django.contrib.auth import authenticate, login

from .forms import *


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


class ConfigView(UpdateView):
    model = Config
    template_name = 'manager/bot_config.html'
    form_class = ConfigForm


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
    form_search = BotUsersForm()
    form_table = BotUsersTableForm()
    return render(request, 'manager/bot_users.html', {'form_search': form_search, 'form_table': form_table})


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
