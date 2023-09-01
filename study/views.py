from django.shortcuts import redirect, render
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
        

        ip_user = get_user_ip(request)

        cache_key = f'ip_{ip_user}_data'
        cache_data = cache.get(cache_key)


        dict_data = {
            'total_questions':len(questions),
            'user_question': list(questions),
            'used_question': [],
            'fail_question': {},
            'num_did_question': 0,
            'point': 0,
            'sai':False

        }

        if cache_data is None:
            cache.set(cache_key, dict_data, timeout=30 * 60)

        if len(list(questions)) < 4:
            return HttpResponse('Dữ liệu trong Db chưa đủ')
        cache_data = cache.get(cache_key)
        while True:
            question_main = random.choice(cache_data['user_question'])
            question_temp_1 = random.choice(cache_data['user_question'])
            question_temp_2 = random.choice(cache_data['user_question'])
            question_temp_3 = random.choice(cache_data['user_question'])


            if question_main not in cache_data['used_question'] and question_temp_1.answer.get() != question_temp_2.answer.get() and question_temp_1.answer.get() != question_temp_3.answer.get() and question_temp_2.answer.get() != question_temp_3.answer.get() and question_main != question_temp_1 and question_main != question_temp_2 and question_main != question_temp_3:
                break
            

        # xáo chộn các câu trả Lời
        data_ANSWER_main = [question_main.answer.get(),  question_temp_1.answer.get(), question_temp_2.answer.get(), question_temp_3.answer.get()]
        random.shuffle(data_ANSWER_main)


        context = {
            'total_questions':cache_data['total_questions'],
            'question_main':question_main,
            'answer_temp_1':data_ANSWER_main[0],
            'answer_temp_2':data_ANSWER_main[1],
            'answer_temp_3':data_ANSWER_main[2],
            'answer_temp_4':data_ANSWER_main[3],
            'used_question':len(cache_data['used_question'])+1
        }


        return render(request, 'tracnghiem.html', context)
        # dict_ = 'to work as a/an + N(job):làm nghề gì. shift:ca làm việc. night shift:ca đêm. biology:sinh học . biologist:nhà sinh học. biological:thuộc về sinh học. to join hands = to work together: chung tay. to be willing + V(bare):sẵn lòng làm gì. household chores:việc nhà. to run the hoursehold: điều hành gia đình. to make sure: đảm bảo. rush=hurry=go quickly : vội vã. responsibility: trách nhiệm. to be + responsible for V-ing/sth: chịu trách nhiệm về việc gì. to take the responsibility for + V-ing/sth: đảm nhận trách nhiệm về việc gì. pressure: áp lưc. to be + under pressure: bị áp lực. caring:quan tâm. to take out: xóa bỏ .mischievous:tinh nghịch. mischief:sự tinh nghịch. give sb a hand = help sb:  giúp đỡ ai . obedient:ngoan ngoãn. disobedient: không ngoan. obeđience: sự ngoan ngoãn. obey:nghe theo. close-knit: gắn bó. be + supportive of sb: tương trợ ai. frankly: 1 cách thẳng thắn. frank: trung thực . to make a decision:đưa ra quyết định.  solve:giải quyết. solution: giải pháp. secure = safe:an toàn . security:bảo mật. to be + crowded with: đông đúc (ngươiè). wel_behaved: biết cư xử tốt. confidence: sự tự tin. to be + confidence : tin tưởng . to be + based on = to rely on: dự trên nền tẳng. come up = appear/happend : xảy ra. hard-working: chăm chỉ. to be + good at + V-ing: giỏi về cái gì  '
        
        
        # pairs = dict_.split('. ')

        # dictionary = {}

        # for pair in pairs:
        #     parts = pair.split(':', 1)
            
        #     if len(parts) == 2:
        #         key, value = parts
        #         dictionary[key] = value
            
    def post(self, request):

        result = request.POST.get('result', None)
        question_main = request.POST.get('question_response')

        if result == None:
            return redirect('tracnghiem')

        ip_user = get_user_ip(request)

        cache_key = f'ip_{ip_user}_data'
        cache_data = cache.get(cache_key)



        #tính toán cộng  điểm
        

        AW = QuestionsModel.objects.get(question = question_main)

  
        list_ = cache_data['used_question']
        list_.append(AW)
        cache_data['used_question'] = list_
        cache.set(cache_key, cache_data, timeout=30 * 60)

        if str(AW.answer.get())==str(result):
            cache_data['point'] += 10/cache_data['total_questions']
            cache_data['num_did_question'] += 1
            cache.set(cache_key, cache_data, timeout=30 * 60)
        else:
            if 'fail_question' not in cache_data:
                cache_data['fail_question'] = {} 
            dict_ = cache_data['fail_question']
            dict_[str(question_main)] = (str(result), str(AW.answer.get()))
            cache_data['fail_question'] = dict_
            cache_data['sai']=True
            cache.set(cache_key, cache_data,timeout=30 * 60  )
        
        context = {
            'total_questions':cache_data['total_questions'],
            'num_did_question':cache_data['num_did_question'],
            'point':cache_data['point'],
            'items_3': cache_data['fail_question'].items(),
            'sai':cache_data['sai']
        }      
        if len(cache_data['used_question']) == len(cache_data['user_question']):
            # return HttpResponse(cache_data['fail_question'].items())
            return render(request, 'end2.html', context)
        

        return redirect('tracnghiem')
    
