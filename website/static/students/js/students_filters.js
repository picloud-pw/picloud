function init_students_filters(container) {
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
            <select class="ui dropdown" id="student_status">
                <option value="any" selected>Any</option>
            </select>
          </div>
          <div class="ui divider"></div>
          <div class="inline field">
            <div class="ui slider checkbox" id="custom_avatar">
              <input type="checkbox" tabindex="0" class="hidden">
              <label>Custom avatar</label>
            </div>
          </div>
          <div class="ui divider"></div>
        </div>
    `;
    $('.ui.checkbox').checkbox();

    axios.get('/students/statuses')
        .then((response) => {
            let statuses = response.data['statuses'];
            let container = document.getElementById('student_status');
            for (let s of statuses) {
                container.innerHTML += `
                    <option value="${s['id']}">${s['title']}</option>
                `;
            }
            $('#student_status').dropdown()
        })

    init_departments_search((result, response) => {
            display_department_hierarchy(
                document.getElementById('department_hierarchy'),
                result['department_id']
            );
        })

}