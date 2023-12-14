from calendar import c
from django.shortcuts import render,redirect
from django.views import View
from rest_framework.views import APIView 
from .serializers import UserSerializer
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from django.utils import timezone
from .models import UserModel, NotificationCommomModel
from post_app.models import LikeModel, PostModel, CommentModel

from django.core.serializers import serialize

def convert_list_to_json(comment_list):
    # Sử dụng hàm serialize để chuyển danh sách CommentModel thành JSON
    serialized_comments = serialize('json', comment_list)

    # Trả về JSON đã được chuyển đổi
    return serialized_comments



# Create your views here.
def get_user_ip(request) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



#điều chỉnh giờ do server chênh lêhcj 7h
def add_hours_to_time(original_time, hours_to_add):
    return original_time + timezone.timedelta(hours=hours_to_add)



class APIGetPostComment(APIView):
    def get(self, request):
        request_for = request.GET

        post_id = request_for.get('post_id')
        try:
            container_comments = False
            #lấy bài viết
            cache_post_key = 'allpost'
            cache_post_data = cache.get(cache_post_key)
            #lấy comment thuộc về bài viết
            cache_comment_key = 'allcomment'            
            cache_comment_data = cache.get(cache_comment_key, [])
            
            for item in cache_post_data:
                if item.post_id == post_id:
                    post = item
                    break
            #điều chỉnh lại giờ chênh lệch
            post.create_at = add_hours_to_time(post.create_at, 7)
            #lấy comment thuộc về post
            if not cache_comment_data:
                try:
                    comments = CommentModel.objects.filter(post=post).order_by('-create_at')
                    for comment in comments:
                        cache_comment_data.append([post_id, comment])
                    cache.set(cache_comment_key, cache_comment_data)
                except CommentModel.DoesNotExist:
                    container_comments = False
            # cache đã chứa comment
            cache_comment_data = cache.get(cache_comment_key, [])
            #lọc comment thuộc về bài viết

            if cache_comment_data:
                container_comments = []
                for item in cache_comment_data: #itemm dạng [post_id, comment]
                    if item[0] == post_id:
                        container_comments.append(item[1])

            #nếu đã duyệt qua hết mà không kiếm được comment thì trả về luôn
            if not container_comments:
                container_comments = False
            else:
            #điều chỉnh lại thời gian bị lệch so với server
                for comment in container_comments:
                    comment.create_at = add_hours_to_time(comment.create_at, 7)
                
                #hoàn tất comments -> chuyển đổi thành json từ list
                container_comments = convert_list_to_json(container_comments)
            try:
                img = post.img.url[len('media/'):]
            except:
                img = False
            data_response = {
                'success':True,
                'post': {
                    'username':post.user.username,
                    'avatar':post.user.avatar.url[len('media/'):],
                    'img':img,
                    'time':post.create_at.strftime("%H:%M - %d.%m.%Y"),
                    'title':post.title,
                    'content':post.content,
                    'comments':container_comments,
                },


            }
            return JsonResponse(data_response)
        except PostModel.DoesNotExist:
            data_response = {
                'success':False,
                'post_id':post_id
                }

            return JsonResponse(data_response) 
