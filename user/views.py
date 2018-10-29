import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from lot.models import Lot, LotGallery
from utils.mailer import Mailer
from user.forms import RegisterForm, UserForm, LotAddForm, LotEditForm, LotImageUploadForm, LotImageDelForm
from user.models import User
from utils.context import Context

# Create your views here.

class RegisterView(View):

    def get(self, request):
        form = RegisterForm()

        return render(request, "user/register.html", {
            "form": form,
            "context": Context.get(request)
        })

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = User().add_user(form.cleaned_data)
            if new_user:
                Mailer().send(new_user.email, 'sign_up', context={"login": new_user.username})
                return HttpResponseRedirect('/register/done/')
            else:
                message = 'Ошибка при регистрации пользователя: ' + str(form.cleaned_data)
        else:
            message = 'Ошибка при регистрации пользователя, проверьте поля '

        return render(request, "user/register.html", {
            "form": form,
            "message": message,
            "context": Context.get(request)
        })


class RegisterDoneView(View):

    def get(self, request):
        return render(request, "user/register_done.html", {
            "context": Context.get(request)
        })


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        form = UserForm()
        form.set_initial(request.user)

        return render(request, "user/profile.html", {
            "form": form,
            "context": Context.get(request)
        })

    def post(self, request):
        form = UserForm(request.POST, request.FILES, instance=request.user)
        message = ''
        if form.is_valid():
            upd_user = User().update_user(request.user, form.cleaned_data)
            if upd_user:
                message = 'Профиль пользователя обновлен'
                request.user.avatar = 'avatars/' + str(request.user.avatar)    # Корректируем путь к аватару, чтобы показать его сразу, без перезагрузки страницы
        else:
            message = 'Ошибка при обновлении профиля'

        return render(request, "user/profile.html", {
            "form": form,
            "message": message
        })


class LotAddView(LoginRequiredMixin, View):

    def get(self, request):
        form = LotAddForm()
        lot_gallery = LotGallery.objects.get_images_forms(None, LotImageUploadForm, LotImageDelForm)

        return render(request, "user/add_lot.html", {
            "form": form,
            "lot_gallery": lot_gallery,
            "context": Context.get(request)
        })

    def post(self, request):
        form = LotAddForm(request.POST, request.FILES)
        if form.is_valid():
            result, err = Lot.objects.add_lot(form.cleaned_data, request.user)
            if result:
                # Mailer().send(email, 'lot_add', context={"login": new_user.username})
                return HttpResponseRedirect('/user/lot/add/done/')
            else:
                message = 'Ошибка при добавлении лота: ' + str(err) + str(form.cleaned_data)
        else:
            message = 'Ошибка при добавлении лота, проверьте поля '

        return render(request, "user/add_lot.html", {
            "form": form,
            "context": Context.get(request),
            "message": message,
        })


class LotAddDoneView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "user/add_lot_done.html", {
            "context": Context.get(request)
        })


class LotEditView(LoginRequiredMixin, View):

    def get(self, request, id):
        lot = get_object_or_404(Lot, id=id)
        if lot.author == request.user:
            form_main = LotEditForm()
            form_main.set_options(id)

            lot_gallery = LotGallery.objects.get_images_forms(lot, LotImageUploadForm, LotImageDelForm)

            return render(request, "user/edit_lot.html", {
                "lot_id": lot.id,
                "lot_gallery": lot_gallery,
                "form": form_main,
                "context": Context.get(request)
            })

    def post(self, request, id):
        lot = get_object_or_404(Lot, id=id)
        if lot.author == request.user:
            form = LotEditForm(request.POST, request.FILES)
            if form.is_valid():
                result, err = Lot.objects.update_lot(id, form.cleaned_data)
                if result:
                    return HttpResponseRedirect('/user/lot/edit/done/')
                    #message = str(form.cleaned_data)
                else:
                    message = 'Ошибка при редактировании лота: ' + str(err) + str(form.cleaned_data)

            else:
                message = 'Ошибка при редактировании лота, проверьте поля '

            return render(request, "user/edit_lot.html", {
                "lot_id": lot.id,
                "form": form,
                "context": Context.get(request),
                "message": message,
            })


class LotEditDoneView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "user/edit_lot_done.html", {
            "context": Context.get(request)
        })


class UserLotsView(LoginRequiredMixin, View):
    def get(self, request):
        page = request.GET.get('page')
        lots_list = Lot.objects.filter(author=request.user).order_by('-upd_date')
        paginator = Paginator(lots_list, 12)

        try:
            lots = paginator.get_page(page)
        except PageNotAnInteger:
            lots = paginator.get_page(1)
        except EmptyPage:
            lots = paginator.get_page(page)

        return render(request, "user/lots.html", {
            "lots": lots,
            "context": Context.get(request)
        })


class LotImageAddView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = LotImageUploadForm(request.POST, request.FILES)
        if image_form.is_valid():
            LotGallery.objects.save_tmp_image(image_form.cleaned_data['image'])
            del_form = LotImageDelForm()
            del_form.set_initial(status='added', num=image_form.cleaned_data['num'], filename=image_form.cleaned_data['image'])

            return render(request, "user/lot_image.html", {
                "image_form": image_form,
                "del_form": del_form
            })


class LotImageDelView(LoginRequiredMixin, View):
    def post(self, request):
        del_form = LotImageDelForm(request.POST, request.FILES)
        if del_form.is_valid():
            image_form = LotImageUploadForm()
            image_form.set_initial(status='deleted', num=del_form.cleaned_data['num'])

            return render(request, "user/lot_image_empty.html", {
                "image_form": image_form
            })