from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.views import View
from .models import *
import random
from django.core.cache import cache
# Create your views here.

def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_key_from_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None 

class Login(View):
    def get(self, request):
        return render(request, 'login.html')        

    def post(self, request):
        ip_user = get_user_ip(request)
        username = request.POST.get('username', None)

        if username is None:
            return redirect('login')
        if len(username)>12:
            return redirect('login')
        UserModel.objects.create(ip_address=ip_user, username=username)
        return redirect('index')    

class index(View):

    # def __init__(self) -> None:
    #     request = HttpRequest()
    #     self.ip_user = get_user_ip(request)
    def get(self, request):
        ip_user = get_user_ip(request)
        try:

            cache_key = f'key_{ip_user}'
            cache_data = cache.get(cache_key)

            if cache_data is None:
                data = {
                    'data_unit':{},
                    #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
                    'tracnghiem':[[], {}, 0, 0],
                    'tuluan':[[], {}, 0, 0]
                }

                cache.set(cache_key, data, timeout=24*60*60)

            
          

            #xét sếp hạng & data_unit & username
            count_pass_all = UserModel.objects.all()
            user = UserModel.objects.get(ip_address = ip_user)
            data_unit = StorageDataModel.objects.all()

            list_user = []
            list_XH = []
            for user_ in count_pass_all:
                list_XH.append(user_.count_pass)
                list_user.append(user_)
            
            sorted_list_user = sorted(list_user, key=lambda user: user.count_pass, reverse=True)

            # # Kết hợp list_user và list_XH lại với nhau để sắp xếp cùng nhau
            # combined_list = list(zip(list_XH, list_user))

            # # Sắp xếp combined_list theo giá trị của list_XH (giảm dần)
            # sorted_combined_list = sorted(combined_list, reverse=True)

            # # Tách lại list_XH và list_user sau khi đã sắp xếp
            # sorted_list_XH, sorted_list_user = zip(*sorted_combined_list)

            user_XH = sorted_list_user.index(user) + 1
            context = {
                'user':user,
                'data_unit':data_unit,
                'user_XH':user_XH
            }
            return render(request, 'index.html', context)
        except UserModel.DoesNotExist:
            return redirect('login')
        
    def post(self, request):

        name_data = request.POST.get('unit', 'None')
        exam_type = request.POST.get('submit_button')

        if name_data == 'None':
            return redirect('index')
        


        #lấy data_unit
        data_unit = StorageDataModel.objects.get(name_data = name_data)

        #lấy cache dựa theo key+ip
        ip_user = get_user_ip(request)
        cache_key = f'key_{ip_user}'
        cache_data = cache.get(cache_key)

        #xử lí data từ dạng "key:value.key:value" về dạng {key:value;key:value}
        pairs = data_unit.data.split('.')
        dictionary = {}

        for pair in pairs:
            parts = pair.split(':')
            
            if len(parts) == 2:
                key, value = parts
                dictionary[key] = value

        ##########################################
        data = {
            'data_unit':dictionary,
            #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
            'tracnghiem':[[], {}, 0, 0],
            'tuluan':[[], {}, 0, 0]
        }
        cache.set(cache_key, data, 24*60*60)
        # return HttpResponse(cache_data['data_unit'])#out put không là None
      
        if exam_type == 'tracnghiem':
            return redirect('tracnghiem')
        
        return redirect('tuluan')

