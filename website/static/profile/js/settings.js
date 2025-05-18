document.addEventListener("DOMContentLoaded", function () {
    restore_state();
});

let USER_INFO = {};


function restore_state() {
    get_userinfo().then(() => {
        display_avatar();
        display_personal_info();
        display_department();
    })
}

function get_userinfo() {
    return axios.get('/students/me').then((response) => {
        USER_INFO = response.data;
    })
}

function display_avatar() {
    document.getElementById('user_avatar_container').innerHTML = `
        <div class="ui basic no-margin-padding segment" style="text-align: center">
            <img src="${USER_INFO['avatar']}" alt="avatar" style="width: 200px; margin: 20px; border-radius: 100px">
            <div class="ui basic fluid button" id="set_default_avatar_btn" style="margin-bottom: 20px">
                Set default avatar
            </div>
            <div class="ui basic fluid button" id="delete_avatar_btn" style="margin-bottom: 20px">
                Delete avatar <br> (will be set after next login)
            </div>
        </div>
    `;
    document.getElementById('set_default_avatar_btn').onclick = () => {
        set_default_avatar();
    }
    document.getElementById('delete_avatar_btn').onclick = () => {
        delete_avatar();
    }
}

function delete_avatar() {
    axios.post('/students/me/avatar/delete', null, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {
            USER_INFO['avatar'] = response.data['avatar'];
            display_avatar();
            show_alert("success", "You avatar has been removed.");
        })
        .catch((error) => {
            show_alert('warning', "Something went wrong. Please try again later or contact us about this error.")
        })
}

function set_default_avatar() {
    axios.post('/students/me/avatar/set_default', null, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {
            USER_INFO['avatar'] = response.data['avatar'];
            display_avatar();
            show_alert("success", "You avatar has been set.");
        })
        .catch((error) => {
            show_alert('warning', "Something went wrong. Please try again later or contact us about this error.")
        })
}

function display_personal_info() {
    document.getElementById('personal_info_container').innerHTML = `
        <form class="ui form" id="personal_info_form">
            <div class="field">
                <label>Username</label>
                <input class="ui fluid input" name="username" value="${USER_INFO['user']['username']}"/>
            </div>
            <div class="field">
                <label>First name</label>
                <input class="ui fluid input" name="first_name" value="${USER_INFO['user']['first_name']}"/>
            </div>
            <div class="field">
                <label>Last name</label>
                <input class="ui fluid input" name="last_name" value="${USER_INFO['user']['last_name']}"/>
            </div>
            <div class="field">
                <label>Email</label>
                <input class="ui fluid input" disabled name="email" value="${USER_INFO['user']['email']}"/>
            </div>
            <div class="ui basic button" id="save_personal_info_btn">Save</div>
        </form>
    `;
    document.getElementById('save_personal_info_btn').onclick = () => {
        let form = document.getElementById('personal_info_form');
        save_edit_form(form).then(request => {
            display_personal_info();
        });
    };
}

function display_department() {
    document.getElementById('user_department_container').innerHTML = `
        <h2 class="ui header">Department</h2>
        <div id="user_department_hierarchy"></div>
        <div class="ui basic button" style="margin-top: 20px"
            onclick="display_department_edit_form()">
            Change department
        </div>
    `;
    display_department_hierarchy(
        document.getElementById('user_department_hierarchy'),
        USER_INFO['department']['id']
    );
}


function display_department_edit_form() {
    let container = document.getElementById('edit_form_modal_container');
    let form_id = random_ID();
    container.innerHTML = `
        <div class="ui tiny modal" id="${form_id}_modal">
          <i class="close icon"></i>
          <div class="header">Edit department</div>
          <div class="scrolling content">
            <form class="ui form" id="${form_id}">
                <div class="field">
                    <label>Department</label>
                    <div class="ui loading search">
                        <div class="ui fluid input">
                            <input class="prompt" name="department_name" type="text" placeholder="Enter search query">
                        </div>
                        <input name="department_id" type="hidden">
                        <div class="search results"></div>
                    </div>
                    <div id="search_department_hierarchy" style="margin-top: 20px"></div>
                </div>
            </form>
          </div>
          <div class="actions">
            <div class="ui black deny button">Cancel</div>
            <div class="ui positive right labeled icon button"> Save <i class="checkmark icon"></i> </div>
          </div>
        </div>
    `;

    init_departments_search((result, response) => {
        $("input[name='department_id']").val(result['department_id']);
        display_department_hierarchy(
            document.getElementById('search_department_hierarchy'),
            result['department_id']
        );
    })

    $(`#${form_id}_modal`).modal({
        onApprove: (elem) => {
            let form = document.getElementById(form_id);
            save_edit_form(form).then(request => {
                display_department();
            });
        },
    }).modal('show');
}

function save_edit_form(form) {
    let formData = new FormData(form);

    return axios.post(`/students/me/edit`, formData, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then(response => {
            if (response.data['status'] === 'success') {
                USER_INFO = response.data['user_info'];
            }
            show_alert(response.data['status'], response.data['message']);
            return response;
        })
        .catch(error => {
            show_alert('error', error);
        })
}
