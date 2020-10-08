document.addEventListener("DOMContentLoaded", function () {

    init_search();
    init_root_departments_list();

});

const departments_container = document.getElementById('departments_container');
const breadcrumbs_container = document.getElementById('breadcrumbs_container');

function init_search() {
    $('.ui.search').search({
        apiSettings: {
            url: "/hierarchy/departments/search?q={query}",
            onResponse: (response) => {
                let departments = response['departments'];
                let modified_response = [];
                for (let department of departments) {
                    modified_response.push({
                        department_id: department['id'],
                        title: department['name'],
                        price: `[${department['type']['name']}]`,
                    })
                }
                return {results: modified_response}
            },
        },
        onSelect: (result, response) => {
            init_child_department_list(result['department_id']);
        },
        maxResults: 10,
        minCharacters: 2,
    });
}

function init_root_departments_list() {
    departments_container.classList.add('loading');
    departments_container.innerText = '';
    breadcrumbs_container.style.display = 'none';
    axios.get(`/hierarchy/departments/search?parent_department_id=null`)
        .then((response) => {
            let departments = response.data['departments'];
            for (let d of departments) {
                departments_container.innerHTML += `
                    <div class="item" style="cursor: pointer" onclick="init_child_department_list('${d['id']}')">
                        <div class="ui tiny avatar image">
                            <img src="${d['logo']}" alt="logo">
                        </div>
                        <div class="middle aligned content">
                          <div class="header">${d['name']}</div>
                        </div>
                    </div>
               `;
            }

        })
        .finally(() => {
            departments_container.classList.remove('loading');
        })
}

function init_child_department_list(parent_department_id) {
    departments_container.innerText = '';
    departments_container.classList.add('loading');
    breadcrumbs_container.style.display = 'block';

    init_breadcrumbs(parent_department_id);
    axios.get(`/hierarchy/departments/search?parent_department_id=${parent_department_id}`)
        .then((response) => {
            let departments = response.data['departments'];
            for (let d of departments) {
                departments_container.innerHTML += `
                    <div class="item" style="cursor: pointer" onclick="init_child_department_list('${d['id']}')">
                        <div class="middle aligned content">
                          <div class="header">${d['name']}</div>
                        </div>
                    </div>
               `;
            }
        })
        .finally(() => {
            departments_container.classList.remove('loading');
        })
}

function init_breadcrumbs(department_id) {

    function shift_breadcrumb(container, node, is_last=false) {
        container.innerHTML = `
            <a class="section" title="${node['name']}"
                onclick="init_child_department_list('${node['id']}')">
                ${node['name'].length > 30 ? node['name'].substr(0, 30) + '...' : node['name']}
            </a>
            ${is_last ? '' : '<i class="right chevron icon divider"></i>'}
        ` + container.innerHTML;
    }

    breadcrumbs_container.innerHTML = `<div class="ui huge breadcrumb" id="breadcrumbs"></div>`;
    let container = document.getElementById('breadcrumbs');

    axios.get(`/hierarchy/departments/get?id=${department_id}`)
        .then((response) => {
            let department = response.data['department'];
            let parent = response.data['hierarchy'];
            shift_breadcrumb(container, department, true);
            while (parent) {
                shift_breadcrumb(container, parent);
                parent = parent['parent'];
            }
            $("a.section").popup({position: 'bottom center'});
        });
}

function update_url() {

}

