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
                        price: `[${department['type']['name']}]`,
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