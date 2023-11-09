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