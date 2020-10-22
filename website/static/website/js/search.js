function init_search(container, search_type, on_select = null) {

    container.innerHTML += `

              <div class="ui disabled dropdown icon circular basic button" id="search_type" style="text-align: center">
                <i class="filter icon"></i>
                <span class="text" style="width: 100px;"></span>
                <div class="menu">
                    <div class="item" data-value="posts">Posts</div>
                    <div class="item" data-value="departments">Departments</div>
                    <div class="item" data-value="students">Students</div>
                </div>
              </div>

              <span class="ui fluid search">
                  <div class="ui left icon input">
                    <i class="search icon"></i>
                    <input class="prompt" id="search" type="text" placeholder="Enter search query"
                        style="border-radius: 50px;">
                  </div>
                  <div class="search results"></div>
              </span>
        
    `;
    $('#search_type').dropdown({
        onChange: function() {

        }
    }).dropdown("set selected", search_type);

    $('.ui.search').search({
        apiSettings: get_settings(search_type),
        onSelect: on_select,
        maxResults: 10,
        minCharacters: 2,
    });
}

function get_settings(search_type) {
    let settings = {};

    if (search_type === 'posts') {
        settings = {
            url: "/posts/search?q={query}",
            onResponse: (response) => {
                let posts = response['posts'];
                let modified_response = [];
                for (let post of posts) {
                    modified_response.push({
                        post_id: post['id'],
                        title: post['title'],
                        price: post['author']['username'],
                        description: `[${post['created_date_human']}] ${post['subject']['name']}`,
                    })
                }
                return {results: modified_response}
            },
        }
    }

    if (search_type === 'departments') {
        settings = {
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
        }
    }

    if (search_type === 'students') {
        settings = {
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
        }
    }

    return settings;
}
