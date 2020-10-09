document.addEventListener("DOMContentLoaded", function () {

    init_personal_info();

});

function init_personal_info() {
    let container = document.getElementById('personal_info_container');
    container.classList.add('loading');

    axios.get('/me')
        .then((response) => {
            let me = response.data;

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
                     <i class="ui pencil icon"></i> 
                  </a>
                </div>
                <div class="content">
                  <i class="at icon"></i> ${me['user']['email']}
                  <a class="right floated"> 
                      <i class="ui pencil icon"></i>
                  </a>
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
              <div class="ui basic button">Choose department</div>
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


