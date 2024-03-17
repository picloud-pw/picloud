function display_departments_list(container, parent_department_id, query) {
    container.innerHTML = `
        <div class="ui link doubling three stackable cards" id="sub_department_cards"></div>
    `;
    let endpoint = `/hierarchy/departments/search` +
        `?parent_department_id=${parent_department_id}` +
        `&q=${query}`;
    axios.get(endpoint)
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
                document.getElementById('sub_department_cards').innerHTML += `
                    <div class="ui fluid card" style="cursor: unset">
                        <a class="content" href="/deps/${d['id']}/">
                          <div class="header">${d['name']}</div>
                        </a>
                        <div class="extra content">
                            <div class="ui basic label">${d['type']['name']}</div>
                            <div class="ui basic blue right floated mini button" onclick="change_department('${d['id']}')">
                                Choose this department
                            </div>
                        </div>
                    </div>
               `;
            }
        })
}

function change_department(department_id) {
    let form_data = new FormData();
    form_data.append("department_id", department_id);

    axios.post(`/students/me/edit`, form_data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {
            show_alert("success", "Your Department changed!");
            console.log(response);
        })
}