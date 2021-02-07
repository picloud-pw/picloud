let ME = null;
let POSTS = {};

document.addEventListener("DOMContentLoaded", function () {

    axios.get('/students/me')
        .then(response => {
            ME = response.data;
            init_page();
        })

});

function init_page() {

    load_drafts();

}

function init_hierarchy_section(department_id = null, subject_id = null) {
    if (department_id) {
        display_department_hierarchy(
            document.getElementById('department_hierarchy'),
            department_id,
        );
        init_subjects_list(department_id, subject_id);
    } else if (ME['department']) {
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

function load_post_types(container) {
    let select = document.getElementById(container);
    select.innerText = '';
    axios.get('/posts/types/get')
        .then(response => {
            let types = response.data['types'];
            for (let type of types) {
                select.innerHTML += `
                    <option value="${type['title']}">${type['title']}</option>
                `;
            }
            $(`#${container}`).dropdown();
        })

}


function init_subjects_list(department_id, subject_id) {
    let select = document.getElementById('subject');
    select.innerText = '';
    axios.get(`/hierarchy/subjects/search?department_id=${department_id}`)
        .then(response => {
            let subjects = response.data['subjects'];
            for (let s of subjects) {
                select.innerHTML += `
                    <option value="${s['id']}" ${s['id'] === subject_id ? 'selected' : ''}>
                        ${s['name']} (sem. ${s['semester'] ? s['semester'] : '---'})
                    </option>
                `;
            }
            $('#subject').dropdown();
        })
}

function change_display_mode(post_id) {
    let btn_icon = document.getElementById(`${post_id}_display_mode_icon`);
    btn_icon.className = btn_icon.className === 'eye icon' ? 'edit icon' : 'eye icon';

    let textarea = document.getElementById(`${post_id}_textarea`);
    textarea.style.display = textarea.style.display === 'none' ? 'block' : 'none';

    let render_area = document.getElementById(`${post_id}_render_area`);
    if (render_area.style.display === 'none') {
        let converter = new showdown.Converter();
        render_area.innerHTML = converter.makeHtml(textarea.value);
        render_area.style.display = 'block';
    } else {
        render_area.style.display = 'none';
    }
}

function load_drafts() {
    axios.get('/posts/search?is_draft=True')
        .then((response) => {
            let drafts = response.data['posts'];
            console.log(drafts);
            if (!drafts.length) {
                new_draft_post();
                init_hierarchy_section();
            } else {
                let last_draft = drafts[0];
                init_hierarchy_section(
                    last_draft['subject'] ? last_draft['subject']['departments'][0]['id'] : null,
                    last_draft['subject'] ? last_draft['subject']['id'] : null,
                );
                fill_post_body(last_draft);
            }
        })
}

function new_draft_post() {
    let data = new FormData();
    axios.post('/posts/new', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {
            fill_post_body(response.data);
        })
}

function fill_post_body(post) {
    let post_id = post['id'];
    let body_segment = document.createElement('div');
    body_segment.id = post_id;
    body_segment.className = 'ui segment';
    document.getElementById('bodies_editor_container').appendChild(body_segment);
    body_segment.innerHTML = `
        <div class="ui circular right floated icon mini button" style="margin: -25px"
            onclick="remove_post('${post_id}')">
            <i class="ui x icon"></i>
        </div>
        <div class="fields">
            <div class="six wide field">
                <label>Post type</label>
                <select class="ui search dropdown" id="${post_id}_type"></select>
            </div>
            <div class="ten wide field">
                <label>Title</label>
                <input type="text" id="${post_id}_title" placeholder="Title" value="${post['title']}">
            </div>
        </div>
        <div id="${post_id}_toolbar"></div>
        <textarea id="${post_id}_textarea">${post['text'] ? post['text']: ''}</textarea>
        <div id="${post_id}_render_area" style="display: none"></div>
    `;

    load_post_types(`${post_id}_type`);
    display_toolbar(post_id, `${post_id}_toolbar`);

    $(`#${post_id}`).find('input, select, textarea').each(function () {
        $(this).change(function () {
            save_post_changes(post_id);
        });
    });
}

function remove_post(post_id) {
    let data = new FormData();
    data.append("id", post_id);
    axios.post('/posts/delete', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {
            delete POSTS[post_id];
            document.getElementById(post_id).remove();
        })
}

function save_post_changes(post_id) {
    POSTS[post_id] = {
        'id': post_id,
        'type': $(`#${post_id}_type`).dropdown('get value'),
        'title': $(`#${post_id}_title`).val(),
        'text': $(`#${post_id}_textarea`).val(),
    }
    let data = new FormData();
    for (let field in POSTS[post_id]) {
        data.append(field, POSTS[post_id][field]);
    }
    axios.post('/posts/update', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {})
}

function display_toolbar(post_id, container) {
    document.getElementById(container).innerHTML = `
        <div class="ui basic segment" style="padding: 0 0 10px 0">
            <div class="ui icon mini buttons" style="vertical-align: bottom">
                <div class="ui button" onclick="header('${post_id}', 1)"><i class="heading icon"></i></div>
                <div class="ui button" onclick="header('${post_id}', 3)"><i class="heading small icon"></i></div>
                <div class="ui button" onclick="header('${post_id}', 6)"><i class="heading mini icon"></i></div>
            </div>
            <div class="ui icon mini buttons">
                <div class="ui button" onclick="outline('${post_id}', 'bold')"><i class="bold icon"></i></div>
                <div class="ui button" onclick="outline('${post_id}', 'italic')"><i class="italic icon"></i></div>
            </div>
            <div class="ui icon mini buttons">
                <div class="ui button" onclick="code_block('${post_id}')"><i class="code icon"></i></div>
                <div class="ui button" onclick="list_item('${post_id}')"><i class="list ol icon"></i></div>
            </div>
            <div class="ui icon mini buttons">
                <div class="ui button" onclick="link_template('${post_id}', 'link')"><i class="linkify icon"></i></div>
                <div class="ui button" onclick="link_template('${post_id}', 'image')"><i class="image outline icon"></i></div>
            </div>
            <a class="ui circular icon right floated blue basic mini button"
               href="https://github.com/sandino/Markdown-Cheatsheet/blob/master/README.md"
               target="_blank"
               title="Markdown syntax guide">
                <i class="info icon"></i>
            </a>
            <div class="ui basic icon right floated circular mini button"
                 title="Change mode – 'edit' / 'preview'"
                 onclick="change_display_mode('${post_id}')">
                <i id="${post_id}_display_mode_icon" class="eye icon"></i>
            </div>
        </div>
    `;
}
