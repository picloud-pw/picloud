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
        <div class="ui secondary huge menu" style="margin-bottom: 20px">
            <a class="active item" data-tab="posts_tab">Posts</a>
            <a class="item" data-tab="drafts_tab">Drafts</a>
            <a class="item" data-tab="moderation_tab">Moderation</a>
        </div>
        <div class="ui bottom attached active loading tab" data-tab="posts_tab" id="user_posts"></div>
        <div class="ui bottom attached tab" data-tab="drafts_tab" id="user_drafts"></div>
        <div class="ui bottom attached tab" data-tab="moderation_tab" id="moderation_posts"></div>
    `;
    new PostFeed({
        'author_id': user_id,
        'is_draft': false,
        'is_approved': true,
    }).display_posts_as_tiles(document.getElementById('user_posts'));

    new PostFeed({
        'author_id': user_id,
        'is_draft': true,
        'is_approved': false,
    }).display_posts_as_tiles(document.getElementById('user_drafts'));

    new PostFeed({
        'author_id': user_id,
        'is_draft': false,
        'is_approved': false,
    }).display_posts_as_tiles(document.getElementById('moderation_posts'));

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

function display_student_card(container, student_id) {
    container.classList.add('loading');
    axios.get(`/students/get?id=${student_id}`)
        .then((response) => {
            let user = response.data;
            document.title = user['user']['username'];
            document.getElementById('student_info').innerHTML = `
                <div class="ui fluid card">
                  <div class="image">
                    <img src="${user['avatar']}" alt="avatar">
                  </div>
                  <div class="content">
                    <div class="header">${user['user']['username']}</div>
                    <div class="meta">
                      <span class="date">Last login at ${new Date(user['user']['last_login']).toPrettyString()}</span>
                    </div>
                  </div>
                  <div class="content">
                      <span title="Status">
                          <i class="map marker icon"></i> ${user['status']['title']}
                      </span>
                      <span class="right floated" title="Karma"> 
                          ${user['karma']} <i class="certificate icon"></i>
                      </span>
                  </div>
                </div>
            `;

            display_student_department(user['department'] ? user['department']['id'] : null);
        }).finally(() => {
        container.classList.remove('loading');
    })
}

function display_student_department(department_id) {
    let container = document.getElementById('student_department');
    if (department_id) {
        display_department_hierarchy(
            container,
            department_id,
        )
    } else {
        container.innerHTML = `
            <div class="ui basic placeholder segment">
                <div class="ui icon header">
                    <i class="university icon"></i>
                    Student hasn't chosen a department yet.
                </div>
            </div>
        `;
    }

}
