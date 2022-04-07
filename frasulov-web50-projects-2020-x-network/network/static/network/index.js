document.addEventListener('DOMContentLoaded', function() {
    // alert("necesen")
    get_posts()

    if (document.querySelector('form')){
        document.querySelector('form').onsubmit = () => {
            const title = document.getElementById('title').value
            const body = document.getElementById('body').value
            if (title !== ""){
                createPost(title, body)}
            else{
                message = document.querySelector('.bg-danger')
                message.innerHTML = 'There must be a title for post';
                message.classList.remove('d-none')
                message.classList.add('d-block')
                setTimeout(function(){
                message.style.animationPlayState = 'running'
                message.addEventListener('animationend', () => {
                message.style.animationPlayState = 'paused'
                message.classList.remove('d-block');
                message.classList.add('d-none');
            })
            }, 1500)
            }
            document.getElementById('body').value = ""
            document.getElementById('title').value = ""
            return false;
        }
    }
});

function update(page, has_previous, has_next){
    document.getElementById('page').innerHTML = page
    if (has_previous){
        document.getElementById('previous').classList.remove('d-none')
    }else{
        document.getElementById('previous').classList.add('d-none')
    }
    if (has_next){
        document.getElementById('next').classList.remove('d-none')
    }else{
        document.getElementById('next').classList.add('d-none')

    }
}
function display_posts(posts, current){
    document.getElementById('all').innerHTML = ''
    posts.forEach(post => {
        postView(post, current)
    });
}

function get_posts()
    {
        let link = window.location.href;
        let page;
        let n = link.indexOf("=");
        if (n === -1){
            page = 0
        }else{
            page = parseInt(link.substring(n+1, link.length))
        }
        fetch(`posts`)
        .then(response => response.json())
        .then(result => {
            current = result.currentUser;
            if (page >= result.page_obg.length){
                page = 0
            }
            display_posts(result.page_obg[page].posts, current)
            next = document.getElementById('next')
            previous = document.getElementById('previous')
            update(result.page_obg[page].page, result.page_obg[page].has_previous, result.page_obg[page].has_next)
            next.onclick = () =>{
                page++;

                document.getElementById('nextA').href = `?page=${page}`
                document.getElementById('previousA').href =  `?page=${page-1}`
                display_posts(result.page_obg[page].posts)
                update(result.page_obg[page].page,result.page_obg[page].has_previous, result.page_obg[page].has_next)
            }
            previous.onclick = () =>{
                page--;
                document.getElementById('nextA').href = `?page=${page+1}`
                document.getElementById('previousA').href =  `?page=${page}`
                display_posts(result.page_obg[page].posts)
                update(result.page_obg[page].page,result.page_obg[page].has_previous, result.page_obg[page].has_next)
            }
            console.log(result.page_obg[0])
        
        
        })
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

function createPost(title, body){
    fetch('/create', {
        method: 'POST',
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Accept": "application/json",
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: title,
            body: body
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        if (result.error){
            alert(result.error)
        }else{
            document.getElementById('all').innerHTML = "";
            get_posts()
            message = document.querySelector('.bg-success')
            message.innerHTML = result.message;
            message.classList.remove('d-none')
            message.classList.add('d-block')
            setTimeout(function(){
                message.style.animationPlayState = 'running'
                message.addEventListener('animationend', () => {
                message.style.animationPlayState = 'paused'
                message.classList.remove('d-block');
                message.classList.add('d-none');
            })
            }, 3000)
        }
    })
    }


function postView(post, current)
{

    const postdiv = document.createElement('div')
    postdiv.id = 'post'

    const userdiv = document.createElement('div')
    userdiv.id = 'user'

    const img = document.createElement('img')
    img.src = "https://images.pexels.com/photos/1804796/pexels-photo-1804796.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
    img.classList.add('user-photo')

    const atag = document.createElement('a')
    atag.href = `/profile/${post.user}`
    atag.innerHTML = post.user
    userdiv.append(img)
    userdiv.append(atag)

    const detail = document.createElement('div')
    detail.classList.add('detail')

    const h3tag = document.createElement('h3')
    h3tag.innerHTML = post.title

    const bodydiv = document.createElement('div')
    bodydiv.innerHTML = post.body

    const createddiv = document.createElement('div')
    createddiv.classList.add('text-muted');
    createddiv.style.fontSize = "14px"
    createddiv.innerHTML = post.created;

    const likediv = document.createElement('div')
    const spantag = document.createElement('span')
    spantag.innerHTML = `  ${post.nlikes} people liked`
    if (current !== ""){
        const buttontag = document.createElement('button');
        buttontag.classList.add('like');
        buttontag.style.backgroundColor = 'white'
        buttontag.style.border = 'none'
        buttontag.style.padding = '0'
        const tagi = document.createElement('i')
        tagi.classList.add('fas')
        tagi.classList.add('fa-heart')
        if (post.liked === 'True')
            tagi.classList.add('red')
        buttontag.onclick = () => {    
            // spantag.innerHTML = ''
            fetch(`like/${post.id}`)
            .then(response => response.json())
            .then(result => {
                console.log(result)
                if(!result.error)
                {
                    spantag.innerHTML = ` ${result.count} people liked`
                    if (result.liked === 'True'){
                        tagi.classList.add('red')
                    }else{
                        tagi.classList.remove('red')
                    }
                }

            })
        }
        buttontag.append(tagi)
        likediv.append(buttontag)
    }else{
        spantag.innerHTML = `<i style="color:red" class="fas fa-heart"></i> ${post.nlikes} people liked`
    }
    likediv.append(spantag)
    if (post.user == current){
        const atag2 = document.createElement('a')
        atag2.href = ""
        atag2.innerHTML = "Edit"
        atag2.onclick = () =>{
            const textArea = document.createElement('textarea')
            textArea.classList.add('form-control');
            textArea.style.width = '96%';
            textArea.value = post.body
            textArea.addEventListener('input', function(){
                this.style.height = 'auto'; 
                this.style.height = this.scrollHeight + 'px'; 
            }, false);
            bodydiv.innerHTML = '';
            const editbutton = document.createElement('button')
            editbutton.classList.add('btn')
            editbutton.classList.add('btn-primary')
            editbutton.classList.add('mt-2')
            editbutton.classList.add('mb-2')
            editbutton.innerHTML = 'Save'
            editbutton.onclick = () => {
                fetch(`update/${post.id}`, {
                    method: 'PUT',
                    credentials: "same-origin",
                    headers: {
                      "X-CSRFToken": getCookie("csrftoken"),
                      "Accept": "application/json",
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        body: textArea.value
                    })
                })
                .then(response => response.json())
                .then(result => {
                    bodydiv.innerHTML = result.newbody
                    location.reload();
                });
            }
            bodydiv.append(textArea);
            bodydiv.append(editbutton);

            return false
        }
        detail.append(atag2)
    }
    detail.append(h3tag)
    detail.append(bodydiv)
    detail.append(createddiv)
    detail.append(likediv)

    postdiv.append(userdiv)
    postdiv.append(detail)

    document.getElementById('all').append(postdiv);
}


