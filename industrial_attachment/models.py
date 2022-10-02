from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    is_supervisor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    full_name = models.CharField(verbose_name="Full Name:", max_length=50)
    phone_number = models.CharField(verbose_name="Phone No.", max_length=12)
    date_joined = models.DateTimeField(auto_now_add=True)


class Supervisor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    """ this is the attachment done on an area of Maybe
    (INFORMATION, HEALTH,BANK...)
    a number of students can be attached to a category
    a number of areas can come under a category"""
    category_field = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    category_name = models.CharField(
        max_length=50, verbose_name="Attachment Area:")
    attachment_year = models.DateField(
        verbose_name="Year Of Attachment", auto_now_add=True)

    class Meta:
        "conversion name of many categories "
        verbose_name_plural = "Categories"

    def __str__(self):
        "the string representation of the category name"
        return self.category_name


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    "detailed information about the student"
    SEX_TYPE = (
        ('', "..."),
        ('M', "Male"),
        ('F', "Female"),
        ('o', "Other"),
    )
    student_id = models.CharField(
        max_length=25, verbose_name="Student ID:", blank=False, null=False)
    gender = models.CharField(verbose_name="Gender:",
                              choices=SEX_TYPE, max_length=5)
    student_programme = models.CharField(
        verbose_name="Programme:", max_length=50)

    def __str__(self):
        return self.user.username


class Company(models.Model):
    """ name of the area of student attachment (war memorial hospital) under health
    a category can have many areas"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Company Name:", max_length=50)
    region = models.CharField(verbose_name="Region", max_length=50)
    district = models.CharField(verbose_name="Distrit:", max_length=50)
    contact_person = models.CharField(
        verbose_name="Contact Person:", max_length=50)
    contact_number = models.CharField(verbose_name="Contact:", max_length=12)
    latitude = models.CharField(verbose_name="Latitude:", max_length=50)
    longitude = models.CharField(verbose_name="longtitude:", max_length=50)
    # give the time the student started the attachment with company
    time_started = models.DateTimeField(auto_now_add=True)

    class Meta:
        "conversion name of many areas"
        verbose_name_plural = "Companies"

    def __str__(self):
        "string representation of the area of name"
        return self.name


class LogBook(models.Model):
    """student ot a logbook for recording activities every student has a logbook"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.TextField(
        verbose_name="Please Write The Activity For The Day.")
    self_input = models.TextField(
        verbose_name="Please Write What You Have Been Able To Do.")
    recommendation = models.TextField(
        verbose_name="What Is Your recommendation:")
    conclusion = models.TextField(verbose_name="Write Your Conclusion:")
    latitude = models.CharField("Latitude:", max_length=50, null=False)
    longitude = models.CharField("Longitude:", max_length=50, null=False)
    # record the datetime the student sumbit the information
    activity_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        "plural form of the logbook"
        verbose_name_plural = "Log Books"

    def __str__(self):
        "string representation of the logbook"
        return "Activity On "+str(self.activity_date)
