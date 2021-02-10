function display_student_drafts(container, student_id) {
    container.innerHTML = `
        <div class="ui segment">
            <div class="ui dividing header">Drafts</div>
            <div class="ui relaxed divided list" id="drafts_container">
                <div class="ui placeholder">
                  <div class="paragraph">
                    <div class="line"></div>
                    <div class="line"></div>
                    <div class="line"></div>
                    <div class="line"></div>
                    <div class="line"></div>
                  </div>
                </div>
            </div>
        </div>
    `;
    container = document.getElementById('drafts_container');
    axios.get(`/posts/search?author_id=${student_id}&is_draft=True`)
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
                container.innerHTML = `
                    <div class="ui basic placeholder segment" style="min-height: 100px">
                      <div class="ui icon header">
                        <i class="pencil icon"></i>
                        No drafts are listed for this student.
                      </div>
                    </div>
                `;
            }

        }).finally(() => {})
}