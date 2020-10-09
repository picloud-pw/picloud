document.addEventListener("DOMContentLoaded", function () {

    let personal_info_container = document.getElementById('personal_info_container');
    personal_info_container.classList.add('loading');
    let user_department_container = document.getElementById('user_department_container');
    user_department_container.classList.add('loading');
    axios.get('/me')
        .then((response) => {
            let me = response.data;
            display_personal_info(personal_info_container, me);
            display_user_department(user_department_container, me);
        })
        .finally(() => {
            personal_info_container.classList.remove('loading');
            user_department_container.classList.remove('loading');
        });

});

function display_personal_info(container, me) {
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
}

function display_user_department(container, me) {
    container.innerHTML = ``;
}


