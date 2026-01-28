from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Subject, Teacher, Grade


@login_required
def grade_detail(request, grade_id):
    """Отображение деталей одной оценки"""
    try:
        grade = get_object_or_404(Grade, id=grade_id)

        # Проверяем, имеет ли пользователь доступ к этой оценке
        user = request.user
        if hasattr(user, "teacher") and grade.teacher == user.teacher:
            # Учитель может видеть все свои оценки
            pass
        elif hasattr(user, "student") and grade.student == user.student:
            # Ученик может видеть свои оценки
            pass
        elif hasattr(user, "parent"):
            # Родитель может видеть оценки своих детей
            if grade.student in user.parent.children.all():
                pass
            else:
                messages.error(request, "У вас нет доступа к этой оценке.")
                return redirect("my_grades")
        elif user.is_superuser:
            # Суперпользователь может видеть всё
            pass
        else:
            messages.error(request, "У вас нет доступа к этой оценке.")
            return redirect("my_grades")

        return render(request, "journal/grade_detail.html", {"grade": grade})
    except Exception as e:
        messages.error(request, f"Ошибка при загрузке деталей оценки: {str(e)}")
        return redirect("my_grades")


@login_required
def add_grade(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, "Только учитель может ставить оценки.")
        return redirect("home")

    if request.method == "POST":
        try:
            student_id = int(request.POST["student"])
            subject_id = int(request.POST["subject"])
            value = int(request.POST["value"])
            comment = request.POST.get("comment", "").strip()

            # Проверка диапазона значений оценки
            if value < 1 or value > 5:
                messages.error(request, "Оценка должна быть от 1 до 5!")
                return redirect("add_grade")

            # Проверка обязательности комментария
            if value < 5 and not comment:
                messages.error(request, "Комментарий обязателен при оценке ниже 5!")
                return redirect("add_grade")
        except (ValueError, KeyError):
            messages.error(request, "Неверные данные для создания оценки!")
            return redirect("add_grade")

        subject = get_object_or_404(Subject, id=subject_id)
        if not teacher.subjects.filter(id=subject.pk).exists():
            messages.error(request, "Вы не преподаёте этот предмет!")
            return redirect("add_grade")

        student = get_object_or_404(Student, id=student_id)
        try:
            Grade.objects.create(
                student=student,
                subject=subject,
                teacher=teacher,
                value=value,
                comment=comment,
            )
            messages.success(request, "Оценка успешно добавлена!")
        except Exception as e:
            messages.error(request, f"Ошибка при добавлении оценки: {str(e)}")
        return redirect("add_grade")

    students = Student.objects.all()
    subjects = teacher.subjects.all()

    context = {"students": students, "subjects": subjects}
    return render(request, "journal/add_grade.html", context)


@login_required
def my_grades(request):
    user = request.user
    grades = []

    try:
        if hasattr(user, "teacher"):
            grades = Grade.objects.filter(teacher=user.teacher).select_related(
                "subject",
                "teacher",
                "student",
            )
        elif hasattr(user, "student"):
            grades = Grade.objects.filter(student=user.student).select_related(
                "subject", "teacher"
            )
        elif hasattr(user, "parent"):
            children = user.parent.children.all()
            grades = Grade.objects.filter(student__in=children).select_related(
                "student", "subject", "teacher"
            )
        elif user.is_superuser:
            return redirect("admin:index")
        else:
            messages.info(request, "У вас нет доступа к оценкам.")
            return redirect("login")
    except Exception as e:
        messages.error(request, f"Ошибка при загрузке оценок: {str(e)}")
        return redirect("home")

    # Подсчет количества уникальных предметов
    subjects_count = grades.values("subject").distinct().count()

    return render(
        request,
        "journal/my_grades.html",
        {"grades": grades, "subjects_count": subjects_count},
    )


def home(request):
    if request.user.is_authenticated:
        return redirect("my_grades")
    return render(request, "journal/home.html")
