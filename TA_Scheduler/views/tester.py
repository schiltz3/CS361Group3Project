from django.shortcuts import render
from django.views import View


class TestHomePage(View):
    def get(self, request):
        return render(request, "testhome.html")
