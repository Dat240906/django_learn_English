from django.shortcuts import render
from django.views import View
from .models import PostModel

# Create your views here.


class index(View):
    def get(self, request):
        post = PostModel.objects.all()
        return render(request, "post.html", {'posts':post})