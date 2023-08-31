from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *
import random
from django.core.cache import cache
# Create your views here.



class index(View):
    def get(self, request):
        return render(request, 'index.html')



def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
class Tracnghiem(View):
    def get(self, request):
        # Truy vấn tất cả câu hỏi từ cơ sở dữ liệu
        questions = QuestionsModel.objects.all()
        

        ipv6_address = get_user_ip(request)
        # key = (request)

        # # cache.set()
        # cache_key = f'ip_{key}_data'
        # cache_data = cache.get(cache_key)

        # dict_data = {
        #     'all_question': list(questions),
        #     'used_question': [],
        #     'point':0

        # }

        # if cache_data is None:
        #     cache.set(cache_key, dict_data, timeout=None)

        return HttpResponse(ipv6_address)
        # dict_ = 'to work as a/an + N(job):làm nghề gì, shift:ca làm việc, night shift:ca đêm, biology:sinh học , biologist:nhà sinh học, biological:thuộc về sinh học, to join hands = to work together: chung tay, to be willing + V(bare):sẵn lòng làm gì, household chores:việc nhà, to run the hoursehold: điều hành gia đình, to make sure: đảm bảo, rush=hurry=go quickly : vội vã, responsibility: trách nhiệm, to be + responsible for V-ing/sth: chịu trách nhiệm về việc gì, to take the responsibility for + V-ing/sth: đảm nhận trách nhiệm về việc gì, pressure: áp lưc, to be + under pressure: bị áp lực, caring:quan tâm, to take out: xóa bỏ ,mischievous:tinh nghịch, mischief:sự tinh nghịch, give sb a hand = help sb:  giúp đỡ ai , obedient:ngoan ngoãn, disobedient: không ngoan, obeđience: sự ngoan ngoãn, obey:nghe theo, close-knit: gắn bó, be + supportive of sb: tương trợ ai, frankly: 1 cách thẳng thắn, frank: trung thực , to make a decision:đưa ra quyết định,  solve:giải quyết, solution: giải pháp, secure = safe:an toàn , security:bảo mật, to be + crowded with: đông đúc (ngươiè), wel_behaved: biết cư xử tốt, confidence: sự tự tin, to be + confidence : tin tưởng , to be + based on = to rely on: dự trên nền tẳng, come up = appear/happend : xảy ra, hard-working: chăm chỉ, to be + good at + V-ing: giỏi về cái gì  '
        
        
        # pairs = dict_.split(', ')

        # dictionary = {}

        # for pair in pairs:
        #     parts = pair.split(':', 1)
            
        #     if len(parts) == 2:
        #         key, value = parts
        #         dictionary[key] = value
            