class Home(APIView):
    def get(self, request):

        #xử lí login gần đây, nếu không có sẽ chuyển về login
        ip_user = get_user_ip(request)
        cache_key_user = f'test{ip_user}'
        cache_data_user = cache.get(cache_key_user)

        cache_post_key = 'allpost'
        cache_post_data = cache.get(cache_post_key, [])

        
        if cache_data_user and cache_data_user['active']:

            ## notification
            cache_key_noti = 'noti'
            cache_data_noti = cache.get(cache_key_noti)
            if not cache_data_noti:
                noties = NotificationCommomModel.objects.all().order_by('-create_at')
                for noti in noties:
                    noti.create_at = add_hours_to_time(noti.create_at, 7) 
                data = {
                    'noties':noties
                }
                cache.set(cache_key_noti, data)
            else:
                noties = cache_data_noti['noties']
            ## user
            user = cache_data_user['user']
            username = cache_data_user['username']
            money = user.money

            # post
            # posts = PostModel.objects.all().order_by('-create_at')
            if not cache_post_data:
                allpost = []
                posts = PostModel.objects.all().order_by('-create_at')
                for post in posts:
                    allpost.append(post)
                
                cache.set(cache_post_key, allpost)
            #xếp lại, comment nào vào đúng post ấy
            else:
                #lấy dữ liệu bằng cache, không liên quan đến DB
                posts = [post for post in cache_post_data]


            for post in posts:
                print(post)
                #thêm post
                post.create_at = add_hours_to_time(post.create_at, 7)

            if cache_data_user.get('list_post_liked', None) == None:
                try:
                    modelLike = LikeModel.objects.filter(user_liked = cache_data_user['username'])
                    list_post_liked = [item.post.post_id for item in modelLike]  
                except LikeModel.DoesNotExist:
                    list_post_liked = []
            else:
                list_post_liked = cache_data_user['list_post_liked']



            context = {
                'noties':noties,
                'username':username,
                'money':money,
                'posts':posts,
                'avatar':user.avatar,
                'posts':posts,
                'list_post_liked':list_post_liked
            }



            return render(request, 'home.html', context=context)

        cache_data_user={
            'ip_address':ip_user,
            'active':False
        }
        cache.set(cache_key_user, cache_data_user, timeout=60*60*24)
        return redirect('login')
class Login(APIView):
    def get(self, request):

        return render(request, 'login.html')
    def post(self,request):
        collect_data = UserSerializer(data=request.data)
        if not collect_data.is_valid():
            data_response = {
                'success':False,
                "message":'Dữ liệu quá kí tự cho phép',
            }
            return JsonResponse(data_response)
        
        try:
            username = collect_data.data['username']
            password = collect_data.data['password']
            

            #truy suất ở cache đã lưu khi tạo acc
            user = UserModel.objects.get(username=username)
            password_db = user.password
            if password != password_db:
                data_response = {
                        'success':False,
                        "message":'Sai mật khẩu hoặc tài khoản',
                    }
                return JsonResponse(data_response)
            user.save()
            # đăng nhập thành công thì sẽ lưu active để lưu cache login
            ip_user = get_user_ip(request)
            cache_key = f'test{ip_user}'
            cache_data = {
                'user':user,
                'ip_address':ip_user,
                'username':username,
                'active':True
            }
            cache.set(cache_key, cache_data, timeout=60*60*24)
            ######################################
            data_response = {
                'success':True,
                'redirect_url': '/',
                'message':'Đăng nhập thành công'
            }
            return JsonResponse(data_response)
            
        
        except UserModel.DoesNotExist:
            data_response = {
                    'success':False,
                    "message":'Sai mật khẩu hoặc tài khoản',
                }
            return JsonResponse(data_response)
        except:
            data_response = {
                    'success':False,
                    "message":'Lỗi không xác định',
                }
            return JsonResponse(data_response)



class Register(APIView):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        ip_user = get_user_ip(request)
        collect_data = UserSerializer(data=request.data)
        if not collect_data.is_valid():
            data_response = {
                    'success':False,
                    "message":'Dữ liệu quá kí tự cho phép',
                }
            return JsonResponse(data_response)
        # Xử lý đăng ký ở đây, ví dụ: tạo tài khoản và đăng nhập
        users = [user.username for user in UserModel.objects.all()]
        username = collect_data.data['username'].lower()
        password = collect_data.data['password'].lower()
        if username in users:
            data_response = {
                    'success':False,
                    "message":'Tài khoản đã tồn tại',
                }
            return JsonResponse(data_response)

        
        UserModel.objects.create(username=username, password= password, ip_address = ip_user)
        # đăng nhập thành công thì sẽ lưu active để lưu cache login
        ip_user = get_user_ip(request)

        user = UserModel.objects.get(ip_address = ip_user, username=username)
        cache_key = f'test{ip_user}'
        cache_data = {
            'user':user,
            'ip_address':ip_user,
            'username':username,
            'active':True
        }
        cache.set(cache_key, cache_data, timeout=60*60*24)
        ######################################
        
        data_response = {
                    'success':True,
                    'redirect_url': '/',
                    'message':'Tạo tài khoản thành công'
                }
        return JsonResponse(data_response)
    



class ShowCache(View):
    def get(self, request):
        data = cache.get('test127.0.0.1')
        return JsonResponse({'success':True})