from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from home_app.models import UserModel
from .models import GiftCodeModel, SiteRewardTempModel, SiteRewardTempModel
from home_app.views import get_user_ip
from django.core.cache import cache
import time

# Create your views here.


class EarnMoneySite(View):
    
    def get(self, request):
        ip_user = get_user_ip(request)
        cache_key_user = f'test{ip_user}'
          #check cache, chưa có sẽ về login
        try:
            context = {
                'coin_in_day':self.coin_day(request),
              
                'coin_total':cache.get(cache_key_user)['user'].money
                
            }
        except TypeError:
                return redirect('login')
        return render(request, 'earn_money_app.html', context = context)


    def time_reset_in_day(self, hour, minute, second):
        default_hour = 24
        default_min = 60
        default_sec = 60

        hour_remaining = default_hour - hour 
        min_remaining = default_min - minute 
        sec_remaining = default_sec - second

        #covert hour*3600, min*60
        covert_time_to_second = (hour_remaining * 60 * 60) + (min_remaining * 60) + (sec_remaining)

        return covert_time_to_second


    def coin_day(self, request):

        #set giá trị ban đầu
        coin_day = 0

        ip_user = get_user_ip(request)

        #lấy thời gian còn lại trong ngày để set cache coin đẫ lưu trong ngày 
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min
        second = time.localtime().tm_sec
        second_reset_cache = self.time_reset_in_day(hour, minute, second)
        
        cache_key_earn_coin_in_day = f'earn_coin_in_day_{ip_user}'
        cache_data_earn_coin_in_day = cache.get(cache_key_earn_coin_in_day, None)

        if not cache_data_earn_coin_in_day:
            data = {
                'coin':float(0)
            }
            cache.set(cache_key_earn_coin_in_day, data, timeout=second_reset_cache)

            coin_day = cache.get(cache_key_earn_coin_in_day)['coin']
            return coin_day

        coin_day = cache_data_earn_coin_in_day['coin']
        return coin_day





class EarnMoneyWeb1s(View):
    def get(self, request):
        return render(request, 'earn_money_web1s.html')






class EarnMoneyYoutube(View):
    def get(self, request):
        return render(request, 'earn_money_youtube.html')





class EarnMoneyTiktok(View):
    def get(self, request):
        return render(request, 'earn_money_tiktok.html')
    


class EarnMoneyFacebook(View):
    def get(self, request):
        return render(request, 'earn_money_facebook.html')



class EarnMoneyGetCoin(APIView):
    def get(self, request):
        return render(request, 'earn_money_get_coin.html')
    

    def post(self, request):

        giftcode = request.POST['code']
        access_token = request.POST['access_token']

        try:
            gift_in_DB = GiftCodeModel.objects.get(code = giftcode)

        except GiftCodeModel.DoesNotExist:
            return JsonResponse({
                        'status':'error', 
                        'message':'Mã nhận không chính xác hoặc hết hạn!'
                    })
        user = UserModel.objects.get(access_token = access_token)
       
        try:
            #save cache
            cache_key_user = f'test{user.ip_address}'
            cache_data_user = cache.get(cache_key_user)
            cache_data_user['user'].money += gift_in_DB.value
            cache.set(cache_key_user, cache_data_user)
            
        except TypeError:
            return JsonResponse({
                'status':'error',
                'message':"Lỗi server, acc được nhận phải truy cập lại vào web!"
            })
       #save DB
        user.money += gift_in_DB.value
        user.save()

        message_plus_coin = f'Thành công, +{gift_in_DB.value}$ vào tài khoản {user.username}' 

        gift_in_DB.delete()
        return JsonResponse({
            'status':'success',
            'message':message_plus_coin
        })
    





class HandleRewardSiteTemp(APIView):
    def get(self, request, endpoint):

        try:
            end_point_DB = SiteRewardTempModel.objects.get(endpoint = endpoint)
        except SiteRewardTempModel.DoesNotExist:
            return HttpResponse('<h1>Not Found</h1>')
        
        return render(request, 'reward_site_temp.html')
    
@method_decorator(csrf_exempt, name='dispatch')
class DeleteRewardSiteTemp(APIView):
    def delete(self, request):

        endpoint = request.data.get('endpoint')

        site_cover_endpoint = SiteRewardTempModel.objects.get(endpoint= endpoint)
        site_cover_endpoint.delete()
        try:
            site_cover_endpoint = SiteRewardTempModel.objects.get(endpoint=endpoint)
            site_cover_endpoint.delete()

            return JsonResponse({
                'status': 'success',
                'message': 'Xóa thành công'
            })
        except SiteRewardTempModel.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Endpoint không tồn tại'
            })

class HandlePlusMoneyByAccessToken(APIView):
    def post(self, request):
        try:
            endpoint = request.POST['endpoint']
            end_point_DB = SiteRewardTempModel.objects.get(endpoint = endpoint)
        except SiteRewardTempModel.DoesNotExist:
            return HttpResponse('<h1>Not Found</h1>')
        request_from_client = request.POST['request'] 

        if request_from_client == 'collect':
            
            access_token = request.POST['access_token']

            try:
                user = UserModel.objects.get(access_token = access_token)
            except UserModel.DoesNotExist:
                return JsonResponse({
                    'status':'error',
                    'message':"Access_token sai!"
                })

        
            try:
                #save cache
                cache_key_user = f'test{user.ip_address}'
                cache_data_user = cache.get(cache_key_user)
                cache_data_user['user'].money += 0.1
                cache.set(cache_key_user, cache_data_user)
                
            except TypeError:
                return JsonResponse({
                    'status':'error',
                    'message':"Lỗi server, acc được nhận phải truy cập lại vào web!"
                })
        #save DB
            user.money += 0.1
            user.save()

            message_plus_coin = f'Thành công, +{0.1}$ vào tài khoản {user.username}' 
            return JsonResponse({
                'status':'success',
                'message':message_plus_coin
            })


class CreateGiftcode(APIView):
    def post(self, request):
        try:
            endpoint = request.POST['endpoint']
            end_point_DB = SiteRewardTempModel.objects.get(endpoint = endpoint)
        except SiteRewardTempModel.DoesNotExist:
            return HttpResponse('<h1>Not Found</h1>')
        giftcode = request.POST['giftcode']
        GiftCodeModel.objects.create(code= giftcode, value= float(0.1))

        return JsonResponse({
            'status':'success',
            'message':'Tạo thành công, hãy sao chép giftcode và nhập ngay!'
        })