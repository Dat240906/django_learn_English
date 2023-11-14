const link1s = document.querySelector('.link1s_method_js')
const web1s = document.querySelector('.web1s_method_js')
const youtube = document.querySelector('.youtube_method_js')
const tiktok = document.querySelector('.tiktok_method_js')
const facebook = document.querySelector('.facebook_method_js')


function redirect(url) {
    var path_main = '/'
    if (url === 'link1s') {
        path_main = 'link1s'
    }else if (url === 'web1s') {
        path_main = 'web1s'
    }else if (url === 'youtube') {
        path_main = 'youtube'
    }else if (url === 'tiktok') {
        path_main = 'tiktok'
    }else if (url === 'facebook') {
        path_main = 'facebook'
    }

    window.location.href = path_main;
}


link1s.addEventListener('click',function() {redirect('link1s')} )
web1s.addEventListener('click',function() {redirect('web1s')})
youtube.addEventListener('click',function() {redirect('youtube')})
tiktok.addEventListener('click',function() {redirect('tiktok')})
facebook.addEventListener('click',function() {redirect('facebook')})