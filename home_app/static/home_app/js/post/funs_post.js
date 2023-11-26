const objects_comment = document.querySelectorAll('.opctncm')
const post_username = document.querySelector('.post-child-comment .info .username-js')
const post_time = document.querySelector('.post-child-comment .info .time-js')
const post_title = document.querySelector('.post-child-comment .title-js')
const post_content = document.querySelector('.post-child-comment .content-js')
const container_loading = document.querySelector('.container-loading')
const post_avatar_user = document.querySelector('.post-child-comment .avatar-user-js')
const post_img = document.querySelector('.post-child-comment .post-img .post-img-js')
for (const object of objects_comment) {
    object.addEventListener('click', async () => {
        const post_id = object.id
        console.log(post_id)
        const container_comment = document.querySelector('.container-total-comment')
        container_comment.style.display = "block"

        //thêm loading 
        container_loading.style.display = 'block'

        //gửi API lên server
        try {
            const response = await fetch(`api/v1/post-comments/?post_id=${post_id}`, {
                method: 'GET', 
                
            })

            if (response.ok) {
                const data = await response.json();
                

                //ẩn loading
                container_loading.style.display = 'none'
                // // chỉnh sửa các thông tin của container-comment để đưa lên
                
                post_username.textContent = data.post.username
                post_time.textContent = data.post.time
                post_title.textContent = data.post.title
                post_content.textContent = data.post.content
                post_avatar_user.src = 'media/' + data.post.avatar;
                if (!data.post.img) {
                    post_img.style.display = 'none'
                } else {
                    post_img.style.display = 'block'
                    post_img.src = 'media/' + data.post.img;
                }
                
            }else {
                console.log('Không tìm thấy "success" trong dữ liệu phản hồi');
            }
        } catch (error) {
            console.log(error);
        }
    })
}
document.querySelector('.clctncm').addEventListener('click', function (event) {
    const container_comment = document.querySelector('.container-total-comment')
    container_comment.style.display = "none"

    //tạo sự mượt mà
    post_username.textContent = ''
    post_time.textContent = ''
    post_title.textContent = ''
    post_content.textContent = ''
    post_avatar_user.src = '';
    post_img.src = '';
})



document.querySelector('.image-input-js').addEventListener('change', (event) => {

   //xem người dùng đã chon ảnh chưa 
   if (event.target.files.length > 0) {
        const file = event.target.files[0]
        const reader  = new FileReader()

        reader.onload = function(e) {
            document.querySelector('#preview-image-js').src = e.target.result

        }
        reader.readAsDataURL(file);
    
   }
})

// <!-- tạo bài viết -->

document.querySelector('.bt-create-post-js').addEventListener('click',async (event) =>  {
    event.preventDefault()
    container_loading.style.display = 'block'
    const title = document.querySelector('.form-create-post .title-create-js').value
    const content = document.querySelector('.form-create-post .content-create-js').value
    const img = document.querySelector('.image-input-js').files[0]
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    const formData = new FormData()
    formData.append('title', title)
    formData.append('content', content)
    formData.append('img', img)
    console.log(title);
    console.log(content);
    console.log(img);
    try {
        const response = await fetch('post/api/v1/create-post/', {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': csrf_token,
            }
        })

        if (!response.ok) {
            return alert(response.error)
        }
        
        const data = await response.json()
        
        if (!data.success) {
            return console.log(data.error)
        }

        
        container_loading.style.display = 'none'
        window.location.reload();
    } catch (error) {
        return console.log(error)
    }
    
})