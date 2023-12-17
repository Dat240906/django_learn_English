const items = document.querySelectorAll('.nav_item');
for (let item of items) {
    item.addEventListener('click', () => {
        item.style.color = '#009EF7';
        item.style.borderBottom = '2px solid #009EF7';
        for (let otherItem of items) {
            if (otherItem !== item) {
                otherItem.style.color = 'white';
                otherItem.style.borderBottom = 'none';
            }
        }   
    });
}
    
const choose = document.querySelector('#choose_method')
const momo_method = document.querySelector('#method_momo')
const bank_method = document.querySelector('#method_bank')
const paypal_method = document.querySelector('#method_paypal')


choose.addEventListener('change', () => {
    momo_method.style.display = 'none'
    bank_method.style.display = 'none'
    paypal_method.style.display = 'none'


    const method_choosed = choose.value

    if (method_choosed === 'momo') {
        momo_method.style.display = 'block'
    } else if (method_choosed === 'bank' ) {
        bank_method.style.display = 'block'
    } else if (method_choosed === 'paypal' ) {
        paypal_method.style.display = 'block'
    } else {
        momo_method.style.display = 'none'
        bank_method.style.display = 'none'
        paypal_method.style.display = 'none'
    }
})








// edit info 
document.querySelector('.btn-edit-info-js').addEventListener('click', async (e) => {
    e.preventDefault()

    const loading = document.querySelector('.container-loading')
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const email = document.querySelector('.email-in-editinfo-js').value
    const number_phone = document.querySelector('.numberphone-in-editinfo-js').value
    const address = document.querySelector('.address-in-editinfo-js').value
    const info = document.querySelector('.info-js')
    formData = new FormData()
    formData.append('email', email)
    formData.append('number_phone', number_phone)
    formData.append('address', address)

    loading.style.display= 'block'

    try {
        const response = await fetch('api/v1/update-data/', {
            method: 'POST', 
            body:formData,
            headers:{
                'X-CSRFToken':csrf_token
            }
        })

        if (!response.ok){
            loading.style.display= 'none'
            return alert(response.error)
        }

        const data = await response.json()
        if (data.success) {
            loading.style.display= 'none'
            info.textContent = data.message
            info.classList.add('color-green')
            info.classList.remove('display-none-noti')

            setTimeout(() => {

                window.location.reload()
            }, 2000)
            return

        }
        loading.style.display= 'none'
        info.textContent = data.message
        info.classList.add('color-red')
        info.classList.remove('display-none-noti')

    } catch (error) {
        loading.style.display= 'none'
        alert(error)
    }
})




//add bank

function sendAPI(csrf_token, formData) {
    return fetch('api/v1/add-bank/', {
        method:'POST',
        body:formData,
        headers: {
            'X-CSRFToken':csrf_token
        }
    })
}
async function handleRespon(info, loading, response) {
    loading.style.display= 'none'
    if (!response.ok) {
            alert('lỗi phản hồi')
            return 
        }

    const data = await response.json()
    if (!data.success) {
        info.textContent = data.message
        info.classList.add('color-red')
        info.style.display = 'block'
        return
    }

    info.textContent = data.message
    info.classList.add('color-green')
    info.style.display = 'block'
    setTimeout(() => {
        window.location.reload()
    }, 2000)
}       
document.querySelector('.btn-addbank-js').addEventListener('click', async (e) => {
    e.preventDefault()
    const loading = document.querySelector('.container-loading')
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const method_pay = document.querySelector('.method-pay-js').value
    const info = document.querySelector('.info-addbank-js')

    
    info.style.display = 'none'
    //momo
    const phone_number_momo = document.querySelector('.phone-number-momo-js')
    //paypal
    const email_paypal = document.querySelector('.email-paypal-js')
    //bank
    const name_bank = document.querySelector('.name-bank-js')
    const name_acc_bank = document.querySelector('.name-acc-bank-js')
    const stk_bank = document.querySelector('.stk-bank-js')

    function returnNotData() {
        info.textContent = 'Chưa có dữ liêu'
        info.classList.add('color-red')
        info.style.display = 'block'
         
    }
    if (method_pay == 'none') {
        return returnNotData()
    }

    if (method_pay == 'momo') {

        if (phone_number_momo.value == '') {
            return returnNotData()
        }

        const formData = new FormData()
        info.textContent

        formData.append('method_pay','momo')
        formData.append('phone_number_momo',phone_number_momo.value)
        loading.style.display= 'block'
        const response = await sendAPI(csrf_token, formData)
        return handleRespon(info,loading,  response)

    } else if (method_pay == 'paypal') {
        function isValidEmail(email) {
            // Thực hiện kiểm tra định dạng email ở đây, bạn có thể sử dụng regex hoặc các cách kiểm tra khác.
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        }
        if (!isValidEmail(email_paypal.value)) {
            info.textContent = 'Email không hợp lệ!'
            info.classList.add('color-red')
            info.style.display = 'block'
            return
        }
        if (email_paypal.value == '') {
            return returnNotData()
        }

        const formData = new FormData()


        formData.append('method_pay','paypal')
        formData.append('email_paypal',email_paypal.value)
        loading.style.display= 'block'
        const response = await sendAPI(csrf_token, formData)
        return handleRespon(info,loading,  response)
    } else if (method_pay == 'bank') {

        if (name_bank.value == '' || name_acc_bank.value == '' || stk_bank.value == '') {
            return returnNotData()
        }

        const formData = new FormData()


        formData.append('method_pay','bank')
        formData.append('name_bank',name_bank.value)
        formData.append('name_acc_bank',name_acc_bank.value)
        formData.append('stk_bank',stk_bank.value)
        loading.style.display= 'block'
        const response = await sendAPI(csrf_token, formData)
        return handleRespon(info,loading,  response)
    }
})