from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from .admin import UserCreationForm, EmployeeCreationForm, EmployerChangeForm
from .models import User

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

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
    if request.user.is_authenticated and request.user.is_company:
        users = User.objects.filter(user_type=3, created_by=request.user)
    context = {'users': users}
    return render(request, 'index.html', context)


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
        print(obj.created_by.id)
        if not obj.created_by == self.request.user:
            raise Http404
        return obj
