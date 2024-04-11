let USER_INFO = {};

document.addEventListener("DOMContentLoaded", function () {
    restore_state();
});

function save_state() {}

function restore_state() {
    let pathname = new URL(window.location.href).pathname;
    let path_parts = pathname.split('/');

    if (path_parts.length === 4) {
        let username = path_parts[2];
        get_userinfo(username).then(() => {
            display_user_card(document.getElementById('user_avatar'));
            display_posts(document.getElementById('user_content'), USER_INFO['id']);
            display_user_department(document.getElementById('user_stats'), USER_INFO['department'])
        })
    }
}

function get_userinfo(username) {
    return axios.get(`/students/get?username=${username}`)
        .then((response) => {
            USER_INFO = response.data;
        })
}

function display_posts(container, user_id) {
    container.innerHTML = `
        <div class="ui secondary huge menu">
            <a class="active item" data-tab="posts_tab">Posts</a>
            <a class="item" data-tab="drafts_tab">Drafts</a>
            <a class="item" data-tab="moderation_tab">Moderation</a>
        </div>
        <div class="ui bottom attached active loading tab" data-tab="posts_tab" id="user_posts"></div>
        <div class="ui bottom attached tab" data-tab="drafts_tab" id="user_drafts"></div>
        <div class="ui bottom attached tab" data-tab="moderation_tab" id="moderation_posts"></div>
    `;
    get_student_posts(user_id, false, true).then((response) => {
        let container = document.getElementById('user_posts');
        container.classList.remove('loading');
        display_students_posts_as_tiles(container, response.data['posts']);
    })

    get_student_posts(user_id, true, false).then((response) => {
        let container = document.getElementById('user_drafts');
        display_students_posts_as_tiles(container, response.data['posts']);
    })

    get_student_posts(user_id, false, false).then((response) => {
        let container = document.getElementById('moderation_posts');
        display_students_posts_as_tiles(container, response.data['posts']);
    })

    $('.menu .item').tab();
}

function display_user_department(container, department) {
    if (!department) {
        container.innerHTML += `
            <div class="ui basic placeholder segment">
              <div class="ui icon header">
                <i class="university icon"></i>
                User hasn't chosen a department yet.
              </div>
            </div>
        `;
    } else {
        container.innerHTML += `
            <h2 class="ui header">Department</h2>
            <div id="hierarchy_container"></div>
        `;
        display_department_hierarchy(
            document.getElementById('hierarchy_container'),
            department['id']
        );
    }
}

function display_user_card(container) {
    container.innerHTML = `
        <div class="ui image">
            <img src="${USER_INFO['avatar']}" alt="avatar" 
                style="padding-top: 30px; background-color: #fff">
        </div>
        <h1 class="ui header" style="overflow: hidden; text-overflow: ellipsis">
            ${USER_INFO['user']['username']}
        </h1>
    `;
}
