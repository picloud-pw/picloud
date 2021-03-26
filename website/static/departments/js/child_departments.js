function child_departments_list(container, parent_department_id, max_display=7) {
    container.innerHTML += render_loader();

    axios.get(`/hierarchy/departments/search?parent_department_id=${parent_department_id}`)
        .then((response) => {
            let departments = response.data['departments'];
            let visible_part_id = random_ID();
            let hidden_part_id = random_ID();
            if (departments.length) {
                container.innerHTML = `
                    <div class="ui divided relaxed link list" id="${visible_part_id}"></div>
                    ${ departments.length > max_display ? `<hr>
                        <div class="ui accordion">
                          <div class="title" style="text-align: center; color: #5d84ae">Show all...</div>
                          <div class="content">
                            <div class="ui divided relaxed link list" id="${hidden_part_id}"></div>
                          </div>
                        </div>` : ''
                    }
                `;
            } else {
                container.innerHTML = render_placeholder(
                    'university',
                    'Looks like there is no sub-departments...'
                );
            }
            for (let i in departments) {
                let d = departments[i];
                container = document.getElementById(i < max_display ? visible_part_id : hidden_part_id)
                container.innerHTML += `
                    <a class="item" style="cursor: pointer" onclick="init_child_department_page('${d['id']}')">
                        <i class="large middle aligned university icon"></i>
                        <div class="middle aligned content">
                          <div class="header">${d['name']}</div>
                          <div class="description">${d['type']['name']}</div>
                        </div>
                    </a>
               `;
            }
            $('.ui.accordion').accordion();
        })
        .finally(() => {
            departments_container.classList.remove('loading');
        })
}