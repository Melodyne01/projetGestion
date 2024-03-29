from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from .forms import RequestRegisration
from users.forms import AddChannel
from .models import Request
from .filters import RequestFilter
from users.models import Channel
from users.models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string

@login_required
def requests(request):
    if request.user.is_staff or request.user.profile.isSaler:
        #get all Requests using filters (admin)
        filteredRequests = RequestFilter(request.GET, queryset=Request.objects.all())
    elif request.user.profile.factionRole == "Leader":
        #get factions Requests using filters (faction lead)
        filteredRequests = RequestFilter(request.GET, queryset=Request.objects.filter(faction=request.user.profile.faction))
    else:
        #get current user Requests using filters (consultant)
         filteredRequests = RequestFilter(request.GET, queryset=Request.objects.filter(consultant=request.user.profile))
    context = {
        'filteredRequestsFrom' : filteredRequests.form,
        'filteredRequests' : filteredRequests.qs,
    }

    return render(request, 'request/requests.html', context)

@login_required 
def request_detail_view(request, id):
    oldData = get_object_or_404(Request, pk=id)
    if request.method == 'POST':
        form = RequestRegisration(request.POST,request.FILES, instance=oldData)
        newData = request.POST.copy()
        if newData['faction']:
            requestFactionMembersConcerned = Profile.objects.filter(factionRole="Leader").filter(faction=newData['faction'])
        if form.is_valid():
            form.save()
            message = render_to_string("request/requestUptadedEmail.html",{
            'id': oldData.id,
            'user': request.user
        })
            #Send email to leaders
            if newData['faction']:
                for member in requestFactionMembersConcerned:
                    send_mail('Request N° '+str(id)+' assigned to your faction has been updated', message='text',html_message=message,recipient_list=[member.user.username], from_email=settings.EMAIL_HOST_USER, fail_silently=False,)
            #Send email to assigned consultant
            if newData['consultant']:
                assignedConsultant = get_object_or_404(User, pk=newData['consultant'])
                send_mail('Request N° '+str(id)+' assigned to you has been updated',message='text',html_message=message,recipient_list=[assignedConsultant.username],from_email=settings.EMAIL_HOST_USER,fail_silently=False,)
            return redirect('requests')
    else:
        form = RequestRegisration(instance=oldData)
    context = {
        'form': form,
        'data':oldData,
    }
    return render(request, 'request/request_detail.html', context)

@staff_member_required()
@login_required
def addRequest(request):
    requestFactionMembersConcerned = []
    if request.method == "POST":
        #Call the request regisrtration form
        form = RequestRegisration(request.POST)
        #Create a copy of the request to have access to the data into the form
        data = request.POST.copy()
        #If the request is assigned to one faction
        if data['faction']:
            requestFactionMembersConcerned = Profile.objects.filter(factionRole="Leader").filter(faction=data['faction'])
        if form.is_valid():
            #save the request
            form.save()
            #create the HTML template to send by email
            message = render_to_string("request/requestCreatedEmail.html",{
            'user': request.user
        })
            #Send email to leaders
            if data['faction']:
                #Send email to each faction leads
                for member in requestFactionMembersConcerned:
                    send_mail('One new request has been assigned to your faction',message='text',html_message=message,recipient_list=[member.user.username],from_email=settings.EMAIL_HOST_USER,fail_silently=False,)
            #Send email to assigned consultant
            if data['consultant']:
                assignedConsultant = get_object_or_404(User, pk=data['consultant'])
                send_mail(
                'One new request has been assigned to you',message='text',html_message=message,recipient_list=[assignedConsultant.username],from_email=settings.EMAIL_HOST_USER,fail_silently=False,)
            messages.success(request, 'Request created')
            return redirect('requests')
    else:
        form = RequestRegisration()  
    return render(request, 'request/addRequest.html', {'form': form})

@staff_member_required()
@login_required
def deleteRequestConfirmation(request, id):
    #redirect to the confirmation page
    return render(request, 'request/deleteRequestConfirmation.html', {'id': id})

@staff_member_required()
@login_required
def deleteRequest(request, id):
    #Delete the request selected
    requestsToDelete = Request.objects.get(pk=id)
    requestsToDelete.delete()

    return redirect('requests')

@staff_member_required()
@login_required
def channel_detail_view(request, id):
    data = get_object_or_404(Channel, pk=id)

    if request.method == 'POST':
        form = AddChannel(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = AddChannel(instance=data)
    context = {
        'form': form,
        'data':data
    }
    return render(request, 'users/channel.html', context)

