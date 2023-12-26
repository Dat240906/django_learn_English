// <!-- hàm xóa endpoint -->
function getEndPoint() {
    const currentURL = window.location.href;
    const urlObject = new URL(currentURL);
    const pathUrl = urlObject.pathname;

    // Tách chuỗi path
    const paths = pathUrl.split('/').filter(Boolean); // Lọc bỏ các giá trị rỗng

    // Lấy giá trị cuối cùng của mảng
    const endpoint = paths[paths.length - 1];

    return endpoint;
}
async function deleteEndPoint(csrf_token) {
    
    const endpoint = getEndPoint()
    const formData = new FormData()
    formData.append('endpoint', endpoint)

    const response = await fetch('/earn_money/delete-endpoint/', {
        method: 'DELETE', 
        body:formData,
        headers:{
            'X-CSRFToken':csrf_token
        }

    })
    return
}

// <!-- collect -->

document.querySelector('.btn-collect-js').addEventListener('click', async(e) => {
    e.preventDefault()
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    const info = document.querySelector('.info')
    const endpoint = getEndPoint()
    info.style.display = 'none'
    
    formData = new FormData()
    formData.append('endpoint', endpoint)
    formData.append('request', 'collect')

    try {
        const response = await fetch('/earn_money/plus-money/', {
            method:'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrf_token,
            }

        })

        if (!response.ok){return alert(response.error)}

        const data = await response.json()
        if (data.status == 'error') {
            info.textContent = data.message
            info.style.color ='red'
            info.style.display = 'block'
            return 
        }
        
        info.textContent = data.message
        info.style.color ='green'
        info.style.display = 'block'
        deleteEndPoint(csrf_token)
        setTimeout(()=>{
            window.location.href = '/'
        }, 2000)
        return 

    } catch (error) {
        return alert(error)
        
    }

})

// <!-- create giftcode   -->
function generateRandomString() {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    const stringLength = 15;
    let randomString = '';

    for (let i = 0; i < stringLength; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        randomString += characters.charAt(randomIndex);
    }

    return randomString;
}
document.querySelector('.btn-open-container-create-giftcode-js').addEventListener('click', () => {

    // Sử dụng hàm để lấy chuỗi ngẫu nhiên
    const randomString = generateRandomString();
    const giftcode = document.querySelector('.giftcode-js')
    giftcode.value = randomString
})

document.querySelector('.btn-create-giftcode-js').addEventListener('click', async (e) => {
    e.preventDefault()
    const giftcode = document.querySelector('.giftcode-js').value
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    const info = document.querySelector('.info_create-js')
    const endpoint = getEndPoint()
    info.style.display = 'none'

    const formData = new FormData()
    formData.append('giftcode', giftcode)
    formData.append('endpoint', endpoint)

    try {
        const response = await fetch('/earn_money/create-giftcode/', {
            method: "POST",
            body:formData,
            headers:{
                'X-CSRFToken': csrf_token,
            }
        })

        if (!response.ok){return alert(response.error)}

        const data = await response.json()
        if (data.status == 'error') {
            info.textContent = data.message
            info.style.color ='red'
            info.style.display = 'block'
            return 
        }
        
        info.textContent = data.message
        info.style.color ='green'
        info.style.display = 'block'
        deleteEndPoint(csrf_token)
        return 
        
    } catch (error) {
        alert(error)
    }
})
