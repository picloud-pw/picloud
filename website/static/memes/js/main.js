let MASONRY = null;
let PAGE = 1;

document.addEventListener("DOMContentLoaded", function () {

    const grid = document.querySelector('#memes_container');
    clear_posts_container(grid);
    MASONRY = new Masonry(grid, {
        itemSelector: ".meme",
        columnWidth: ".post-size-reference",
        gutter: ".post-grid-gutter-size-reference",
        percentPosition: true,
    });
    imagesLoaded(grid).on('progress', () => {
        MASONRY.layout();
    });

    get_sources();

});

function get_sources() {
    axios.get(`/memes/sources`)
        .then((response) => {
            let sources = response.data['sources'];

            let ids = [];
            for (let source of sources) {
                ids.push(source['id'])
            }

            load_memes(ids)
        })
}

function load_memes(sources_ids) {
    let container = document.getElementById('memes_container');
    container.classList.add('loading');
    axios.get(`/memes/memes?ids=${sources_ids.join(',')}`)
        .then((response) => {
            let memes = response.data['memes'];
            for (let meme of memes) {
                let element = render_meme(meme);
                container.appendChild(element);
                MASONRY.appended(element);
                imagesLoaded(element).on('progress', () => {
                    MASONRY.layout();
                });
            }
        })
        .finally(() => {
            container.classList.remove('loading');
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

function render_meme(mem) {
    let element = document.createElement("div");
    element.classList.add("meme");

    let attachments = '';
    if (mem['attachments']) {
        for (let attachment of mem['attachments']) {
            if (attachment['type'] === 'photo') {
                // photo with best quality
                attachments += `<img src="${attachment['photo']['sizes'][6]['url']}" alt="Mem image">`;
            }
        }
    }

    element.innerHTML = `
        ${mem['text'] ? '<p class="meme-text">' + mem['text'] + '</p>' : ''}
        ${attachments ? '<div class="meme-gallery">' + attachments + '</div>' : ''}
        <p class="meme-source">
            <a href="https://vk.com/wall${mem['from_id']}_${mem['id']}" target="_blank">
                Source <span class="glyphicon glyphicon-new-window"></span>
            </a>
        </p>
    `;

    return element;
}
