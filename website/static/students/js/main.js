document.addEventListener("DOMContentLoaded", function () {

    init_students_search(
        (result, response) => {
            display_student_page(result['id']);
    });
    restore_state();

});

let PAGE = 1;
let STUDENT_ID = null;

function save_state() {
    let state = {};
    if (STUDENT_ID) {
        state = {
            "id": STUDENT_ID,
        };
    }
    push_state(state);
}

function restore_state() {
    let params = new URLSearchParams(document.location.search);

    STUDENT_ID = params.get("id");

    if (STUDENT_ID) {
        display_student_page(STUDENT_ID)
    } else {
        init_students_list();
    }

}

function display_student_page(student_id) {
    STUDENT_ID = student_id;
    save_state();

    let container = document.getElementById("students_container");
    container.innerHTML = `
        <div class="ui centered stackable grid">
            <div class="ui four wide column" id="student_info"></div>
            <div class="ui six wide column" id="students_posts"></div>
        </div>
    `;
    display_student_card(
        document.getElementById('student_info'),
        student_id
    );
    display_students_posts(
        document.getElementById('students_posts'),
        student_id
    );



}

function display_student_card(container, student_id){
    container.classList.add('loading');
    axios.get(`/students/get?id=${student_id}`)
        .then((response) => {
            let user = response.data;
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
        }).finally(() => {
            container.classList.remove('loading');
        })
}

function display_students_posts(container, student_id){
    container.innerHTML = `
        <div class="ui segment">
            <div class="ui dividing header">Posts</div>
            <div class="ui relaxed divided list" id="posts_container"></div>
        </div>
    `;
    container = document.getElementById('posts_container');
    container.parentElement.classList.add('loading');
    axios.get(`/posts/search?author_id=${student_id}`)
        .then((response) => {
            let posts = response.data['posts'];
            for (let post of posts){
                container.innerHTML += `
                    <div class="item">
                        <i class="large sticky note outline middle aligned icon"></i>
                        <div class="content">
                          <a class="header" href="" target="_blank">${post['title']}</a>
                          <div class="description">${post['created_date_human']}</div>
                        </div>
                    </div>
                `;
            }
            if (!posts.length) {
                container.innerHTML = `
                    <div class="ui placeholder segment">
                      <div class="ui icon header">
                        <i class="sticky note outline icon"></i>
                        No posts are listed for this student.
                      </div>
                    </div>
                `;
            }

        }).finally(() => {
            container.parentElement.classList.remove('loading');
        })
}

function init_students_list() {
    PAGE = 1;

    let rc = document.getElementById("students_container");
    rc.innerHTML = `
        <div class="ui centered grid">
            <div class="ui ten wide column" style="text-align: center">
                <div class="ui basic segment divided items" id="students_list"></div>
                <div class="ui button" id="load_button">
                    Load more
                </div>
            </div>
        </div>
    `;
    let students_list_container = document.getElementById('students_list');

    rc.addEventListener('scroll', function () {
        if (rc.scrollHeight - rc.scrollTop <= rc.clientHeight) {
            load_students(students_list_container);
        }
    });
    document.getElementById('load_button').onclick = () => {
        load_students(students_list_container);
    }

    load_students(students_list_container);

}

function load_students(container) {
    let load_button = document.getElementById('load_button');
    load_button.classList.add('loading');
    axios.get(`/students/search?p=${PAGE}`)
        .then((response) => {
            let students = response.data['students'];
            for (let student of students) {
                container.innerHTML += `
                    <div class="item">
                        <div class="ui tiny image">
                          <img class="avatar" src="${student['avatar']}" alt="${student['user']['username']} avatar">
                        </div>
                        <div class="middle aligned content">
                          <a class="header" onclick="display_student_page('${student['id']}')">
                            ${student['user']['username']}
                          </a>
                          <div class="meta">
                            <span>${student['status']['title']}</span>
                          </div>
                        </div>
                    </div>
                `;
            }
            PAGE += 1;
        })
        .finally(() => {
            load_button.classList.remove('loading');
        })
}