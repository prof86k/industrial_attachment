from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from . import models as mdl


class StudentCreationForm(UserCreationForm):
    'student registration form for stidents to register thier account'
    full_name = forms.CharField(max_length=50, required=True)
    active_email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=12, required=True)

    class Meta(UserCreationForm.Meta):
        # initialize the default user fields
        model = mdl.User

    @transaction.atomic
    def save(self):
        'creating the user in the model '
        user = super().save(commit=False)
        # get the additional fields with clean data to create user
        user.email = self.cleaned_data['active_email']
        user.full_name = self.cleaned_data['full_name']
        user.phone_number = self.cleaned_data['phone']
        # the user is a student
        user.is_student = True
        user.save()
        # save the student model
        student = mdl.Student.objects.create(user=user)
        # return the student as user instance
        return user


class LogBookForm(forms.ModelForm):
    class Meta:
        model = mdl.LogBook
        fields = ["activity", 'self_input',
                  'recommendation', 'conclusion',
                  'latitude', 'longitude',
                  ]


class Companyform(forms.ModelForm):
    class Meta:
        model = mdl.Company
        fields = [
            'category', 'name', 'region', 'district',
            'contact_person', 'contact_number',
            'latitude', 'longitude',
        ]


class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = mdl.Student
        fields = ('student_id', 'gender', 'student_programme')


#  ================== supervisor area ===========

class SupervsorCreationForm(UserCreationForm):
    'specify the additional fields that will be use to register the supervisor'
    active_email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=12, required=True)

    class Meta(UserCreationForm.Meta):
        # get the default user fields
        model = mdl.User

    @transaction.atomic
    def save(self):
        'for user to process multiple fields add transction atomic decorators'
        user = super().save(commit=False)
        # get all the additinal fields clean data to save
        user.email = self.cleaned_data['active_email']
        user.full_name = self.cleaned_data['full_name']
        user.phone_number = self.cleaned_data.get('phone')
        # the user is now a supervisor
        user.is_supervisor = True
        # save the registered user
        user.save()
        # create user with the addtitional fields
        supervisor = mdl.Supervisor.objects.create(user=user)
        # return the currently created user
        return user


class SupervisorDetailsForm(forms.ModelForm):
    class Meta:
        model = mdl.Supervisor

        fields = ('title',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = mdl.Category
        fields = ('category_name',)
