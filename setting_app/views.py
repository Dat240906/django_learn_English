from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from django.views import View
from home_app.models import UserModel, NotificationCommomModel
from home_app.views import get_user_ip
from django.core.cache import cache
from rest_framework.views import APIView 

# Create your views here.


class SettingSite(View):
    def get(self, request):
        try:
            ip_user = get_user_ip(request)

            cache_key_user = f'test{ip_user}'
            cache_data_user = cache.get(cache_key_user)

            cache_key_noti = 'noti'
            cache_data_noti = cache.get(cache_key_noti)


            username = cache_data_user['user'].username
            money = cache_data_user['user'].money
            access_token = cache_data_user['user'].access_token
            noties = cache_data_noti['noties']

            context = {
                'username':username,
                'money':money,
                'access_token':access_token,
                'noties':noties
            }
            return render(request, 'setting.html', context=context)

        except:
            return redirect('login')
class ChangePasswordAPI(APIView):
    def post(self, request):
        
        ip_user = get_user_ip(request)
        cache_key_user = f'test{ip_user}'
        cache_data_user = cache.get(cache_key_user)

        password_in_db = cache_data_user['user'].password

        password_to_client = request.POST['password']
        new_password_to_client = request.POST['newpassword']

        if password_in_db == password_to_client:
            #thực hiện đổi trong cache và DB
            user_new = cache_data_user['user']
            user_new.password = new_password_to_client
            cache_data_user['user'] = user_new

            cache.set(cache_key_user, cache_data_user)


            user_model = UserModel.objects.get(ip_address = ip_user, username = cache_data_user['username']) 
            user_model.password = new_password_to_client
            user_model.save()

            return JsonResponse({
                'success':True,
                'message':'Success'
            })
        return JsonResponse({
            'success':False,
            'message':'Mật khẩu không đúng!'
        })




