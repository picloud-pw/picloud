function display_students_posts(container, student_id) {
    container.innerHTML = `
        <div class="ui segment">
            <div class="ui dividing header">Posts</div>
            <div class="ui relaxed divided list" id="posts_container">
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
    container = document.getElementById('posts_container');
    axios.get(`/posts/search?author_id=${student_id}`)
        .then((response) => {
            container.innerHTML = "";
            let posts = response.data['posts'];
            for (let post of posts) {
                container.innerHTML += `
                    <div class="item">
                        <i class="large sticky note outline middle aligned icon"></i>
                        <div class="content">
                          <a class="header" href="/posts/?id=${post['id']}" target="_blank">${post['title']}</a>
                          <div class="description">${post['created_date_human']}</div>
                        </div>
                    </div>
                `;
            }
            if (!posts.length) {
                container.innerHTML = `
                    <div class="ui basic placeholder segment" style="min-height: 100px">
                      <div class="ui icon header">
                        <i class="sticky note outline icon"></i>
                        No posts are listed for this student.
                      </div>
                    </div>
                `;
            }

        }).finally(() => {})
}