export class Chats {

    selected_chat = null;

    constructor(container) {
        this.restore_state(container);
    }

    save_state() {
        let state = {};
        if (this.selected_chat) {
            state['c'] = this.selected_chat;
            push_state(state);
        }
    }

    restore_state(container) {
        let params = new URLSearchParams(document.location.search);
        this.selected_chat = params.get('c');

        this.el_id = random_ID();
        container.innerHTML = `
            <div class="ui padded chats grid">
                <div class="ui segment no-margin-padding four wide computer only left column" id="${this.el_id}_list"></div>
                <div class="ui segment no-margin-padding eight wide computer sixteen wide tablet center column" id="${this.el_id}_content"></div>
                <div class="ui segment no-margin-padding four wide computer only right column" id="${this.el_id}_bar"></div>
            </div>
        `;

        this.init_chat_lists_segment(document.getElementById(`${this.el_id}_list`));
        this.init_chat_content_segment(document.getElementById(`${this.el_id}_content`));
        this.init_chat_bar_segment(document.getElementById(`${this.el_id}_bar`));

        if (this.selected_chat) {
            this.open_chat(this.selected_chat);
        }
    }


    init_chat_lists_segment(container) {
        let top_segment = document.createElement('div');
        top_segment.className = 'ui top segment';
        top_segment.style.paddingTop = '22px';

        let chats_filter = document.createElement('div');
        chats_filter.className = 'ui transparent left icon fluid large input';
        chats_filter.style.paddingRight = '45px';
        let chats_filter_input = document.createElement('input');
        chats_filter_input.type = 'text';
        chats_filter_input.placeholder = 'Search...';
        chats_filter_input.oninput = () => { this.filter_chats(chats_filter_input.value) };
        chats_filter.appendChild(chats_filter_input);
        chats_filter.innerHTML += `<i class="search icon"></i>`;
        top_segment.appendChild(chats_filter);

        let new_chat_btn = document.createElement('div');
        new_chat_btn.className = 'ui basic circular icon extra-btn button';
        new_chat_btn.onclick = () => { this.toggle_new_chat_form() }
        new_chat_btn.innerHTML = `<i class="ui plus icon"></i>`;
        top_segment.appendChild(new_chat_btn);

        let middle_segment = document.createElement('div');
        middle_segment.className = 'ui middle segment';
        middle_segment.style.padding = '0';
        middle_segment.id = `${this.el_id}_chats_list`;

        container.innerHTML = ``;
        container.appendChild(top_segment);
        container.appendChild(middle_segment);

        this.load_chat_lists();
    }

    filter_chats(query) {
        $('#chat_list .item .content a.header').each((i, el) => {
            if ((el.innerText).toLowerCase().includes(String(query).toLowerCase())) {
                $(el).parent().parent().removeClass('hidden');
            } else {
                $(el).parent().parent().addClass('hidden');
            }
        })
    }

    init_chat_content_segment(container) {
        container.innerHTML = `
            <div class="ui top segment" id="chat_header"></div>
            <div class="ui middle no-margin-padding segment" id="chat_messages">
                <div class="ui basic placeholder segment" style="height: 100%">
                  <div class="ui icon header">
                    <i class="pdf comments outline icon"></i>
                    Select a chat <br> or 
                    <a id="create_new_chat_suggestion" style="cursor: pointer">create a new one.</a>
                  </div>
                </div>
            </div>
            <div class="ui bottom segment" id="chat_form"></div>
        `;
        document.getElementById('create_new_chat_suggestion').onclick = () => {
            this.toggle_new_chat_form();
        }
    }

    init_chat_bar_segment(container) {
        container.innerHTML = `
            <div class="ui top segment"></div>
            <div class="ui middle segment" id="${this.el_id}_bar_content"></div>
        `;
        this.display_emojis_list(document.getElementById(`${this.el_id}_bar_content`));
    }

    display_emojis_list(container) {
        container.innerHTML = `
            <div class="ui basic no-margin-padding emojis_list segment" id="${this.el_id}_emojis_list"></div>
        `;
        let emojis_html = '';
        for (let code of EMOJI_CODES) {
            emojis_html += `
                <div onclick="document.getElementById('text_message_input').value += '&#${code};'">
                    &#${code};
                </div>
            `;
        }
        document.getElementById(`${this.el_id}_emojis_list`).innerHTML = emojis_html;
    }

    toggle_new_chat_form() {
        let modal_id = random_ID();
        $.modal({
            title: 'New Chat',
            closeIcon: true,
            class: 'tiny',
            content: `
                <div id="new_chat_alerts"></div>
                <div class="ui left icon fluid input">
                  <input type="text" placeholder="Chat title ..." id="${modal_id}_chat_title">
                  <i class="users icon"></i>
                </div>
            `,
            actions: [
                {
                    text: 'Create Chat',
                    click: () => {
                        let title = document.getElementById(`${modal_id}_chat_title`).value;
                        this.create_new_chat(title);
                    }
                }
            ],
        }).modal('show');
    }

    toggle_chat_settings_form(chat_name) {
        let modal_id = random_ID();
        $.modal({
            title: 'Chat Settings',
            closeIcon: true,
            class: 'tiny',
            actions: [
                {
                    text: 'Share',
                    class: 'disabled',
                    click: () => { },
                },
                {
                    text: 'Delete Chat',
                    class: 'red basic left floated',
                    click: () => { this.delete_chat_approve_popup(chat_name); }
                }
            ],
        }).modal('show');
    }

