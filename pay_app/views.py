from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
# Create your views here.


class PaySite(View):
    def get(self, request):
        return render(request, 'pay_app.html')
