from django.urls import path
from .views import service_view, generate_excel ,test

urlpatterns = [
    path('', service_view, name='services'),  # صفحه خدمات
    path('ngram/', generate_excel, name='generate_excel'),  # صفحه ایجاد فایل اکسل
    path('test/',test,name='test')
]
