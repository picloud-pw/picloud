document.addEventListener("DOMContentLoaded", function () {

    restore_state();

});

let POST_ID = null;

function save_state() {
    let state = {};
    if (POST_ID) {
        state = {
            "id": POST_ID,
        };
    }
    push_state(state);
}

function restore_state() {
    let params = new URLSearchParams(document.location.search);

    POST_ID = params.get("id");

    if (POST_ID) {
        init_page(POST_ID);
    } else {

    }

}

function init_page(post_id) {
    let container = document.getElementById("posts_container");
    container.innerHTML = `
        <div class="ui seven wide computer sixteen wide tablet column">
            <div id="post"></div>
            <div class="ui segment">
                ${show_ad_block('horizontal')}
            </div>
        </div>
        <div class="ui five wide computer sixteen wide tablet column">
            <div class="ui segment" id="comments_list" style="margin-top: 10px; min-height: 80px"></div>
            <div class="ui segment" id="comments_form">
                <div class="ui icon fluid input">
                  <input type="text" placeholder="Add comment" id="comment_text" >
                  <i class="paper plane outline icon"></i>
                </div>
            </div>
        </div>
    `;
    display_post(document.getElementById('post'), post_id);
    display_comments(post_id);
    push_ads();

    document.getElementById("comment_text")
        .addEventListener("keyup", function(event) {
        if (event.keyCode === 13) {
            add_comment();
        }
    });
}

function add_comment() {
    let field = document.getElementById("comment_text");

    let data = new FormData();
    data.append("post_id", POST_ID);
    data.append("text", field.value);
    axios.post('/posts/comments/add', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {
            display_comments(POST_ID);
            field.value = "";
        })
}

function delete_comment(comment_id) {
    let data = new FormData();
    data.append("id", comment_id);
    axios.post('/posts/comments/delete', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {
            display_comments(POST_ID);
        })
}

function display_post(container, post_id) {
    container.classList.add('loading');
    axios.get(`/posts/search?id=${post_id}`)
        .then((response) => {
            let posts = response.data['posts'];
            container.appendChild(render_post(posts[0]));
        })
        .finally(() => {
            container.classList.remove('loading');
        })
}

function display_comments(post_id) {
    let container = document.getElementById('comments_list');
    container.classList.add('loading');
    axios.get(`/posts/comments/get?post_id=${post_id}`)
        .then((response) => {
            let comments = response.data['comments'];
            if (comments.length) {
                container.innerHTML = `
                    <div class="ui comments" id="comments_container"></div>
                `;
                for (let comment of comments) {
                    document.getElementById('comments_container').innerHTML += `
                        <div class="comment">
                            <a class="avatar" href="/students?id=${comment['author']['id']}">
                                <img src="${comment['author']['avatar']}" alt="ava"> 
                            </a>
                            <div class="content">
                              <a class="author" href="/students?id=${comment['author']['id']}">
                                ${comment['author']['username']}
                              </a>
                              <div class="metadata">
                                <span class="date">${new Date(comment['created_date']).toPrettyString()}</span>
                              </div>
                              <div class="text">${comment['text']}</div>
                              <div class="actions">
                                <a class="delete" onclick="delete_comment('${comment['id']}')">
                                    Delete
                                </a>
                              </div>
                            </div>
                        </div>
                    `;
                }
            } else {
                container.innerHTML = `
                    <div class="ui placeholder basic segment">
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