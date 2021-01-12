let ME = null;

document.addEventListener("DOMContentLoaded", function () {

    axios.get('/students/me')
        .then(response => {
            ME = response.data;
            init_page();
        })

});

function init_page() {
    load_post_types();
    init_hierarchy_section();
}

function init_hierarchy_section() {
    if (ME['department']) {
        display_department_hierarchy(
            document.getElementById('department_hierarchy'),
            ME['department']['id'],
        );
        init_subjects_list(ME['department']['id']);
    } else {
        init_departments_search((result, response) => {
            $("input[name='department_id']").val(result['department_id']);
            display_department_hierarchy(
                document.getElementById('department_hierarchy'),
                result['department_id']
            );
            init_subjects_list(result['department_id']);
        })
    }

}

function load_post_types() {
    let select = document.getElementById('post_type');
    select.innerText = '';
    axios.get('/posts/types/get')
        .then(response => {
            let types = response.data['types'];
            for (let type of types) {
                select.innerHTML += `
                    <option value="${type['title']}">${type['title']}</option>
                `;
            }
            $('#post_type').dropdown();
        })

}


function init_subjects_list(department_id) {
    let select = document.getElementById('subject');
    select.innerText = '';
    axios.get(`/hierarchy/subjects/search?department_id=${department_id}`)
        .then(response => {
            let subjects = response.data['subjects'];
            for (let s of subjects) {
                select.innerHTML += `
                    <option value="${s['id']}">
                        ${s['name']} (sem. ${s['semester'] ? s['semester'] : '---'})
                    </option>
                `;
            }
            $('#subject').dropdown();
        })
}

function change_display_mode() {
    let btn_icon = document.getElementById('display_mode_icon');
    btn_icon.className = btn_icon.className === 'eye icon' ? 'edit icon' : 'eye icon';

    let textarea = document.getElementById('textarea');
    textarea.style.display = textarea.style.display === 'none' ? 'block' : 'none';

    let render_area = document.getElementById('render_area');
    if (render_area.style.display === 'none') {
        let converter = new showdown.Converter();
        render_area.innerHTML = converter.makeHtml(textarea.value);
        render_area.style.display = 'block';
    } else {
        render_area.style.display = 'none';
    }
}

function submit_form() {

}
