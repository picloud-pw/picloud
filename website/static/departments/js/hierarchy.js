function display_department_hierarchy(container, department_id) {

    function format_item(department) {
        return `
            <div class="ui list">
                <div class="item">
                    <i class="university icon"></i>
                    <div class="content">
                      <a class="header" href="/departments?id=${department['id']}" target="_blank">
                        ${department['name']}
                      </a>
                      <div class="description">${department['type']['name']}</div>
                      ${department['child'] ? format_item(department['child']) : ''}
                </div>
            </div>
        `;
    }

    container.classList.add('loading');
    axios.get(`/hierarchy/departments/get?id=${department_id}`)
        .then((response) => {
            let department = response.data['hierarchy'];
            container.innerHTML = format_item(department);
        })
        .finally(() => {
            container.classList.remove('loading');
        });
}