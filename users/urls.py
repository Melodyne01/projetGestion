from django.urls import path
from . import views

urlpatterns = [
    path('', views.users, name='users'),
    path('<int:id>', views.user_detail_view, name='user'),
    path('deleteConfirmation/<int:id>',views.deleteUserConfirmation, name="deleteUserConfirmation"),
    path('delete/user/<int:id>',views.deleteUser, name="deleteUser"),
    path('deleteFactionConfirmation/<int:id>',views.deleteFactionConfirmation, name="deleteFactionConfirmation"),
    path('delete/faction/<int:id>',views.deleteFaction, name="deleteFaction"),
    path('deleteChannelConfirmation/<int:id>',views.deleteChannelConfirmation, name="deleteChannelConfirmation"),
    path('delete/channel/<int:id>',views.deleteChannel, name="deleteChannel"),
    path('resetPassword/<int:id>',views.resetPassword, name="resetPassword"),
]