function child_departments_list(container, parent_department_id) {
    container.innerHTML += `
        <div class="ui divided relaxed list" id="departments_list">
            ${render_loader()}
        </div>
    `;
    container = document.getElementById('departments_list');
    axios.get(`/hierarchy/departments/search?parent_department_id=${parent_department_id}`)
        .then((response) => {
            let departments = response.data['departments'];
            container.innerHTML = departments.length ? '' :
                render_placeholder('university', 'Looks like there is no sub-departments...');
            for (let d of departments) {
                container.innerHTML += `
                    <div class="item" style="cursor: pointer" onclick="init_child_department_page('${d['id']}')">
                        <i class="large university middle aligned icon"></i>
                        <div class="middle aligned content">
                          <div class="header">${d['name']}</div>
                          <div class="description">${d['type']['name']}</div>
                        </div>
                    </div>
               `;
            }
        })
        .finally(() => {
            departments_container.classList.remove('loading');
        })
}