from .models import *
from .forms import *
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db.models import Q


def index(request):
    return render(request, 'index.html')


def logout(request):
    request.session.pop('username', None)
    return redirect('check_password')
    # https://stackoverflow.com/questions/44113178/deleting-session-variable-while-avoiding-keyerror-exception


def display_main_menu(request):
    print(request.user)
    if request.session.has_key('username'):
        return redirect('display_tickets')
    else:
        return redirect('check_password')


def display_users(request):
    if request.session.has_key('username'):
        username = request.session['username']
        if request.session['role'] == 2:
            searchedText = ""
            if request.method == 'POST':
                    form = FormSearchForUsers(request.POST)
                    if form.is_valid():
                        searchedText=form.cleaned_data['searchInput']

            context = {
                'username': username,
                'role': request.session['role'],
                'users': User.objects.filter(Q(userLogin__icontains=searchedText) |
                                             Q(userFirstName__icontains=searchedText) |
                                             Q(userLastName__icontains=searchedText) |
                                             Q(userID__icontains=searchedText)),
                'form': FormSearchForUsers,
            }
            return render(request, 'user_related/users.html', context)
        else:
            return redirect('display_tickets')
    else:
        return redirect('check_password')


def display_user_detail(request, user_id):
    if request.session.has_key('username'):
        username = request.session['username']
        if request.session['role'] == 2:

            profile_data = User.objects.get(userID=user_id)
            my_account = User.objects.get(userLogin=username)

            if my_account.userID==user_id:
                profile=True
            else:
                profile=False

            if request.method == 'POST':
                form1 = FormChangeUserInfo(request.POST)
                if form1.is_valid():
                    profile_data.userFirstName = form1.cleaned_data['userFirstName']
                    profile_data.userLastName = form1.cleaned_data['userLastName']
                    profile_data.userPhoneNumber = form1.cleaned_data['userPhoneNumber']
                    profile_data.save()

                form2 = FormChangeUserPassword(request.POST)
                if form2.is_valid():
                    if form2.cleaned_data['userPassword'] == form2.cleaned_data['userPasswordRepeat']:
                        profile_data.userPassword = form2.cleaned_data['userPassword']
                        profile_data.save()
                    else:
                        messages.info(request, 'Hasła są różne!')


                form3 = FormChangeUserInfoImp(request.POST)
                if form3.is_valid():
                    if check_for_similar_login(form3.cleaned_data['userLogin'],profile_data.userLogin) == True:
                        messages.info(request, 'Istnieje już użytkownik o takim loginie!')
                    else:
                        profile_data.userLogin = form3.cleaned_data['userLogin']
                        profile_data.userRole = form3.cleaned_data['userRole']
                        profile_data.save()


            context = {
                'my_profile': profile,
                'role': request.session['role'],
                'username': username,
                'form1': FormChangeUserInfo(initial={
                    'userFirstName': profile_data.userFirstName,
                    'userLastName': profile_data.userLastName,
                    'userPhoneNumber': profile_data.userPhoneNumber}),
                'form2': FormChangeUserPassword,
                'form3': FormChangeUserInfoImp(initial={
                    'userLogin':profile_data.userLogin,
                    'userRole': profile_data.userRole}),
            }
            return render(request, 'user_related/user_details.html', context)
        else:
            return redirect('display_tickets')
    else:
        return redirect('check_password')


def display_my_profile(request): #https://stackoverflow.com/questions/604266/django-set-default-form-values
    if request.session.has_key('username'):
        username = request.session['username']
        profile_data = User.objects.get(userLogin=username)

        if request.method == 'POST':
            form1 = FormChangeUserInfo(request.POST)
            if form1.is_valid():
                profile_data.userFirstName = form1.cleaned_data['userFirstName']
                profile_data.userLastName = form1.cleaned_data['userLastName']
                profile_data.userPhoneNumber = form1.cleaned_data['userPhoneNumber']
                profile_data.save()

            form2 = FormChangeUserPassword(request.POST)
            if form2.is_valid():
                if form2.cleaned_data['userPassword'] == form2.cleaned_data['userPasswordRepeat']:
                    profile_data.userPassword = form2.cleaned_data['userPassword']
                    profile_data.save()
                else:
                    messages.info(request, 'Hasła są różne!')


            form3 = FormChangeUserInfoImp(request.POST)
            if form3.is_valid():
                profile_data.userLogin = form3.cleaned_data['userLogin']
                profile_data.userRole = form3.cleaned_data['userRole']
                profile_data.save()

        context = {
            'my_profile': True,
            'role': request.session['role'],
            'username': username,
            'form1': FormChangeUserInfo(initial={
                'userFirstName': profile_data.userFirstName,
                'userLastName': profile_data.userLastName,
                'userPhoneNumber': profile_data.userPhoneNumber}),
            'form2': FormChangeUserPassword,
            'form3': FormChangeUserInfoImp(initial={
                'userLogin': profile_data.userLogin,
                'userRole': profile_data.userRole}),
        }
        return render(request, 'user_related/user_details.html', context)
    else:
        return redirect('check_password')


