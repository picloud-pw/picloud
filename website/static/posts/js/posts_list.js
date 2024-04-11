function get_student_posts(student_id, is_draft=false, is_approved=true) {
    let filter = '';
    filter += `is_draft=${is_draft ? 'True' : 'False'}&`;
    filter += `is_approved=${is_approved ? 'True' : 'False'}&`;
    return axios.get(`/posts/search?author_id=${student_id}&${filter}`);
}

function display_students_posts_as_list(container, student_id) {
    let el_id = random_ID();
    container.innerHTML = `
        <div class="ui relaxed divided list" id="${el_id}"> ${render_loader()} </div>
    `;
    container = document.getElementById(el_id);
    get_student_posts(student_id)
        .then((response) => {
            container.innerHTML = "";
            let posts = response.data['posts'];
            for (let post of posts) {
                container.innerHTML += `
                    <div class="item">
                        <i class="large sticky note outline middle aligned icon"></i>
                        <div class="content">
                          <a class="header" href="/posts/${post['id']}/" target="_blank">${post['title']}</a>
                          <div class="description">${post['created_date_human']}</div>
                        </div>
                    </div>
                `
            }
            if (!posts.length) {
                container.innerHTML = render_placeholder(
                    'sticky note outline',
                    'No posts are listed for this student.'
                );
            }
        }).finally(() => {})
}

function display_students_posts_as_tiles(container, posts) {
    let el_id = random_ID();
    container.innerHTML = `
        <div class="ui two doubling stackable cards" style="margin-top: 20px" id="${el_id}"></div>
    `;

    container = document.getElementById(el_id);
    for (let post of posts) {
        container.innerHTML += `
            <div class="ui card">
              <div class="ui content">
                  <a class="ui header" href="/posts/${post['id']}/" 
                    style="white-space: nowrap; text-overflow: ellipsis; overflow: hidden; margin-bottom: 5px;">
                    ${post['title'] ? post['title'] : ' -- untitled post --'}
                  </a>
                  <div class="meta">
                    <span class="date">${post['created_date_human']}</span>
                  </div>
              </div>
              <div class="ui content">
                <a class="ui basic label" href="/subs/${post['subject'] ? post['subject']['id'] : ''}">
                    ${post['subject'] ? post['subject']['name'] : '--- no subject ---'}
                </a>
                <span class="ui basic label">
                    ${post['type'] ? post['type']['title'] : '--- no type ---'}
                </span>
              </div>
            </div>
        `;
    }
    if (!posts.length) {
        container.innerHTML = `
            <div class="ui fluid card">
                ${render_placeholder(
                    'sticky note outline',
                    'No posts are listed for selected filters.'
                )}
            </div>
        `;
    }
}