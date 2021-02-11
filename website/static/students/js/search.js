function init_students_search(on_select = null) {
    $('.ui.search').search({
        apiSettings: {
            url: "/students/search?q={query}",
            onResponse: (response) => {
                let students = response['students'];
                let modified_response = [];
                for (let student of students) {
                    modified_response.push({
                        id: student['id'],
                        title: student['user']['username'],
                        description: student['status']['title'],
                        price: `[${student['karma']}]`,
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