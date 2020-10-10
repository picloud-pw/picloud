document.addEventListener("DOMContentLoaded", function () {

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
            for (let mem of memes) {
                let attachments = '';
                if (mem['attachments']) {
                    for (let attachment of mem['attachments']) {
                        if (attachment['type'] === 'photo') {
                            attachments += `<img src="${attachment['photo']['photo_604']}" alt="Mem image">`;
                        }
                    }
                }
                container.innerHTML += `
                    <div class="meme">
                        ${mem['text'] ? '<p class="meme-text">' + mem['text'] + '</p>' : ''}
                        ${attachments ? '<div class="meme-gallery">' + attachments + '</div>' : ''}
                        <p class="meme-source">
                            <a href="https://vk.com/wall${mem['from_id']}_${mem['id']}" target="_blank">
                                Source <span class="glyphicon glyphicon-new-window"></span>
                            </a>
                        </p>
                    </div>
                `;
            }
        })
        .finally(() => {
            container.classList.remove('loading');
        })
}