import uuid 

from django import forms

from users.models import Invite

class EmployeeInviteForm(forms.ModelForm):

    class Meta:
        model = Invite
        fields = ('email',)


    def save(self, commit=True):
        invite = super().save(commit=False)
        invite.token = uuid.uuid1()
        if commit:
            invite.save()
        return invite