document.addEventListener("DOMContentLoaded", function () {

    init_students_search(
        (result, response) => {
            display_student_page(result['id']);
        });
    restore_state();

});

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
        display_student_search_page();
    }

}

function display_student_search_page() {
    document.getElementById('students_container').innerHTML = `
        <div class="ui centered stackable grid">
            <div class="four wide computer ten wide tablet sixteen wide mobile column">
                <div class="ui segment">
                    <div class="ui dividing header">Filters</div>
                    <div id="filters_container"></div>
                </div>
                <div class="ui segment">
                    ${show_ad_block('vertical')}
                </div>
            </div>
            <div class="five wide computer ten wide tablet sixteen wide mobile column">
                <div class="ui segment">
                    <div class="ui dividing header">Students</div>
                    <div id="students_list"></div>
                </div>
            </div>
        </div>
    `;

    init_students_filters(
        document.getElementById('filters_container'),
        document.getElementById('students_list'),
    );
    push_ads();
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
                <div class="ui segment">
                    <div class="ui dividing header">Posts</div>
                    <div id="students_posts"></div>
                </div>
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

function display_student_card(container, student_id) {
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
