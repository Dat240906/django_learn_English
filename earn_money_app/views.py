from math import e
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from home_app.models import UserModel
from .models import GiftCodeModel,linkWeb1sStorage, SiteRewardTempModel, SiteRewardTempModel
from home_app.views import get_user_ip
from django.core.cache import cache
import time
import socket

# Create your views here.


class EarnMoneySite(View):
    def getInfoUser(self, request):
        """get username, money, noties, avatar"""
        access_token = request.session['userModel']['access_token']

        cache_key_user = f'test{access_token}'
        
        cache_data_user = cache.get(cache_key_user)

        cache_key_noti = 'noti'
        cache_data_noti = cache.get(cache_key_noti)

        
        username = cache_data_user['user'].username
        
        money = cache_data_user['user'].money
        noties = cache_data_noti['noties']
        avatar =cache_data_user['user'].avatar

        return username, money, noties, avatar
    def get(self, request):
        try:
            # ip_user = get_user_ip(request)
            access_token = request.session['userModel']['access_token']
            cache_key_user = f'test{access_token}'

            username, money, noties, avatar = self.getInfoUser(request)
            #check cache, chưa có sẽ về login
            try:
                context = {
                    'coin_in_day':self.coin_day(request),
                    'username':username,
                    'money':money,
                    'noties':noties,
                    'avatar':avatar,
                    'coin_total':cache.get(cache_key_user)['user'].money
                    
                }
            except TypeError:
                    return redirect('login')
            return render(request, 'earn_money_app.html', context = context)
        except TypeError:
            return redirect('login')
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





class EarnMoneyWeb1s(EarnMoneySite, View):
    def get(self, request):
        try:
            username, money, noties, avatar = self.getInfoUser(request)
        except TypeError:
            return redirect('login')


        context = {
            'username':username,
            'money':money,
            'noties':noties,
            'avatar':avatar
        }
        return render(request, 'earn_money_web1s.html', context = context)






class EarnMoneyYoutube(EarnMoneySite, View):
    def get(self, request):
        try:
            username, money, noties, avatar = self.getInfoUser(request)
        except TypeError:
            return redirect('login')

        context = {
            'username':username,
            'money':money,
            'noties':noties,
            'avatar':avatar
        }
        return render(request, 'earn_money_youtube.html', context = context)





class EarnMoneyTiktok(EarnMoneySite, View):
    def get(self, request):
        try:
            username, money, noties, avatar = self.getInfoUser(request)
        except TypeError:
            return redirect('login')

        context = {
            'username':username,
            'money':money,
            'noties':noties,
            'avatar':avatar
        }
        return render(request, 'earn_money_tiktok.html', context = context)
    


class EarnMoneyFacebook(EarnMoneySite, View):
    def get(self, request):
        try:
            username, money, noties, avatar = self.getInfoUser(request)
        except TypeError:
            return redirect('login')

        context = {
            'username':username,
            'money':money,
            'noties':noties,
            'avatar':avatar
        }
        return render(request, 'earn_money_facebook.html', context = context)



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
            access_token = request.session['userModel']['access_token']

            cache_key_user = f'test{access_token}'
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
            access_token = request.session['userModel']['access_token']
            site_reward = SiteRewardTempModel.objects.get(endpoint = endpoint)
            
            user_joined = site_reward.list_access_token_user_retrieved

            #nếu chưa có ai vào web thì chấp nhận user này vào và thêm accesstoken
            if not user_joined:
                user_joined[access_token] = access_token
                site_reward.list_access_token_user_retrieved = user_joined
                site_reward.save()
            #nếu có người vào rổi thì xem phải là user cũ không, kh phải sẽ không cho vào 
            else:
                try:
                    #nếu lấy phải accestoken lạ sẽ lỗi keyerror
                    user_joined[access_token]
                except KeyError:
                    return HttpResponse('<h1>Not Found</h1>') 

                

        except SiteRewardTempModel.DoesNotExist:
            return HttpResponse('<h1>Not Found</h1>')
        
        #xử lí lỗi không lấy đươc accestoken
        except TypeError:
            return redirect('login')
        return render(request, 'reward_site_temp.html')
    
@method_decorator(csrf_exempt, name='dispatch')
class DeleteRewardSiteTemp(APIView):
    def delete(self, request):

        endpoint = request.data.get('endpoint')
        #xóa web reward
        site_cover_endpoint = SiteRewardTempModel.objects.get(endpoint= endpoint)
        site_cover_endpoint.delete()

        # thêm accesstoken user vào link để chỉ rằng người này đã vào link này rồi



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
            
            access_token = request.session['userModel']['access_token']

            try:
                user = UserModel.objects.get(access_token = access_token)
            except UserModel.DoesNotExist:
                return JsonResponse({
                    'status':'error',
                    'message':"Access_token sai!"
                })

        
            try:
                #save cache
                access_token = request.session['userModel']['access_token']

                cache_key_user = f'test{access_token}'
                cache_data_user = cache.get(cache_key_user)
                cache_data_user['user'].money += float(0.1)
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
    




class getJobWeb1sAPI(APIView):
    def get(self, request):
        access_token = request.session['userModel']['access_token']

        all_job = linkWeb1sStorage.objects.all()
        list_job_of_user = []
        for job in all_job:
            access_token_in_job = job.list_access_token_user_retrieved.get(access_token, False)

            #tìm job mà user chưa làm 
            if not access_token_in_job:

                list_job_of_user.append(job)

        jobs = [job.link for job in list_job_of_user]
        
        return JsonResponse({
            'jobs':jobs # jobs = [oj1, oj2]
        })
    


class CreatelinkWeb1s(APIView):


    def get(self, request):
        # Lấy địa chỉ IP của máy chủ từ yêu cầu HTTP
        server_ip = request.get_host().split(":")[0]

        return JsonResponse({
            'ip': server_ip
        })