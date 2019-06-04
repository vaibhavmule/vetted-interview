from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from .admin import UserCreationForm, EmployeeCreationForm, EmployerChangeForm
from .forms import EmployeeInviteForm
from .models import User, Invite


def accept_invite(request, token):
    invite = get_object_or_404(Invite, token=token)
    user, created = User.objects.get_or_create(email=invite.email, created_by=invite.created_by)
    if request.method == 'POST':
        form = EmployeeCreationForm(data=request.POST, instance=user)
        form.save()
        invite.delete()
        return HttpResponseRedirect('/')
    else:
        form = EmployeeCreationForm(instance=user)

    return render(request, 'registration/signup.html', {'form': form})

def edit_profile(request):
    if request.method == 'POST':
        form = EmployerChangeForm(data=request.POST, instance=request.user)
        form.save()
        return HttpResponseRedirect('/')
    else:
        form = EmployerChangeForm(instance=request.user)

    return render(request, 'registration/edit-profile.html', {'form': form})

def index(request):
    users = []
    invites = []
    if request.user.is_authenticated and request.user.is_company:
        users = User.objects.filter(user_type=3, created_by=request.user)
        invites = Invite.objects.filter(created_by=request.user)
    context = {'users': users, 'invites': invites}
    return render(request, 'index.html', context)


class InviteEmployee(generic.CreateView):
    form_class = EmployeeInviteForm
    template_name = 'invite_employee.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect('/')


class AddEmployee(generic.CreateView):
    form_class = EmployeeCreationForm
    template_name = 'add_employee.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect('/')


class RemoveEmoloyee(generic.DeleteView):
    model = User
    success_url = reverse_lazy('index')
    template_name = 'remove_employee.html'

    def get_object(self, queryset=None):
        obj = super(RemoveEmoloyee, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj
