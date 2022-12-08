from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserUpdateForm, AddFactionForm, EditProfile, LinkUserToFaction, AddChannel
from django.contrib.auth.models import User
from .models import Faction, Profile, Channel
from request.models import Request
from django.shortcuts import get_object_or_404
import datetime
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string
from django.conf import settings as conf_settings

#Home page
def home(request):
    #Get the list of registered users
    users = User.objects.all()
    #If list is empty
    if not users:
        #Create default superuser
        user = User.objects.create_user( "tanguy.baldewyns@gmail.com", password="aaaaaa", is_staff=True, is_superuser=True)
        user.save()

    return redirect('login')

@staff_member_required()
@login_required
def register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        form = UserUpdateForm(data)
        if form.is_valid():
            form.save()
            user = get_object_or_404(User, username=data['username'])
            randomPassword = User.objects.make_random_password()
            user.set_password(randomPassword)
            user.save()
            message = render_to_string("users/registerEmail.html",{
            'user': user.username,
            'password': randomPassword
        })
            send_mail(
                    'Welcome To Business & Decision Belgium',
                    message='text',
                    html_message=message,
                    recipient_list=[data['username']],
                    from_email=conf_settings.EMAIL_HOST_USER,
                    fail_silently=False,
                    )
            messages.success(request, 'Account created')
            return redirect('users')
    else:
        form = UserUpdateForm()    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST ,instance=request.user)

        if u_form.is_valid():
            u_form.save()
            
            messages.success(request, 'Account updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }
    return render(request, 'users/profile.html', context)

@staff_member_required()
@login_required
def users(request):
    users = User.objects.all()

    return render(request, 'users/users.html', {'users': users})

@staff_member_required()
@login_required 
def user_detail_view(request, id):
    
    data = get_object_or_404(User, pk=id)
    profile = get_object_or_404(Profile, user=data)
    requestFromUser = []
    if profile.factionRole == "Leader":
        requestFromUser = Request.objects.filter(faction=profile.faction).values()
    else:
        requestFromUser += Request.objects.filter(consultant=profile).values()
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=data)
        p_form = EditProfile(request.POST ,instance=profile)
        if form.is_valid() and p_form.is_valid():
            # update the existing `Band` in the database
            form.save()
            p_form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('users')
    else:
        form = UserUpdateForm(instance=data)
        p_form = EditProfile(instance=profile)
    
    context = {
        'data': data,
        'form': form,
        'p_form': p_form,
        'requestFromUser': requestFromUser 
    }

    return render(request, 'users/user.html', context)

@staff_member_required()
@login_required
def settings(request):
    factions = Faction.objects.all()
    profiles = Profile.objects.all()
    channels = Channel.objects.all()
    
    f_form = AddFactionForm()
    c_form = AddChannel()
    
    if request.method == "POST":
        if 'addChannel' in request.POST:
            c_form = AddChannel(request.POST)
            if c_form.is_valid():
                c_form.save()
                messages.success(request, 'Channel created')
                return redirect('settings')
        elif 'addFaction' in request.POST:
            f_form = AddFactionForm(request.POST)
            if f_form.is_valid():
                f_form.save()
                messages.success(request, 'Faction created')
                return redirect('settings')
    
    context = {
        'f_form': f_form,
        'c_form': c_form,
        'factions':factions,
        'profiles':profiles,
        'channels':channels
    }
    return render(request, 'users/settings.html', context)

@staff_member_required()
@login_required
def faction_detail_view(request, id):
    data = get_object_or_404(Faction, pk=id)

    if request.method == 'POST':
        form = AddFactionForm(request.POST, instance=data)
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            return redirect('settings')
    else:
        form = AddFactionForm(instance=data)
    context = {
        'form': form,
        'data':data
    }
    return render(request, 'users/faction.html', context)

@staff_member_required()
@login_required
def resetPassword(request, id):

    user = get_object_or_404(User, pk=id)
    randomPassword = User.objects.make_random_password()
    user.set_password(randomPassword)
    user.save()
    message = render_to_string("users/registerEmail.html",{
    'user': user.username,
    'password': randomPassword
    })

    send_mail(
        'Welcome To Business & Decision Belgium',
        message='text',
        html_message=message,
        recipient_list=[user.username],
        from_email=conf_settings.EMAIL_HOST_USER,
        fail_silently=False,
    )

    return redirect('user', id=user.id)

@staff_member_required()
@login_required
def deleteUserConfirmation(request, id):

    user = User.objects.get(pk=id)
    return render(request, 'users/deleteUserConfirmation.html', {'user': user})

@staff_member_required()
@login_required
def deleteUser(request, id):

    userToDelete = User.objects.get(pk=id)
    userToDelete.delete()

    return redirect('users')


@staff_member_required()
@login_required
def deleteChannelConfirmation(request, id):

    channel = Channel.objects.get(pk=id)
    return render(request, 'users/deleteChannelConfirmation.html', {'channel': channel})
    
@staff_member_required()
@login_required
def deleteChannel(request, id):

    channelToDelete = Channel.objects.get(pk=id)
    channelToDelete.delete()

    return redirect('settings')

@staff_member_required()
@login_required
def deleteFactionConfirmation(request, id):

    faction = Faction.objects.get(pk=id)
    return render(request, 'users/deleteFactionConfirmation.html', {'faction': faction})
    
@staff_member_required()
@login_required
def deleteFaction(request, id):

    factionToDelete = Faction.objects.get(pk=id)
    factionToDelete.delete()

    return redirect('settings')