function render_post_item(post) {
    return `
        <div class="item">
            <i class="large sticky note outline middle aligned icon"></i>
            <div class="content">
              <a class="header" href="/posts/${post['id']}/" target="_blank">${post['title']}</a>
              <div class="description">${post['created_date_human']}</div>
            </div>
        </div>
    `;
}

function display_students_posts(container, student_id) {
    let el_id = random_ID();
    container.innerHTML = `
        <div class="ui relaxed divided list" id="${el_id}"> ${render_loader()} </div>
    `;
    container = document.getElementById(el_id);
    axios.get(`/posts/search?author_id=${student_id}`)
        .then((response) => {
            container.innerHTML = "";
            let posts = response.data['posts'];
            for (let post of posts) {
                container.innerHTML += render_post_item(post);
            }
            if (!posts.length) {
                container.innerHTML = render_placeholder(
                    'sticky note outline',
                    'No posts are listed for this student.'
                );
            }
        }).finally(() => {})
}