from django import views
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [path("top/", TemplateView.as_view())]
