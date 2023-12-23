import requests
import json

# Địa chỉ URL của endpoint
url = "https://web1s.com/member/api/mass-shrinker"

# Dữ liệu bạn muốn gửi
data = {
    "urls": "https://www.facebook.com/profile.php?id=100054958380559"
}

# Header của request
headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    # Thêm các trường header cần thiết khác
}

# Thêm cookie vào header
cookies = {
    'lang': 'eyJpdiI6IjBrRkx2bHVIazJyOU53b3hDdktGaEE9PSIsInZhbHVlIjoiTGI3VkhJV1BUWmQxemJGNGlWN1oxaVBIY0o3SytQcThmcmNpeTN2Tm1YbmFKcmo3eE9VU2pJWFgrcXVUc2RHQyIsIm1hYyI6IjAwNzIzYjU4NGRhYTBiNGU0MDU2MWQyM2JlYjI5OTAzMTRiZGRhMmEyN2E4OGNjZTFkYzU1MDhiYWE0ZGNhMjkifQ',
    'csaas_user_id': '0.qhal42p3x8',
    'XSRF-TOKEN':'et8gupeiTht1ipyUHEqxv7JzPGPy2Aq6GMqkdat3',
    'web1s_session':'lpQhcVaPorFeelAky8SDiYfJJMxJRtJZLwP2UmFU'
    # Thêm các cookie cần thiết khác
}

# Tạo request
response = requests.post(url, data=json.dumps(data), headers=headers, cookies=cookies)

# Kiểm tra phản hồi từ server
if response.status_code == 200:
    # Xử lý dữ liệu nhận được từ server
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