class Tracnghiem(View):
    question_main = None
    def get(self, request):
        
        #lấy cache dựa theo key+ip
        ip_user = get_user_ip(request)
        cache_key = f'key_{ip_user}'
        cache_data = cache.get(cache_key)
        #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
        
        # cache_data = cache.get(cache_key)
        data_unit = cache_data['data_unit']

        random_vietanh = random.choice([1,2])
        if random_vietanh == 1:# câu hỏi là tiếng anh
            while True:
                question_main = random.choice([qs for qs in data_unit.keys()])
                question_temp_1 = random.choice([qs for qs in data_unit.keys()])
                question_temp_2 = random.choice([qs for qs in data_unit.keys()])
                question_temp_3 = random.choice([qs for qs in data_unit.keys()])

                AW_main = data_unit[question_main]
                AW_temp1 = data_unit[question_temp_1]
                AW_temp2 = data_unit[question_temp_2]
                AW_temp3 = data_unit[question_temp_3]
                if question_main not in cache_data['tracnghiem'][0] and AW_temp1 != AW_temp2 and AW_temp1 != AW_temp3 and AW_temp2 != AW_temp3 and question_main != question_temp_1 and question_main != question_temp_2 and question_main != question_temp_3:
                    break
        else:
            while True:
                question_main = random.choice([qs for qs in data_unit.values()])
                question_temp_1 = random.choice([qs for qs in data_unit.values()])
                question_temp_2 = random.choice([qs for qs in data_unit.values()])
                question_temp_3 = random.choice([qs for qs in data_unit.values()])

                AW_main = get_key_from_value(data_unit,question_main)
                AW_temp1 = get_key_from_value(data_unit,question_temp_1)
                AW_temp2 = get_key_from_value(data_unit,question_temp_2)
                AW_temp3 = get_key_from_value(data_unit,question_temp_3)
                if question_main not in cache_data['tracnghiem'][0] and AW_temp1 != AW_temp2 and AW_temp1 != AW_temp3 and AW_temp2 != AW_temp3 and question_main != question_temp_1 and question_main != question_temp_2 and question_main != question_temp_3:
                    break

        # xáo chộn các câu trả Lời
        data_ANSWER_main = [AW_main, AW_temp1, AW_temp2, AW_temp3]
        random.shuffle(data_ANSWER_main)

        #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
        context = {
            'total_questions':len(cache_data['data_unit']),
            'question_main':question_main,
            'answer_temp_1':data_ANSWER_main[0],
            'answer_temp_2':data_ANSWER_main[1],
            'answer_temp_3':data_ANSWER_main[2],
            'answer_temp_4':data_ANSWER_main[3],
            'used_question':len(cache_data['tracnghiem'][0])+1
        }


        return render(request, 'tracnghiem.html', context)

    def post(self, request):

        result = request.POST.get('result', None)
        question_main = request.POST.get('question_response')

        if result == None:
            return redirect('tracnghiem')

        ip_user = get_user_ip(request)

        cache_key = f'key_{ip_user}'
        cache_data = cache.get(cache_key)
        data_unit = cache_data['data_unit']
        data_tracnghiem = cache_data['tracnghiem']


        #tính toán cộng  điểm
        
        if question_main in [key for key in data_unit.keys()]:
            AW = data_unit[question_main]
        else:
            AW = get_key_from_value(data_unit, question_main)
        #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
        #thêm câu đã làm  
        list_ = data_tracnghiem[0]
        list_.append(question_main)
        data_tracnghiem[0] = list_
        cache.set(cache_key, cache_data, timeout=24*60*60)

        #xét tính đúng sai của câu hỏi
        if str(AW)==str(result):
            data_tracnghiem[3] += 10/len(data_unit)
            data_tracnghiem[2] += 1
            cache.set(cache_key, cache_data, timeout=24*60*60)
        else:
            _ = data_tracnghiem[1]
            _[str(question_main)] = (str(result), str(AW))
            data_tracnghiem[1] = _
            cache.set(cache_key, cache_data,timeout=24*60*60)
        
        context = {
            'total_questions':len(cache_data['data_unit']),
            'num_did_question':data_tracnghiem[2],
            'point':data_tracnghiem[3],
            'items_3': data_tracnghiem[1].items(),
            'sai':True if len(data_tracnghiem[1]) > 0 else False
        }      
        if len(data_tracnghiem[0  ]) == len(cache_data['data_unit']):
             #cộng số lần thi trong DB
            data_user = UserModel.objects.get(ip_address=ip_user)
            data_user.count_pass +=1
            data_user.save()
            return render(request, 'end2.html', context)
        

        return redirect('tracnghiem')
    
