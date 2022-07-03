import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import FileUpload
from django.conf import settings
from django.http import HttpResponse, Http404

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username):
            messages.error(request, "username already exist!")
            return redirect('signup')
        if User.objects.filter(email=email):
            messages.error(request, "email already exist!")
            return redirect('signup')
        if not username.isalnum:
            messages.error(request, 'username incorrect')
            return redirect('signup')
        if password1 != password2:
            messages.error(request, "password didn't match")
            return redirect('signup')
        
        newUser = User.objects.create_user(username, email, password1)
        newUser.first_name = firstName
        newUser.last_name = lastName
        newUser.save()
        messages.success(request, "Your account has been created")
        return redirect('signin')
    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            messages.error(request, "Wrong Credentials!")
            return redirect('signin')
    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    return redirect('home')

def list(request):
    if request.method == 'POST':
        print(request.FILES['filee'])
        _, file_extension = str(request.FILES['filee']).split('.')
        newFile = FileUpload(
            user=request.user, file=request.FILES['filee'], file_type=file_extension)
        newFile.save()
        return redirect('list')
    documents = FileUpload.objects.filter(user=request.user.id)
    return render(request, 'authentication/index.html', context={'documents': documents})


def download(request, pk):
    fileUpload = FileUpload.objects.get(id=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, fileUpload.file.path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404

def home(request):
    context = {
        'total_users': getTotalUsers(),
        'total_files': getTotalFiles(),
        'file_types': getFileTypes(),
        'users': getUsers(),
    }
    return render(request, "authentication/home.html", context=context)

#Utilities Method
def getTotalUsers():
    return User.objects.count()

def getTotalFiles():
    return FileUpload.objects.count()

def getFileTypes():
    fileTypes = []
    file_types = FileUpload.objects.values_list(
        'file_type', flat=True).distinct()
    for type in file_types:
        total = FileUpload.objects.filter(file_type=type).count()
        fileTypes.append({'name': type, 'total_files': total})
    return fileTypes

def getUsers():
    users = []
    for user in User.objects.all():
        users.append({"username": user.username,
                     "total_files": user.files.count()})
    return users