from django.contrib import admin
from .models import SchoolClass, Subject, Student, Parent, Teacher, Grade

admin.site.register([Subject, Student, Parent, Teacher, Grade, SchoolClass])
