from django.contrib import admin
from django.urls import path
from home import views
from .views import run_face_recognition_view
admin.site.site_header = "Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome"
urlpatterns = [
    path("",views.index, name='home'),
    path("about",views.about, name='about') ,#if /about in URL then the code redirects to views.about function 
    path("services",views.services, name='services'), # This is URL Dispatching
    path("contact",views.contact, name='contact'),
    path('upload/', views.upload_photo_page, name='upload_photo_page'),
    path('run_code/', run_face_recognition_view, name='run_code'),
    path('view-attendance/', views.view_attendance, name='view_attendance')
]  