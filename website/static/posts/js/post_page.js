import {Post} from "./post.js";

export class PostPage {

    post_id = null;

    constructor(container, settings) {
        this.container = container;
        this.restore_state();
    }

    restore_state() {
        let params = new URLSearchParams(document.location.search);

        let pathname = new URL(window.location.href).pathname;
        let path_parts = pathname.split('/');

        if (path_parts.length === 4) {
            this.post_id = path_parts[2]
            this.init_page(this.post_id);
        } else {
            show_alert('warning', 'Somthing wrong with URL');
        }
    }

    init_page(post_id) {
        this.container.innerHTML = `
            <div class="ui centered stackable padded grid">
                <div class="ui seven wide computer sixteen wide tablet column">
                    <div id="post"></div>
                    <div class="ui segment" id="comments_list" style="margin-top: 10px; min-height: 80px"></div>
                    <div class="ui segment" id="comments_form">
                        <div class="ui icon fluid input">
                          <input type="text" placeholder="Add comment" id="comment_text" >
                          <i class="paper plane outline icon"></i>
                        </div>
                    </div>
                </div>
            </div>
        `;
        this.display_post(document.getElementById('post'), post_id);
        this.display_comments(post_id);

        document.getElementById("comment_text").addEventListener("keyup",  (event) => {
            if (event.keyCode === 13) {
                this.add_comment();
            }
        });
    }

    add_comment() {
        let field = document.getElementById("comment_text");

        let data = new FormData();
        data.append("post_id", this.post_id);
        data.append("text", field.value);
        axios.post('/posts/comments/add', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
            .then((response) => {
                this.display_comments(this.post_id);
                field.value = "";
            })
    }

    delete_comment(comment_id) {
        let data = new FormData();
        data.append("id", comment_id);
        axios.post('/posts/comments/delete', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
            .then((response) => {
                this.display_comments(this.post_id);
            })
    }

    display_post(container, post_id) {
        container.classList.add('loading');
        axios.get(`/posts/get?id=${post_id}`)
            .then((response) => {
                let post = response.data;
                document.title = post['title'];
                container.appendChild(new Post().render_post(post));
            })
            .finally(() => {
                container.classList.remove('loading');
            })
    }

    display_comments(post_id) {
        let container = document.getElementById('comments_list');
        container.classList.add('loading');
        axios.get(`/posts/comments/get?post_id=${post_id}`)
            .then((response) => {
                let comments = response.data['comments'];
                if (comments.length) {
                    container.innerHTML = `<div class="ui comments" id="comments_container"></div>`;
                    for (let comment of comments) {
                        let comment_el = document.createElement('div');
                        comment_el.className = "comment";
                        comment_el.innerHTML = `
                            <a class="avatar" href="/profile/${comment['author']['username']}/">
                                <img src="${comment['author']['avatar']}" alt="ava"> 
                            </a>
                            <div class="content">
                              <a class="author" href="/profile/${comment['author']['username']}/">
                                ${comment['author']['username']}
                              </a>
                              <div class="metadata">
                                <span class="date">${new Date(comment['created_date']).toPrettyString()}</span>
                              </div>
                              <div class="text">${comment['text']}</div>
                              <div class="actions">
                                <a class="delete" id="${comment['id']}_comment_del_btn">
                                    Delete
                                </a>
                              </div>
                            </div>
                        `;
                        document.getElementById('comments_container').appendChild(comment_el);
                        document.getElementById(`${comment['id']}_comment_del_btn`).onclick = () => {
                            this.delete_comment(comment['id'])
                        }
                    }
                } else {
                    container.innerHTML = `
                    <div class="ui basic segment" style="text-align: center">
                      <div class="ui icon header">
                        <i class="comments outline icon"></i>
                        No comments are listed for this post.
                      </div>
                    </div>
                `;
                }
            })
            .finally(() => {
                container.classList.remove('loading');
            })
    }

}
