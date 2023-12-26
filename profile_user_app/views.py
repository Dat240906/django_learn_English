import json
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.core.serializers import serialize
from home_app.views import get_user_ip
from django.core.cache import cache
from django.views import View
from django.http import JsonResponse
from home_app.models import UserModel
from .models import PayByBankModel, PayByMoMoModel, PayByPaypalModel

# Create your views here.


class ProfileSite(View):
    def get(self, request):
        try:
            # ip_user = get_user_ip(request)
            access_token = request.session['userModel']['access_token']


            cache_key_user = f'test{access_token}'
            cache_data_user = cache.get(cache_key_user)

            cache_key_noti = 'noti'
            cache_data_noti = cache.get(cache_key_noti)


            username = cache_data_user['user'].username
            money = cache_data_user['user'].money
            access_token = cache_data_user['user'].access_token
            noties = cache_data_noti['noties']
            email = cache_data_user['user'].email
            number_phone = cache_data_user['user'].number_phone
            address = cache_data_user['user'].address

            context = {
                'username':username,
                'money':money,
                'avatar':cache_data_user['user'].avatar,
                'access_token':access_token,
                'noties':noties,
                'email':email,
                'number_phone':number_phone,
                'address':address
            }
            return render(request, 'profile_user_app.html', context=context)

        except:
            return redirect('login')
        


class UpdateDataUserAPI(APIView):
    def post(self, request):

        # ip_user = get_user_ip(request)
        access_token = request.session['userModel']['access_token']

        cache_key_user = f'test{access_token}'
        cache_data_user = cache.get(cache_key_user)

        #nhận từ client
        username = request.POST.get('username', False)
        email = request.POST.get('email', False)
        number_phone = request.POST.get('number_phone', False)
        address = request.POST.get('address', False)
        

        all_username = UserModel.objects.all().values_list('username', flat=True)
        username_to_remove = cache_data_user['username']
        filtered_usernames = [username for username in all_username if username != username_to_remove]

        if username in filtered_usernames:
            return JsonResponse({
                'success':False,
                'message':'Name đã tồn tại!'
            }) 
        #save DB

        user_db = UserModel.objects.get(access_token = access_token)
        
        user_db.email = email
        user_db.number_phone = number_phone
        user_db.address = address

        user_db.save()
        #save cache
        dataUser = cache_data_user['user']
        dataUser.email = email
        dataUser.number_phone = number_phone
        dataUser.address = address
        
        cache_data_user['user'] = dataUser
        cache.set(cache_key_user, cache_data_user)


        return JsonResponse({
            'success':True,
            'message':'Đã chỉnh sửa!'
        })



class AddMethodAPI(APIView):
    def post(self, request):
        # ip_user = get_user_ip(request)
        access_token = request.session['userModel']['access_token']

        cache_key_user = f'test{access_token}'
        cache_data_user = cache.get(cache_key_user)

        method_pay = request.POST['method_pay']

        
        


        if method_pay == 'momo':
            #momo
            phone_number_momo = request.POST['phone_number_momo']
            try:
                PayByMoMoModel.objects.get(user = cache_data_user['user'], number_account = phone_number_momo)
                return JsonResponse({
                    'success':False,
                    'message':'Thông tin đã được thêm!'
                })
            except PayByMoMoModel.DoesNotExist:
                pass
            
            
            PayByMoMoModel.objects.create(user = cache_data_user['user'], number_account = phone_number_momo)
            return JsonResponse({
                'success':True,
                'message':'Lưu thông tin hoàn tất!'
            })
        elif method_pay == 'paypal':
            #paypal
            email_paypal = request.POST['email_paypal']

            try:
                PayByPaypalModel.objects.get(user = cache_data_user['user'], email_account = email_paypal)
                return JsonResponse({
                    'success':False,
                    'message':'Thông tin đã được thêm!'
                })
            except PayByPaypalModel.DoesNotExist:
                pass
            
            PayByPaypalModel.objects.create(user = cache_data_user['user'], email_account = email_paypal)
            return JsonResponse({
                'success':True,
                'message':'Lưu thông tin hoàn tất!'
            })
        elif method_pay == 'bank': 
            
            #bank
            name_bank = request.POST['name_bank']
            stk_bank = request.POST['stk_bank']
            name_acc_bank = request.POST['name_acc_bank']
            try:
                PayByBankModel.objects.get(user = cache_data_user['user'], name_bank = name_bank, name_account = name_acc_bank, number_account = stk_bank)
                return JsonResponse({
                    'success':False,
                    'message':'Thông tin đã được thêm!'
                })
            except PayByBankModel.DoesNotExist:
                pass
            

            PayByBankModel.objects.create(user = cache_data_user['user'], name_bank = name_bank, name_account = name_acc_bank, number_account = stk_bank)
            return JsonResponse({
                'success':True,
                'message':'Lưu thông tin hoàn tất!'
            })
        
        return JsonResponse({
            'success':False,
            'message':f'Lưu thông tin không hoàn tất{request.ERROR}'
        })
    



    

class GetPostsAPI(APIView):
    def get(self, request):

        list_post_of_user = []

        # ip_user = get_user_ip(request)
        access_token = request.session['userModel']['access_token']

        cache_key_user = f'test{access_token}'
        cache_data_user = cache.get(cache_key_user)

        cache_key_post = 'allpost'
        cache_data_post = cache.get(cache_key_post)

        # chuyển đổi từ queryset thành json
        json_data = serialize('json', cache_data_post)
        list_post_data = json.loads(json_data)


        for post in list_post_data:
            if post['fields']['user'] == cache_data_user['user'].id:
                list_post_of_user.append(post)

        return JsonResponse({
            'posts':list_post_of_user
        })