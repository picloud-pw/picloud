document.addEventListener("DOMContentLoaded", function () {

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

            init_user_department(me['department']);
            container.innerHTML = `
              <div class="ui fluid info card" style="padding: 20px">
                <div class="blurring dimmable image">
                    <div class="ui dimmer">
                      <div class="content">
                        <div class="center">
                          <div class="ui inverted button">Update avatar</div>
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

function init_user_department(department) {
    let container = document.getElementById('user_department_container');
    container.innerHTML = `
        <div class="ui dividing header">Department</div>
    `;

    if (!department) {
        container.innerHTML += `
            <div class="ui basic placeholder segment">
              <div class="ui icon header">
                <i class="university icon"></i>
                You haven't chosen a department yet.
              </div>
              <div class="ui basic button" onclick="init_edit_form('department')">Choose department</div>
            </div>
        `;
        return;
    }

    container.classList.add('loading');
    axios.get(`/hierarchy/departments/get?id=${department['id']}`)
        .then((response) => {
            department = response.data['department'];
            container.innerHTML += `
            <div class="ui fluid items">
                <div class="ui item">
                    <div class="middle aligned content">
                      <div class="header">${department['name']}</div>
                    </div>
                </div>
            </div>
            <div class="ui divider"></div>
            
        `;
        })
        .finally(() => {
            container.classList.remove('loading');
        });

}


function init_edit_form(field) {
    let fields = '';

    if (field === 'name') {
        fields = `
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
        fields = `
            <div class="field">
                <label>Username</label>
                <input class="ui fluid input" name="username" value="${USER_INFO['user']['username']}"/>
            </div>
        `;
    }

    let container = document.getElementById('edit_form_modal_container');
    container.innerHTML = `
        <div class="ui tiny modal" id="edit_form_modal">
          <i class="close icon"></i>
          <div class="header">Edit personal information</div>
          <div class="content">
            <form class="ui form" id="edit_form">
                ${fields}
            </form>
          </div>
          <div class="actions">
            <div class="ui black deny button">Cancel</div>
            <div class="ui positive right labeled icon button"> Save <i class="checkmark icon"></i> </div>
          </div>
        </div>
    `;

    $('#edit_form_modal')
        .modal({
            onApprove: (elem) => {
                save_edit_form();
            },
        })
        .modal('show');
}

function save_edit_form() {
    let formData = new FormData(
        document.getElementById('edit_form')
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

