# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import Http404
from django.utils import simplejson
from models import Runner
import threading
import time
from hashlib import md5
# Create your views here.

request_list = []
mu = threading.Lock()

class ServerThread(threading.Thread):
    def get_Loc(self,loc_str):
        loc_str = loc_str.strip()[1:-1]
        (latitude,longtitude) = loc_str.split(',')
        return (float(latitude),float(longtitude))
    def get_key(self,loc_str):
        lat,lt = self.get_Loc(loc_str)
        
        loc_key = '' 
        return loc_key
    def response(self,request,nearRunners):
        nearRunnerList = []
        if len(nearRunners) > 0:
            #near user found
            nearUserCount = 0
            for runner_request in nearRunners:
                aRunner = {}
                user_id = runner_request.session['user_id']
                try:
                    user = Runner.objects.filter(id = user_id)
                    aRunner['userName'] = user.userName
                    aRunner['phoneNum'] = user.phoneNum
                    aRunner['userlocation'] = runner_request.POST['myLocation']
                    aRunner['distance'] = 100
                    nearRunnerList.append(aRunner)
                    nearUserCount += 1
                    if nearUserCount > 10:
                        break
                except:
                    continue
            json = {
                    'code':200,
                    'phase':'near user found',
                    'userlist':nearRunnerList}
            
        else:
            #handle no near user
            pass
    def handleRequest(self,request_list):
        locationHash = {}
        for request in request_list:
            loc_str = request.POST['myLocation']
            loc_key = self.get_key(loc_str)
            if loc_key not in locationHash.keys():
                locationHash[loc_key] = []
            locationHash[loc_key].append(request)
        for request in request_list:
            loc_str = request.POST['myLocation']
            loc_key = self.get_key(loc_str)
            self.response(request, locationHash[loc_key])
            
    def run(self):
        global request_list
        while(True):
            time.sleep(60)
            if mu.accquire():
                self.handleRequest(request_list)
                mu.release()

#instanlized
serverThread = ServerThread()

def checkLogin(request):
    if 'user_id' in request.session.keys():
        return True
    return False

def login(request):
    if request.method != 'POST':
        return render_to_response('account/login.html',{'title':'login'})    
        #raise Http404('Only POSTs are allowed')
    else:
        username = request.POST['userName']
        pwd = request.POST['password']
        pwd = md5(pwd).hexdigest()
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
        return render_to_response('account/registe.html',{'title':'registe'})
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
            password = md5(password).hexdigest()
            
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
        return render_to_response('account/logout.html',{'title':'log out'})
        #raise Http404('Only POST are allowed')
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
    if checkLogin(request) == False:
        #raise Http404('Please login')
        return render_to_response('account/login.html',{'title':'login'})
    if request.method == 'GET':
        return render_to_response('nearShakingRunner.html',{'title':'get near shaking runners'})
    if request.method == 'POST':
        if mu.accquire():
            request_list.append(request)
            mu.release()
        #print 'post'
#         userlist = [{
#                      'userName':'testT',
#                     'userLocation':'(127,110)',
#                     'distance':100
#                      },
#                     {
#                      'userName':'我是花无缺',
#                     'userLocation':'(127,110)',
#                     'distance':100
#                      }]
#         json = {
#             'code': 200,
#             'phase':'near user found',
#             'userlist':userlist}
#         
#         return HttpResponse(simplejson.dumps(json,ensure_ascii=False))
        

def getMyDiet(request):
    pass

def pushMyDiet(request):
    pass
