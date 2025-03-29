from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse 
from .models import Invite
from django.http import JsonResponse
import requests 
from .models import Invite, Oath, Table
from .forms import inviteForm, oathForm, tableForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

 #here's a home definition 
def home(request, invite_id):
    if request.user.is_superuser :
        return redirect ('scan_qr', invite_id=invite_id)
    else :
        invite = Invite.objects.get(id=invite_id)
        invites = Invite.objects.filter(id=invite_id)
        oaths = Oath.objects.filter(invite=invite_id)
        return render(request, 'index/home.html', {'invite':invite, 'oaths':oaths,'invites':invites})

#here's a error page
def error(request, exception=None):
    return render (request, 'error.html')


"""   
here's a whole processus for table field, add,table_id, edit  delete, and search
"""
#table list or page 
def table(request):
    tables = Table.objects.all()
    return render (request, 'table/tables.html', {'tables':tables})

#add
def table_form(request):
    if request.user.is_superuser :
        if request.method == 'POST':
            form = tableForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'table créée avec success')
                return redirect ('table')
            else :
                messages.error(request,'erreur sur le nom ou le numero ou les éléments inscrit sont déjà utilisé')
                return redirect (reverse('table_form'))
        else :
            form = tableForm()
        return render (request, 'table/table_form.html', {'form':form})
    else :
        return redirect ('error')

#table_id 
def table_detail(request, table_id):
    if request.user.is_superuser :
        table = get_object_or_404(Table, id=table_id)
        return render (request, 'table/table_detail.html', {'table':table})
    else :
        return redirect ('error')
    
#table_edit 
def table_edit(request, table_id):
    if request.user.is_superuser :
        table = get_object_or_404(Table, id=table_id)
        if request.method == 'POST':
            form = tableForm(request.POST, instance = table)
            if form.is_valid():
                form.save()
                return redirect ('table_detail', table_id=table.id)
            else :
                messages.error('aucune information disponible')
                return render ('table_form')
        else :
            form = tableForm(instance=table)
        return render (request, 'table/table_edit.html', {'form':form, 'table':table})
    else :
        return redirect ('error')   
#delete 
def table_delete(request, table_id):
    if request.user.is_superuser :
        table = get_object_or_404(Table, id=table_id)
        table.delete()
        return redirect ('table')
    else :
        return redirect ('error')
    
#seach a table
def table_search(request):
    if request.user.is_superuser:
        query = request.GET.get('q')
        resultats = []
        if query : 
            resultats = Table.objects.filter(Q(name__icontains=query)) |  Table.objects.filter(Q(number__icontains=query))
        return render (request, 'table/table_search.html', {'resultats':resultats, 'query':query})
    else :
        return redirect('error')
"""
here's a way to add an invite in your system, edit, search and delete 
"""   
#page for invite list and detail
def invite(request):
    if request.user.is_superuser:
        invites = Invite.objects.all().order_by('-created_at')
        sent = Invite.objects.filter(is_sent=False)
        scans = Invite.objects.filter(is_scan=True).order_by('-is_scan')
        return render (request, 'invites/invite.html', {'invites':invites, 'sent':sent, 'scans':scans})
    else :
        return redirect ('error')

