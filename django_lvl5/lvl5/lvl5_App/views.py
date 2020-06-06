from django.shortcuts import render
# from lvl5_App.models import UserProfileInfo
from lvl5_App.forms import UserForm,UserProfileInfo_Form
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request,'lvl5_App/index.html')

@login_required
def special(request):
    return HttpResponse("You Are Logged In!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfo_Form(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            # Grabing data from the form  class
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Again Checking for profile_pics
            profile = profile_form.save(commit = False)
            #Next line is for the OneToOneField relation set in models
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            mobile = request.POST.get('mobile_no')

            if mobile :
                OTP = generate_otp(mobile)
                otp = request.POST.get('otp')
                if OTP == otp:
                    registered =  True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfo_Form()

    return render(request,'lvl5_App/registration.html',{'registered':registered,'user_form':user_form,'profile_form':profile_form})

def user_login(request):
    if request.method == 'POST':
        # gets the value from the login.html
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username , password = password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return  HttpResponse("Account Not Active!")
        else:
            print("Someone tried to login But Failed!")
            print("Username: {}, Password: {}".format(username,password))
            return HttpResponse("Invalid Detail!")
    else:
        return  render(request,'lvl5_App/login.html',{})

def generate_otp(mobile):
    import random,string,requests

    Otp = ''.join([random.choice(string.digits) for n in range(6)])
    url = "https://www.fast2sms.com/dev/bulk"

    payload = "sender_id=FSTSMS&message=Your%20OTP%20is%20{}&language=english&route=p&numbers={}".format(Otp,mobile)
    headers = {
        'authorization': "ogilVNPTfbFwBLan9QOuhKEpA8Y7y5M1vecDztC3UH2kRWdxsqQXjbW9sYBtr1ocd7aFTg0LkHqZNASV",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    return Otp
