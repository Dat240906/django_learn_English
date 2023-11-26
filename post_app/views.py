from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView 
from .models import PostModel
from .forms import CreatePostForm
from django.core.cache import cache
# Create your views here.


class index(View):
    def get(self, request):
        post = PostModel.objects.all()
        return render(request, "post.html", {'posts':post})
    

def get_user_ip(request) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CreatePostApi(APIView):
    def post(self, request):
        ip_user = get_user_ip(request)
        form = CreatePostForm(request.POST, request.FILES, user_cache = cache.get(f'test{ip_user}')) 
        if not form.is_valid():
            print(request.FILES.get('img'))
            return JsonResponse({
                'success':False,
                'error':form.errors,
            })
        
 


        # user = cache.get(f'test{ip_user}')['user']
        # title = form.cleaned_data['title']
        # content = form.cleaned_data['content']
        # img = form.cleaned_data['img']  
        form.save()
        return JsonResponse({
                'success':True,
                'message':'success',
                
            })