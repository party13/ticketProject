from django.shortcuts import render, redirect

from .models import UserKB
from .forms import ResetPasswordForm
from django.contrib.auth import logout, login
from django.views.generic import View
from django.db.models import Q
from datetime import date, timedelta

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate

from .forms import UserForm



class Cabinet(View):
    def get(self, request):
        user = request.user
        userForm = UserForm(instance=user)
        context = {
            'user_name': user,
            'form': userForm,
        }
        return render(request, template_name='registration/cabinet.html', context=context )

    def post(self, request):
        print ('cabinet post')
        user = request.user
        userForm = UserForm(request.POST, instance=user)

        if userForm.is_valid():
            print('successfully updated')
            user.save()
            return redirect('cabinet')

        print('update failed!')
        context = {
            'user_name': user,
            'form': userForm,
        }
        return render(request, template_name='registration/cabinet.html', context=context)



class MyLogin(auth_views.LoginView):
    def get(self, request ):
        userlogin = request.user
        context = {
            'user_login': userlogin,
            'form': AuthenticationForm(),
        }
        return render(request, template_name='registration/login.html', context=context )

    def post(self, request, next=''):
        user = request.POST.get('username')
        psw = request.POST.get('password')

        user = authenticate(username=user, password=psw)
        if user:
            login(request, user)
            print('login success: ', user)
            return redirect('all' )
        else:
            print(' invalid username or password ')
            context = {
                #'errors': 'error',
                'form' : AuthenticationForm(data=request.POST)
            }
            return render(request, template_name='registration/login.html', context = context)


class MyResetPassword(View):
    def get(self, request):
        print ('!my resetpassword view: GET')
        context =  {
            'form': ResetPasswordForm(),
        }
        return render(request, 'registration/password_reset.html', {'form': ResetPasswordForm()} )

    def post(selfself,request):
        form = ResetPasswordForm(data = request.POST)
        error = ''
        if form.is_valid():
            email = request.POST.get('email')
            tabelNm = request.POST.get('tabelNum')

            try:
                user = UserKB.objects.get( tabelNumber__iexact = tabelNm , email__iexact=email)
                if user.is_active:
                    form.save(user)
                else:
                    print('user is not active')
                    error ="current user is not active."
                    raise form.ValidationError(form.error_messages['password_mismatch'],
                                               code='password_mismatch' )
            except:
                error="user not found or tabel # and @ don't match"


            return render(request, template_name='registration/password_reset_ok.html',
                          context = {'email': email, 'error':error} )

        return render(request, 'registration/password_reset.html', {'form': form} )

class MyChangePassword(auth_views.PasswordChangeView):
    def get(self, request):
        user=request.user
        form = PasswordChangeForm(user=user)

        context = {'form':form, 'user_name':user}
        return render(request, template_name='registration/password_change.html', context=context)

    def post(self, request):
        user = request.user
        print ('changing password for user : ', user)
        form = PasswordChangeForm(user = user, data=request.POST)
        error=''
        if form.is_valid():
            print('all good psswrd chngd')
            context = {'form': form,
                       'errors': error,
                       'user_name': user}
            form.save()
            return render(request, template_name='registration/password_change_ok.html', context=context)
        print('smth wrong')

        return render(request, template_name='registration/password_change.html', context = {'form':form})


def logout_view(request):
    print('logout function')
    logout(request)
    return render(request, 'tickets/index.html')