# invite's form 
#invite modif 
def invite_form (request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = inviteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect ('invite')
        else : 
            form = inviteForm()
        return render (request, 'invites/invite_form.html', {'form':form})
    else :
        return redirect ('error')
#invite's detail
def invite_detail(request, invite_id):
    if request.user.is_superuser:
        invite = get_object_or_404(Invite, id=invite_id)
        return render (request, 'invites/invite_detail.html', {'invite':invite})
    else :
        return redirect ('error')

#invite modif 
def invite_edit (request, invite_id):
    if request.user.is_superuser:
        invite = get_object_or_404(Invite, id=invite_id)
        if request.method == 'POST':
            form = inviteForm(request.POST, instance=invite)
            if form.is_valid():
                form.save()
                return redirect ('invite_detail', invite_id=invite.id)
        else : 
            form = inviteForm(instance=invite)
        return render (request, 'invites/invite_edit.html', {'invite':invite, 'form':form})
    else :
        return redirect ('error')

#delete an invite file 
def invite_delete(request, invite_id):
    if request.user.is_superuser:
        invite = get_object_or_404(Invite, id=invite_id)
        return redirect ('invite')
    else :
        return redirect ('error')

#invite's search 
def invite_search(request):
    if request.user.is_superuser:
        query = request.GET.get('q')
        resultats = []
        results = []
        if query :
            resultats = Invite.objects.filter(Q(name__icontains=query)) | Invite.objects.filter(Q(last_name__icontains=query))  | Invite.objects.filter(Q(first_name__icontains=query))
            results = Invite.objects.filter(Q(name__icontains=query)).filter(is_sent=False) | Invite.objects.filter(Q(last_name__icontains=query)).filter(is_sent=False)  | Invite.objects.filter(Q(first_name__icontains=query)).filter(is_sent=False)
        return render (request, 'invites/invite_search.html', {'query':query, 'resultats':resultats, 'results':results})
    else :
        return redirect ('error')  

def invite_scan(request):
    if request.user.is_superuser : 
        invites = Invite.objects.filter(is_scan= True)
        return render (request, 'invites/invite_scan.html', {'invites':invites})
    else :
        return redirect('error')

def scan_invite(request, invite_id):
    invite = get_object_or_404(Invite, id=invite_id)
    whatsap_number = invite.whatsapp_num
    message =f"🎊 💑 Unis par l'amour, le couple TSHIMANGA KASONGO ALBERT & MWAYUMA NGONGO PRINCESS DEBORAH, \n"
    message +=f"Vous invites à célébrer le plus beau jour de leur vie. 🎉 🎊 \n\n\n"
    message +=    f" 🔔 🔔 Cliquer sur ce lien pour télécharger et consulter votre invitation unique : {f"https://weddingdeborah-b491437285b8.herokuapp.com/{invite.id}"}\n"
    import urllib.parse
    message_encoded = urllib.parse.quote(message)
    invite.is_sent = True
    invite.save()
    url = f"https://api.whatsapp.com/send?phone={whatsap_number}&text={message_encoded}"
    import webbrowser
    webbrowser.open(url)
    # Rediriger vers WhatsApp
    return redirect(url)


"""
here's the CRUD for Oath field
"""
# Oath page for list
@login_required(login_url='/account/login/')
def oath(request):
    oaths = Oath.objects.all().order_by('-created_at')
    return render (request,'oaths/oath.html', {'oaths':oaths})

@login_required
#Oath form's page
def oath_form(request):
    if request.method == 'POST':
        form = oathForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('oath')
    else :
        form = oathForm()
    return render (request, 'oath_form.html', {'form':form})

def oath_home_form(request, invite_id):
    invite = get_object_or_404(Invite, id=invite_id)
    if request.method == 'POST':
        form = oathForm(request.POST, )
        if form.is_valid():
            form.save()
            return redirect('home', invite_id=invite.id)
    else :
        form = oathForm()
    return render (request, 'index/home.html', {'form':form, 'invite':invite})


def oath_home_delete(request, invite_id, oath_id):
    oath = get_object_or_404(Oath, id=oath_id)
    invite = get_object_or_404(Invite, id=invite_id)
    oath.delete()
    return redirect (home, invite_id=invite.id)

#oath page for mofication field
def oath_edit(request, oath_id):
    oath = get_object_or_404(Oath, id=oath_id)
    if request.method == 'POST':
        form = oathForm(request.POST, instance=oath)
        if form.is_valid():
            form.save()
            return redirect('oath_detail', oath_id=oath.id)
    else :
            form = oathForm(instance=oath)
    return render (request, 'oaths/oath_edit.html', {'form':form, 'oath':oath})

    
#oath page for detail 
def oath_detail(request, oath_id):
    oath = get_object_or_404(Oath, id=oath_id)
    return render (request, 'oaths/oath_detail.html', {'oath':oath})
    
#oath page for delete the field
def oath_delete(request, oath_id):
    oath = get_object_or_404(Oath, id=oath_id)
    oath.delete()
    return redirect ('oath')

#oath's search page
def oath_search(request):
    query  = request.GET.get('q')
    resultats = []
    if query:
        resultats = Oath.objects.filter(Q(invite__name__icontains=query)) |  Oath.objects.filter(Q(invite__first_name__icontains=query))
    return render (request, 'oaths/oath_search.html', {'query':query, 'resultats':resultats})


#here's th parameters for profile
@login_required(login_url='/account/login/')
def profile(request):
    if request.user.is_superuser:
        invites = Invite.objects.all().order_by('-created_at')[:5]
        tables = Table.objects.all().order_by('-created_at')[:5]
        oaths = Oath.objects.all().order_by('-created_at')[:5]
        return render (request, 'profile/profile.html', { 'invites':invites, 'tables':tables, 'oaths':oaths})
    else :
        return redirect('error')
    
def scan(request):
    invite= Invite.objects.all()
    return render (request, 'qr_code/qr_code.html', {'invite':invite})
    
def scan_error(request, invite_id):
    invite = get_object_or_404(Invite, id=invite_id)
    return render (request, 'qr_code/scan_error.html', {'invite':invite})
def scan_qr(request, invite_id):
    if request.user.is_superuser:
        invite = get_object_or_404(Invite, id=invite_id)
        if invite.is_scan  :
            return redirect ('scan_error', invite_id=invite.id)

        else :
            invite.is_scan = True
            invite.save()
            return redirect('invite_detail', invite_id=invite.id)
    else :
        return redirect('home')

#THE WAY to desconnect the user 
def logout_view(request):
    logout(request)
    request.session.flush() 
    return redirect ('login')
