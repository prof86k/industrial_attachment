from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import time

# pdf generator
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
from . import forms as fms
from . import models as mdl
from .decorators import is_not_student, is_not_supervisor, is_unauthenticated


def main_view(request):
    context = {'current_date': time.strftime("%Y")}
    return render(request, "industrial_attachment/main_page.html", context)


@is_unauthenticated
@login_required
def home_page(request):
    "collect basic information about the user and company"
    if request.method == "POST":
        # if the user try to submit valid informationf company
        student_id = request.POST['student_id']
        gender = request.POST['gender']
        programme = request.POST['programme']
        name = request.POST['name']
        region = request.POST['region']
        district = request.POST['district']
        contact_person = request.POST['person']
        contact_number = request.POST['contact-number']

    return redirect("attachment:student-profile")


@is_unauthenticated
@login_required
@is_not_student
def profile_view(request):
    "students profile page that returns students informations"
    # user = get_object_or_404(mdl.User, user=request.user)
    student = get_object_or_404(mdl.Student, user=request.user)
    if request.method == "POST":
        company_form = fms.Companyform(request.POST)
        student_form = fms.StudentDetailsForm(request.POST)
        if company_form.is_valid() and student_form.is_valid():
            new_infor = student_form.save(commit=False)
            new_infor.user = request.user
            new_infor.save()
            new_inf = company_form.save(commit=False) 
            new_inf.student = student
            new_inf.save()
            return redirect('attachment:student-profile')
    else:
        company_form = fms.Companyform()
        student_form = fms.StudentDetailsForm()
    try:
        com_data = get_object_or_404(mdl.Company, student=student)
    except Exception as e:
        com_data = None
    context = {
        'com_form':company_form,
        'stud_form':student_form,
        'com_data': com_data,
        'user_data': student,
        'current_date': time.strftime("%Y"),
    }
    return render(request, "attachment_students/profile.html", context)


@is_unauthenticated
@login_required
def submit_log_activity(request):
    "student can save their daily activity using the log Book"
    student = get_object_or_404(mdl.Student, user=request.user)
    if request.method == 'POST':
        # take a post data from student
        logbookform = fms.LogBookForm(request.POST)
        if logbookform.is_valid():
            new_data = logbookform.save(commit=False)
            new_data.student = student
            new_data.save()
            return redirect('attachment:student-profile')
    else:
        logbookform = fms.LogBookForm()
    context = {
        'logbookform': logbookform,
        'effective': datetime.utcnow(),
        'current_date': time.strftime("%Y")
    }
    return render(request, "attachment_students/logbook.html", context)


@login_required
@is_unauthenticated
def view_logbook_activities(request):
    "get all the activities of the student from their logbook"
    student = get_object_or_404(mdl.Student, user=request.user)
    logbook_activities = student.logbook_set.all().order_by('-activity_date')
    context = {
        'logbook_activities': logbook_activities,
        'student': student,
        'current_date': time.strftime("%Y")
    }

    return render(request, "attachment_students/view_activities.html", context)


@is_unauthenticated
@login_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(mdl.LogBook,id=activity_id)
    if request.method == 'POST':
        log_form = fms.LogBookForm(instance=activity,data=request.POST)
        if log_form.is_valid():
            log_form.save()
            return redirect('attachment:student-view-activities')
    else:
        log_form = fms.LogBookForm(instance=activity)
    context = {
        'form':log_form,
    }
    "allow the user to make corrections to the data entered except the longitude and latitude values"
    return render(request, 'attachment_students/edit_activity.html',context)

def print_my_logbook(request):
    student = get_object_or_404(mdl.Student,user=request.user)
    log_activities = student.logbook_set.all()

    buffer = io.BytesIO()
    canvas_object = canvas.Canvas(buffer,pagesize=letter,bottomup=0,initialFontName="Helvetica",initialFontSize=12)
    text = canvas_object.beginText()
    text.setTextOrigin(inch, inch)

    # write to the pdf
    text.textLines("Student ID:"+str(student.student_id),trim=1)
    text.textLines("\n")
    for obj in log_activities:
        text.textLines("Activity Date:   "+str(obj.activity_date)+"\n")
        text.textLines("\n")
        text.textLines("=======================================================\n")
        text.textLines("\t Activity: \n"+str(obj.activity+"\n"))
        text.textLines("\n")
        text.textLines("\t Self Input:\n"+str(obj.self_input+"\n"))
        text.textLines("\n")
        text.textLines("\t Recomendation:\n"+str(obj.recommendation+"\n"))
        text.textLines("\n")
        text.textLines("\t Conclusion:\n      "+str(obj.conclusion+"\n"))
        text.textLines("\n")

    canvas_object.drawText(text)
    canvas_object.showPage()
    canvas_object.save()
    buffer.seek(0)

    return FileResponse(buffer,as_attachment=True,filename=f'LogBook Of {student.student_id}.pdf')

# ================ user creation forms here ==================================
def student_registration(request):
    "student creation form here"
    if request.method == "POST":
        # student form is posted
        # student form contains data
        student_form = fms.StudentCreationForm(request.POST)
        if student_form.is_valid():
            # student form is valid with at least 8 charaters password
            request.user.is_student = True
            # user is now student
            student_form.save()
            return redirect('attachment:student-login')
    else:
        student_form = fms.StudentCreationForm()

    context = {
        'student_form': student_form,
        'current_date': time.strftime("%Y")
    }

    return render(request, 'attachment_students/student_registration.html', context)


