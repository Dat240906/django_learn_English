
// tạo nhiều bình luận dựa trên response

function CreateComment(list_comment) {

    //list_comment dạng :{"model": "post_app.commentmodel", "pk": 17, "fields": {"post": 54, "user": "admin", "content_comment": "được", "create_at": "2023-11-29T13:30:35.404Z"}}, {"model": "post_app.commentmodel", "pk": 16, "fields": {"post": 54, "user": "admin", "content_comment": "được", "create_at": "2023-11-29T13:30:25.451Z"}}
    const container_comments = document.querySelector('.container-comment-js')
    for (let comment of list_comment) {
        //khởi tạo
        console.log(comment.fields.user)
        console.log(comment.fields.content_comment)
        const father_element = document.createElement('div')
        father_element.classList.add('user-comment')
        // const child1_img_user_element = document.createElement('img').add('img-user')
        
        const child2_element = document.createElement('div')
        child2_element.classList.add('info-user')
        const username_in_child2_element = document.createElement('p')
        username_in_child2_element.classList.add('name-user-comment')
        const create_at = document.createElement('i')
        const content_in_child2_element = document.createElement('p')
        content_in_child2_element.classList.add('content-user','pd-6')

        // chatgpt: chỉnh sửa định dạng time create
        // Chuỗi ngày giờ ban đầu
        var originalDateString = `${comment.fields.create_at}`

        // Tạo đối tượng Date từ chuỗi ngày giờ
        var originalDate = new Date(originalDateString);

        // Lấy các thành phần ngày giờ từ đối tượng Date
        var hours = originalDate.getUTCHours();
        var minutes = originalDate.getUTCMinutes();
        var day = originalDate.getUTCDate();
        var month = originalDate.getUTCMonth() + 1; // Tháng bắt đầu từ 0, nên cần cộng thêm 1
        var year = originalDate.getUTCFullYear();

        // Tạo chuỗi mới theo định dạng mong muốn
        var time_create = hours + ":" + minutes + " - " + day + "/" + month + "/" + year;


        //điền thông tin
        create_at.textContent = ` - ${time_create}`
        username_in_child2_element.textContent = comment.fields.user
        content_in_child2_element.textContent = comment.fields.content_comment

        //lồng các phần tử vào với nhau
        username_in_child2_element.appendChild(create_at)
        child2_element.appendChild(username_in_child2_element)
        child2_element.appendChild(content_in_child2_element)

        father_element.appendChild(child2_element)

        container_comments.appendChild(father_element)
    }
}

const objects_comment = document.querySelectorAll('.opctncm')
const post_username = document.querySelector('.post-child-comment .info .username-js')
const post_time = document.querySelector('.post-child-comment .info .time-js')
const post_title = document.querySelector('.post-child-comment .title-js')
const post_content = document.querySelector('.post-child-comment .content-js')
const container_loading = document.querySelector('.container-loading')
const post_avatar_user = document.querySelector('.post-child-comment .avatar-user-js')
const post_img = document.querySelector('.post-child-comment .post-img .post-img-js')
const nobody_comment = document.querySelector('.container-comment-js .nobody-comment-js')
for (const object of objects_comment) {
    object.addEventListener('click', async () => {
        const post_id = object.id
        const container_comment = document.querySelector('.container-total-comment')
        container_comment.style.display = "block"

        var comments_remove = document.getElementsByClassName('user-comment')
        //change type
        var elements_array = Array.from(comments_remove)
        elements_array.forEach(function(element) {
            element.parentNode.removeChild(element)
        })
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
                
                if (!data.post.comments) {
                    nobody_comment.style.display = 'block'
                    return 
                }
                const list_comments = JSON.parse(data.post.comments)
                CreateComment(list_comments)
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
    nobody_comment.style.display = 'none'
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

document.querySelector('.cancel-image-js').addEventListener('click', ()=> {
    document.querySelector('.image-input-js').value = null
    document.querySelector('#preview-image-js').src = ''
    
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
            container_loading.style.display = 'none'
            return console.log(data.error)
        }

        
        container_loading.style.display = 'none'
        window.location.reload();
    } catch (error) {
        return console.log(error)
    }
    
})




// thêm comment 

const btns = document.querySelectorAll('.button-add-comment-js')
btns.forEach(btn => {
    btn.addEventListener('click',async (e) => {
        e.preventDefault()
        container_loading.style.display = 'block'
        const postId = btn.id
        const content = document.querySelector(`.post-container-comment .${postId}`).value
        const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        if (content == ''){
            return container_loading.style.display = 'none'
        }
        try {
            const form = new FormData()
            form.append('content', content)
            form.append('post_id', postId)
            const response = await fetch('post/api/v1/add-comment/', {
                method:"POST",
                body:form,
                headers: { 
                    'X-CSRFToken': csrf_token, }
            })

            if (!response.ok){
                container_loading.style.display = 'none'
                return alert('lỗi!')
            }
            container_loading.style.display = 'none'

            window.location.reload()       
        } catch (error) {
            alert(error)
        }
    })
});



// like post
const like_click_allbutton = document.querySelectorAll('.click-like-js')

for (const item_click of like_click_allbutton) {
    item_click.addEventListener('click', async () => {
        
        const post_id = item_click.id
        try {
            
            const response = await fetch(`/post/api/v1/add-like/?post_id=${post_id}`, {
                method: "GET",
            }) 

            if (!response.ok) {return}
            
            data = await response.json()
            if (data.message === 'liked') {
                item_click.classList.add('color-red')
            }else {
                item_click.classList.remove('color-red')

            }

        } catch (error) {
            alert(error)
        }
        

    })}

