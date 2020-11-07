let MASONRY = null;

document.addEventListener("DOMContentLoaded", function () {

    const grid = document.querySelector('#posts_container');
    clear_posts_container(grid);
    MASONRY = new Masonry(grid, {
        itemSelector: ".post",
        columnWidth: ".post-size-reference",
        gutter: ".post-grid-gutter-size-reference",
        percentPosition: true,
    });
    imagesLoaded(grid).on('progress', () => {
        MASONRY.layout();
    });

    init_posts_search(
        (result, response) => {
            window.location.href = `/posts?id=${result['post_id']}`;
        });

    load_posts_list();


});

function load_posts_list() {
    let container = document.getElementById('posts_container');
    container.classList.add('loading');
    axios.get('/posts/search')
        .then((response) => {
            let posts = response.data['posts'];
            for (let post of posts) {
                append_post(post, container);
            }
        })
        .finally(() => {
            container.classList.remove('loading');
        })
}

function display_post(post_id) {
    let postsGrid = document.getElementById("posts_container");
    axios.get(`/posts/search?id=${post_id}`)
        .then((response) => {
            let posts = response.data['posts'];
            clear_posts_container(postsGrid);
            for (let post of posts) {
                append_post(post, postsGrid);
            }
        })
}

function clear_posts_container(postsGrid) {
    postsGrid.innerHTML = '';

    let masonrySizer = document.createElement("div");
    masonrySizer.classList.add("post-size-reference");
    postsGrid.appendChild(masonrySizer);

    let gutterSizer = document.createElement("div");
    gutterSizer.classList.add("post-grid-gutter-size-reference");
    postsGrid.appendChild(gutterSizer);
}

function append_post(post, postsContainer) {
    let postElement = render_post(post);
    postsContainer.appendChild(postElement);
    MASONRY.appended(postElement);
    imagesLoaded(postElement).on('progress', () => {
        MASONRY.layout();
    });
}
