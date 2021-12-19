from typing import List
from django.test import TestCase
from django.contrib.auth.models import Group
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.utilities.CourseUtil import CourseUtil
from TA_Scheduler.models import Account, Course

class SetUp:
    courseName: str = "Course1"
    description: str = "description"
    instructor: Account
    tas: List[Account] = []
    courseNames: List[str] = []

    def __init__(self):
        Group.objects.create(name="instructor")
        Group.objects.create(name="ta")
        Group.objects.create(name="admin")

        self.instructor = AccountUtil.getAccountByID(
            AccountUtil.createInstructorAccount("Instructor", "password")
        )

        self.tas = []

        for i in range(4):
            ta_id = AccountUtil.createTAAccount("TA" + str(i), "password" + str(i))
            ta = AccountUtil.getAccountByID(ta_id)
            self.tas.append(ta)

    def setManyCourseNames(self, amount: int):
        self.courseNames = []
        for i in range(amount):
            self.courseNames.append("Course" + str(i))

class CreateCourseUtilTest(TestCase):

    def setUp(self):
        self.util = SetUp()

    def test_createCourse(self):
        index = CourseUtil.createCourse(self.util.courseName, self.util.description, self.util.instructor, self.util.tas)
        self.assertEquals(len(Course.objects.filter(id=index)), 1, msg="Failed to add created course to Course database")

    def test_emptyName(self):
        with self.assertRaises(TypeError, msg="Failed to raise type error when Course name is blank"):
            CourseUtil.createCourse("", self.util.description, self.util.instructor, self.util.tas)

    def test_noneInstructor(self):
        try:
            index = CourseUtil.createCourse(self.util.courseName, self.util.description, None, self.util.tas)
            self.assertEquals(len(Course.objects.filter(id=index)), 1, msg="Failed to add created course with None instructor to Course database")
        except Exception as e:
            self.fail(str(e) + " exception was thrown when trying to create a course without instructor.")

    def test_noneTAs(self):
        try:
            index = CourseUtil.createCourse(self.util.courseName, self.util.description, self.util.instructor, None)
            self.assertEquals(len(Course.objects.filter(id=index)), 1, msg="Failed to add created course with None TAs to Course database")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown when trying to create a course with TAs set to None.")

    def test_emptyTAs(self):
        try:
            index = CourseUtil.createCourse(self.util.courseName, self.util.description, self.util.instructor, [])
            self.assertEquals(len(Course.objects.filter(id=index)), 1, msg="Failed to add created course with empty TAs to Course database")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown when trying to create a course with TAs set to empty list [].")

    def test_accurateFields(self):
        try:
            index = CourseUtil.createCourse(self.util.courseName, self.util.description, self.util.instructor, self.util.tas)
            course = Course.objects.filter(id=index)[0]
            self.assertEquals(course.name, self.util.courseName, msg="Created course with a name that does not match the argument name during creation")
            self.assertEquals(course.description, self.util.description, msg="Created course with a description that does not match the argument description during creation")
            self.assertEquals(course.instructor.id, self.util.instructor.id, msg="Created course with an instructor id that does not match the argument instructor id")
            self.assertListEqual(list(course.tas.all()), self.util.tas, msg="Created course with TAs that do not match argument TAs during creation")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown when trying to create and get a course from the Course database")


class GetCourseByIDTest(TestCase):

    def setUp(self):
        self.util = SetUp()

    def test_getCourseByID(self):
        try:
            course = Course.objects.create(name=self.util.courseName, description=self.util.description, instructor=self.util.instructor)
            self.assertIsNotNone(CourseUtil.getCourseByID(course.id), msg="Failed to find an existing course with given ID")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown when creating and trying to get a course by its ID")

    def test_nonexistentID(self):
        try:
            self.assertIsNone(CourseUtil.getCourseByID(1), msg="Returned a course that was never added.")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown when getting a nonexistent course by ID, should return None")

    def test_idIsNotNumber(self):
        with self.assertRaises(Exception, msg="Did not raise exception when the argument ID was not a number"):
            CourseUtil.getCourseByID("test")

    def test_accurateFields(self):
        try:
            course = Course.objects.create(name=self.util.courseName, description=self.util.description, instructor=self.util.instructor)
            course.tas.set(self.util.tas)
            subject = CourseUtil.getCourseByID(course.id)
            self.assertEquals(subject.name, self.util.courseName, msg="Created course with a name that does not match the argument name during creation")
            self.assertEquals(subject.description, self.util.description, msg="Created course with a description that does not match the argument description during creation")
            self.assertEquals(subject.instructor.id, self.util.instructor.id, msg="Created course with an instructor id that does not match the argument instructor id")
            self.assertListEqual(list(subject.tas.all()), self.util.tas, msg="Created course with TAs that do not match argument TAs during creation")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown on attempt to create and get a course by ID")

class GetAllCoursesTest(TestCase):
    def setUp(self):
        self.amount = 15
        self.util = SetUp()
        self.util.setManyCourseNames(self.amount)
        for i in range(self.amount):
            Course.objects.create(name=self.util.courseName, description=self.util.description, instructor=self.util.instructor).tas.set(self.util.tas)

    def test_getAllCourses(self):
        try:
            courses = CourseUtil.getAllCourses()
            self.assertEquals(len(courses), self.amount, msg="Failed to retrieve all courses from database")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown on attempt to retrieve all courses from database")




    







        



