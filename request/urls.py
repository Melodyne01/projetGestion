from django.urls import path
from . import views

urlpatterns = [
    path('add', views.addRequest, name='addRequest'),
    path('<int:id>', views.request_detail_view, name='request'),
    path('deleteConfirmation/<int:id>',views.deleteRequestConfirmation, name="deleteRequestConfirmation"),
    path('delete/<int:id>',views.deleteRequest, name="deleteRequest"),
    path('', views.requests, name='requests'),

]