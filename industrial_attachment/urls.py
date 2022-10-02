from django.urls import path

from . import views as vws

app_name = "attachment"
urlpatterns = [
    path('', vws.main_view, name="main-page"),
    path('student/registration/', vws.student_registration,
         name='student-registration'),
    path('student/login/', vws.student_login, name="student-login"),
    path('student/logout/', vws.student_logout, name='student-log-out'),
    path('student/profile', vws.profile_view, name='student-profile'),
    path('home/basic/info', vws.home_page, name="home"),
    path('log-book', vws.submit_log_activity, name="student-logbook"),
    path('view/activities', vws.view_logbook_activities,
         name="student-view-activities"),
    path('edit/activity/<int:activity_id>',
         vws.edit_activity, name='edit-activity'),
     path('download/my-logbook',vws.print_my_logbook,name="print-work"),

    # ========================== users registration urls ===================
    path('supervisor/registration/',
         vws.supervisor_registration, name="super-registration"),
    path('supervisor/login/', vws.supervisor_login, name="super-login"),
    path('supervisor/profile/', vws.supervisor_profile, name="super-profile"),
    path('supervisor/detailed_info/',
         vws.super_detailed_info, name='super-details'),
    path('supervisor/view-students/',
         vws.view_supervisor_students, name="view-students"),
    path('supervisor/view-student/<int:student>/-activity/',
         vws.view_supervisor_student_activity, name="view-activity"),
    path('supservisor/logout/', vws.supervisor_logout, name='supervisor-log-out'),
    path('generate/pdf/<int:student_id>',vws.generate_pdf,name="generate-pdf"),

]
