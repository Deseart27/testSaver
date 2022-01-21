from django import forms


class UserForm(forms.Form):
    study_url = forms.CharField(max_length=1000)
