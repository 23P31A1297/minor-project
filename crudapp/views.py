from django.shortcuts import render,redirect
from django.http import HttpResponse
from crudapp.models import student,register,profile,book
from crudapp.forms import Reg
from crudapp.forms import ProfileForm
from django.core.mail import EmailMultiAlternatives, send_mail
from crudproject import settings
from crudapp.forms import Book
from crudapp.forms import registrationform
from django.contrib.auth import authenticate
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


# Create your views here.
def create(request):
    if request.method=="POST":
       na=request.POST['uname']
       roll=request.POST['rnm']
       ag=request.POST['age']
       mb=request.POST['mbl']
       e=request.POST['em']
       add=request.POST['addr']

       student.objects.create(name=na,rollno=roll,age=ag,mobile=mb,email=e,adress=add)
       return HttpResponse("<h1> your data successfully submitted</h1>")
    return render(request,'create.html',{})
 
def read(request):
   data=book.objects.all()
   return render(request,'read.html',{'info':data})

def update(request,id):
   data=student.objects.get(id=id)
   if request.method=='POST':
      data.name=request.POST['uname']
      data.rollno=request.POST['rnm']
      data.age=request.POST['age']
      data.mobile=request.POST['mbl']
      data.email=request.POST['em']
      data.adress=request.POST['addr']
      data.save()
      return redirect('/read')
   return render(request,'update.html',{'data':data})

def delete(request,id):
   return render(request,'delete.html',{})

def reg(request):
   formdata=Reg()
   if request.method=='POST':
    formdata=Reg(request.POST)
   if formdata.is_valid():
       formdata.save()
       return HttpResponse("<h1> data submitted successfully </h1>")
   return render(request,'reg.html',{'data':formdata})

def display(request):
   data=register.objects.all()
   return render(request,'display.html',{'data':data})

def profile(request):
   form=ProfileForm()
   if request.method=='POST':
      form=ProfileForm(request.POST,request.FILES)
      if form.is_valid():
         form.save()
         return HttpResponse("<h1> image uploaded successfully</h1>")
   return render(request,'profile.html',{'f':form})

def data(request):
   data=profile.objects.all()
   return render(request,'data.html',{'info':data})

# def mail(request):
#    if request.method=='POST':
#       sndr=request.POST['sn']
#       sbj=request.POST['sb']
#       m=request.POST['msg']
#       t=settings.EMAIL_HOST_USER
#       res=send_mail(sbj,m,t,[sndr])
#       if res==1:
#          print("mail sent successfully")
#       else:
#          print("mail not sent")
#    return render(request,'mail.html',{})

def mail(request):
    if request.method == 'POST':
        # Read form fields safely
        sndr = request.POST.get('sn', '').strip()
        sbj = request.POST.get('sb', '').strip() or 'No subject'
        m = request.POST.get('msg', '').strip()

        if not sndr:
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'mail.html')

        # from address configured in settings
        from_addr = getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER)

        # Plain text + optional HTML
        text_content = m or "No message provided."
        html_content = f"<p>{m.replace(chr(10), '<br>')}</p>"  # simple conversion

        try:
            # Option A: simple send_mail (plain text)
            # res = send_mail(sbj, text_content, from_addr, [sndr]) 

            # Option B: HTML + plain text (recommended)
            msg = EmailMultiAlternatives(sbj, text_content, from_addr, [sndr])
            msg.attach_alternative(html_content, "text/html")
            res = msg.send()  # returns number of emails sent

            if res:
                messages.success(request, "Mail sent successfully to %s" % sndr)
                logger.info("Mail sent to %s (subject=%s)", sndr, sbj)
            else:
                messages.error(request, "Mail not sent. No recipients accepted by SMTP server.")
                logger.warning("send() returned 0 for recipient %s", sndr)

        except Exception as e:
            # Log exception and show friendly error to user
            logger.exception("Failed to send mail to %s", sndr)
            messages.error(request, f"Failed to send email: {e}")

        # After POST, re-render or redirect (POST-redirect-GET prevents double submit)
        return redirect('mail')  # or render with context

    # GET
    return render(request, 'mail.html', {})

def home(request):
   return render(request,'home.html',{})

def about(request):
   return render(request,'about.html',{})

def contact(request):
   return render(request,'contact.html',{})

def slot(request):
   ba=Book()
   if request.method=='POST':
      ba=Book(request.POST)
   if ba.is_valid():
      ba.save()
      return HttpResponse("<h1> data submitted successfully </h1>")
   return render(request,'slot.html',{'data':ba})

def register(request):
   form=registrationform()
   if request.method=="POST":
      form=registrationform(request.POST)
      if form.is_valid():
         form.save()
         return HttpResponse("<h2> user created successfully</h2>")
   return render(request,'register.html',{'form':form})

def login(request):
   if request.method=="POST":
      username=request.POST['uname']
      password=request.POST['psw']
      u=authenticate(username=username,password=password)
      if u:
         return redirect('read')
      else:
         return HttpResponse("<h2> invalid credentials</h2>")
   return render(request,'login.html',{})