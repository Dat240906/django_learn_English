from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
# Create your views here.


class DocumentSite(View):
    def get(self, request):
        return render(request, 'document.html')
