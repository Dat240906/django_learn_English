from calendar import c
from django.shortcuts import render,redirect
from rest_framework.views import APIView 
from .serializers import UserSerializer
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from django.utils import timezone
from .models import UserModel, NotificationCommomModel
from post_app.models import PostModel, CommentModel




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
            post = PostModel.objects.get(post_id=post_id) 
            #điều chỉnh lại giờ chênh lệch
            post.create_at = add_hours_to_time(post.create_at, 7)
            #lấy comment thuộc về post
            comments = CommentModel.objects.filter(post=post).order_by('-create_at')

            for comment in comments:
                comment.create_at = add_hours_to_time(comment.create_at, 7)

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
        cache_key = f'test{ip_user}'
        cache_data = cache.get(cache_key)

        if cache_data and cache_data['active']:

            ## notification
            noties = NotificationCommomModel.objects.all().order_by('-create_at')
            for noti in noties:
                noti.create_at = add_hours_to_time(noti.create_at, 7) 
            ## user
            user = UserModel.objects.get(username=cache_data['username'])
            username = user.username
            money = user.money

            # post
            posts = PostModel.objects.all().order_by('-create_at')

            #xếp lại, comment nào vào đúng post ấy
            post_and_comment_them = []   # [[post1, comment_of_post1], [post2, comment_of_post2]]
            for post in posts:
                #thêm post
                list_ = []
                post.create_at = add_hours_to_time(post.create_at, 7)
                list_.append(post)

                #thêm comment
                comment = CommentModel.objects.filter(post=post).order_by('-create_at')
                list_.append(comment)

                #Thêm vào list tổng
                post_and_comment_them.append(list_)

            
            
            #sau này muốn dùng js để gọi cmt thì tìm bằng post_id (cho post_id của post bằng với post_id của comment khi comment)



            context = {
                'noties':noties,
                'username':username,
                'money':money,
                'posts':posts,
                'avatar':user.avatar,
                'post_and_comment_them':post_and_comment_them,
            }



            return render(request, 'home.html', context=context)

        cache_data={
            'ip_address':ip_user,
            'active':False
        }
        cache.set(cache_key, cache_data, timeout=60*60*24)
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

        

        # đăng nhập thành công thì sẽ lưu active để lưu cache login
        ip_user = get_user_ip(request)
        cache_key = f'test{ip_user}'
        cache_data = {
            'ip_address':ip_user,
            'username':username,
            'active':True
        }
        cache.set(cache_key, cache_data, timeout=60*60*24)
        ######################################
        UserModel.objects.create(username=username, password= password, ip_address = ip_user)
        data_response = {
                    'success':True,
                    'redirect_url': '/',
                    'message':'Tạo tài khoản thành công'
                }
        return JsonResponse(data_response)