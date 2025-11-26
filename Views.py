from email import errors
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings

from .models import Users
from organization.models import Group, Organization, org_License
from organization.views import check_license_valid

from functools import wraps
import json
import re
import time


allRoles = ['Admin', 'Developer','User']

def loginRequired(*allowedRoles):
    def mydecorator(f):
        @wraps(f)
        def wrapped(request, *args, **kwargs):
            if 'user' in request.session:
                user = request.session['user']
                if 'role' in request.session:
                    role= request.session['role']
                    if  role in allowedRoles:
                        current_time = time.time()
                        session_expiry_time =  settings.USER_SESSION_TIMEOUT
                        last_activity = request.session.get('last_activity')
                        sessionTimeout = False
                        if last_activity and current_time - last_activity > session_expiry_time:
                            sessionTimeout = True
                        request.session['last_activity'] = current_time
                        param = {
                                'current_user' : user,
                                'userId' : request.session['userId'],
                                'current_role' : role,
                                'orgId' : request.session['orgId'],
                                'orgName' : request.session['orgName'],
                                'group' : request.session['group'],
                                'visibility' : {
                                    "allRoles" : ['Admin', 'Developer','User'],
                                    "admin" : ['Admin'],
                                    "adminDev" : ['Admin','Developer'],
                                    "nonAdmin" : ['Developer','User'],
                                    
                                },
                                "sessionTimeout"  :sessionTimeout,
                            }
                        return f(request, *args, **kwargs,param=param)
                    return redirect('login')
            return redirect('login')
        return wrapped
    return mydecorator

allRoles = ['Admin', 'Developer','User']

@loginRequired(*allRoles)
def index(request,param):
    return HttpResponseRedirect(reverse('analyticsViews:insights'))


def error_404_view(request, exception):
    if 'user' in request.session:
        param = {
            'current_user' : request.session['user'],
            'userId' : request.session['userId'],
            'current_role' : request.session['role'],
            'orgId' : request.session['orgId'],
            'orgName' : request.session['orgName'],
            'group' : request.session['group'],
            'visibility' : {
                "allRoles" : ['Admin', 'Developer','User'],
                "admin" : ['Admin'],
                "adminDev" : ['Admin','Developer'],
                "nonAdmin" : ['Developer','User'],
                }
            }
    else :
        return redirect('login')
    return render(request,'404.html',param)

def login(request):
    # param = {}
    param = {"Lerror": False, "error": False}
    if request.method == 'POST':
        try:

            license_response = check_license_valid(request, param)
            if license_response.status_code != 200:
                param["Lerror"] = True
                return render(request, 'apps/users/auth-normal-sign-in.html',param)
            
            else:
                usr = request.POST.get('username','default')
                pwd = request.POST.get('password','default')            
                if not validation("username", usr):
                    raise ValueError("Username is not valid.")
                if not isValidPswd(pswd=pwd):
                    raise ValueError("Password not valid.")
                check_user = Users.objects.filter(username=usr)
                
                if check_user:
                    currentUser= check_user[0]
                    if (pwd==check_user[0].password ):
                        request.session['user'] = usr
                        request.session['userId'] = currentUser.id
                        request.session['role'] = currentUser.group_id.role
                        request.session['orgId'] = currentUser.group_id.organization_id.id
                        request.session['orgName'] = currentUser.group_id.organization_id.name
                        request.session['group'] = currentUser.group_id.name
                        request.session['last_activity'] =  time.time()
                        return redirect('index')
                    else:
                        raise ValueError("Password not matching.")
                else:
                    raise ValueError("Username does not exist.")
        except ValueError as e:
            param["error"] = True
        except Exception as e:
            param["error"] = True
            param["Lerror"] = True
        
    return render(request, 'apps/users/auth-normal-sign-in.html',param)

def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('login')
    return redirect('login')

