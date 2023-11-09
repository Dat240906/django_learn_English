from django.shortcuts import render
from rest_framework.views import APIView 
from .serializers import UserSerializer
from django.http import JsonResponse
from study.models import UserModel




# Create your views here.
def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class Home(APIView):
    def get(self, request):
        return render(request, 'home.html')
    

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

        
        UserModel.objects.create(message = 'Không có',username=username, password= password, ip_address = ip_user)
        data_response = {
                    'success':True,
                    'redirect_url': '/',
                    'message':'Tạo tài khoản thành công'
                }
        return JsonResponse(data_response)