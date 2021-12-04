document.addEventListener("DOMContentLoaded", function () {

    $('.menu .item').tab();
    init_personal_info();

});

let USER_INFO = {};


function init_personal_info() {
    let container = document.getElementById('personal_info_container');
    container.classList.add('loading');

    axios.get('/students/me')
        .then((response) => {
            let me = response.data;
            USER_INFO = me;

            display_students_posts(
                document.getElementById('user_posts'),
                me['id']
            );

            display_student_drafts(
                document.getElementById('user_drafts'),
                me['id']
            );

            display_student_drafts(
                document.getElementById('moderation_posts'),
                me['id'],
                true
            );

            let department_container = document.getElementById('user_department_container');
            department_container.innerHTML = `
                <div class="ui dividing header">Department</div>
            `;

            if (!me['department']) {
                department_container.innerHTML += `
                    <div class="ui basic placeholder segment">
                      <div class="ui icon header">
                        <i class="university icon"></i>
                        You haven't chosen a department yet.
                      </div>
                      <div class="ui basic button" onclick="init_edit_form('department')">Choose department</div>
                    </div>
                `;
            } else {
                department_container.innerHTML += `
                    <div id="hierarchy_container"></div>
                    <div class="ui divider"></div>
                    <div class="ui basic button" onclick="init_edit_form('department')">Change department</div>
                `;
                display_department_hierarchy(
                    document.getElementById('hierarchy_container'),
                    me['department']['id']
                );
            }

            container.innerHTML = `
              <div class="ui fluid info card" style="padding: 20px">
                <div class="blurring dimmable image">
                    <div class="ui dimmer">
                      <div class="content">
                        <div class="center">
                          <div class="ui inverted button" style="width:150px" onclick="init_edit_form('update_avatar')">
                            Update avatar
                          </div>
                          <div class="ui divider"></div>
                          <div class="ui inverted button" style="width:150px" onclick="init_edit_form('delete_avatar')">
                            Delete avatar
                          </div>
                        </div>
                      </div>
                    </div>
                    <img src="${me['avatar']}" alt="avatar" style="padding: 30px; background-color: #fff">
                </div>
                <div class="content">
                  <a class="right floated"> 
                     <i class="ui pencil icon" onclick="init_edit_form('username')"></i> 
                  </a>
                  <div class="header">${me['user']['username']}</div>
                  <div class="meta">
                    <span class="date">Last login at ${new Date(me['user']['last_login']).toPrettyString()}</span>
                  </div>         
                </div>
                <div class="content">
                  <span title="Status">
                      <i class="map marker icon"></i> ${me['status']['title']}
                  </span>
                  <span class="right floated" title="Karma"> 
                      ${me['karma']} <i class="certificate icon"></i>
                  </span>
                </div>
                <div class="content">
                  <i class="user icon"></i> ${me['user']['first_name']} ${me['user']['last_name']}
                  <a class="right floated"> 
                     <i class="ui pencil icon" onclick="init_edit_form('name')"></i> 
                  </a>
                </div>
                <div class="content">
                  <i class="at icon"></i> ${me['user']['email']}
                </div>
              </div>
            `;

            $('.info.card .image').dimmer({on: 'hover'});
            $('span').popup({position: 'bottom center'});

        })
        .finally(() => {
            container.classList.remove('loading');
        });
}


function init_edit_form(field) {
    let container = document.getElementById('edit_form_modal_container');
    let form_id = random_ID();
    container.innerHTML = `
        <div class="ui tiny modal" id="${form_id}_modal">
          <i class="close icon"></i>
          <div class="header">Edit personal information</div>
          <div class="scrolling content">
            <form class="ui form" id="${form_id}"></form>
          </div>
          <div class="actions">
            <div class="ui black deny button">Cancel</div>
            <div class="ui positive right labeled icon button"> Save <i class="checkmark icon"></i> </div>
          </div>
        </div>
    `;

    let fields_container = document.getElementById(form_id);

    if (field === 'name') {
        fields_container.innerHTML = `
            <div class="field">
                <label>First name</label>
                <input class="ui fluid input" name="first_name" value="${USER_INFO['user']['first_name']}"/>
            </div>
            <div class="field">
                <label>Last name</label>
                <input class="ui fluid input" name="last_name" value="${USER_INFO['user']['last_name']}"/>
            </div>
        `;
    }

    if (field === 'username') {
        fields_container.innerHTML = `
            <div class="field">
                <label>Username</label>
                <input class="ui fluid input" name="username" value="${USER_INFO['user']['username']}"/>
            </div>
        `;
    }

    if (field === 'department') {
        fields_container.innerHTML = `
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
        `;
        init_departments_search((result, response) => {
            $("input[name='department_id']").val(result['department_id']);
            display_department_hierarchy(
                document.getElementById('search_department_hierarchy'),
                result['department_id']
            );
        })
    }

    if (!fields_container.innerHTML) {
        fields_container.innerHTML = `
            <div class="ui basic placeholder segment">
              <div class="ui icon header">
                <i class="search icon"></i>
                This fields has not been implemented yet.
              </div>
            </div>
        `
    }

    $(`#${form_id}_modal`)
        .modal({
            onApprove: (elem) => {
                save_edit_form(form_id);
            },
        })
        .modal('show');
}

function save_edit_form(form_id) {
    let formData = new FormData(
        document.getElementById(form_id)
    );

    axios.post(`/students/me/edit`, formData, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then(response => {
            show_alert(response.data['status'], response.data['message']);
            init_personal_info();
        })
        .catch(error => {
            show_alert('error', error);
        })
}

