# ip_middleware.py
class GetClientIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lấy địa chỉ IP từ request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Gán địa chỉ IP vào biến request để có thể sử dụng trong toàn bộ views.py
        request.client_ip = ip

        response = self.get_response(request)
        return response
