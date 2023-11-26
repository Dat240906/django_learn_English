/////////////////////////////////////////////////////////////////////////
var notification = document.querySelector('.notification-js')
var message =document.querySelector(".notification-js p");
var background_color_fail = "#3E1927";
var color_fail  = "#F0879A";
var background_color_success = "#0a785b";
var color_success= "#95e8c5";
var end_point = '/home/login/'
/////////////////////////////////////////////////////////////////////////
document.addEventListener('DOMContentLoaded', function () {
// Đặt mã JavaScript ở đây
document.querySelector('.form-login-container-js').addEventListener('submit', async function (event) {
event.preventDefault();
notification.style.display = 'none'                 
var data_input = {
'username':document.querySelector('.username-js').value,
'password':document.querySelector('.password-js').value
        }

function changeRespondFail(message_change) {
    notification.style.backgroundColor = background_color_fail;
    notification.style.color = color_fail;
    message.textContent = message_change+'!!'
    notification.style.display = 'block';
}

function changeRespondSuccess(message_change) { 
    notification.style.backgroundColor = background_color_success;
    notification.style.color = color_success;
    message.textContent = message_change+'!!'
    notification.style.display = 'block';
}

try {
    const response = await fetch('/login/', {
        method: "POST",
        body: JSON.stringify(data_input),
        headers: {
            "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            "Content-Type": "application/json",
        }
    });
    
    if (response.ok) {
        const data = await response.json();

        if ('success' in data) {
            if (data.success) {
                changeRespondSuccess(data.message);
                window.location.href = data.redirect_url;
            } else {
                changeRespondFail(data.message);
            }
        } else {
            console.log('Không tìm thấy "success" trong dữ liệu phản hồi');
        }
    } else {
        changeRespondFail('error here');
    }
} catch (error) {
    console.log(error);
    changeRespondFail(error.message);
}
})
});