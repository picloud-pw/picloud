document.addEventListener("DOMContentLoaded", function () {

    init_students_list();

});

let PAGE = 1;

function init_students_list() {
    PAGE = 1;

    let rc = document.getElementById("students_container");
    rc.addEventListener('scroll', function () {
        if (rc.scrollHeight - rc.scrollTop <= rc.clientHeight) {
            load_students();
        }
    });

    load_students();

}

function load_students() {
    let container = document.getElementById('students_container');
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
                          <a class="header">${student['user']['username']}</a>
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