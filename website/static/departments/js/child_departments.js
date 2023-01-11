function child_departments_list(container, parent_department_id, max_display=7) {
    axios.get(`/hierarchy/departments/search?parent_department_id=${parent_department_id}`)
        .then((response) => {
            let departments = response.data['departments'];
            if (!departments.length) {
                container.innerHTML = render_placeholder(
                    'university',
                    'Looks like there is no sub-departments...'
                );
            }
            for (let i in departments) {
                let d = departments[i];
                container.innerHTML += `
                    <div class="ui segments">
                      <div class="ui segment">
                         <h4 class="ui header">${d['name']}</h4>
                      </div>
                      <div class="ui secondary segment">
                        <div class="ui basic label">${d['type']['name']}</div>
                        <a class="ui basic blue label" href="/deps/${d['id']}/" style="cursor: pointer">
                            Show sub-departments ...
                        </a>
                        <div class="ui right floated mini blue button" onclick="change_department('${d['id']}');">
                            Choose this department
                        </div>
                        
                      </div>
                    </div>
               `;
            }
        })
}

function change_department(department_id) {
    console.log(department_id);
    let form_data = new FormData();
    form_data.append("department_id", department_id);

    axios.post(`/students/me/edit`, form_data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => { show_alert("success", "Your Department changed!"); console.log(response); })
}