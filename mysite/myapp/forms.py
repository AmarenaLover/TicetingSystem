from django import forms

Roles = ((0, "Konto wyłączone"),
         (1, "Użytkownik"),
         (2, "Administrator"))

Status = ((0, "Brak"),
          (1, "Aktywne"),
          (2, "Moje"),
          (3, "Aktywne/Moje"))


class FormCheckPassword(forms.Form):
    form_login = forms.CharField(label='Login ', max_length=100)
    form_password = forms.CharField(label='Hasło ', widget=forms.PasswordInput)


class FormCreateTicket(forms.Form):
    ticketTitle = forms.CharField(label='Tytuł', max_length=64)
    ticketDescription = forms.CharField(label='Opis zgłoszenia', max_length=1024, widget=forms.Textarea)
    ticketCreator = forms.IntegerField(widget=forms.HiddenInput(), required=False)


class FormAddComent(forms.Form):
    commentContent = forms.CharField(label='Dodaj komentarz', max_length=255, widget=forms.Textarea)


class FormSearchForUsers(forms.Form):
    searchInput = forms.CharField(label='', required=False)


class FormChangeUserInfo(forms.Form):
    userFirstName = forms.CharField(max_length=255)
    userLastName = forms.CharField(max_length=255)
    userPhoneNumber = forms.CharField(max_length=20)


class FormChangeUserPassword(forms.Form):
    userPassword = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    userPasswordRepeat = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)


class FormChangeUserInfoImp(forms.Form):
    userLogin = forms.CharField(label='Login', max_length=255)
    userRole = forms.ChoiceField(label='Uprawnienia', choices=Roles)


class FormFilterTickets(forms.Form):
    ticketFilter = forms.ChoiceField(label='', choices=Status)


class FormCreataeUser(forms.Form):
    userFirstName = forms.CharField(label='Imię',max_length=255)
    userLastName = forms.CharField(label='Nazwisko',max_length=255)
    userPhoneNumber = forms.CharField(label='Kontakt',max_length=20)
    userLogin = forms.CharField(label='Login', max_length=255)
    userRole = forms.ChoiceField(label='Uprawnienia', choices=Roles)
    userPassword = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    userPasswordRepeat = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)