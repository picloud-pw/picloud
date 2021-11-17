document.addEventListener("DOMContentLoaded", function () {

    restore_state();

});

function restore_state() {
    init_chat_lists_segment();
    init_chat_content_segment();
    init_chat_bar_segment();
}

function init_chat_lists_segment() {
    document.getElementById('chat_list').innerHTML = `
        <div class="ui top segment" id="chats_search" style="padding-top: 22px">
            <div class="ui transparent left icon fluid large disabled input" style="padding-right: 45px">
              <input type="text" disabled placeholder="Search...">
              <i class="search icon"></i>
            </div>
            <div class="ui basic circular icon extra-btn button" id="new_chat_btn"
                onclick="toggle_new_chat_form()">
                <i class="ui plus icon"></i>
            </div>
        </div>
        <div class="ui middle segment" id="chats_list" style="padding: 0;"></div>
        <div class="ui middle blue segment" id="new_chat_form">
            <div id="new_chat_alerts"></div>
            <div class="ui left icon fluid input">
              <input type="text" placeholder="Enter chat title" id="new_chat_title">
              <i class="users icon"></i>
            </div>
            <div class="ui divider"></div>
            <div class="ui basic fluid button" onclick="create_new_chat()">
                Create chat
            </div>
        </div>
    `;
    load_chat_lists();
}

function init_chat_content_segment() {
    document.getElementById('chat_content').innerHTML = `
        <div class="ui top segment" id="chat_header"></div>
        <div class="ui middle segment" id="chat_messages" style="overflow: hidden">
            <div class="ui basic placeholder segment" style="height: 100%">
              <div class="ui icon header">
                <i class="pdf comments outline icon"></i>
                Select a chat <br> or 
                <a onclick="toggle_new_chat_form()" style="cursor: pointer">
                    create a new one
                </a>.
              </div>
            </div>
        </div>
        <div class="ui bottom segment" id="chat_form"></div>
    `;
}

function init_chat_bar_segment() {
    document.getElementById('chat_bar').innerHTML = `
        <div class="ui top segment"></div>
        <div class="ui middle segment" id="chat_bar_content"></div>
    `;
    display_emojis_list(document.getElementById('chat_bar_content'));
}

function display_emojis_list(container) {
    container.innerHTML = `
        <div class="ui basic no-margin-padding segment" id="emojis_list"></div>
    `;
    let emojis_html = '';
    for (let code of EMOJI_CODES) {
        emojis_html += `
            <div onclick="document.getElementById('text_message_input').value += '&#${code};'">
                &#${code};
            </div>
        `;
    }
    document.getElementById('emojis_list').innerHTML = emojis_html;
}

function toggle_new_chat_form() {
    $('#new_chat_form').transition('slide down');
    $('#new_chat_btn').toggleClass('rotated');
    document.getElementById('new_chat_alerts').innerText = '';
    document.getElementById('new_chat_title').value = '';
}

function load_chat_lists() {
    let container = document.getElementById('chats_list');
    container.innerHTML = `
        <div class="ui middle aligned selection divided list" id="chats_list_container"></div>
    `;
    container.classList.add('loading');
    axios.get('/chats/chat/list')
        .then((response) => {
            let chats = response.data['chats'];
            for (let chat of chats) {
                document.getElementById('chats_list_container').innerHTML += `
                    <div class="item" onclick="open_chat('${chat['name']}')">
                        <div class="content">
                            <a class="header">${chat['title']}</a>
                        </div>
                    </div>
                `;
            }
        }).finally(() => {
            container.classList.remove('loading');
        })
}

function create_new_chat() {
    let title = document.getElementById('new_chat_title').value;
    let data = new FormData();
    data.append("title", title);
    axios.post('/chats/chat/add', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {
            toggle_new_chat_form();
            load_chat_lists();
        }).catch((error) => {
            document.getElementById('new_chat_alerts').innerHTML = `
                <div class="ui pink message" style="margin-bottom: 20px;">
                  <i class="close icon"></i>
                  <div class="header">Something went wrong... 😰</div>
                  <p>${error.response.data}</p>
                </div>
            `;
            $('.message .close').on('click', function() {
                $(this).closest('.message').transition('fade');
            });
        })
}

function open_chat(chat_name) {
    document.getElementById('chat_header').innerHTML = `
        <h3 class="ui header" style="margin-top: 6px">${chat_name}</h3>
        <div class="ui basic icon circular extra-btn button">
            <i class="ui ellipsis horizontal icon"></i>
        </div>
    `;
    document.getElementById('chat_messages').innerHTML = `
        <div class="ui basic placeholder segment" style="height: 100%">
          <div class="ui icon header">
            <i class="comment alternate outline icon"></i>
            There is no messages yet... <br> Lets text some ...
          </div>
        </div>
    `;
    document.getElementById('chat_form').innerHTML = `
        <div class="ui fluid icon input">
          <input type="text" placeholder="Write a message..." id="text_message_input">
          <i class="circular paper plane outline link icon" onclick="sent_message('${chat_name}')"></i>
        </div>
    `;
    document.getElementById("text_message_input")
        .addEventListener("keyup", (event) => {
              if (event.keyCode === 13) {
                event.preventDefault();
                sent_message(chat_name);
              }
        });
    load_chat_messages(chat_name);
}

function load_chat_messages(chat_name) {
    let container = document.getElementById('chat_messages');
    container.classList.add('loading');
    axios.get(`/chats/message/list?chat_name=${chat_name}`)
        .then((response) => {
            let messages = response.data['messages'];
            if (messages.length) {
                container.innerHTML = `
                    <div class="ui comments" id="chat_messages_container"></div>
                `;
            }
            for (let message of messages) {
                document.getElementById('chat_messages_container').innerHTML += `
                    <div class="comment">
                        <div class="content">
                          <a class="author">${message['author']}</a>
                          <div class="metadata">
                            <span class="date">${new Date(message['created']).toPrettyString()}</span>
                          </div>
                          <div class="text">${message['text']}</div>
                          <div class="actions">
                            ${message['edited'] ? '<span class="reply">(edited)</span>' : ''}
                          </div>
                        </div>
                    </div>
                `;
            }
        }).finally(() => {
            container.classList.remove('loading');
        })
}

function sent_message(chat_name) {
    let message_input = document.getElementById('text_message_input');
    let data = new FormData();
    data.append("chat_name", chat_name);
    data.append("message", message_input.value);
    axios.post('/chats/message/add', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {
           load_chat_messages(chat_name);
        }).catch((error) => {
        }).finally(() => {
            message_input.value = '';
        })
}
