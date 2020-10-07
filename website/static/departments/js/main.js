document.addEventListener("DOMContentLoaded", function () {

    init_root_departments_list();

});

const departments_container = document.getElementById('departments_container');
const breadcrumbs_container = document.getElementById('breadcrumbs_container');

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
                        <div class="content">
                          <div class="header">${d['name']}</div>
                          <div class="description">${d['link']}</div>
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
                        <div class="ui tiny avatar image">
                            <img src="${d['logo']}" alt="logo">
                        </div>
                        <div class="content">
                          <div class="header">${d['name']}</div>
                          <div class="description">${d['link']}</div>
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
    breadcrumbs_container.innerHTML = `<div class="ui huge breadcrumb"></div>`;
    axios.get(`/hierarchy/departments/get?id=${department_id}`)
        .then((response) => {
            let parent = response.data['hierarchy'];
            console.log( response.data);
            while (parent) {
                breadcrumbs_container.innerHTML += `
                    <a class="section">${parent['name']}</a>
                    <i class="right chevron icon divider"></i>
                `;
                parent = parent['parent'];
            }

        });
}

function update_url() {
    
}

