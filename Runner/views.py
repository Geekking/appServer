# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import Http404
from django.utils import simplejson
from models import Runner
# Create your views here.


def checkLogin(request):
    if 'user_id' in request.session.keys():
        return True
    return False

def login(request):
    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')
    else:
        username = request.POST['userName']
        pwd = request.POST['password']
        try:
            user = Runner.objects.get(userName=username)
            if pwd != user.password:
                json = {'code':152,
                    'phase':'password not match'}
                return HttpResponse(simplejson.dumps(json,ensure_ascii = False))
            else:
                json = {'code':150,
                        'phase':'login success'
                        }
                request.session['user_id'] = user.id
                return HttpResponse(simplejson.dumps(json,ensure_ascii = False))
    
        except Runner.DoesNotExist:
            json = {'code':151,
                    'phase':'user not exists!'}
            return HttpResponse(simplejson.dumps(json,ensure_ascii = False))
            
        
            
def registe(request):
    if request.method != 'POST':
        #raise Http404('Only POSTs are allowed')
        return render_to_response('account/login.html',{'title':'login'})
    else:
        if checkLogin(request):
            json = {'code':102,
                    'phase':'user already loggin, please logout'}
            return HttpResponse(simplejson.dumps(json, ensure_ascii = False))
        else:
            userName = request.POST['userName']
            password = request.POST['password']
            phoneNum = request.POST['phoneNum']
            weight   = request.POST['weight']
            height   = request.POST['height']
            try:
                user = Runner.objects.get(userName = userName)
                json = {'code':101,
                        'phase':'user already exist'
                        }
                return HttpResponse(simplejson.dumps(json,ensure_ascii = False ))
        
            except Runner.DoesNotExist:
                user = Runner(userName = userName,password = password,phoneNum = phoneNum,weight = weight,height = height)
                user.save()
                json = {'code':100,
                        'phase':'registe success'}
                return HttpResponse(simplejson.dumps(json,ensure_ascii = False))
                
            
def logout(request):
    if request.method != 'POST':
        raise Http404('Only POST are allowed')
    else:
        if checkLogin(request):
            try:
                del request.session['user_id']
            except KeyError:
                pass
            json = {'code':180,
                    'phase':'logout success'}
            return HttpResponse(simplejson.dumps(json,ensure_ascii = False))
        else:
            json = {'code':180,
                    'phase':' you did not login'}
            return HttpResponse(simplejson.dumps(json,ensure_ascii = False))
            
         
def resetPassword(request):
    pass

def getNearShakingRunner(request):
    if request.method == 'GET':
        print 'post'
        userlist = [{
                     'userName':'testT',
                    'userLocation':'(127,110)',
                    'distance':100
                     },
                    {
                     'userName':'我是花无缺',
                    'userLocation':'(127,110)',
                    'distance':100
                     }]
        json = {
            'code': 200,
            'phase':'near user found',
            'userlist':userlist}
        
        return HttpResponse(simplejson.dumps(json,ensure_ascii=False))
        

def getMyDiet(request):
    pass

def pushMyDiet(request):
    pass