class Tuluan(View):
    def get(self, request):
        

        ip_user = get_user_ip(request)

        cache_key = f'key_{ip_user}'
        cache_data = cache.get(cache_key)


        #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]

        data_unit = cache_data['data_unit']
        data_tuluan = cache_data['tuluan']
        if cache_data is None:
            return redirect('index')



        # if cache_data is None:
        #     cache.set(cache_key, dict_data, timeout=24*60*60

        while True:
            question_main = random.choice([value for value in data_unit.values()])
            # random.choice(cache_data['user_question'])


            if question_main not in data_tuluan[0]:
                break
            
        context = {
            'total_questions':len(data_unit),
            'question_main':question_main,
            'used_question':len(data_tuluan[0])+1
        }
        return render(request, 'tuluan.html', context)
    

    def post(self, request):

        result = request.POST.get('result', None)  
        if result is None or result == '':
            return redirect('tuluan')

        
        ip_user = get_user_ip(request)

        cache_key = f'key_{ip_user}'
        cache_data = cache.get(cache_key)
        #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]

        data_unit = cache_data['data_unit']
        data_tuluan = cache_data['tuluan']
        #câu hỏi trong DB là câu trả lời của user
        question_main =  request.POST.get('question_main') 


        AW = get_key_from_value(data_unit, question_main)

  
        list_ = data_tuluan[0]
        list_.append(AW)
        data_tuluan[0] = list_
        cache.set(cache_key, cache_data, timeout=24*60*60)
        if str(result).strip() in str(AW):
#key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
            data_tuluan[3] += 10/len(data_unit)
            data_tuluan[2] += 1
            cache.set(cache_key, cache_data, timeout=24*60*60)
        else:
            _ = data_tuluan[1]
            _[str(question_main)] = (str(result), str(AW))
            data_tuluan[1] = _
            cache.set(cache_key, cache_data,timeout=24*60*60)
        
        context = {
            'total_questions':len(data_unit),
            'num_did_question':data_tuluan[2],
            'point':data_tuluan[3],
            'items_3': data_tuluan[1].items(),
            'sai':True if len(data_tuluan[1]) > 0 else False
        }      
        if len(data_tuluan[0]) == len(data_unit):

            #cộng số lần thi trong DB
            data_user = UserModel.objects.get(ip_address=ip_user)
            data_user.count_pass +=1
            data_user.save()
            return render(request, 'end.html', context)
        

        return redirect('tuluan')


class End(View):

    def get(self, request):

        pass


def reset(request):

    questions = QuestionsModel.objects.all()
    ip_user = get_user_ip(request)

    cache_key = f'ip_{ip_user}_data_cache_tracnghiem'
    cache_key_ = f'ip_{ip_user}_data_cache_tuluan'


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
    cache.set(cache_key_, dict_data, timeout=24*60*60)
    

    return redirect('index')
def reset_TN(request):

    ip_user = get_user_ip(request)
    cache_key = f'key_{ip_user}'

    data = {
            'data_unit':{},
            #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
            'tracnghiem':[[], {}, 0, 0],
            'tuluan':[[], {}, 0, 0]
        }

    cache.set(cache_key, data, timeout=24*60*60)

    return redirect('tracnghiem')



def reset_TL(request):

    ip_user = get_user_ip(request)
    cache_key = f'key_{ip_user}'

    data = {
            'data_unit':{},
            #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
            'tracnghiem':[[], {}, 0, 0],
            'tuluan':[[], {}, 0, 0]
        }

    cache.set(cache_key, data, timeout=24*60*60)


    return redirect('tuluan')


def return_dict(str):
    pairs = str.split('.')  

    dictionary = {}

    for pair in pairs:
        parts = pair.split(':')
        
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
        

           
        return redirect('ptd_admin')