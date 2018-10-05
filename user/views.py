import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.views.generic import View

from user.models import User
from utils.mailer import Mailer
from user.forms import RegisterForm, UserForm

# Create your views here.

class RegisterView(View):

    def get(self, request):
        form = RegisterForm()

        return render(request, "user/register.html", {
            "form": form,
            #"trends": Trend.get_trends()
        })

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Creating user and profile
            try:
                with transaction.atomic():
                    new_user = User(
                                    username=form.cleaned_data['login'],
                                    password=make_password(form.cleaned_data['password']),
                                    email=form.cleaned_data['email'],
                                    avatar=form.cleaned_data['avatar'],
                                    reg_date=datetime.datetime.now()
                                    )
                    new_user.save()

                Mailer().send(new_user.email, 'sign_up', context={"login": new_user.username})
                return HttpResponseRedirect('/register/done/')
            except Exception as error:
                message = 'Ошибка при регистрации пользователя: ' + str(error) + str(form.cleaned_data)
        else:
            message = 'Ошибка при регистрации пользователя, проверьте поля '

        return render(request, "user/register.html", {
            "form": form,
            "message": message,
            #"trends": Trend.get_trends()
        })


class RegisterDoneView(View):

    def get(self, request):
        return render(request, "user/register_done.html", {
            #"trends": Trend.get_trends()
        })


class UserSettingsView(View):

    def get(self, request):
        return render(request, "index/settings.html", {
            "trends": Trend.get_trends()
        })

    def post(self, request):
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            with transaction.atomic():
                user_form.save()
            message = 'User settings successfully updated'
        else:
            message = 'Error while updating user'
        return render(request, "index/settings.html", {
            "user_form": user_form,
            "message": message,
            "trends": Trend.get_trends()
        })