    delete_chat_approve_popup(chat_name) {
        $.modal({
            title: 'Approve your choice',
            closeIcon: true,
            class: 'tiny',
            content: ``,
            actions: [
                {
                    text: 'Yes, I want to delete this chat.',
                    class: 'fluid red',
                    click: () => {
                        this.selected_chat = null;
                        this.save_state();
                        this.delete_chat(chat_name);
                    }
                }
            ],
        }).modal('show');
    }

    load_chat_lists() {
        let container = document.getElementById(`${this.el_id}_chats_list`);
        container.innerHTML = '';

        let chat_lists = document.createElement('div');
        chat_lists.className = 'ui middle aligned selection divided list';
        container.appendChild(chat_lists);

        container.classList.add('loading');
        axios.get('/chats/chat/list')
            .then((response) => {
                let chats = response.data['chats'];
                for (let chat of chats) {
                    let chat_item = document.createElement('div');
                    chat_item.className = 'item';
                    chat_item.style.padding = '15px';
                    chat_item.onclick = () => {
                        this.selected_chat = chat['name'];
                        this.save_state();
                        this.open_chat(chat['name']);
                    }
                    chat_item.innerHTML = `
                        <img class="ui avatar image" alt="NotFound" 
                            src="https://api.dicebear.com/9.x/identicon/svg?seed=${chat['name']}">
                        <div class="content">
                            <a class="header">${chat['title']}</a>
                            <div class="description"></div>
                        </div>
                    `;
                    chat_lists.appendChild(chat_item);
                }
            }).finally(() => {
                container.classList.remove('loading');
            })
    }

    create_new_chat(title) {
        let data = new FormData();
        data.append("title", title);
        axios.post('/chats/chat/add', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
            .then((response) => {
                this.load_chat_lists();
            }).catch((error) => {
                document.getElementById('new_chat_alerts').innerHTML = `
                    <div class="ui pink message" style="margin-bottom: 20px;">
                      <i class="close icon"></i>
                      <div class="header">Something went wrong... 😰</div>
                      <p>${error.response.data}</p>
                    </div>
                `;
                $('.message .close').on('click', function () {
                    $(this).closest('.message').transition('fade');
                });
            })
    }

    open_chat(chat_name) {
        document.getElementById('chat_header').innerHTML = `
            <div id="chat_header_content"></div>
        `;

        let chat_settings_btn = document.createElement('div');
        chat_settings_btn.className = 'ui basic icon circular extra-btn button';
        chat_settings_btn.onclick = () => { this.toggle_chat_settings_form(chat_name) }
        chat_settings_btn.innerHTML = `<i class="ui ellipsis horizontal icon"></i>`;

        document.getElementById('chat_header').appendChild(chat_settings_btn);

        document.getElementById('chat_messages').innerHTML = `
            <div class="ui basic placeholder segment" style="height: 100%">
              <div class="ui icon header">
                <i class="comment alternate outline icon"></i>
                There is no messages yet... <br> Lets text some ...
              </div>
            </div>
        `;

        this.init_message_input(document.getElementById('chat_form'), chat_name);
        this.load_chat_messages(chat_name);
    }

    init_message_input(container, chat_name) {
        let message_input_form = document.createElement('div');
        message_input_form.className = 'ui fluid icon input';

        let message_input = document.createElement('input');
        message_input.type = 'text';
        message_input.placeholder = 'Write a message...';
        message_input.id = "text_message_input";
        message_input.addEventListener("keyup", (event) => {
            if (event.keyCode === 13) {
                event.preventDefault();
                this.sent_message(chat_name);
            }
        });

        let message_icon = document.createElement('i');
        message_icon.className = 'circular paper plane outline link icon';
        message_icon.onclick = () => { this.sent_message(`${chat_name}`); }

        message_input_form.appendChild(message_input);
        message_input_form.appendChild(message_icon);
        container.innerHTML = '';
        container.appendChild(message_input_form);
    }

    load_chat_messages(chat_name) {
        let container = document.getElementById('chat_messages');
        container.classList.add('loading');
        axios.get(`/chats/message/list?chat_name=${chat_name}`)
            .then((response) => {
                let chat = response.data['chat'];
                let messages = response.data['messages'];
                document.getElementById('chat_header_content').innerHTML = `
                    <div class="ui items">
                      <div class="item" style="margin: 0">
                        <div class="content">
                          <div class="header">${chat['title'] ? chat['title'] : '---'}</div>
                          <div class="meta"> 
                            <span class="members">${chat['members_count']} member(s)</span> 
                          </div>
                        </div>
                      </div>
                    </div>
                `;
                if (!messages.length) {
                    return
                }

                container.innerHTML = `
                    <div class="ui comments" id="chat_messages_container"></div>
                `;
                let messages_template = '';
                for (let message of messages) {
                    messages_template += `
                        <div class="comment">
                            <div class="content">
                              <a class="author" href="/profile/${message['author']}/" target="_blank">${message['author']}</a>
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
                let chat_container = document.getElementById('chat_messages_container');

                chat_container.innerHTML = messages_template;
                container.scrollTop = container.scrollHeight;
            }).finally(() => {
                container.classList.remove('loading');
            })
    }

    delete_chat(chat_name) {
        let data = new FormData();
        data.append("chat_name", chat_name);
        axios.post('/chats/chat/delete', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
            .then((response) => {
                this.load_chat_lists();
            }).catch((error) => {
        }).finally(() => {})
    }

    sent_message(chat_name) {
        let message_input = document.getElementById('text_message_input');
        let data = new FormData();
        data.append("chat_name", chat_name);
        data.append("message", message_input.value);
        axios.post('/chats/message/add', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
            .then((response) => {
                this.load_chat_messages(chat_name);
                message_input.value = '';
            }).catch((error) => {
        }).finally(() => { })
    }

}