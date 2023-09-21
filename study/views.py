from re import U
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from .models import *
import random
from django.core.cache import cache
from .forms import *
from .serializers import NoficationsSerializer
from rest_framework.views  import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import base64
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText

def send_email(content, title, email_victim):
    # Thông tin xác thực OAuth2
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None

    def refresh_token():
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    # Kiểm tra xem đã có thông tin xác thực OAuth2 hay chưa
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Kiểm tra lại token
        if creds and creds.expired and creds.refresh_token:
            refresh_token()
    else:
        # Sử dụng key.json để xác thực
        creds = service_account.from_service_account_file(
            'key.json', scopes=SCOPES)
        
        # Làm mới token sau khi xác thực
        creds.refresh(Request())

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Tạo service Gmail
    service = build('gmail', 'v1', credentials=creds)

    # Tạo email
    message = MIMEText(content)
    message['to'] = email_victim
    message['subject'] = title

    # Gửi email
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    body = {'raw': raw_message}
    service.users().messages().send(userId='me', body=body).execute()
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
        cache.clear()
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    def post(self,request):
        form = LoginForm()
        ip_user = get_user_ip(request)
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username'].lower()
            password = login_form.cleaned_data['password']
            try:
                user = UserModel.objects.get(username=username)
                password_db = user.password
                if password == password_db:
                    user.ip_address = ip_user
                    user.save()
                    cache_key = f'key_{ip_user}'
                    data = {
                        'username':username,
                        'data_unit':{},
                        #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
                        'tracnghiem':[[], {}, 0, 0],
                        'tuluan':[[], {}, 0, 0]
                    }

                    cache.set(cache_key, data, timeout=24*60*60)


                    data_response = {
                        'success':True,
                        'redirect_url': '/'
                    }
                    return JsonResponse(data_response)
                
                data_response = {
                        'success':False,
                        "message":'*sai mật khẩu',
                    }
                return JsonResponse(data_response)
            except UserModel.DoesNotExist:
                data_response = {
                        'success':False,
                        "message":'*không tìm thấy tài khoản',
                    }
                return JsonResponse(data_response)
            
        data_response = {
                        'success':False,
                        "message":'*lỗi về dữ liệu chưa nhập đúng',
                    }
        return JsonResponse(data_response)