class Tuluan(View):
    def get(self, request):
            # Truy vấn tất cả câu hỏi từ cơ sở dữ liệu
        questions = AnswersModel.objects.all()
        

        ip_user = get_user_ip(request)

        cache_key = f'ip_{ip_user}_data'
        cache_data = cache.get(cache_key)
        if cache_data is None:
            cache_data = {
                'total_questions': len(questions),
                'user_question': list(questions),
                'used_question': [],
                'fail_question': {},
                'num_did_question': 0,
                'point': 0,
                'sai':False
            }
            cache.set(cache_key, cache_data, timeout=30 * 60)

        

      

        # if cache_data is None:
        #     cache.set(cache_key, dict_data, timeout=30 * 60)

        while True:
            question_main = random.choice(cache_data['user_question'])
            # random.choice(cache_data['user_question'])


            if question_main not in cache_data['used_question']:
                break
            
        context = {
            'total_questions':cache_data['total_questions'],
            'question_main':question_main,
            'used_question':len(cache_data['used_question'])+1
        }
        return render(request, 'tuluan.html', context)
    

    def post(self, request):

        result = request.POST.get('result', None)  
        if result is None or result == '':
            return redirect('tuluan')
        
        #câu hỏi trong DB là câu trả lời của user
        question_main =  request.POST.get('question_main') 

        ip_user = get_user_ip(request)

        cache_key = f'ip_{ip_user}_data'
        cache_data = cache.get(cache_key)


        QS = AnswersModel.objects.get(answer = question_main)
        AW = QS.question.question

  
        list_ = cache_data['used_question']
        list_.append(AW)
        cache_data['used_question'] = list_
        cache.set(cache_key, cache_data, timeout=30 * 60)
        if str(AW)==str(result):

            cache_data['point'] += 10/cache_data['total_questions']
            cache_data['num_did_question'] += 1
            cache.set(cache_key, cache_data, timeout=30 * 60)
        else:
            if 'fail_question' not in cache_data:
                cache_data['fail_question'] = {} 
            dict_ = cache_data['fail_question']
            dict_[str(question_main)] = (str(result), str(AW))
            cache_data['fail_question'] = dict_
            cache_data['sai']=True
            cache.set(cache_key, cache_data,timeout=30 * 60  )
        
        context = {
            'total_questions':cache_data['total_questions'],
            'num_did_question':cache_data['num_did_question'],
            'point':cache_data['point'],
            'items_3': cache_data['fail_question'].items(),
            'sai':cache_data['sai']
        }      
        if len(cache_data['used_question']) == len(cache_data['user_question']):
            # return HttpResponse(cache_data['fail_question'].items())
            return render(request, 'end.html', context)
        

        return redirect('tuluan')


class End(View):

    def get(self, request):

        pass


def reset(request):

    questions = QuestionsModel.objects.all()
    ip_user = get_user_ip(request)

    cache_key = f'ip_{ip_user}_data'


    dict_data = {
        'total_questions':len(questions),
        'user_question': list(questions),
        'used_question': [],
        'fail_question':{},
        'num_did_question': 0,
        'point': 0,
        'sai':False

        }
    cache.set(cache_key, dict_data, timeout=24*60*60)
    

    return redirect('index')
def reset_TN(request):

    questions = QuestionsModel.objects.all()
    ip_user = get_user_ip(request)

    cache_key = f'ip_{ip_user}_data'


    dict_data = {
        'total_questions':len(questions),
        'user_question': list(questions),
        'used_question': [],
        'fail_question':{},
        'num_did_question': 0,
        'point': 0,
        'sai':False

        }
    cache.set(cache_key, dict_data, timeout=24*60*60)
    

    return redirect('tracnghiem')



def reset_TL(request):

    questions = AnswersModel.objects.all()
    ip_user = get_user_ip(request)

    cache_key = f'ip_{ip_user}_data'


    dict_data = {
        'total_questions':len(questions),
        'user_question': list(questions),
        'used_question': [],
        'fail_question':{},
        'num_did_question': 0,
        'point': 0,
        'sai':False

        }
    cache.set(cache_key, dict_data, timeout=24*60*60)
    

    return redirect('tuluan')


def return_dict(str):
    pairs = str.split('.')

    dictionary = {}

    for pair in pairs:
        parts = pair.split(':', 1)
        
        if len(parts) == 2:
            key, value = parts
            dictionary[key] = value
    return dictionary
class Admin(View):
    def get(self, request):
        
        data = StorageDataModel.objects.all()
        
            
        
        context  = {
            'data':data
        }
        return render(request, 'admin.html', context)
        

class HandleAdmin(View):
    def post(self, request, method):

        get = request.POST

        #add
        if method == 'add':
            name_data = get.get('name_data')
            data = get.get('data')
            StorageDataModel.objects.create(name_data = name_data, data = data)
            return redirect('ptd_admin')
        

        

        #update
        QuestionsModel.objects.all().delete()
        name_data = get.get('name_data')
        DB = StorageDataModel.objects.get(name_data=name_data)
        
        data_get = DB.data
        dict_data = return_dict(str(data_get))

        for key, value in dict_data.items():
            question = QuestionsModel.objects.create(question=key)
            AnswersModel.objects.create(question=question, answer = value)
        return redirect('ptd_admin')