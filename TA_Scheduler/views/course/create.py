from django.shortcuts import render
from TA_Scheduler.models import Account
from django.views import View
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.utilities.CourseUtil import CourseUtil 

class CreateCourse(View):

    # this is called when the user opens the page, the course/create.html
    def get(self, request):
        return render(request, 'course/create.html', {'message' : '', 'instructors' : AccountUtil.getInstructors()})

    # this is called when the user clicks submit.
    def post(self, request):

        # if user is anonymous or not admin, show error
        if request.user.is_anonymous or request.user.account.authority == 0:
            return render(request, 'course/create.html', {'message' : 'User is not authorized to create the course.', 'instructors' : AccountUtil.getInstructors()})

        name = request.POST['name']
        description = request.POST['description']

        # if name is blank show error
        if not name:
            return render(request, 'course/create.html', {'message' : 'Course name must not be blank.', 'instructors' : AccountUtil.getInstructors()})

        instructor = request.POST['instructor']

        # adds course to database
        # TODO need to confirm this works when users can be created
        CourseUtil.createCourse(name, description, instructor)

        return render(request, 'course/create.html', {'message' : 'Course created.'})