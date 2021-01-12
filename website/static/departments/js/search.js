function init_departments_search(on_select = null) {
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
                        price: `<div class="ui basic label">${department['type']['name']}</div>`,
                        description: get_department_description(department),
                    })
                }
                return {results: modified_response}
            },
        },
        onSelect: on_select,
        maxResults: 10,
        minCharacters: 2,
    });
}

function get_department_description(department) {
    let description = '';
    if (department['parent']) {
        description = department['parent']['name'];
        while (department['parent']) department = department['parent'];
        description = `${department['name']} &#x2014; ${description}`;
    }
    return description;
}
