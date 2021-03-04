function display_student_drafts(container, student_id, moderation=false) {
    let inner_id = moderation ? 'moderation' : 'drafts' + '_container';
    container.innerHTML = `
        <div class="ui relaxed divided list" id="${inner_id}">
            ${render_loader()}
        </div>
    `;
    let filter = moderation ? 'is_draft=False&is_approved=False' : 'is_draft=True';
    container = document.getElementById(inner_id);
    axios.get(`/posts/search?author_id=${student_id}&${filter}`)
        .then((response) => {
            container.innerHTML = "";
            let posts = response.data['posts'];
            for (let post of posts) {
                container.innerHTML += `
                    <div class="item">
                        <i class="pencil middle aligned icon"></i>
                        <div class="content">
                          <a class="header" href="/new/post">
                            ${post['title'] ? post['title'] : ' -- untitled post --'}
                          </a>
                          <div class="description">${post['created_date_human']}</div>
                        </div>
                    </div>
                `;
            }
            if (!posts.length) {
                container.innerHTML = render_placeholder(
                    'pencil',
                    moderation ? 'You have not sent posts for moderation yet.' :
                        'No drafts are listed for this student.'
                )
            }

        }).finally(() => {})
}