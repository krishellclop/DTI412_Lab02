
from django.shortcuts import render
from django.http import Http404


# ==========================================
# Course Database
# ==========================================

COURSES_DATA = [
    {
        'id': 101,
        'code': 'DTI412',
        'title': 'Special Topic in Application Development',
        'description': 'Learn modern application development using Django and Python.',
        'credits': 3,
        'instructor': 'Course Instructor',
    },
    {
        'id': 102,
        'code': 'DTI413',
        'title': 'Database Systems & Data Modeling',
        'description': 'Learn database design, data modeling, and database management.',
        'credits': 3,
        'instructor': 'Course Instructor',
    },
    {
        'id': 103,
        'code': 'DTI414',
        'title': 'Frontend Web Technologies & React',
        'description': 'Learn frontend web development and modern React technologies.',
        'credits': 3,
        'instructor': 'Course Instructor',
    },
]


# ==========================================
# 1. Homepage View
# ==========================================

def home_view(request):

    context = {
        'total_courses': len(COURSES_DATA),
        'featured_course': COURSES_DATA[0],
    }

    return render(request, 'catalog/home.html', context)


# ==========================================
# 2. Course List View + Search
# ==========================================

def course_list_view(request):

    # Get search keyword
    query = request.GET.get('q', '').strip()

    # Filter courses by title or course code
    filtered_courses = [
        course for course in COURSES_DATA
        if query.lower() in course['title'].lower()
        or query.lower() in course['code'].lower()
    ]

    context = {
        'courses': filtered_courses,
        'query': query,
    }

    return render(request, 'catalog/course_list.html', context)


# ==========================================
# 3. Course Detail View
# ==========================================

def course_detail_view(request, course_id):

    # Find course using its ID
    course = next(
        (c for c in COURSES_DATA if c['id'] == course_id),
        None
    )

    # Return 404 if course does not exist
    if course is None:
        raise Http404("Course not found")

    context = {
        'course': course,
    }

    return render(request, 'catalog/course_detail.html', context)


# ==========================================
# 4. Inquiry View
# ==========================================

def inquiry_view(request):

    errors = []
    submitted_data = None

    if request.method == 'POST':

        student_name = request.POST.get('student_name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Validate student name
        if not student_name:
            errors.append('Full name is required.')

        # Validate email
        if not email:
            errors.append('Email address is required.')
        elif '@' not in email:
            errors.append('Please enter a valid email address.')

        # Validate inquiry message
        if not message:
            errors.append('Inquiry message is required.')

        # Successful submission
        if not errors:

            submitted_data = {
                'student_name': student_name,
                'email': email,
                'message': message,
            }

    context = {
        'errors': errors,
        'submitted_data': submitted_data,
    }

    return render(request, 'catalog/inquiry.html', context)
