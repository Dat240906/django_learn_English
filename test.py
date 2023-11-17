import requests
import json

url = "https://web1s.com/member/api/links"

headers = {
    "Content-Type": "application/json;charset=UTF-8",
    'Cookie':'lang=eyJpdiI6IjBrRkx2bHVIazJyOU53b3hDdktGaEE9PSIsInZhbHVlIjoiTGI3VkhJV1BUWmQxemJGNGlWN1oxaVBIY0o3SytQcThmcmNpeTN2Tm1YbmFKcmo3eE9VU2pJWFgrcXVUc2RHQyIsIm1hYyI6IjAwNzIzYjU4NGRhYTBiNGU0MDU2MWQyM2JlYjI5OTAzMTRiZGRhMmEyN2E4OGNjZTFkYzU1MDhiYWE0ZGNhMjkifQ%3D%3D; csaas_user_id=0.qhal42p3x8; triggeredForPjlHFsfb=ia8mhd2xti; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IlhqS3FYWmFKQXFoY1VpcCthcHRyU1E9PSIsInZhbHVlIjoiS0hiVDN4QkZoeExOeE01VEoxS3J3bmJ4dG8zdWtveHlTRkVxZkFhSE1UZml6cXcycXRuSG9QSkVGWC9KZEw5bjhCVEVjUXVIbDR3V3hWUTFxU0Z2Q3JFbkRCVVc2U1lZem4zNzh0WjZrM0VoV2hMUE5yRmhYVlVITUxYNCt0NzRjbXhYQ0FsNndmR1Npb1gyM0VFVGRNVTZZbFNWUWp1SFZqOVBVSm04Z0JjQzVDRDFqSDFKNkpiNFJGNkVNMXRPdHVwU1A4bE1ra3dBMWZ6dGcwRDFsM0dtZ1dqdEZlYXJaTkh0cWIxU3Bvcz0iLCJtYWMiOiJlM2I5OWNlNTAyY2VhMmRiOTY1ZTUzNmQ1YjFjYmY5MzRlMTdjZTIwNTc3YzdlOWFiNjcxNjIzM2ZhYmRkNGJlIn0%3D; _ga=GA1.1.1874093538.1698249101; cSaasWidget_ia8mhd2xti=[{"k":"v-widget","v":"2023-11-14T12:09:21.011Z"},{"k":"v-Telegram","v":"2023-11-05T13:57:21.431Z"},{"k":"v-Custom_Link_1","v":"2023-11-05T13:57:21.431Z"},{"k":"v-Custom_Link_2","v":"2023-11-05T13:57:21.432Z"},{"k":"v-Email","v":"2023-11-05T13:57:21.432Z"},{"k":"c-widget","v":"2023-11-05T13:57:21.433Z"}]; activeCsaasWidgets=ia8mhd2xti; sidebar_minimize_state=off; web1s_session=lQVgPRa7i3Ij3UFCq8VL26F8Uj312OZtaF03cgjj; _ga_FFP7FJ85WV=GS1.1.1700045900.10.0.1700045902.0.0.0; csaas_referrer=https://web1s.com/member; XSRF-TOKEN=eyJpdiI6ImluTGUrR0FZRElmRmhxWFU3Vyticmc9PSIsInZhbHVlIjoiS1dPYUF0eUh3SFhTSTM1WEpmRlVzcEtnRERhc2FxUVQyVHEwQUJDLyt3VlQ4Z2ZOazRBRndxcG9oR2tvWUhwZHNnSmg3a1REaC92eE5PSlZOaytJcnk2Rk1rZHEwUUcySmdvN2c1c3Bjdm9UTlpaVXlYM2lIUWhXUVZtY0cxTW8iLCJtYWMiOiIzYWQ5M2MyZjQzMjIxMGNiYzUzYjQyMDgyOTgzZjQ2ZmRiMzNiN2Y4ZDRmZGNkMWU0N2Q4MzRlNjE4YjY0ODdhIn0%3D',
    "X-Xsrf-Token": "eyJpdiI6ImluTGUrR0FZRElmRmhxWFU3Vyticmc9PSIsInZhbHVlIjoiS1dPYUF0eUh3SFhTSTM1WEpmRlVzcEtnRERhc2FxUVQyVpyHEwQUJDLyt3VlQ4Z2ZOazRBRndxcG9oR2tvWUhwZHNnSmg3a1REaC92eE5PSlZOaytJcnk2Rk1rZHEwUUcySmdvN2c1c3Bjdm9UTlpaVXlYM2lIUWhXUVZtY0cxTW8iLCJtYWMiOiIzYWQ5M2MyZjQzMjIxMGNiYzUzYjQyMDgyOTgzZjQ2ZmRiMzNiN2Y4ZDRmZGNkMWU0N2Q4MzRlNjE4YjY0ODdhIn0="
}

data = {
    "alias": "",
    "default_domain": True,
    "description": "",
    "expiration": None,
    "level_id": 23,
    "password": "Thanden365",
    "sub_domain_id": 21,
    "title": "G4U",
    "url": "https://www.facebook.com/profile.php?id=100054958380559"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.status_code)
print(response.text)


{"data":{"user_id":19245,"level_id":23,"folder_id":0,"is_active":1,"url":"https:\/\/www.facebook.com\/profile.php?id=100054958380559","url_hash":"d920135ee6e37b6d0c97820eb6a211bd","alias":"Igp2Yv0vHh","title":"G4U","description":null,"image":null,"hits":0,"method":1,"expiration":null,"last_activity":"2023-11-15T11:09:34.903992Z","password":"Thanden365","sub_domain_id":21,"updated_at":"2023-11-15T11:09:34.000000Z","created_at":"2023-11-15T11:09:34.000000Z","id":63372016,"sub_domain":{"id":21,"domain":"webmotgiay.com","protocol":"https","is_default":0,"is_active":1,"created_at":"2023-08-17T04:58:28.000000Z","updated_at":"2023-08-17T05:02:30.000000Z","list_services":[1,2,3,4,5,6,7],"is_default_note":0,"is_default_file":0,"is_hidden":0,"redirect_domain":"https:\/\/web1s.com","header_ads":null,"center_ads":null,"footer_ads":null,"popup_ads":null},"method_text":"Web"}}