class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    def post(self, request):
        ip_user = get_user_ip(request)
        form = RegisterForm()
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # Xử lý đăng ký ở đây, ví dụ: tạo tài khoản và đăng nhập
            users = [user.username for user in UserModel.objects.all()]
            username = register_form.cleaned_data['username'].lower()
            if username in users:
                data_response = {
                        'success':False,
                        "message":'*tài khoản đã tồn tại',
                    }
                return JsonResponse(data_response)
            password = register_form.cleaned_data['password']
            confirm_password = register_form.cleaned_data['confirm_password']

            if password != confirm_password:
                data_response = {
                        'success':False,
                        "message":'*2 mật khẩu không trùng khớp',
                    }
                return JsonResponse(data_response)
            
            UserModel.objects.create(message = 'Không có',username=username, password= confirm_password, ip_address = ip_user)

            cache_key = f'key_{ip_user}'
            data = {
                'username':username,
                'data_unit':{},
                #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
                'tracnghiem':[[], {}, 0, 0],
                'tuluan':[[], {}, 0, 0]
            }

            cache.set(cache_key, data, timeout=24*60*60)
            data_response = {
                        'success':True,
                        'redirect_url': '/',
                    }
            return JsonResponse(data_response)
        data_response = {
                        'success':False,
                        "message":'*lỗi về dữ liệu chưa nhập đúng',
                    }
        return JsonResponse(data_response)


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
                    'username':cache_data['username'],
                    'data_unit':{},
                    #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
                    'tracnghiem':[[], {}, 0, 0],
                    'tuluan':[[], {}, 0, 0]
                }

                cache.set(cache_key, data, timeout=24*60*60)

            
          

            #xét sếp hạng & data_unit & username
            count_pass_all = UserModel.objects.all()
            user = UserModel.objects.get(username = cache_data['username'],ip_address = ip_user)
            data_unit = StorageDataModel.objects.all()

            list_user = []
            list_XH = []
            for user_ in count_pass_all:
                list_XH.append(user_.count_pass)
                list_user.append(user_)
            
            sorted_list_user = sorted(list_user, key=lambda user: user.count_pass, reverse=True)
            #hàm chuyển đổi str 
            def format_currency(number):
                try:
                    number = int(number)  # Chuyển chuỗi số thành số nguyên (int)
                    formatted_number = "{:,.0f}".format(number)  # Định dạng số và thêm dấu ',' ngăn cách hàng nghìn
                    return formatted_number
                except ValueError:
                    return "Invalid input"  # Trả về thông báo lỗi nếu đầu vào không hợp lệ


            #lấy money trong db
            money = format_currency(user.money)
            #lấy thông báo trong db
            
            message = user.message


            #lấy trạng thái thông báo trong db
            is_noti = user.is_seen_noti
            user_XH = sorted_list_user.index(user) + 1
            context = {
                'user':user,
                'data_unit':data_unit,
                'user_XH':user_XH, 
                'money':money,
                'notification':NotificationsModel.objects.get(pk=1).message,
                'noti_user':message,
                'is_noti':is_noti
            }
            return render(request, 'index.html', context)
        except UserModel.DoesNotExist:
            return redirect('login')
        except TypeError:
            return redirect('login')
    def post(self, request):
        try:
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
                'username':cache_data['username'],
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
        except TypeError:
            return redirect('login')

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
                if AW_main not in cache_data['tracnghiem'][0] and AW_temp1 != AW_temp2 and AW_temp1 != AW_temp3 and AW_temp2 != AW_temp3 and question_main != question_temp_1 and question_main != question_temp_2 and question_main != question_temp_3:
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
        question_main_ = request.POST.get('question_response')

        if result == None:
            return redirect('tracnghiem')

        ip_user = get_user_ip(request)

        cache_key = f'key_{ip_user}'
        cache_data = cache.get(cache_key)
        if cache_data is  None:
            return redirect('index')
        data_unit = cache_data['data_unit']
        data_tracnghiem = cache_data['tracnghiem']


        #tính toán cộng  điểm
        a= None
        if question_main in [key for key in data_unit.keys()]:
            AW = data_unit[question_main]
            
        else:
            AW = get_key_from_value(data_unit, question_main)
            a =get_key_from_value(data_unit, question_main)
            question_main = a
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
            _[str(question_main_)] = (str(result), str(AW))
            data_tracnghiem[1] = _
            cache.set(cache_key, cache_data,timeout=24*60*60)
    
   
        if len(data_tracnghiem[0]) == len(cache_data['data_unit']):
             #cộng số lần thi trong DB
            data_user = UserModel.objects.get(username = cache_data['username'],ip_address=ip_user)
            data_user.count_pass +=1
            #cộng tiền
            money_total = data_tracnghiem[2] * 500
            money_curren = int(data_user.money)
            money_curren += money_total
            data_user.money = str(money_curren)
            data_user.save()
            context = {
                'money':money_total,
                'total_questions':len(cache_data['data_unit']),
                'num_did_question':data_tracnghiem[2],
                'point':data_tracnghiem[3],
                'items_3': data_tracnghiem[1].items(),
                'sai':True if len(data_tracnghiem[1]) > 0 else False
        }   
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
        num_random = random.choice([True, False])
        #true: question là tiếng việt
        #false: question là tiếng anh
        if num_random:
            while True:
                question_main = random.choice([value for value in data_unit.values()])
                # random.choice(cache_data['user_question'])

                qs = get_key_from_value(data_unit, question_main)
                if qs not in data_tuluan[0]:
                    break
        else:
            while True:
                question_main = random.choice([value for value in data_unit.keys()])
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

        if question_main in [key for key in data_unit.keys()]:
            AW =data_unit[question_main]
        else:
            AW = get_key_from_value(data_unit, question_main)

  
        list_ = data_tuluan[0]
        list_.append(AW)
        data_tuluan[0] = list_
        cache.set(cache_key, cache_data, timeout=24*60*60)
        if str(result).strip().lower() in str(AW).strip().lower():
