document.addEventListener("DOMContentLoaded", function () {

    init_students_search(
        (result, response) => {
            display_student_info(result['id']);
    });
    init_students_list();

});

let PAGE = 1;

function display_student_info(student_id) {
    let container = document.getElementById("students_container");
    container.innerHTML = `
        ${student_id}
    `;
}

function init_students_list() {
    PAGE = 1;

    let rc = document.getElementById("students_container");
    rc.innerHTML = `
        <div class="ui basic segment divided items" id="students_list"></div>
        <div class="ui centered button" id="load_button">
            Load more
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
                          <a class="header" onclick="display_student_info('${student['id']}')">
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