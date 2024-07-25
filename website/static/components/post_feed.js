class PostFeed {

    page = 1;

    constructor(filters = {}) {
        if (filters['is_draft'] === undefined) {
            filters['is_draft'] = false;
        }
        if (filters['is_approved'] === undefined) {
            filters['is_approved'] = true;
        }
        this.filters = filters;
    }

    get_student_posts() {
        let filter = `page=${this.page}&`;
        filter += `is_draft=${this.filters['is_draft'] ? 'True' : 'False'}&`;
        filter += `is_approved=${this.filters['is_approved'] ? 'True' : 'False'}&`;

        if (this.filters['author_id']) {
            filter += `author_id=${this.filters['author_id']}`;
        }
        return axios.get(`/posts/search?${filter}`);
    }

    display_posts_as_tiles(container) {
        this.page = 0;
        let el_id = random_ID();
        container.innerHTML = `
            <div class="ui two doubling stackable cards" id="${el_id}"></div>
            <div class="ui basic button" style="margin: 20px 0" id="${el_id}_load_more_btn">Load more ...</div>
        `;

        container.classList.add('loading');
        this._tiles_next_page(el_id).finally(() => {
            container.classList.remove('loading');
        })

        $(`#${el_id}_load_more_btn`).click(() => {
            this._tiles_next_page(el_id);
        });
    }

    _tiles_next_page(el_id) {
        let load_button = document.getElementById(`${el_id}_load_more_btn`);
        load_button ? load_button.classList.add('loading') : null;
        this.page += 1;

        let container = document.getElementById(el_id);
        return this.get_student_posts().then((response) => {
            let resp = response.data;
            for (let post of resp['posts']) {
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
            load_button.classList.remove('loading');
            if (resp['total_posts'] === 0) {
                document.getElementById(el_id).innerHTML = `
                    <div class="ui fluid card">${render_placeholder(
                    'sticky note outline',
                    'No posts are listed for selected filters.'
                    )}</div>
                `;
            }
            console.log(resp);
            if (resp['page'] === resp['total_pages']) {
                load_button.remove();
            }
        })
    }


}