#key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
            data_tuluan[3] += 10/len(data_unit)
            data_tuluan[2] += 1


            cache.set(cache_key, cache_data, timeout=24*60*60)
        else:
            _ = data_tuluan[1]
            _[str(question_main)] = (str(result), str(AW))
            data_tuluan[1] = _
            cache.set(cache_key, cache_data,timeout=24*60*60)
        
        
        if len(data_tuluan[0]) == len(data_unit):
    
            #cộng số lần thi trong DB
            data_user = UserModel.objects.get(username = cache_data['username'],ip_address=ip_user)
            data_user.count_pass +=1
            #cộng tiền
            money_total = data_tuluan[2] * 500
            money_curren = int(data_user.money)
            money_curren += money_total
            data_user.money = str(money_curren)
            data_user.save()
            context = {
                'total_questions':len(data_unit),
                'money':money_total,
                'num_did_question':data_tuluan[2],
                'point':data_tuluan[3],
                'items_3': data_tuluan[1].items(),
                'sai':True if len(data_tuluan[1]) > 0 else False
                }  
            return render(request, 'end.html', context)
        

        return redirect('tuluan')


class End(View):

    def get(self, request):

        pass


def reset(request):
    
    try:
        ip_user = get_user_ip(request)
        cache_key = f'key_{ip_user}'

        cache_data = cache.get(cache_key)
        data = {
            'username':cache_data['username'],
            'data_unit':{},
            #key:[câu đã làm(list), câu sai(dict), tổng câu đã làm(int), điểm(int) ]
            'tracnghiem':[[], {}, 0, 0],
            'tuluan':[[], {}, 0, 0]
        }

        cache.set(cache_key, data, timeout=24*60*60)

        return redirect('index')
    except TypeError:
        return redirect('login')
def reset_TN(request):
    try:

        ip_user = get_user_ip(request)
        cache_key = f'key_{ip_user}'

        cache_data = cache.get(cache_key)

        cache_data['tracnghiem'] = [[], {}, 0, 0]

        cache.set(cache_key, cache_data, timeout=24*60*60)

        return redirect('tracnghiem')
    except:return redirect('index')


def reset_TL(request):
    try:
        ip_user = get_user_ip(request)
        cache_key = f'key_{ip_user}'

        cache_data = cache.get(cache_key)

        cache_data['tuluan'] = [[], {}, 0, 0]

        cache.set(cache_key, cache_data, timeout=24*60*60)


        return redirect('tuluan')
    except:return redirect('index')


def return_dict(str):
    pairs = str.split('.')  

    dictionary = {}

    for pair in pairs:
        parts = pair.split(':')
        
        if len(parts) == 2:
            key, value = parts
            dictionary[key] = value
    return dictionary
    
class NoficationsAPI(APIView):
    def post(self, request):
        ip_user = get_user_ip(request)
        cache_key = f'key_{ip_user}'
        cache_data = cache.get(cache_key)

        collect_data = NoficationsSerializer(data=request.data)

        if collect_data.is_valid():

            
            type = collect_data.data['type']

            if type == "change_noti_all":
                message = collect_data.data['message']
                # json = {
                #     'type':'change_noti_all',
                #     'message':'message'
                # }
                obj = NotificationsModel.objects.get(pk=1)
                obj.message = message
                obj.save()

            elif type == "change_noti_user":
                message = collect_data.data['message']
                # json = {
                #     'type':'change_noti_user',
                #     'ip_address':ip_user,
                #     'username':username,
                #     'message':'message'
                # }
                ip_user_from_admin = collect_data.data['ip_address']
                username_from_admin = collect_data.data['username']

                user_db = UserModel.objects.get(username=username_from_admin, ip_address = ip_user_from_admin)

                #thay đôiỉ noti
                user_db.message = message
                
                #thay đổi trạng thái thông báo
                user_db.is_seen_noti = True

                user_db.save()
            elif type == "is_noti":
                # json = {
                #     'type':'is_noti',
                # }

                user_db = UserModel.objects.get(username=cache_data['username'], ip_address = ip_user)
                user_db.is_seen_noti = False
                user_db.save()
            return Response(data='done', status=status.HTTP_200_OK)       
        return Response(data='er', status=status.HTTP_400_BAD_REQUEST)       

class Contact(View):
    def post(self, request):
        try:
                
            formModel = ContactForm(request.POST)

            if formModel.is_valid():
                formModel.save()
                return redirect('index')
            return redirect('index')
        except:
            return redirect('index')