@loginRequired(*allRoles)
def register(request,param):
    submittedData= {}
    if request.method=="POST":
        errors = []
        
        try:
            fname= request.POST.get('fname')
            lname= request.POST.get('lname')
            group= request.POST.get('group')
            username= request.POST.get('username')
            email= request.POST.get('email')
            password= request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            submittedData = {
                'fname': { "default" : fname},
                'lname': { "default" : lname},
                'group': { "default" : group},
                'username': { "default" : username},
                'email': { "default" : email},
                'password': { "default" : password},
                'cpassword': { "default" : cpassword}
            }
            
            validations = [
                ['fname', validation('name', fname)],
                ['lname', validation('name', lname)],
                ['username', validation('username', username)],
                ['email', validation('email', email)],
                ['password', isValidPswd(password)]
            ]
            flag= False
            for i in validations:
                if not i[1] :
                    flag= True
                    submittedData[i[0]]['error'] = True
            
            if  cpassword!= password:
                flag= True
                submittedData["cpassword"]['error'] = True

            if Users.objects.filter(username=username)  :
                print(Users.objects.filter(username=username), Users.objects.filter(username=username) !=None)
                errors.append("This username is taken.")
                flag= True
            
            if  Users.objects.filter(email=email) :
                print(Users.objects.filter(email=email) ,Users.objects.filter(email=email) !=None )
                errors.append("User with this email already exists.")
                flag= True
            if flag== True:
                raise Exception()
            
            g= Group.objects.filter(id=group)[0]
            u= Users(firstname=fname, lastname= lname, group_id=g, username=username, password=password,email=email)
            u.save()
            messages.success(request,"Added user.")
            param["otherdetails"] = "Added user with id : "+str(u.id)
            return render(request, 'apps/requests/requestMessage.html', param)
        except Exception as e:
            param['errors']= errors
    param['submittedData'] = submittedData        
    orgId = request.session["orgId"]
    org = Organization.objects.filter(id=orgId)[0]
    groups= Group.objects.filter(organization_id= org)
    groupDetails= []
    for i in groups:
        temp = {
            "id" : i.id,
            "name": i.name,
            "role": i.role
            }
        groupDetails.append(temp)
    param["groupDetails"] = groupDetails
    
    allOrgs = []
    allOrgObjs = Organization.objects.all()
    if allOrgObjs:
        for i in allOrgObjs:
            allOrgs.append(i.name)
    param['orgs'] = allOrgs    
    
    return render(request, 'apps/users/register.html',param)

@loginRequired(*allRoles)
def notifications(request,param):
    notifs = []
    try:
        jsonFileName = "notif1"
        with open('config.json') as f:
            config = json.load(f)
        path = config['loc']
        jsonFilePath =str(path)+f"analysis/notifications/{jsonFileName}.json"
        data= None
        with open(jsonFilePath,'r') as f:
                data= json.load(f)
        if type(data) == type(notifs) :
                notifs= data
    except Exception as E:
        print(E)

    paginate_count = 2
    page = request.GET.get('page', 1)
    paginator = Paginator(notifs, paginate_count)            
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    param['posts'] = posts
    return render(request, 'apps/users/notifications.html',param)


def validation(type,value):
    flag= False
    regex = {
        "email":r'^([A-Z|a-z|]{1})+([A-Z|a-z|0-9]{1,10}(\.|_){0,1})+[A-Z|a-z|0-9]\@([A-Z|a-z])+((\.){0,1}[A-Z|a-z]){2,15}\.[a-z]{2,3}$',
        "username": r"^([A-Za-z])([A-Za-z0-9]){4,19}",
        "name": r"^([A-Za-z])([a-z]){2,19}",
    }
    if type in regex:
        if re.fullmatch(regex[type], value)!=None:
            flag= True
    return flag


def isValidPswd(pswd):
    conditions = [
        len(pswd) <8 ,
        len(pswd) > 16,
        not re.search("[a-z]", pswd),
        not re.search("[A-Z]", pswd), 
        not re.search("[0-9]", pswd),
        not re.search("[_@$!&*]", pswd), 
        re.search("\s", pswd) 
    ]
    if any(conditions):
        return False
    return True


"""
    API VALIDATION
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
import datetime
import jwt
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions

@api_view(['GET'])
def profile(request):
    user = request.user
    serialized_user = UserSerializer(user).data
    return Response({'user': serialized_user })

@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def apiLogin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None): raise exceptions.AuthenticationFailed('username and password required')
    user = Users.objects.filter(username=username).first()
    if(user is None): raise exceptions.AuthenticationFailed('user not found')
    if user.password != password : raise exceptions.AuthenticationFailed('wrong password')
    serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }
    return response

def isJwtAuthenticated(func):
    @wraps(func)
    @ensure_csrf_cookie
    def authenticate(request,*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header: raise exceptions.AuthenticationFailed('Authorization header required.')
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode( access_token, settings.JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError: raise exceptions.AuthenticationFailed('Access Token expired')
        except IndexError: raise exceptions.AuthenticationFailed('Token prefix missing')
        
        user = Users.objects.filter(id=payload['user_id']).first()
        if user is None: raise exceptions.AuthenticationFailed('User not found')

        return func(request,*args, **kwargs)
    return authenticate

@api_view(['POST'])
@isJwtAuthenticated
def isLoggedIn(request):
    response = Response("Authentication working")
    return response

def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=0, minutes=settings.JWT_TOKEN_EXPIRY_MINS),
        'iat': datetime.datetime.now(datetime.timezone.utc),
    }
    access_token = jwt.encode(access_token_payload, settings.JWT_SECRET, algorithm='HS256')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7),
        'iat': datetime.datetime.now(datetime.timezone.utc)
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.JWT_SECRET, algorithm='HS256')
    return refresh_token
