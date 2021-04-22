from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *
from django.db.models import Sum



def index(request):
    return render(request, "index.html")

# def create_user(request):
#     if request.method == "POST":
#         errors = User.objects.create_validator(request.POST)
#         if len(errors) > 0:
#             for key, value in errors.items():
#                 messages.error(request, value)
#             return redirect('/')
#         else:
#             password = request.POST['password']
#             pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
#             user = User.objects.create(name=request.POST['name'], email = request.POST['email'], password = pw_hash)
#             request.session['user_id'] = user.id
#             return redirect('/main')
#     return redirect('/')

    
# def login(request):
#     if request.method == "POST":
#         users_with_email = User.objects.filter(email = request.POST['email'])
#         if users_with_email:
#             user = users_with_email[0]
#             if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
#                 request.session['user_id'] = user.id
#                 return redirect('/main')
#         messages.error(request, "Email or password are not right")
#     return redirect('/')

# def logout(request):
#     print(request.session)
#     request.session.clear()
#     print(request.session)

def main(request):
    # if 'user_id' not in request.session:
    #     return redirect('/')
    all_therapists = Therapist.objects.all()
    all_clients = Client.objects.all()
    session_dict = {}
    evaluation_dict = {}
    noshow_dict = {}
    for therapist in all_therapists:
        sum_sessions = therapist.clients.all().aggregate(Sum('sessions'))
        session_dict[therapist.id] = sum_sessions['sessions__sum']
        sum_evaluations = therapist.clients.all().aggregate(Sum('evaluation'))
        evaluation_dict[therapist.id] = sum_evaluations['evaluation__sum']
        sum_noshows = therapist.clients.all().aggregate(Sum('noshow'))
        noshow_dict[therapist.id] = sum_noshows['noshow__sum']

    
    context ={
        'all_therapists' : Therapist.objects.all(),        
        'all_clients': Client.objects.all(),
        'session_dict': session_dict,
        'evaluation_dict': evaluation_dict,
        'noshow_dict': noshow_dict
        #'one_therapist': Therapist.objects.get(id=therapist_id),
        
    }
    return render(request, "main.html", context)

def add_therapist(request):
    return render(request, "add_therapist.html")

def create_therapist(request):
    # if 'user_id' not in request.session:
    #     return redirect('/')
    if request.method == "POST":
        errors = Therapist.objects.therapist_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/main')
        else:
            therapist = Therapist.objects.create(
            name=request.POST['name'], 
            hours=request.POST['hours'],
            wages= request.POST['wages'])
        return redirect('/main')
    return redirect('/main')

def add_client(request):
    context={        
        'all_therapists' : Therapist.objects.all()
        }
    # one_therapist = Therapist.objects.get(id = therapist_id)
    return render(request, "add_client.html", context)


def create_client(request):
    # if 'user_id' not in request.session:
        # return redirect('/')
    if request.method == "POST":
        errors = Client.objects.client_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/main')
        else:
            therapist_id = request.POST['therapist_who_treats']
            client = Client.objects.create(
            name=request.POST['name'], 
            sessions=request.POST['sessions'],
            evaluation = request.POST['evaluation'],
            no_show = request.POST['no_show'],              
            insurance_amt = request.POST['insurance_amt'],
            copay = request.POST['copay'],
            total_charges = request.POST['total_charges'])
            client.therapists.add(therapist_id)
            return redirect('/main')
            
    return redirect('/main')

def edit_therapist(request, therapist_id):
    context={
        'one_therapist':Therapist.objects.get(id=therapist_id),
        'all_therapists' : Therapist.objects.all()
    }
    return render(request, 'edit_therapist.html', context)

def update_therapist(request, therapist_id):
    if request.method =="POST":
        # therapist_id = Therapist.objects.get(id=therapist_id)
        errors = Therapist.objects.therapist_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/therapists/{therapist_id}/edit_therapist')
            
        else:
            # therapist_id = request.POST[therapist_id]
            therapist_to_update = Therapist.objects.get(id=therapist_id)
            therapist_to_update.name = request.POST['name']
            therapist_to_update.wages = request.POST['wages']
            therapist_to_update.hours = request.POST['hours']
            therapist_to_update.save()
            return redirect(f'/therapists/{therapist_id}/edit_therapist')
    return redirect( '/')

def edit_client(request, client_id):
    context={
        'one_client': Client.objects.get(id =client_id),
        'all_clients' : Client.objects.all()
    }

    return render(request, 'edit_client.html', context)

def update_client(request, client_id):
    # if 'user_id' not in request.session:
    #     return redirect('/')
    if request.method == "POST":
        
        errors = Client.objects.client_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit_client')
        else:
            therapist_id = request.POST['therapist_who_treats']
            client_id = request.POST['id']
            client_to_update = Client.objects.get(id = client_id)
            client_to_update.name=request.POST['name'], 
            client_to_update.sessions=request.POST['sessions'],
            client_to_update.evaluation = request.POST['evaluation'],
            client_to_update.no_show = request.POST['no_show'], 
            client_to_update.therapist_who_treats=request.POST['one_therapist'],                
            client_to_update.insurance_amt = request.POST['insurance_amt'],
            client_to_update.copay = request.POST['copay'],
            client_to_update.total_charges = request.POST['total_charges']
            client_to_update.save()
            
            return redirect('/edit_client')
    return redirect('/main')


def show_therapist(request, therapist_id):

    # if 'user_id' not in request.session:
    #     return redirect('/')
    # client_id = request.POST['clients']
    # one_client = Client.objects.get(id = client_id)    
    copay = Client.objects.aggregate(Sum('insurance_amt'))['insurance_amt__sum']
    insurance_amt = Client.objects.aggregate(Sum('copay'))['copay__sum']
    context = {
        'clients':insurance_amt,
        'total':copay,
        # 'revenue':amount_received
    }
    # client_id = request.POST['one_client']
    one_therapist = Therapist(id = therapist_id)
    context = {
        'one_therapist': Therapist.objects.get(id=therapist_id),
        'all_therapists' : Therapist.objects.all(),
        'all_clients' : Client.objects.all(),
        # 'one_client': Client.objects.get(id=client_id)
    }
    return render(request, 'about_therapist.html', context)
    

def show_client(request, client_id):
    # if 'user_id' not in request.session:
    #     return redirect('/')
    
    one_client = Client.objects.get(id=client_id)
    context = {
        'one_client': Client.objects.get(id=client_id),
        'all_clients' : Client.objects.all(),
        'all_therapists': Therapist.objects.all()
    }
    return render(request, 'about_client.html', context)

def delete_therapist(request, therapist_id):
    if request.method == "GET":
        context = {
            "one_therapist": Therapist.objects.get(id=therapist_id)
        }
        return render(request,'delete_therapist.html', context)
    if request.method == "POST":
        therapist_to_delete = Therapist.objects.get(id=therapist_id)
        therapist_to_delete.delete()
        print("Therapist successfully deleted")
    
    return render( request, "delete_therapist.html")

def delete_client(request, client_id):
    if request.method == "GET":
        context = {
            "one_client": Client.objects.get(id=client_id)
        }
        return render(request,'delete_client.html', context)
    if request.method == "POST":
        client_to_delete = Client.objects.get(id=client_id)
        client_to_delete.delete()

        print("Client successfully deleted")

    return render( request, "delete_client.html")