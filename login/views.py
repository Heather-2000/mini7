from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *


def login_page(request):
    return render(request, 'login/login_page.html')


def join_page(request):
    return render(request, 'login/join_page.html')


def logout(request):
    response = redirect('/')
    response.delete_cookie('login')
    return response


@csrf_exempt
def join_chk(request):
    result = 'success'
    try:
        _user = User()
        _user.id = request.POST['id']
        _user.pw = request.POST['pw']
        _user.save()
    except Exception as e:
        print(e)
        result = 'id overlap'
    context = {'result': result}
    return JsonResponse(context)


@csrf_exempt
def login_chk(request):
    if request.method == 'POST':
        result = 'success'
        _user = User.objects.filter(id=request.POST['id'], pw=request.POST['pw'])
        if not _user.exists():
            result = 'id or pw mistake'
            context = {'result': result}
            return JsonResponse(context, status=401)
        else:
            response = JsonResponse({'result': result})
            response.set_cookie('login', request.POST['id'], max_age=3600)
            request.user = request.POST['id']
            return response
    else:
        return JsonResponse({'result': 'invalid request method'}, status=400)
