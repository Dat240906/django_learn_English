from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from study.consumers import OnlineUsersConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        re_path(r"^ws/online_users/$", OnlineUsersConsumer.as_asgi()),
    ]),
})