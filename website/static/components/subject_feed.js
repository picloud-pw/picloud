class SubjectFeed {

    page = 1;

    constructor(filters = {}) {
        if (filters['is_approved'] === undefined) {
            filters['is_approved'] = true;
        }
        this.filters = filters;
    }

    get_subjects() {
        let filter = `page=${this.page}&`;
        filter += `is_approved=${this.filters['is_approved'] ? 'True' : 'False'}&`;

        if (this.filters['department_id']) {
            filter += `department_id=${this.filters['department_id']}`;
        }
        if (this.filters['author_id']) {
            filter += `author_id=${this.filters['author_id']}`;
        }
        return axios.get(`/hierarchy/subjects/search?${filter}`);
    }

    display_subjects_as_tiles(container) {
        this.page = 0;
        let el_id = random_ID();
        container.innerHTML = `
            <div class="ui two doubling stackable cards" id="${el_id}"></div>
            <div class="ui basic button" style="margin: 20px 0" id="${el_id}_load_more_btn">Load more ...</div>
        `;

        $(`#${el_id}_load_more_btn`).click(() => {
            this._tiles_next_page(el_id);
        });

        container.classList.add('loading');
        return this._tiles_next_page(el_id).finally(() => {
            container.classList.remove('loading');
        })

    }

    _tiles_next_page(el_id) {
        let load_button = document.getElementById(`${el_id}_load_more_btn`);
        load_button ? load_button.classList.add('loading') : null;
        this.page += 1;

        let container = document.getElementById(el_id);
        return this.get_subjects().then((response) => {
            let resp = response.data;
            this.total_subjects = resp['total_subjects'];
            for (let item of resp['subjects']) {
                container.innerHTML += `
                    <div class="ui card">
                      <div class="ui content">
                          <a class="ui header" href="/subs/${item['id']}/" 
                            style="white-space: nowrap; text-overflow: ellipsis; overflow: hidden; margin-bottom: 5px;">
                            ${item['name'] ? item['name'] : ' -- untitled --'}
                          </a>
                          <div class="meta">
                            <span class="date">${item['semester']} semestr</span>
                          </div>
                      </div>
                      <div class="ui content">
                        <span class="ui basic label">Posts count: ${item['posts']}</span>
                      </div>
                    </div>
                `;
            }
            load_button.classList.remove('loading');
            if (resp['total_subjects'] === 0) {
                document.getElementById(el_id).innerHTML = `
                    <div class="ui fluid card">${render_placeholder(
                    'sticky note outline',
                    'No items are listed for selected filters.'
                    )}</div>
                `;
            }
            if (resp['page'] === resp['total_pages']) {
                load_button.remove();
            }
        })
    }

}
