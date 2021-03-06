from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Account(models.Model):
    """Represents a row in the Account database.

    account.id --> id in db
    account.user --> associated User object
    account.user.username --> username
    account.user.password --> password
    account.user.first_name --> first name of user
    account.user.last_name --> last name of user
    account.user.email --> email address
    account.address --> home address
    account.phone --> phone number
    """

    # unique database primary key
    id = models.AutoField(verbose_name="Account ID", primary_key=True)

    # the one-to-one mapping with the built-in User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    address = models.CharField(max_length=50, null=True, blank=True)
    phone = models.PositiveBigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    """Represents a row in the course database.

    id - generated, and is the primary key
    name - name of the course (CompSci 250)
    description - optional description of the course (prereqs, what it's about, etc.)
    instructor - the account of the instructor
    """

    id = models.AutoField("Course ID", primary_key=True)
    name = models.CharField("Course Name", max_length=200, blank=False)
    description = models.CharField("Course Description", max_length=5000)

    # SET_NULL --> when an instructor is deleted, set this thing to null
    # ForeignKey is many-to-one relation (an instructor can have many courses)
    instructor = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name="instructors"
    )

    # multiple TAs can have multiple courses
    tas = models.ManyToManyField(Account, related_name="tas", blank=True)

    def __str__(self):
        return self.name
