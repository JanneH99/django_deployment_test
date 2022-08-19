from django.shortcuts import render
from .forms import UserProfileInfoForm, UserForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.




def home(request):
    return render(request, 'user_app/home.html')

def RegistrationView(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()


            try:
                validate_password(user.password, user)
            except ValidationError as e:
                user_form.add_error('password', e)
                return render(request, 'user_app/registration.html', {'user_form': user_form,
                                                                      'profile_form': profile_form,
                                                                      'registered': registered})

            user.set_password(user.password)

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)


    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'user_app/registration.html', {'user_form':user_form,
                                                          'profile_form' : profile_form,
                                                          'registered':registered})



def user_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('user_app:home'))

            else:
                    return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print("Someone tried to login")
            return HttpResponse("INVALID LOGIN DETAILS")
    else:
        return render(request, 'user_app/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_app:home'))
