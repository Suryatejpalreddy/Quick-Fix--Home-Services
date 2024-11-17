from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('userregister/', views.userregister, name='userregister'),
    path('technicianlogin/', views.technicianlogin, name='technicianlogin'),
    path('technicianregister/', views.technicianregister, name='technicianregister'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('viewusers/', views.viewusers, name='viewusers'),
    path('viewtech/', views.viewtech, name='viewtech'),
    path('authorize/<int:id>/', views.authorize, name='authorize'),
    path('unauthorize/<int:id>/', views.unauthorize, name='unauthorize'),
    path('services/', views.services, name='services'),
    path('profile/', views.profile, name='profile'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('viewservice/<int:id>/', views.viewservice, name='viewservice'),
    path('search/', views.search, name='search'),
    path('bookservice/<int:id>/', views.bookservice, name='bookservice'),
    path('viewbookings/', views.viewbookings, name='viewbookings'),
    path('viewrequests/', views.viewrequests, name='viewrequests'),
    path('acceptrequest/<int:id>/', views.acceptrequest, name='acceptrequest'),
    path('rejectrequest/<int:id>/', views.rejectrequest, name='rejectrequest'),
    path('complete/<int:id>/', views.complete, name='complete'),
    path('history/', views.history, name='history'),
    path('feedback/<int:id>/', views.feedback, name='feedback'),
    path('contact/', views.contact, name='contact'),
    path('contactform/', views.contactform, name='contactform'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    



]