def display_ticket_detail(request, ticket_id):
    if request.session.has_key('username'):
        username = request.session['username']
        if request.method == 'POST':
                form = FormAddComent(request.POST)
                if form.is_valid():
                    logged_in_user = User.objects.get(userLogin=username)
                    comment_ticket_id = Ticket.objects.get(ticketID=ticket_id)
                    new_comment = Comment(commentCreator=logged_in_user,
                                          commentTicket=comment_ticket_id,
                                          commentDescription=form.cleaned_data['commentContent'])
                    new_comment.save()

        context = {
            'admins': User.objects.filter(userRole=2),
            'role': request.session['role'],
            'username': username,
            'ticket_detail': Ticket.objects.select_related('ticketCreator', 'ticketTechnician').filter(ticketID=ticket_id),
            'form': FormAddComent,
            'ticket_comments': Comment.objects.select_related('commentCreator').filter(commentTicket=ticket_id),
        }
        return render(request, 'ticket_related/ticket_detail.html', context)
    else:
        return redirect('check_password')


def check_password(request):
    if request.method == 'POST':
        form = FormCheckPassword(request.POST)
        if form.is_valid():
            input_username = form.cleaned_data['form_login']
            input_password = form.cleaned_data['form_password']
            try:
                logged_in_user = User.objects.get(userLogin=input_username)
                if logged_in_user.userRole == 0:
                    messages.info(request, 'Brak dostępu do konta')
                else:
                    if logged_in_user.userPassword == input_password:
                        request.session['username'] = input_username
                        request.session['role'] = logged_in_user.userRole
                        return redirect('display_main_menu')  # Redirect to a success page.
                    else:
                        messages.info(request, 'Niewłaściwy login lub hasło')
            except:
                    messages.info(request, 'Niewłaściwy login lub hasło')
    return render(request, 'logging.html', {'form': FormCheckPassword()})


def encrypting_password(raw_password):
    encrypted_password = make_password(raw_password)
    return encrypted_password


def create_ticket(request):
    if request.session.has_key('username'):
        username = request.session['username']

        if request.method == 'POST':
            form = FormCreateTicket(request.POST)
            if form.is_valid():
                logged_in_user = User.objects.get(userLogin=username)
                new_ticket = Ticket(ticketCreator=logged_in_user,
                                    ticketTitle=form.cleaned_data['ticketTitle'],
                                    ticketDescription=form.cleaned_data['ticketDescription'])
                new_ticket.save()
                return redirect('display_tickets')
        return render(request, 'ticket_related/create_ticket.html', {"username": username, 'form': FormCreateTicket, 'role': request.session['role'],})
    else:
        return redirect('check_password')


def create_user(request):
    if request.session.has_key('username'):
        username = request.session['username']
        role = request.session['role']
        if role == 2:
            if request.method == 'POST':
                form = FormCreateUser(request.POST)
                if form.is_valid():
                    if check_for_similar_login(form.cleaned_data['userLogin']) == True:
                        messages.info(request, 'Istnieje już użytkownik o takim loginie!')
                    else:
                        if form.cleaned_data['userPassword'] == form.cleaned_data['userPasswordRepeat']:
                            new_ticket = User(userLogin=form.cleaned_data['userLogin'],
                                              userFirstName=form.cleaned_data['userFirstName'],
                                              userLastName=form.cleaned_data['userLastName'],
                                              userPhoneNumber=form.cleaned_data['userPhoneNumber'],
                                              userPassword=form.cleaned_data['userPassword'],
                                              userRole=form.cleaned_data['userRole'])
                            new_ticket.save()
                            return redirect('display_users')
                        else:
                            messages.info(request, 'Hasła są różne!')

            context = {"username": username,
                       'role': request.session['role'],
                       'form': FormCreateUser,
            }
            return render(request, 'user_related/create_user.html', context)
        else:
            return redirect('display_tickets')
    else:
        return redirect('check_password')


