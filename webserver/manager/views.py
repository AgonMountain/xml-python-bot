from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, UpdateView, DetailView, DeleteView
from django.contrib.auth import authenticate, login

from .forms import *
from .models import *


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
                return HttpResponseRedirect('/config/')
        return render(request, 'manager/login.html', context)


class ConfigView(View):

    def get(self, request, *args, **kwargs):
        telegram_messenger = Messenger.objects.get(name='telegram')
        telegram_config = Config.objects.get(messenger=telegram_messenger.id)
        # vk_messenger = Messenger.objects.get(name='vk')
        # vk_config = Config.objects.get(messenger=vk_messenger.id)

        form_telegram_config = ConfigForm(initial={
            'token': telegram_config.token,
            'is_on': telegram_config.is_on,
        })
        # form_vk_config = ConfigForm(initial={
        #     'token': vk_config.token,
        #     'is_on': vk_config.is_on,
        # })
        return render(request, 'manager/config.html', {'form_telegram_config': form_telegram_config})

    def post(self, request, *args, **kwargs):
        if 'telegram_save_btn' in request.POST:
            form_telegram_config = ConfigForm(request.POST)
            telegram_messenger = Messenger.objects.get(name='telegram')
            telegram_config = Config.objects.get(messenger=telegram_messenger.id)
            if form_telegram_config.is_valid():
                telegram_config.is_on = form_telegram_config.cleaned_data['is_on']
                telegram_config.token = form_telegram_config.cleaned_data['token']
                telegram_config.save()

        # if 'vk_save_btn' in request.POST:
        #     form_vk_config = ConfigForm(request.POST)
        #     vk_messenger = Messenger.objects.get(name='vk')
        #     vk_config = Config.objects.get(messenger=vk_messenger.id)
        #     if form_vk_config.is_valid():
        #         vk_config.is_on = form_vk_config.cleaned_data['is_on']
        #         vk_config.token = form_vk_config.cleaned_data['token']
        #         vk_config.save()

        telegram_messenger = Messenger.objects.get(name='telegram')
        telegram_config = Config.objects.get(messenger=telegram_messenger.id)
        # vk_messenger = Messenger.objects.get(name='vk')
        # vk_config = Config.objects.get(messenger=vk_messenger.id)

        form_telegram_config = ConfigForm(initial={
            'token': telegram_config.token,
            'is_on': telegram_config.is_on,
        })
        # form_vk_config = ConfigForm(initial={
        #     'token': vk_config.token,
        #     'is_on': vk_config.is_on,
        # })
        return render(request, 'manager/config.html', {'form_telegram_config': form_telegram_config})


class UsersView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        form_search = FindUserForm()
        return render(request, 'manager/users.html', {'form_search': form_search, 'users': users})

    def post(self, request, *args, **kwargs):
        form_search = FindUserForm(request.POST or None)
        if form_search.is_valid():
            user_id = form_search.cleaned_data['user_id']
            if user_id != '':
                if User.objects.filter(user_id=user_id).exists():
                    user_td = User.objects.get(user_id=user_id)
                    return render(request, 'manager/users.html', {'form_search': form_search, 'user_td': user_td})
                else:
                    return render(request, 'manager/users.html', {'form_search': form_search, 'error': "Пользователь не найден"})
        form_search = FindUserForm()
        users = User.objects.all()
        return render(request, 'manager/users.html', {'form_search': form_search, 'users': users})


class SchemesView(View):

    def get(self, request, *args, **kwargs):
        schemes = []
        dbschemes = Scheme.objects.all()
        for dbscheme in dbschemes:
            schemes.append({'id': dbscheme.id, 'name': dbscheme.name,
                            'elements_number': len(Element.objects.filter(scheme=dbscheme.id))})
        return render(request, 'manager/schemes.html', {'schemes': schemes})


class SchemeUpdateView(UpdateView):
    model = Scheme
    template_name = 'manager/scheme.html'
    form_class = SchemeForm


class SchemeDeleteView(DeleteView):
    model = Scheme
    template_name = 'manager/delete_scheme.html'
    success_url = '/schemes/'


class ElementUpdateView(UpdateView):
    model = Element
    template_name = 'manager/element.html'
    form_class = SchemeForm


class ElementDeleteView(DeleteView):
    model = Element
    template_name = 'manager/delete_scheme.html'
    success_url = '/schemes/<int:pk>'


class ElementAdditionUpdateView(UpdateView):
    model = ElementAddition
    template_name = 'manager/element_addition.html'
    form_class = AdditionForm


class ElementAdditionDeleteView(DeleteView):
    model = ElementAddition
    template_name = 'manager/delete_scheme.html'
    success_url = '/elements/<int:pk>/'


class ElementTransitionUpdateView(UpdateView):
    model = ElementTransition
    template_name = 'manager/element_transition.html'
    form_class = TransitionForm


class ElementTransitionDeleteView(DeleteView):
    model = ElementTransition
    template_name = 'manager/delete_scheme.html'
    success_url = '/elements/<int:pk>'
