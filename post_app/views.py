from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView 
from .models import PostModel, CommentModel
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
            return JsonResponse({
                'success':False,
                'error':form.errors,
            })
        
 

        # img = form.cleaned_data['img']  
        post = form.save()

        cache_post_key = 'allpost'
        cache_post_data = cache.get(cache_post_key, [])

        cache_post_data.insert(0, post)
        cache.set(cache_post_key, cache_post_data, timeout=12* 30*24 *60*60)
        return JsonResponse({
                'success':True,
                'message':'success',
                
            })
    
class AddComment(APIView):
    def post(self, request):

        content = request.POST["content"]
        post_id = request.POST["post_id"]
        ip_user = get_user_ip(request)
        cache_key_user = f'test{ip_user}'
        cache_data_user = cache.get(cache_key_user)
        

        post = PostModel.objects.get(post_id=post_id)
        comment_new_create = CommentModel.objects.create(user = cache_data_user['user'].username, post=post, content_comment = content)
        #cộng lượt comment ở DB
        post.num_comment += 1
        post.save()


        cache_comments_key = 'allcomment'
        cache_comments_data = cache.get(cache_comments_key, [])
        cache_comments_data.append([post_id, comment_new_create]) 
        cache.set(cache_comments_key, cache_comments_data)
        #cộng lượt comment ở cache
        cache_post_key = 'allpost'
        cache_post_data = cache.get(cache_post_key)
        cache_comments_data = cache.get(cache_comments_key, [])
        num_comment = 0
        for comment in cache_comments_data:
            if comment[0] == post_id:
                num_comment +=1

        for post in cache_post_data:
            if post.post_id == post_id:
                post.num_comment = num_comment
                cache.set(cache_post_key,cache_post_data)
                break
        return  HttpResponse()
class CheckCache(View):
    def get(self, request):
        cache_post_key = 'allpost'
        cache_post_data = cache.get(cache_post_key)

        for value in cache_post_data.values():
            print(value.user.username)
        return HttpResponse('thanhf coong')
        

