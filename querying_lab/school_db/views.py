from django.shortcuts import render
from .models import Student, Instructor, Course, StudentCourse

def index(request):
    students = Student.objects.all()

    # The following line creates a list that allows you to examine the data 
    # from a Queryset in an easier to visualize way
    # It is not required for functionality!
    # Place a breakpoint on line 14, then compare 'students' and 'data_visualization'
    data_visualization = [item for item in students]

    context = {
        'students': students
    }
    return render(request, 'school/index.html', context)

def problem_one(request):
    # Find all students who have a GPA greater than 3.0. 
    # Order the data by highest GPAs first.

    students_gpa_over_3 = Student.objects.filter(gpa__gte=3).order_by('-gpa')
    
    data_visualization = [item for item in students_gpa_over_3]
    
    context = {
        'students_gpa_over_3': students_gpa_over_3
    }
    return render(request, 'school/one.html', context)

def problem_two(request):
    # Find all instructors hired prior to 2010
    # Order by hire date
    instructors_hired_before_2010 = Instructor.objects.filter(hire_date__lt='2010-01-01').order_by('hire_date')
    
    data_visualization = [item for item in instructors_hired_before_2010]
    
    context = {
        'instructors_hired_before_2010': instructors_hired_before_2010
    }
    return render(request, 'school/two.html', context)

def problem_three(request):
    # Find all students who have a A+ in any class and are NOT getting a C+ in any class. 
    # Order the data by student's first name alphabetically.

    students_with_c = Student.objects.filter(studentcourse__grade='C+')
    students_with_Aplus = StudentCourse.objects.filter(grade='A+').exclude(student_id__in=students_with_c).order_by('student_id__first_name')
    
    data_visualization = [item for item in students_with_Aplus]
    
    context = {
        'students_with_Aplus': students_with_Aplus
    }
    return render(request, 'school/three.html', context)

def problem_four(request):
    # Find all students who are taking the Programming class. 
    # Order by their grade. 
    programming_students = StudentCourse.objects.filter(course__name='Programming').order_by('grade')
    
    data_visualization = [item for item in programming_students]
    
    context = {
        'programming_students': programming_students
    }
    return render(request, 'school/four.html', context)

def problem_five(request):
    # Find all students getting an A in the Programming class. 
    # Order by last name.

    programming_students = StudentCourse.objects.filter(course__name='Programming')
    programming_students_with_A = programming_students.filter(grade='A').order_by('student__last_name')
    
    data_visualization = [item for item in programming_students_with_A]
    
    context = {
        'programming_students_with_A': programming_students_with_A
    }
    return render(request, 'school/five.html', context)

def problem_six(request):
    # Find all students with a GPA less than 3.0 who are getting an A in Programming class.
    # Order by GPA.
    programming_students = StudentCourse.objects.filter(course__name='Programming')
    programming_students_with_A = programming_students.filter(grade='A')
    programming_students_with_A_gpa_lessthan3 = programming_students_with_A.filter(student__gpa__lt=3).order_by('student__gpa')
    
    data_visualization = [item for item in programming_students_with_A_gpa_lessthan3]
    
    context = {
        'programming_students_with_A_gpa_lessthan3': programming_students_with_A_gpa_lessthan3
    }
    return render(request, 'school/six.html', context)

################## BONUS #################
# These problems will require using Aggregate functions along with annotate()
# https://docs.djangoproject.com/en/4.0/topics/db/aggregation/
# https://docs.djangoproject.com/en/4.0/ref/models/querysets/#annotate

# Create a view function and template for each bonus problem you complete

# BONUS ONE
from django.db.models import Count, Sum
# Write a query to find any instructors who are only teaching one single course. Display the instructor and the course
def bonus_one(request):
    instructors_one_course = Instructor.objects.all().annotate(Count('course')).filter(course__count=1)
    course_names = []
    
    for instructor in instructors_one_course:
        instructor_course = Course.objects.get(instructor_id=instructor.id)
        course_names.append(instructor_course)
         
    data_visualization = [item for item in instructors_one_course]
    
    context = {
        'instructors_one_course': instructors_one_course,
        'course_names': course_names}

    return render(request, 'school/bonus_one.html', context)

# BONUS TWO
# Display all students along with the number of credits they are taking
def bonus_two(request):
    all_students = Student.objects.all()
    student_hours = {}
    
    for student in all_students:
        student_courses = StudentCourse.objects.filter(student_id=student.id)
        credit_hours = student_courses.aggregate(Sum('course__credits'))
        student_hours.__setitem__(student, credit_hours)
        
    data_visualization = [item for item in student_hours]
    
    context = {
        'all_students': all_students,
        'student_hours': student_hours
    }

    return render(request, 'school/bonus_two.html', context)

# BONUS THREE
# Find all students who are getting an A in any course and average their GPAs. Display the number of students and their Average GPA

# BONUS FOUR
# Write a function that will replace student GPAs in the database with an accurate score based only on their current grades
# This may require multiple queries
# See https://www.indeed.com/career-advice/career-development/gpa-scale for a chart of what point value each grade is worth