class WithdrawMoney(View):
    def post(self, request):
        try:
            money = request.POST.get('money')
            ip_user = get_user_ip(request)
            data = request.POST
            cache_key = f'key_{ip_user}'
            cache_data = cache.get(cache_key)

            stk = data.get('stk')
            ttk = data.get('ttk')
            bank = data.get('bank')
            gmail = data.get('gmail')
            if money == '' or stk == '' or ttk =='' or gmail=='':
                return redirect('index')
            user = UserModel.objects.get(username = cache_data['username'],ip_address = ip_user)
            
            money_user = user.money
            if int(money)>=10000 and int(money)<= int(money_user):
                    WithdrawMoneyModel.objects.create(gmail=gmail,username=cache_data['username'], money=money,stk=stk, ttk=ttk, bank=bank)
                    a = int(user.money) - int(money)
                    user.money = str(a)
                    user.save()
                    send_email('Đơn rút tiền đã nhận được, chúng tôi sẽ cập nhận tình trạng của nó qua GMAIL và WEBSITE. ', 'Exam-Relax', gmail)
                    send_email(f'Hệ thống thông báo: [RÚT TIỀN] [{user.username}] [{money}đ]', 'Exam-Relax', 'phungthanhdat001@gmail.com')
                    
                    return redirect('index')
                
            return redirect('index')
        except TypeError:return redirect('index')
class Admin(View):
    def get(self, request):

        all_user = UserModel.objects.all()
        contacts = ContactModel.objects.all()
        user_withdraw_money = WithdrawMoneyModel.objects.all()

        context = {
            'users':all_user,
            'contacts':contacts,
            'all_menu':user_withdraw_money
        }
        return render(request, 'admin.html', context)

class HandleAdmin(View):



    def post(self, request, method):

            data = request.POST

            #add
            if method == 'adddata':
                name_data = data.get('name_data')
                data = data.get('data')
                StorageDataModel.objects.create(name_data = name_data, data = data)
                return redirect('admin_06')
            
            elif method == 'updatenoti':
            
                message = data.get('message')
                victim = data.get('victim')
                if victim == 'None' or victim is None:
                    return redirect('admin_06')

                elif victim == 'all':
                    user_model = UserModel.objects.all()
                    noti_model = NotificationsModel.objects.get(pk=1)

                    noti_model.message = message
                    noti_model.save()
                    return redirect('admin_06')

                else:

                    user_model = UserModel.objects.get(username = victim)
                    user_model.message = message
                    user_model.is_seen_noti = True
                    # victim is user
                    user_model.save()
                    return redirect('admin_06')
            elif method == 'replycontact':
                message = data.get('message')
                victim = data.get('victim')
                user_model = UserModel.objects.get(username = victim)
                user_model.message = message
                user_model.is_seen_noti = True
                # victim is user
                user_model.save()
                return redirect('admin_06')
            

            elif method == 'withdrawmoney':
                info_bill = data.get('pay').split('-')
                type = data.get('type')
                username = info_bill[0]
                note_message = data.get(f'note_{username}', None)

                money = info_bill[1]
                user = UserModel.objects.get(username = username)
                model = WithdrawMoneyModel.objects.get(username =username, money=money)
                if type == 'done':
                    model.delete()
                    user.message = f"Đơn rút {money}đ (Nhà cái đến từ Châu Âu lấy (99%) -> {int(money)//100}đ: <p style='color:green;display: inline-block'>THÀNH CÔNG</p>"
                    user.is_seen_noti = True
                    user.save()
                    send_email(f'Đơn rút {money}đ (Nhà cái đến từ Châu Âu lấy (99%) -> {int(money)//100}đ: THÀNH CÔNG', 'Exam-Relax', f'{model.gmail}' )
                    return redirect('admin_06')
                #hủy
                
                a = int(user.money)
                total = a+int(money)
                user.money = str(total)
                user.message = f'Đơn rút {money}đ: <p style="color:red;display: inline-block">BỊ TỪ CHỐI</p>, lí do:{note_message}'
                user.is_seen_noti = True
                user.save()
                send_email(f'Đơn rút {money}đ: BỊ TỪ CHỐI, lí do:{note_message}', 'Exam-Relax', f'{model.gmail}' )
                model.delete()
                return redirect('admin_06')
            return redirect('admin_06')