from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .models import Task
from .serializers import TaskSerializer
import hashlib
# Create your views here.

        

def sign(request):
    if request.method=='POST':
        objects=Task.objects.all()
        serializer=TaskSerializer(objects,many=True)
        first=request.POST.get('first_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        last=request.POST.get('last_name')
        try:
            hash_password = hashlib.md5(password.encode()).hexdigest()
        except:
            hash_password=''
        if last==first==password==None and email!=None:
            for obj in objects:
                if obj.email==email:
                    return JsonResponse({'user_id':email,'login_type':'signin'},safe=False)
            return  JsonResponse({'user_id':'Not Registered','login_type':'signup'},safe=False)

        if None not in [first,last,email,password]:
            for obj in objects:
                if obj.email==email:
                    return  JsonResponse({'message':'Create user failed, User already exist'})
            task=Task(first=first,email=email,password=hash_password,last=last)
            task.save()
            return JsonResponse({'message':'New User registered'})
        if email!=None and password!=None:
            for obj in objects:
                if obj.email==email:
                    if obj.password==hash_password:
                        return  JsonResponse({'message':'Login Sucessfull'})
                    else:
                        return JsonResponse({'message':'Login Failed'})
            return  JsonResponse({'message':'User Not Registered'})
    return HttpResponse('This is Sign Page')



def add(request):
    if request.method=='POST':
        email=request.POST.get('email')
        category=request.POST.get('category')
        try:
            obj=Task.objects.get(email=email)
            category=category.lower()
            if category in obj.favourite:
                return JsonResponse({'message':'Category Already exist in user favourites'})
            else:
                if obj.favourite=='':
                    obj.favourite=' '+category
                else:
                    obj.favourite+=', '+category
                obj.save()
                return JsonResponse({'message':'Category added in user favourites'})
        except:
            return JsonResponse({'message':'User does not exist'})
        
            
           

def delete(request):
    if request.method=='POST':
        email=request.POST.get('email')
        category=request.POST.get('category')
        try:
            obj=Task.objects.get(email=email)
        except:
            return JsonResponse({'message':'User dose not exist'})
        category=' '+category.lower()
        if category not in obj.favourite:
            return JsonResponse({'message':'Category does not exist in user favourites'})
        else:
            favourite=obj.favourite.split(',')
            favourite.remove(category)
            obj.favourite=','.join(favourite)
            obj.save()
            return JsonResponse({'message':'Category deleted from user favourites'})
        

def show(request):
    if request.method=='POST':
        email=request.POST.get('email')
        try:
            obj=Task.objects.get(email=email)
            favourite=obj.favourite.split(',')
            return JsonResponse({'first_name':obj.first,'last_name':obj.last,'email':email,'favourite':[fav[1:] for fav in favourite]})

        except:
            return JsonResponse({'message':'User dose not exist'})
    return JsonResponse({'message':'incorrect request'})

        