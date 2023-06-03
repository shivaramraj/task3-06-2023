from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from app.forms import *
from django.views.generic import DetailView
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required




def register(request):
    d={'UFO':UserForm()}
    if request.method=='POST':
        UFD=UserForm(request.POST)
        if UFD.is_valid():
            NSUFO=UFD.save(commit=False)
            password=UFD.cleaned_data['password']
            NSUFO.set_password(password)
            NSUFO.save()
            # send_mail('registration process','your registration is sucessful',
            #           'shivaramraj8804@gmail.com',[NSUFO.email],
            #           fail_silently=False)
            
            return HttpResponse('Registered sucessfully')
        else:
            return HttpResponse('data is in valid')

    return render(request,'register.html',d)


def home(request):
    if request.session.get('username'):
        QO=Question.objects.all()
        username=request.session.get('username')
        d={'username':username,'questions':QO}
        return render(request,'home.html',d)
    return render(request,'home.html')


def login_user(request):
    if request.method=='POST':
        username=request.POST['user']
        password=request.POST['password']
        AO=authenticate(username=username,password=password)
        if AO and AO.is_active:
            login(request,AO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid user credentials')
    return render(request,'login.html')
@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def questions(request):
    d={'QFO':QuestionForm()}
    if request.method=='POST':
        QD=QuestionForm(request.POST)
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        NSQO=QD.save(commit=False)
        NSQO.user=UO
        NSQO.save()
        return HttpResponse('Question uploded sucessfully')
    return render(request,'questions.html',d)

def displayquestions(request):
    QO=Question.objects.all()
    d={'QO':QO}
    return render(request,'displayquestios.html',d)

def insertanswer(request,pk):
    if request.method=='POST':
        QO=Question.objects.get(pk=pk)
        answer=request.POST['answer']
        username=request.session.get('username')
        userid=User.objects.get(username=username)
        answercreate=Answer.objects.get_or_create(user=userid,questions=QO,answers=answer)[0]
        answercreate.save()
        return HttpResponse('answer inserted sucessfully')
        
    return render(request,'insertanswer.html')

class Detail_answers(DetailView):
    model=Answer
    template_name='detail_answer.html'