def close_ticket(request, ticket_id):
    if request.session.has_key('username'):
        username = request.session['username']

        ticket = Ticket.objects.get(ticketID=ticket_id)
        ticket.ticketStatus = 1
        ticket.save()

        logged_in_user = User.objects.get(userLogin=username)
        comment_ticket_id = Ticket.objects.get(ticketID=ticket_id)
        new_comment = Comment(commentCreator=logged_in_user,
                              commentTicket=comment_ticket_id,
                              commentDescription='Status zmieniono na: Zrealizowane')
        new_comment.save()

        return redirect('display_ticket_detail', ticket_id)
    else:
        return redirect('check_password')


def open_ticket(request, ticket_id):
    if request.session.has_key('username'):
        username = request.session['username']

        ticket = Ticket.objects.get(ticketID=ticket_id)
        ticket.ticketStatus = 0
        ticket.save()

        logged_in_user = User.objects.get(userLogin=username)
        comment_ticket_id = Ticket.objects.get(ticketID=ticket_id)
        new_comment = Comment(commentCreator=logged_in_user,
                              commentTicket=comment_ticket_id,
                              commentDescription='Status zmieniono na: Niezrealizowane')
        new_comment.save()

        return redirect('display_ticket_detail', ticket_id)
    else:
        return redirect('check_password')


def asign_ticket(request, ticket_id, admin_id):
    if request.session.has_key('username'):
        username = request.session['username']
        if request.session['role'] == 2:
            if admin_id == 0:
                ticket = Ticket.objects.get(ticketID=ticket_id)
                ticket.ticketTechnician = None
                ticket.save()
                logged_in_user = User.objects.get(userLogin=username)
                comment_ticket_id = Ticket.objects.get(ticketID=ticket_id)
                new_comment = Comment(commentCreator=logged_in_user,
                                      commentTicket=comment_ticket_id,
                                      commentDescription=f'Przypisano do zgłoszenia: -')
                new_comment.save()
            else:
                admin = User.objects.get(userID=admin_id)
                ticket = Ticket.objects.get(ticketID=ticket_id)
                ticket.ticketTechnician = admin
                ticket.save()
                logged_in_user = User.objects.get(userLogin=username)
                comment_ticket_id = Ticket.objects.get(ticketID=ticket_id)
                new_comment = Comment(commentCreator=logged_in_user,
                                      commentTicket=comment_ticket_id,
                                      commentDescription=f'Przypisano do zgłoszenia: {admin.userFirstName} {admin.userLastName}')
                new_comment.save()
        return redirect('display_ticket_detail', ticket_id)
    else:
        return redirect('check_password')


def check_for_similar_login(new_login, current_user=None):
    login_list = User.objects.all().values_list('userLogin', flat=True)
    if new_login == current_user:
        return False
    if new_login in login_list:
        return True
    else:
        return False


def display_tickets(request):
    if request.session.has_key('username'):
        username = request.session['username']
        role = request.session['role']
        filter_option = 0
        searched_text = ""

        if role == 2:
            data_set = Ticket.objects.all()
        else:
            user = User.objects.get(userLogin=username)
            data_set = Ticket.objects.filter(ticketCreator=user)


        if request.method == 'POST':
            form = FormSearchForUsers(request.POST)
            form_f = FormFilterTickets(request.POST)

            if form_f.is_valid():
                filter_option = form_f.cleaned_data['ticketFilter']
                data_set = filter_tickets(request, role, request.session['username'], filter_option)

            if form.is_valid():
                searched_text = form.cleaned_data['searchInput']
                data_set = data_set.filter(
                                            Q(ticketTitle__icontains=searched_text) |
                                            Q(ticketDescription__icontains=searched_text) |
                                            Q(ticketCreationDate__icontains=searched_text) |
                                            Q(ticketStatus__icontains=searched_text))

        data_set = data_set.order_by('-ticketID')

        context = {
            'username': username,
            'role': role,
            'tickets': data_set,
            'form': FormSearchForUsers(initial={'searchInput': searched_text}),
            'form_f': FormFilterTickets(initial={'ticketFilter': filter_option}),
        }
        return render(request, 'ticket_related/tickets.html', context)

    else:
        return redirect('check_password')

# NIE DZIAŁA
def filter_tickets(request, user_role, user_login, filter_option):
    user = User.objects.get(userLogin=user_login)
    if user_role == 2:
        data_set = Ticket.objects.all()
    else:
        data_set = Ticket.objects.filter(ticketCreator=user)

    if filter_option == "0":
        new_data_set = data_set
    elif filter_option == "1":
        new_data_set = data_set.filter(ticketStatus=0)
    elif filter_option == "2":
        new_data_set = data_set.filter(Q(ticketTechnician=user) | Q(ticketCreator=user))
    else:
        new_data_set = data_set.filter(Q(ticketStatus=0) & (Q(ticketTechnician=user) | Q(ticketCreator=user)))

    return new_data_set