def student_login(request):
    "authenticate the user and login them in to their profile"
    if request.method == "POST":
        # get the posted data from the form
        username = request.POST['username']
        password = request.POST['password']
        # authenticate user
        student_user = authenticate(
            request, username=username, password=password)
        if student_user is not None:
            # user is an object of a student table
            results = login(request, user=student_user)
            # login and redirect to their profile
            # username = kkuma
            # password = prof86k000
            return redirect('attachment:student-profile')
    context = {'current_date': time.strftime("%Y")}
    return render(request, "attachment_students/student_login.html", context)


def student_logout(request):
    "logout the current student"
    logout(request)
    return redirect('attachment:student-login')
# =================== supervisor profile and access form ==========================


@is_unauthenticated
@login_required
@is_not_supervisor
def supervisor_profile(request):
    "supervisor profile page form"
    current_super_user = get_object_or_404(mdl.Supervisor, user=request.user)
    context = {
        'current_user': current_super_user,
        'current_date': time.strftime("%Y"),
    }
    return render(request, 'attachment_supervisors/super_profile.html', context)


def supervisor_registration(request):
    "supervisor creation form here"
    if request.method == "POST":
        # user post data
        # form with data
        supervisor_form = fms.SupervsorCreationForm(request.POST)
        if supervisor_form.is_valid():
            # user form is valid with at least 8 characters
            request.user.is_supervisor = True
            # user is now supervisor
            supervisor_form.save()
            return redirect("attachment:super-login")

    else:
        supervisor_form = fms.SupervsorCreationForm()

    context = {
        'super_form': supervisor_form,
        'current_date': time.strftime("%Y"),
    }
    return render(request, 'attachment_supervisors/super_registration.html', context)


def supervisor_login(request):
    "authenticate the user if they are supervisor objects"
    if request.method == "POST":
        # get the posted data from the form
        username = request.POST['username']
        password = request.POST['password']
        # use the authentication function to authenticate them
        supervisor_user = authenticate(
            request, username=username, password=password)
        # this returns the supervisor user object as current user
        if supervisor_user is not None:
            # user is a supervisor
            login(request, user=supervisor_user)
            # user is login successfully and then taken their profile
            return redirect('attachment:super-profile')
    context = {'current_date': time.strftime("%Y"), }
    return render(request, 'attachment_supervisors/super_login.html', context)


@login_required
def super_detailed_info(request):
    'supervisor detailed information '
    current_super_user = get_object_or_404(mdl.Supervisor, user=request.user)
    if request.method == "POST":
        # get the posted data
        title= request.POST['title']
        field = request.POST['field']
        supervisor = mdl.Supervisor(user=request.user,title=title)

        category = mdl.Category(category_field=current_super_user,category_name=field)
        supervisor.save()
        category.save()
        print(title," ",field)
        return redirect('attachment:super-profile')

@is_unauthenticated
@login_required
@is_not_supervisor
def generate_pdf(request,student_id):
    student = get_object_or_404(mdl.Student, user=student_id)
    
    logbook_activities = student.logbook_set.all().order_by('activity_date')


    buffer = io.BytesIO() 
    canvas_obj = canvas.Canvas(buffer,pagesize=letter,bottomup=0)

    # create a text object
    text_obj =  canvas_obj.beginText()
    text_obj.setTextOrigin(inch,inch)
    text_obj.setFont("Helvetica",12)

    # add some text
    text_obj.textLines("\t Student ID: "+str(student.student_id))
    text_obj.textLines("\n")
    for obj in logbook_activities:
        text_obj.textLines("Activity Date:   "+str(obj.activity_date)+"\n")
        text_obj.textLines("\n")
        text_obj.textLines("=======================================================\n")
        text_obj.textLines("\t Activity: \n"+str(obj.activity+"\n"))
        text_obj.textLines("\n")
        text_obj.textLines("\t Self Input:\n"+str(obj.self_input+"\n"))
        text_obj.textLines("\n")
        text_obj.textLines("\t Recomendation:\n"+str(obj.recommendation+"\n"))
        text_obj.textLines("\n")
        text_obj.textLines("\t Conclusion:\n      "+str(obj.conclusion+"\n"))
        text_obj.textLines("\n")


    canvas_obj.drawText(text_obj)
    canvas_obj.showPage() 
    canvas_obj.save()
    buffer.seek(0)

    return FileResponse(buffer,as_attachment=True,filename=f"{student.student_id} logbook.pdf")


@login_required
def view_supervisor_students(request):
    "view all students belonging to a supervisor"
    try:
        supervisor = get_object_or_404(mdl.Supervisor, user=request.user)
        category = get_object_or_404(mdl.Category, category_field=supervisor)
    except Exception:
        category=None
    
    context = {
        'category': category,
        'current_date': time.strftime("%Y"),
    }
    return render(request, 'attachment_supervisors/super_view_students.html', context)


@login_required
def view_supervisor_student_activity(request, student):
    "supervisor view student activities"
    student = get_object_or_404(mdl.Student, user=student)
    logbook_activities = student.logbook_set.all().order_by('-activity_date')
    context = {
        'logbook_info': logbook_activities,
        'current_date': time.strftime("%Y"),
    }
    return render(request, 'attachment_supervisors/super_view_student_activity.html', context)


def supervisor_logout(request):
    "logout supervisor"
    logout(request)
    return redirect("attachment:super-login")
# =================================== student login profile ===================
