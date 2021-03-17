document.addEventListener("DOMContentLoaded", function () {

    restore_state();

});

let SUBJECT_ID = null;

function save_state() {
    let state = {};
    if (SUBJECT_ID) {
        state = {
            "id": SUBJECT_ID,
        };
    }
    push_state(state);
}

function restore_state() {
    let params = new URLSearchParams(document.location.search);

    SUBJECT_ID = params.get("id");

    if (SUBJECT_ID) {
        init_page(SUBJECT_ID);
    } else {

    }

}

function init_page() {
    let container = document.getElementById('subjects_container');
    container.innerHTML = `
        <div class="six wide column">
            <div class="ui segment" id="subject" style="min-height: 80px"></div>
            <div class="ui segment">
                ${show_ad_block('horizontal')}
            </div>
            <div class="ui segment" id="hierarchy" style="min-height: 80px"></div>
        </div>
        <div class="six wide column">
            <div class="ui segment" id="posts" style="min-height: 80px"></div>
        </div>
    `;
    display_subject(document.getElementById('subject'));
    display_posts(document.getElementById('posts'));
}

function display_subject(container) {
    container.classList.add('loading');
    axios.get(`/hierarchy/subjects/get?id=${SUBJECT_ID}`)
        .then((response) => {
            let subject = response.data['subject'];
            container.innerHTML = `
                <div class="ui items">
                  <div class="item">
                    <div class="content">
                      <div class="header">${subject['name']}</div>
                      <div class="meta">
                        <span>Semester – ${subject['semester']}</span>
                      </div>
                      <div class="extra">
                        <div class="ui label">
                            <i class="university icon"></i>
                            Departments – ${subject['departments'].length}
                        </div>
                        <div class="ui label">
                            <i class="user icon"></i>
                            Students – ${subject['students']}
                        </div>
                        <div class="ui label">
                            <i class="sticky note outline icon"></i>
                            Posts – ${subject['posts']}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
            `;

            display_departments(subject['departments']);

        })
        .finally(() => {
            container.classList.remove('loading');
        })
}

function display_departments(departments) {
    document.getElementById('hierarchy').innerHTML = `
        <h4 class="ui dividing header">Departments</h4>
        <div id="first_department"></div>
        <div class="ui fluid accordion" id="accordion" style="display: none">
            <div class="title"><i class="dropdown icon"></i>Other related departments</div>
            <div class="content" id="departments_accordion"></div>
        </div>
    `;
    display_department_hierarchy(
        document.getElementById('first_department'),
        departments[0]['id']
    );
    if (departments.length > 1) {
        document.getElementById('accordion').style.display = 'block';
        for (let i in departments) {
            if (i === '0' ) continue;
            let container = document.createElement('div');
            document.getElementById('departments_accordion')
                .appendChild(container);
            display_department_hierarchy(container, departments[i]['id']);
        }
        $('.ui.accordion').accordion();
    }
}

function group_posts_by_type(posts) {
    let groups = {};
    for (let post of posts) {
        if (!groups[post['type']['plural']]) {
            groups[post['type']['plural']] = [];
        }
        groups[post['type']['plural']].push(post);
    }
    return groups;
}

function display_posts(container) {
    container.classList.add('loading');
    axios.get(`/posts/search?subject_id=${SUBJECT_ID}`)
        .then((response) => {
            let groups = group_posts_by_type(response.data['posts']);
            for (let group in groups) {
                let group_id = random_ID();
                container.innerHTML += `
                    <h4 class="ui dividing header">${group}</h4>
                    <div class="ui relaxed divided list" id="${group_id}"></div>
                `;
                for (let post of groups[group]) {
                    document.getElementById(group_id).innerHTML += `
                        <div class="item">
                            <i class="large sticky note outline middle aligned icon"></i>
                            <div class="content">
                              <a href="/posts?id=${post['id']}">${post['title']}</a>
                              <div class="description">
                                ${post['author']['user']['username']} • ${post['created_date_human']}
                              </div>
                            </div>
                        </div>
                    `;
                }
            }
        })
        .finally(() => {
            container.classList.remove('loading');
        })
}