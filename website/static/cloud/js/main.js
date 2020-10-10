document.addEventListener("DOMContentLoaded", function () {

    init_search();
    load_posts_list();

});

function init_search() {
    $('.ui.search').search({
        apiSettings: {
            url: "/posts/search?q={query}",
            onResponse: (response) => {
                let posts = response['posts'];
                let modified_response = [];
                for (let post of posts) {
                    modified_response.push({
                        post_id: post['id'],
                        title: post['title'],
                        price: post['author']['username'],
                        description: `[${post['created_date_human']}] ${post['subject']['name']}`,
                    })
                }
                return {results: modified_response}
            },
        },
        onSelect: (result, response) => {
            display_post(result['post_id']);
        },
        maxResults: 10,
        minCharacters: 2,
    });
}

function load_posts_list() {
    let container = document.getElementById('posts_container');
    container.classList.add('loading');
    axios.get('/posts/search')
        .then((response) => {
            let posts = response.data['posts'];
            for (let post of posts) {
                container.innerHTML += render_post(post);
            }
        })
        .finally(() => {
            container.classList.remove('loading');
        })
}

function render_post(post) {
    return `
        <article class="post" style="max-width: 700px">
            <div class="post-container" id="post-${post['id']}">
                <header>
                    <h1>
                        <a href="">${post['title']}</a>
                        ${post['parent_post'] ? '<i class="ui archive icon" title="There is parent post"></i>' : ''}
                    </h1>
                    <p class="subject">
                        <span class="type">${post['type']['title']}</span>
                        |
                        <a class="subject" href="" title="${post['subject']['name']}">
                            ${post['subject']['name']} 
                            <sup>${post['subject']['semester'] > 0 ? post['subject']['semester'] : ''}</sup>
                        </a>
                    </p>
                </header>
                <hr/>
                ${post['html'] ? `<div class="text">${post['html']}</div> <hr/>` : ''}
                
                ${post['image'] ? `
                    <img class="post-img" 
                         ratio="${post['image']['width']}x${post['image']['height']}"
                         src="${post['image']['url']}" 
                         alt="${post['image']['url']}">
                ` : ''}
                
                ${post['link'] ? `
                    <a class="ui primary right labeled icon button btn-follow-link" href="${post['link']}" target="_blank">
                        Open link <i class="angle double right icon"></i>
                    </a>
                ` : ''}

                ${post['file'] ? `
                    <a class="ui green right labeled icon button btn-download" href="${post['file']['url']}">
                        Download '<strong>${post['file']['extension']}</strong>' file <i class="download icon"></i>
                    </a>
                ` : ''}
                
                ${post['is_parent'] ? `
                    <br> <a class="ui button" href="">Child posts</a>
                ` : ''}
                
                <hr/>
                <footer>
                    <a class="post-author" title="Author" href="">${post['author']['username']}</a>
                    <span class="post-created-date">
                        • <span title="Created date and time">${post['created_date_human']}</span>
                    </span>
                    <span class="post-footer-badges">
                        <span class="ui" style="color: #999999" title="Views count">
                            <i class="eye icon"></i>${post['views']}
                        </span>
                        <a class="comments-counter" href="">
                            <i class="comment icon" title="Comments count"></i> ${post['comments']}
                        </a>
                    </span>
                </footer>
            </div>
        </article>
    `;
}

function display_post(post_id) {
    let container = document.getElementById("posts_container");
    axios.get(`/posts/search?id=${post_id}`)
        .then((response) => {
            let post = response.data['posts'][0];
            container.innerHTML = render_post(post);
        })

}
