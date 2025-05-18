let STUDENTS_LIST_FILTERS = {
    'ps': 8,
};

function init_students_filters(container, list_container) {
    container.innerHTML = `
        <div class="ui form" id="filters_form">
          <div class="field">
            <label>Department</label>
            <div class="ui loading fluid search">
                <div class="ui fluid input">
                    <input class="fluid prompt" name="department_name" type="text"
                           placeholder="Enter search query">
                </div>
                <input name="department_id" type="hidden">
                <div class="search results"></div>
            </div>
            <div id="department_hierarchy" style="margin-top: 10px"></div>
          </div>
          <div class="field">
            <label>Student status</label>
            <select class="ui fluid compact dropdown" id="student_status">
                <option value="any" selected>Any</option>
            </select>
          </div>
          <div class="ui divider"></div>
          <div class="inline field">
            <div class="ui slider checkbox">
              <input type="checkbox" tabindex="0" class="hidden" id="custom_avatar">
              <label>Custom avatar</label>
            </div>
          </div>
          <div class="ui divider"></div>
        </div>
    `;

    $('.ui.checkbox').checkbox({
        'onChange': function () {
            update_filters();
            init_students_list(list_container, STUDENTS_LIST_FILTERS);
        }
    });

    $('#student_status').dropdown({
        onChange: function () {
            update_filters();
            init_students_list(list_container, STUDENTS_LIST_FILTERS);
        }
    })
    axios.get('/students/statuses')
        .then((response) => {
            let statuses = response.data['statuses'];
            let container = document.getElementById('student_status');
            for (let s of statuses) {
                container.innerHTML += `
                    <option value="${s['id']}">${s['title']}</option>
                `;
            }
        })

    init_departments_search((result, response) => {
            update_filters('department_id', result['department_id']);
            init_students_list(list_container, STUDENTS_LIST_FILTERS);
            display_department_hierarchy(
                document.getElementById('department_hierarchy'),
                result['department_id']
            );
        })

    update_filters();
    init_students_list(list_container, STUDENTS_LIST_FILTERS);
}

function update_filters(key = null, value= null) {
    if (key && value) {
        STUDENTS_LIST_FILTERS[key] = value;
        return;
    }

    let status_id = $('#student_status').dropdown('get value');
    if (status_id === 'any') {
        delete STUDENTS_LIST_FILTERS['status_id'];
    } else {
        STUDENTS_LIST_FILTERS['status_id'] = status_id;
    }

    let avatar = $('.ui.checkbox').checkbox('is checked');
    if (!avatar) {
        delete STUDENTS_LIST_FILTERS['avatar'];
    } else {
        STUDENTS_LIST_FILTERS['avatar'] = true;
    }
}