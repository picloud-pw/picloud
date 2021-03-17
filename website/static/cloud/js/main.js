let MASONRY = null;
let PAGE = 1;

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
        }
    );

    load_posts_list();

});

function load_posts_list() {
    let btn = document.getElementById('load_more_btn');
    btn.classList.add('loading');
    let container = document.getElementById('posts_container');
    axios.get(`/posts/search?page=${PAGE}`)
        .then((response) => {
            append_element( render_ad(), container );
            let posts = response.data['posts'];
            for (let post of posts) {
                let rendered_post = render_post(post);
                append_element(rendered_post, container);
            }
            push_ads();
            MASONRY.layout();
        })
        .finally(() => {
            btn.classList.remove('loading');
            PAGE += 1;
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

function append_element(element, postsContainer) {
    postsContainer.appendChild(element);
    MASONRY.appended(element);
    imagesLoaded(element).on('progress', () => {
        MASONRY.layout();
    });
}

function render_ad() {
    let element = document.createElement("article");
    element.classList.add("post");
    element.style.padding = '20px';
    element.innerHTML = show_ad_block();
    return element;
}
