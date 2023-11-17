from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
# Create your views here.


class EarnMoneySite(View):
    def get(self, request):
        return render(request, 'earn_money_app.html')







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