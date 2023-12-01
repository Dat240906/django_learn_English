
// đóng thông báo ở login singup
document.querySelector(".notification-js .close-noti-js").addEventListener('click', () => {
    document.querySelector('.notification-js').style.display = 'none'
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