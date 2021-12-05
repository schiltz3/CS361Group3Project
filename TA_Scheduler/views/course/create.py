from django.shortcuts import render, redirect
from TA_Scheduler.models import Account
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.utilities.CourseUtil import CourseUtil
from typing import Union, Optional


class CreateCourse(View):
    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        """
        Called when the user opens the page, course/create.html
        @param request: Request from course/create.html
        @return: Response with "instructors"
        @pre: User is not anonymous, instructor, or ta
        @post: None
        @par: Side effect: Redirects you to login or dashboard depending on your group
        """
        # TODO: should be pulled out to a utis class
        # if user is anonymous or not admin, redirect to correct page
        if request.user.is_anonymous:
            return redirect("/", {"error": "User is not authorized to create a course"})
        elif request.user.groups.filter(name="instructor").exists():
            return redirect(
                "/dashboard/instructor/",
                {"error": "Instructors are not authorized to create courses"},
            )
        elif request.user.groups.filter(name="ta").exists():
            return redirect(
                "/dashboard/ta/", {"error": "TAs are not authorized to create courses"}
            )

        return render(
            request,
            "course/create.html",
            {"message": "", "instructors": AccountUtil.getInstructors()},
        )

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        """
        Called when the user clicks submit.
        @param request: Request from course/create.html
        @return: Response with "instructors", "message", "warning" and "error" or redirect
        @pre: None
        @post: Correct return or new class object
        @par: Side effect: Create a new class object
        """

        name: Optional[str] = str(request.POST.get("name", None))
        description: Optional[str] = str(request.POST.get("description", None))
        instructor: Optional[str] = str(request.POST.get("instructor", None))

        if name:
            if all(x.isalpha() or x.isspace() for x in description):
                for course in CourseUtil.getAllCourses():
                    if (course.name.casefold() == name.casefold()) and (
                            course.instructor.user.username.casefold()
                            == instructor.casefold()
                    ):
                        return render(
                            request,
                            "course/create.html",
                            {
                                "warning": "Class already exists with this instructor.",
                                "instructors": AccountUtil.getInstructors(),
                            },
                        )
            else:
                return render(
                    request,
                    "course/create.html",
                    {
                        "warning": "Name can only contain [A-z][0--9]",
                        "instructors": AccountUtil.getInstructors(),
                    },
                )
        else:
            return render(
                request,
                "course/create.html",
                {
                    "warning": "Name must not be blank.",
                    "instructors": AccountUtil.getInstructors(),
                },
            )
        if description:
            if not all(x.isalpha() or x.isspace() for x in description):
                return render(
                    request,
                    "course/create.html",
                    {
                        "warning": "Description can only contain [A-z][0--9]",
                        "instructors": AccountUtil.getInstructors(),
                    },
                )
        else:
            return render(
                request,
                "course/create.html",
                {
                    "warning": "Description must not be blank.",
                    "instructors": AccountUtil.getInstructors(),
                },
            )

        if instructor:
            try:
                instructor_account = AccountUtil.getAccountByUsername(instructor)
            except IndexError:
                instructor_account = None
                return render(
                    request,
                    "course/create.html",
                    {
                        "error": "Instructor could not be found.",
                        "instructors": AccountUtil.getInstructors(),
                    },
                )
        else:
            return render(
                request,
                "course/create.html",
                {
                    "warning": "Instructor must not be blank.",
                    "instructors": AccountUtil.getInstructors(),
                },
            )

        # adds course to database if instructor, name and description are not none
        if instructor_account and name and description:
            CourseUtil.createCourse(name, description, instructor_account)
            return render(
                request,
                "course/create.html",
                {
                    "message": "Course created.",
                    "instructors": AccountUtil.getInstructors()
                },
            )
        return render(
            request,
            "course/create.html",
            {
                "error": "Class could not be created.",
                "instructors": AccountUtil.getInstructors(),
            },
        )
