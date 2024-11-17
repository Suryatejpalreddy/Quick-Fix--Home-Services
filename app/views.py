from django.shortcuts import render,redirect
from django.contrib import messages
from . models import *
from django.db.models import Q
import random
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def userlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        data = UsersModel.objects.filter(email=email, password=password).exists()
        if data:
            request.session['email']=email
            request.session['login']='user'
            return redirect('home')
        else:
            messages.success(request, 'Invalid Email or Password')
            return redirect('userlogin')
    return render(request, 'userlogin.html')

def userregister(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        dob = request.POST['dob']
        gender = request.POST['gender']
        contact = request.POST['contact']
        address = request.POST['address']
        profile = request.FILES['profile']
        
       
        data = UsersModel.objects.filter(email=email).exists()
        if data:
            messages.success(request, 'Email already existed')
            return redirect('userregister')
        else:
            UsersModel.objects.create(name=name, email=email, password=password, dob=dob, gender=
                                      gender, contact=contact, address=address, profile=profile).save()
            messages.success(request, 'Registration Successfull')
            return redirect('userregister')
    return render(request, 'userregister.html')

def technicianlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if TechnicianModel.objects.filter(email=email,status='pending').exists():
            messages.error(request, 'Admin Not Accepted Your Registration')
            return redirect('login')
        data = TechnicianModel.objects.filter(email=email, password=password).exists()
        if data:
            request.session['email']=email
            request.session['login']='tech'
            return redirect('home')
        else:
            messages.success(request, 'Invalid Email or Password')
            return redirect('technicianlogin')
    return render(request, 'technicianlogin.html')

def technicianregister(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        dob = request.POST['dob']
        gender = request.POST['gender']
        contact = request.POST['contact']
        address = request.POST['address']
        profile = request.FILES['profile']
        amount = request.POST['amount']
        techrole = request.POST['techrole']
        data = TechnicianModel.objects.filter(email=email).exists()
        if data:
            messages.success(request, 'Email already existed')
            return redirect('technicianregister')
        else:
            TechnicianModel.objects.create(name=name, email=email, password=password, dob=dob, gender=
                                      gender, contact=contact, address=address, profile=profile,amount=amount,techrole=techrole).save()
            messages.success(request, 'Registration Successfull')
            return redirect('technicianregister')
    return render(request, 'technicianregister.html')

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        if email == 'admin@gmail.com' and password == 'admin':
            request.session['login'] = 'admin'
            request.session['email'] = 'admin@gmail.com'
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('adminlogin')
    return render(request, 'adminlogin.html')

def home(request):
    login = request.session['login']
    data = TechnicianModel.objects.all()[:6]
    return render(request, 'home.html', {'login':login,'data':data})

def logout(request):
    del request.session['login']
    del request.session['email']
    return redirect('index')


def viewusers(request):
    users = UsersModel.objects.all()
    login =request.session['login']
    return render(request, 'viewusers.html',{'data':users,'login':login})

def authorize(request,id):
    users = TechnicianModel.objects.get(id=id)
    login =request.session['login']
    users.status='Authorized'
    users.save()
    messages.success(request, 'Technician Authorized Sucessfully!')
    return redirect('viewtech')

def unauthorize(request,id):
    users = TechnicianModel.objects.get(id=id)
    login =request.session['login']
    users.status='Un Authorized'
    users.save()
    messages.success(request, 'Technician Un Authorized Sucessfully!')
    return redirect('viewtech')

def viewtech(request):
    tech = TechnicianModel.objects.all()
    login =request.session['login']
    return render(request, 'viewtech.html',{'data':tech,'login':login})


def services(request):
    services = TechnicianModel.objects.filter(status='Authorized')
    login =request.session['login']
    return render(request, 'services.html',{'data':services,'login':login})


def profile(request):
    login =request.session['login']
    email = request.session['email']
    data = TechnicianModel.objects.filter(email=email)
    return render(request, 'profile.html',{'login':login, 'data':data})


def updateprofile(request):
    login =request.session['login']
    email = request.session['email']
    
    if request.method == 'POST':
        contact = request.POST['contact']
        address = request.POST['address']
        profile = request.FILES['profile']
        amount = request.POST['amount']
        data = TechnicianModel.objects.get(email=email)
        data.contact = contact
        data.address = address
        data.profile = profile
        data.amount = amount
        data.save()
        # messages.success(request, 'Profile Updated Sucessfully!')
        return redirect('profile')
    return render(request, 'updateprofile.html',{'login':login})


def viewservice(request,id):
    data = TechnicianModel.objects.filter(id=id)
    login =request.session['login']
   
    feedback = ServiceBookingModel.objects.filter(sid=id)
    return render(request, 'viewservice.html',{'login':login, 'data':data, 'feedback':feedback})


def search(request):
    login = request.session['login']
    if request.method == 'POST':
        address = request.POST['location']
        service = request.POST['service']
        data = TechnicianModel.objects.filter(address=address,techrole=service)
        return render(request, 'services.html',{'login':login, 'data':data})
    else:
        messages.success(request, 'No Data Found')
        return redirect('services')
    
def bookservice(request,id):
    email = request.session['email']
    req = TechnicianModel.objects.get(id=id)
    data =  UsersModel.objects.get(email=email)
    ServiceBookingModel.objects.create(
        useremail=email,
        sid=id,
        techemail=req.email,
        techrole=req.techrole,
        contact=data.contact,
        address=data.address,
        amount=req.amount,
        username=data.name,
        profile=req.profile
    ).save()
    messages.success(request, 'Service Request is sent to Technician')
    return redirect('viewbookings')

def viewbookings(request):
    
    login = request.session['login']
    email = request.session['email']
    data = ServiceBookingModel.objects.filter(useremail=email)
    
    return render(request, 'viewbookings.html',{'login':login, 'data':data})


def viewrequests(request):
    login = request.session['login']
    email = request.session['email']
    data = ServiceBookingModel.objects.filter(
    Q(techemail=email) &
    (Q(status='pending') | Q(status='Accepted'))
)
    return render(request, 'viewrequests.html',{'login':login, 'data':data})


def acceptrequest(request,id):
    data = ServiceBookingModel.objects.get(id=id)
    data.status='Accepted'
    data.save()
    messages.success(request, 'Request Accepted Successfully!')
    return redirect('viewrequests')

def rejectrequest(request,id):
    data = ServiceBookingModel.objects.get(id=id)
    data.status='Rejected'
    data.save()
    messages.success(request, 'Request Rejected Successfully!')
    return redirect('viewrequests')
    

def complete(request,id):
    data = ServiceBookingModel.objects.get(id=id)
    data.status='Completed'
    data.save()
    messages.success(request, 'Work Completed Successfully!')
    return redirect('viewrequests')

def history(request):
    login = request.session['login']
    email = request.session['email']
    status_filter = request.GET.get('status_filter', '')
    print(status_filter)
    if login == 'user':
        if status_filter:
            data = ServiceBookingModel.objects.filter(useremail=email,status=status_filter)
        else:
            data = ServiceBookingModel.objects.filter(useremail=email)
    elif login == 'tech':
        if status_filter:
            data = ServiceBookingModel.objects.filter(techemail=email,status=status_filter)
        else:
            data = ServiceBookingModel.objects.filter(techemail=email)
    else:
        if status_filter:
            data = ServiceBookingModel.objects.filter(status=status_filter)
        else:
            data = ServiceBookingModel.objects.all()
    return render(request, 'history.html',{'login':login, 'data':data})

def feedback(request, id):
    login = request.session['login']
   
    data = ServiceBookingModel.objects.get(id=id)
    if request.method == 'POST':
        feedback = request.POST.get('message')
        data.feedback=feedback
        data.save()
        
        messages.success(request, 'Feedback Sent Successfully!')
        return redirect('viewbookings')
    else:
        
        return render(request, 'feedback.html',{'data':data,'login':login,'name':data.username, 'id':id})


def contact(request):
    login = request.session['login']
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        data = ContactUsModel(name=name,email=email,contact=phone,message=message)
        data.save()
        messages.success(request, 'Message Sent Successfully!')
        return redirect('contact')
    return render(request, 'contact.html',{'login':login})


def contactform(request):
    login = request.session['login']
    data=ContactUsModel.objects.all()
    return render(request, 'contactform.html',{'login':login,'data':data})



def forgotpassword(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        otp = random.randint(10000,999999)
        if UsersModel.objects.filter(email=email).exists():
            data = UsersModel.objects.get(email=email)
            data.otp = otp
            data.save()
        elif TechnicianModel.objects.filter(email=email).exists():
            data = TechnicianModel.objects.get(email=email)
            data.otp = otp
            data.save()
        else:
            messages.success(request, 'Email not Existed')
            return redirect('forgotpassword')
    

        # email_subject = 'Reset Your Password'
        # email_message = f"""
        # Hello {data.email},

        # Welcome to Our Website!

        # Here are your account details:
        # Email: {data.email}
        # OTP: {otp}

        # Please keep this information safe.

        # Best regards,
        # Your Website Team
        # """

        # # Send the email
        # try:
        #     send_mail(
        #         email_subject,
        #         email_message,
        #         'alwaysmstpr@gmail.com',  # From email
        #         [data.email],  # Recipient email
        #         fail_silently=False  # Raise errors if sending fails
        #     )
        #     messages.success(request, 'OTP sent successfully!')
        # except Exception as e:
        messages.error(request, f'Your reset otp: {otp}')

        return redirect('resetpassword')


    return render(request, 'forgotpassword.html')






def resetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(type(otp))
        # data = OfficersModel.objects.get(email=email,otp=int(otp))
        # print(data.firstname)
        if password == confirm_password:
            if UsersModel.objects.filter(email=email).exists():
                data = UsersModel.objects.get(email=email)
                if data.otp == int(otp):
                    data.password = password
                    data.save()
                else:
                    messages.error(request, 'Invalid OTP!')
                    return redirect('resetpassword')
            elif TechnicianModel.objects.filter(email=email).exists():
                data = TechnicianModel.objects.get(email=email)
                if data.otp == int(otp):
                    data.password = password
                    data.save()
                else:
                    messages.error(request, 'Invalid OTP')
                    return redirect('resetpassword')
          
           
            messages.success(request, 'Password Reset Successfully!')
            return redirect('resetpassword')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('resetpassword')
    return render(request, 'resetpassword.html')
