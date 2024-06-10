let chats = document.querySelectorAll('.chat-link')
let chat_socket = null
function dropdownFunction() {
    document.getElementById('profileDropdown').classList.toggle('show');
};

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            };
        };
    };
};
chats.forEach(function (link) {
    link.addEventListener('click', function (event) {
        event.preventDefault()
        let chat_id = this.getAttribute('data-chat-id')
        if(chat_socket != null) {
            chat_socket.close();
            document.getElementById('messages').innerHTML = '';
        }
        chat_socket = new WebSocket('ws://localhost:8000/ws/chat/' + chat_id + '/');
        function generateMessageHTML(message) {
            const date = formatDate(message.date_sent);
            if (message.content) {
                return `<p>${message.author_name} - ${message.content}</p><span>${date}</span>`;
            } else if (message.image) {
                return `<img src="${message.image}"><p>${message.author_name}</p><span>${date}</span>`;
            } else if (message.file) {
                return `<a href="${message.file}" target="_blank">Download File</a><p>${message.author_name}</p><span>${date}</span>`;
            } else if (message.video) {
                return `<video controls><source src="${message.video}"></video><p>${message.author_name}</p><span>${date}</span>`;
            } else if (message.audio) {
                return `<audio controls><source src="${message.audio}"></audio><p>${message.author_name}</p><span>${date}</span>`;
            } else if (message.sticker) {
                return `<img src="${message.sticker}"><p>${message.author_name}</p><span>${date}</span>`;
            }
            return '';
        }
        chat_socket.onmessage = function (event) {
            let data = JSON.parse(event.data);
            console.log(data)
            if(data.type === 'error'){
                console.log(data.message)
            }
            if(data.type === 'new_message'){
                let messages = document.getElementById('messages')
                const messageHTML = generateMessageHTML(data.message);
                if (messageHTML) {
                    messages.insertAdjacentHTML('beforeend', `<div>${messageHTML}</div>`);
                }
            }
        }

        function formatDate(dateString) {
            let options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' };
            return new Date(dateString).toLocaleDateString('en-GB', options).replace(",", "");
        }

        fetch('{% url "chat" chat_id=0%}'.replace('0', chat_id))
            .then(response => response.json())
            .then(data => {
            data.messages.forEach(message => {
                let messages = document.getElementById('messages')
                console.log(message)
                const messageHTML = generateMessageHTML(message);
                if (messageHTML) {
                    messages.insertAdjacentHTML('beforeend', `<div>${messageHTML}</div>`);
                }


            })
//            let title = document.getElementById('app')
//            title.innerHTML = data.chat.name
        })


        let form = document.getElementById('form')
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            let formData = new FormData(form);
            formData.append('user',{{ user.id }})
            let file = formData.get('file');
            let image = formData.get('image');
            let video = formData.get('video');
            let audio = formData.get('audio');
            let messageContent = formData.get('message');
            let message = {
                'message': messageContent,
                'user': {{ user.id }},
                'file': file ? URL.createObjectURL(file) : null,
                'image': image ? URL.createObjectURL(image) : null,
                'video': video ? URL.createObjectURL(video) : null,
                'audio': audio ? URL.createObjectURL(audio) : null,
            };

            console.log(message)

            chat_socket.send(JSON.stringify({message}));
            form.reset()
        })

    })
})
