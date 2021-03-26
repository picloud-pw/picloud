document.addEventListener("DOMContentLoaded", function () {

    init_departments_search(
        (result, response) => {
            init_child_department_page(result['department_id']);
        });

    restore_state();

});

const departments_container = document.getElementById('departments_container');
const breadcrumbs_container = document.getElementById('breadcrumbs_container');

let DEPARTMENT_ID = null;

function save_state() {
    let state = {};
    if (DEPARTMENT_ID) {
        state = {
            "id": DEPARTMENT_ID,
        };
    }
    push_state(state);
}

function restore_state() {
    let params = new URLSearchParams(document.location.search);

    DEPARTMENT_ID = params.get("id");

    if (DEPARTMENT_ID) {
        init_child_department_page(DEPARTMENT_ID);
    } else {
        init_universities_list();
    }

}

function init_universities_list() {
    document.title = 'Universities';
    departments_container.classList.add('loading');
    departments_container.innerText = '';
    breadcrumbs_container.style.display = 'none';

    departments_container.innerHTML = `
        <div class="six wide computer ten wide tablet sixteen wide mobile column"
                     style="margin: 40px; padding: 20px" id="universities">
        </div>
    `;
    let container = document.getElementById('universities');
    axios.get(`/hierarchy/departments/search?parent_department_id=null`)
        .then((response) => {
            let departments = response.data['departments'];
            for (let d of departments) {
                container.innerHTML += `
                    <div class="ui link items segment" style="cursor: pointer"
                            onclick="init_child_department_page('${d['id']}')">
                        <div class="item">
                            <div class="ui tiny avatar image">
                                <img src="${d['logo']}" alt="logo">
                            </div>
                            <div class="middle aligned content">
                              <div class="header">${d['name']}</div>
                            </div>
                        </div>
                    </div>
               `;
            }

        })
        .finally(() => {
            departments_container.classList.remove('loading');
        })
}

function init_child_department_page(parent_department_id) {
    DEPARTMENT_ID = parent_department_id;
    save_state();

    departments_container.innerText = '';
    departments_container.classList.add('loading');
    breadcrumbs_container.style.display = 'block';

    init_breadcrumbs(parent_department_id);
    departments_container.innerHTML = `
        <div class="seven wide column">
            <div class="ui segment">
                <div class="ui dividing header">Sub-departments</div>
                <div id="departments"></div>
            </div>
            <div class="ui segment">
                <div class="ui dividing header">Subjects</div>
                <div id="subjects"></div>
            </div>
        </div>
        <div class="seven wide column">
            <div class="ui segment">
                ${show_ad_block('horizontal')}
            </div>
            <div class="ui segment">
                <div class="ui dividing header">Students</div>
                <div id="students"></div>
            </div>
        </div>
    `;
    child_departments_list(
        document.getElementById('departments'),
        parent_department_id
    );
    department_subjects_list(
        document.getElementById('subjects'),
        parent_department_id
    );
    init_students_list(
        document.getElementById('students'),
        {
            'department_id': parent_department_id,
            'ps': 3,
        },
    )
    push_ads();
}

function init_breadcrumbs(department_id) {

    function format_breadcrumbs(container, node) {
        container.innerHTML += `
            <a class="step ${!node['child'] ? 'active' : ''}" title="${node['name']}"
                onclick="init_child_department_page('${node['id']}')">
                <i class="ui university icon"></i>
                <div class="content">
                    <div class="title">
                        ${node['name'].length > 50 ? node['name'].substr(0, 50) + '...' : node['name']}
                    </div>
                    <div class="description"></div>
                </div>
            </a>
        `;
        if (node['child']) {
            format_breadcrumbs(container, node['child']);
        } else {
            document.title = node['name'];
        }
    }

    breadcrumbs_container.innerHTML = `<div class="ui fluid steps" id="breadcrumbs"></div>`;
    let container = document.getElementById('breadcrumbs');
    container.innerText = "";

    axios.get(`/hierarchy/departments/get?id=${department_id}`)
        .then((response) => {
            let hierarchy = response.data['hierarchy'];
            format_breadcrumbs(container, hierarchy);
            $("a.section").popup({position: 'bottom center'});
        });
}
