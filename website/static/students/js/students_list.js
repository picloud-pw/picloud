let STUDENTS_PAGE = 1;

function init_students_list(container, filters=null) {
    STUDENTS_PAGE = 1;
    if (!filters) {
        filters = {'ps': 5}
    }
    let students_list_id = random_ID();
    let load_btn_id = students_list_id + "_load_button";

    container.innerHTML = `
        <div class="ui basic segment divided items" id="${students_list_id}">
            ${render_loader('avatar')}
        </div>
        <div class="ui fluid basic mini button" id="${load_btn_id}"> load more ... </div>
    `;

    document.getElementById(load_btn_id).onclick = () => {
        load_students(students_list_id, load_btn_id, filters);
    }

    load_students(students_list_id, load_btn_id, filters);
}

function load_students(container_id, load_btn_id, filters) {
    let container = document.getElementById(container_id);
    let load_button = document.getElementById(load_btn_id);
    load_button.classList.add('loading');
    let params = `p=${STUDENTS_PAGE}`;
    params += filters ? "&" + jQuery.param(filters) : '';
    axios.get(`/students/search?${params}`)
        .then((response) => {
            let students = response.data['students'];
            if (students.length) {
                // remove loader
                if (STUDENTS_PAGE === 1) container.innerHTML = '';
            } else {
                if (STUDENTS_PAGE === 1)
                    container.innerHTML = render_placeholder(
                        'user',
                        'Looks like there is not students for selected filters'
                    );
                load_button.remove();
            }
            for (let student of students) {
                container.innerHTML += `
                    <div class="item">
                        <div class="ui tiny image">
                          <img class="avatar" src="${student['avatar']}" alt="${student['user']['username']} avatar">
                        </div>
                        <div class="middle aligned content">
                          <a class="header" href="/students/?id=${student['id']}">
                            ${student['user']['username']}
                          </a>
                          <div class="meta">
                            <span>${student['status']['title']}</span>
                          </div>
                        </div>
                    </div>
                `;
            }
            STUDENTS_PAGE += 1;
        })
        .finally(() => {
            load_button.classList.remove('loading');
        })
}