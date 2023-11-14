# your_proxy_script.py

from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # In địa chỉ của yêu cầu đến terminal
    print(flow.request.pretty_url)

    # Bạn có thể xử lý yêu cầu ở đây nếu cần

def response(flow: http.HTTPFlow) -> None:
    # In địa chỉ và nội dung của phản hồi đến terminal
    print(flow.request.pretty_url)
    print(flow.response.text)

    # Bạn có thể xử lý phản hồi ở đây nếu cần

# Chạy proxy server
if __name__ == "__main__":
    from mitmproxy import options
    from mitmproxy.tools import main

    opts = options.Options(listen_host="0.0.0.0", listen_port=8080)
    main(opts)
