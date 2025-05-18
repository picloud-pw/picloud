class ProfilePage {

    constructor() {
        this.restore_state();
    }

    save_state() {}

    restore_state() {
        let pathname = new URL(window.location.href).pathname;
        let path_parts = pathname.split('/');

        if (path_parts.length === 4) {
            let username = path_parts[2];
            axios.all([this.get_userinfo(username), this.get_me(),]).then(() => {
                this.its_my_profile = this.me['id'] === this.student['id'];

                this.display_user_card(document.getElementById('user_avatar'));
                this.display_posts(document.getElementById('user_content'), this.student['id']);
                this.display_user_department(document.getElementById('user_stats'), this.student['department'])
            })
        }
    }

    get_me() {
        return axios.get('/students/me').then(response => {
            this.me = response.data;
        })
    }

    get_userinfo(username) {
        return axios.get(`/students/get?username=${username}`).then((response) => {
            this.student = response.data;
        })
    }

    display_posts(container, user_id) {
        container.innerHTML = `
            <div class="ui secondary huge menu" style="margin-bottom: 20px">
                <a class="active item" data-tab="posts_tab" id="posts_tab">Posts</a>
                <a class="item" data-tab="subjects_tab" id="subjects_tab">Subjects</a>
                ${this.its_my_profile ? `
                    <a class="item" data-tab="drafts_tab" id="drafts_tab">Drafts</a>
                    <a class="item" data-tab="moderation_tab" id="moderation_tab">Moderation</a>
                ` : ''}
            </div>
            <div class="ui bottom attached active loading tab" data-tab="posts_tab" id="user_posts"></div>
            <div class="ui bottom attached tab" data-tab="subjects_tab" id="user_subjects"></div>
            ${this.its_my_profile ? `
                <div class="ui bottom attached tab" data-tab="drafts_tab" id="user_drafts"></div>
                <div class="ui bottom attached tab" data-tab="moderation_tab" id="moderation_posts"></div>
            ` : ''}
        `;

        this.post_feed = new PostFeed({'author_id': user_id, 'is_draft': false, 'is_approved': true,});
        this.post_feed.display_posts_as_tiles(document.getElementById('user_posts')).then(() => {
            document.getElementById('posts_tab').innerHTML +=
                this.get_label(this.post_feed.total_posts);
        });

        this.subject_feed = new SubjectFeed({'author_id': user_id,});
        this.subject_feed.display_subjects_as_tiles(document.getElementById('user_subjects')).then(() => {
            document.getElementById('subjects_tab').innerHTML +=
                this.get_label(this.subject_feed.total_subjects);
        });

        if (this.its_my_profile) {
            this.drafts_feed = new PostFeed({'author_id': user_id, 'is_draft': true, 'is_approved': false,});
            this.drafts_feed.display_posts_as_tiles(document.getElementById('user_drafts')).then(() => {
                document.getElementById('drafts_tab').innerHTML +=
                    this.get_label(this.drafts_feed.total_posts);
            });

            this.moderation_feed = new PostFeed({'author_id': user_id, 'is_draft': false, 'is_approved': false,});
            this.moderation_feed.display_posts_as_tiles(document.getElementById('moderation_posts')).then(() => {
                document.getElementById('moderation_tab').innerHTML +=
                    this.get_label(this.moderation_feed.total_posts);
            });
        }

        $('.menu .item').tab();
    }

    get_label(number) {
        return `<span class="ui blue label">${number}</span>`;
    }

    display_user_department(container, department) {
        if (!department) {
            container.innerHTML += `
                <div class="ui basic placeholder segment">
                  <div class="ui icon header">
                    <i class="university icon"></i>
                    User hasn't chosen a department yet.
                  </div>
                </div>
            `;
        } else {
            container.innerHTML += `
                <h2 class="ui header">Department</h2>
                <div id="hierarchy_container"></div>
            `;
            display_department_hierarchy(
                document.getElementById('hierarchy_container'),
                department['id']
            );
        }
    }

    display_user_card(container) {
        container.innerHTML = `
            <div class="ui image">
                <img class="avatar" src="${this.student['avatar']}" alt="avatar" 
                    style="background-color: #fff; width: 200px; border-radius: 500px; overflow: hidden">
            </div>
            <h1 class="ui header" style="overflow: hidden; text-overflow: ellipsis">
                ${this.student['user']['username']}
            </h1>
        `;
    }

    display_student_card(container, student_id) {
        container.classList.add('loading');
        axios.get(`/students/get?id=${student_id}`)
            .then((response) => {
                let user = response.data;
                document.title = user['user']['username'];
                document.getElementById('student_info').innerHTML = `
                    <div class="ui fluid card">
                      <div class="image">
                        <img src="${user['avatar']}" alt="avatar">
                      </div>
                      <div class="content">
                        <div class="header">${user['user']['username']}</div>
                        <div class="meta">
                          <span class="date">Last login at ${new Date(user['user']['last_login']).toPrettyString()}</span>
                        </div>
                      </div>
                      <div class="content">
                          <span title="Status">
                              <i class="map marker icon"></i> ${user['status']['title']}
                          </span>
                          <span class="right floated" title="Karma"> 
                              ${user['karma']} <i class="certificate icon"></i>
                          </span>
                      </div>
                    </div>
                `;

                this.display_student_department(user['department'] ? user['department']['id'] : null);
            }).finally(() => {
            container.classList.remove('loading');
        })
    }

    display_student_department(department_id) {
        let container = document.getElementById('student_department');
        if (department_id) {
            display_department_hierarchy(
                container,
                department_id,
            )
        } else {
            container.innerHTML = `
                <div class="ui basic placeholder segment">
                    <div class="ui icon header">
                        <i class="university icon"></i>
                        Student hasn't chosen a department yet.
                    </div>
                </div>
            `;
        }

    }


}
