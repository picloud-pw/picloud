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
            <div class="ui four wide column">
                <div id="student_info"></div>
                <div class="ui segment">
                    <div class="ui dividing header">Department</div>
                    <div id="student_department"></div>
                </div>
            </div>
            <div class="ui six wide column">
                <div id="students_posts"></div>
            </div>
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

            display_student_department(user['department'] ? user['department']['id'] : null);
        }).finally(() => {
            container.classList.remove('loading');
        })
}

function display_student_department(department_id){
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

function init_students_list() {
    PAGE = 1;

    let rc = document.getElementById("students_container");
    rc.innerHTML = `
        <div class="ui centered grid">
            <div class="four wide column">
                <div class="ui segment">
                    <div class="ui dividing header">Filters</div>
                    <div id="filters_container"></div>
                </div>
            </div>
            <div class="six wide column">
                <div class="ui segment">
                    <div class="ui dividing header">Students</div>
                    <div class="ui basic segment divided items" id="students_list"></div>
                    <div class="ui button" id="load_button">
                        Load more
                    </div>
                </div>
            </div>
        </div>
    `;
    let students_list_container = document.getElementById('students_list');
    let filters_container = document.getElementById('filters_container');

    init_filters(filters_container);

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

function init_filters(container) {
    container.innerHTML = `
        <div class="ui form" id="filters_form">
          <div class="field">
            <label>Student status</label>
            <select class="ui dropdown" id="student_status">
                <option value="any" selected>Any</option>
            </select>
          </div>
          <div class="ui divider"></div>
          <div class="inline field">
            <div class="ui slider checkbox" id="custom_avatar">
              <input type="checkbox" tabindex="0" class="hidden">
              <label>Custom avatar</label>
            </div>
          </div>
          <div class="ui divider"></div>
        </div>
    `;
    $('.ui.checkbox').checkbox();

    axios.get('/students/statuses')
        .then((response) => {
            let statuses = response.data['statuses'];
            let container = document.getElementById('student_status');
            for (let s of statuses) {
                container.innerHTML += `
                    <option value="${s['id']}">${s['title']}</option>
                `;
            }
            $('#student_status').dropdown()
        })

}
