from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.contrib.auth import login


class Login(View):
    def get(self, request):
        return render(request, "login/login.html", {})

    def post(self, request):
        user1 = AccountUtil.getAccountByUsername(request.POST["username"])
        if user1 is None:
            return render(
                request,
                "login/login.html",
                {"error": "Invalid username", "username": request.POST["username"]},
            )
        else:
            invalidPassword = user1.user.check_password(request.POST["password"])
        if not invalidPassword:
            return render(
                request,
                "login/login.html",
                {"error": "Invalid password", "password": request.POST["password"]},
            )
        else:
            request.session["username"] = user1.user.username

            # login as the user in django
            login(request, user1.user)
            if user1.user.groups.filter(name="admin").exists():
                return redirect("/dashboard/admin/")
            elif user1.user.groups.filter(name="instructor").exists():
                return redirect("/dashboard/instructor/")
            else:
                return redirect("/dashboard/ta/")
