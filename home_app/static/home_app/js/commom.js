

const loading = document.querySelector('.container-loading')



document.querySelector('.accout-out').addEventListener('click', () => {
    window.location.href = '/login/' 
})
const obj = document.querySelector('.header-notification')
const triangle = document.querySelector('.triangle')
const container = document.querySelector('.container-noti')
const fullscreen = document.querySelector('.fullscreen-noti')
obj.addEventListener('click', () => {
    triangle.style.display = 'block'
    container.style.display = 'block'
    fullscreen.style.display = 'block'
})

fullscreen.addEventListener('click', () => {
    triangle.style.display = 'none'
    container.style.display = 'none'
    fullscreen.style.display = 'none'
})


// đóng thông báo ở login singup
const noti = document.querySelector(".notification-js .close-noti-js")
if (noti) {
    noti.addEventListener('click', () => {
        document.querySelector('.notification-js').style.display = 'none'
})
}

