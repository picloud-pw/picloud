import {PostEditor} from "./posts_editor.js";

export class DraftsEditorPage {

    me = null;

    constructor(container) {
        axios.get('/students/me').then(response => {
            this.me = response.data;
            this.restore_state(container);
        })
    }

    restore_state(container) {
        let params = new URLSearchParams(document.location.search);
        let draft_id = params.get("id");

        let el_id = random_ID();
        container.innerHTML = `
            <div class="ui centered stackable grid" style="padding: 20px 10px; text-align: left">
                <div class="ten wide computer twelve wide tablet sixteen wide mobile column">
                    <div class="ui segment">
                        <span style="margin-right: 10px" id="${el_id}_drafts_selector"></span>
                        <span class="ui button" id="${el_id}_new_draft_btn"> New draft </span>
                        <span class="ui right floated button" id="${el_id}_submit_btn">Publish draft</span>
                        <span class="ui basic red button" id="${el_id}_remove_post_btn">Delete draft</span>
                    </div>
                    <div id="${el_id}_post_container"></div>
                </div>
            </div>
        `;
        this.posts_container = document.getElementById(`${el_id}_post_container`);
        this.new_draft_btn = document.getElementById(`${el_id}_new_draft_btn`);
        this.remove_post_btn = document.getElementById(`${el_id}_remove_post_btn`);
        this.submit_post_btn = document.getElementById(`${el_id}_submit_btn`);

        this.post_editor = new PostEditor(this.posts_container, {
            'autosave': true,
            'on_title_change': () => { this.drafts_selector.display_drafts(this.post_editor.post['id']); }
        });
        this.drafts_selector = new DraftsSelector(document.getElementById(`${el_id}_drafts_selector`),{
            'on_change': (post) => {
                this.post_editor.display_post(post);
                this.save_state(post['id']);
            }
        });
        this.display_drafts_and_post(draft_id);

        this.new_draft_btn.onclick = () => {
            this.post_editor.new_draft_post().then(() => { this.display_drafts_and_post(); });
        }
        this.remove_post_btn.onclick = () => {
            this.post_editor.remove_post().then(() => { this.display_drafts_and_post(); });
        }
        this.submit_post_btn.onclick = () => {
            this.post_editor.publish_draft()
                .then((response) => { this.display_drafts_and_post(); })
                .catch((error) => { show_alert('warning', error.response.data.error) });
        }
    }

    save_state(post_id) {
        push_state({ 'id': post_id, });
    }

    display_placeholder() {
        this.posts_container.innerHTML = `
            <div class="ui placeholder segment">
              <div class="ui icon header">
                <i class="search icon"></i> No drafts are listed. Let's create a new one!
              </div>
            </div>
        `;
    }

    display_drafts_and_post(draft_id=null) {
        this.drafts_selector.display_drafts(draft_id).then(() => {
            let selected_draft = this.drafts_selector.get_selected_draft();
            if (selected_draft) {
                this.remove_post_btn.classList.remove('hidden');
                this.submit_post_btn.classList.remove('hidden');

                this.post_editor.display_post(selected_draft);
            } else {
                this.remove_post_btn.classList.add('hidden');
                this.submit_post_btn.classList.add('hidden');

                this.display_placeholder();
            }
        });
    }

}


export class DraftsSelector {

    selector_id = null;
    drafts = {};

    constructor(container, settings = {}) {
        this.settings = settings;
        this.container = container;
        this.on_change = settings['on_change'] ? settings['on_change'] : () => {};
    }

    get_drafts() {
        return axios.get('/posts/search?is_draft=True');
    }

    display_drafts(selected_draft_id=null) {
        return this.get_drafts().then((response) => {
            this.selector_id = random_ID();
            this.drafts = {};
            this.container.innerHTML = `
                <select class="ui selection dropdown" id="${this.selector_id}"></select>
            `;

            for (let draft of response.data['posts']) {
                this.drafts[draft['id']] = draft;
                document.getElementById(this.selector_id).innerHTML += `
                    <option value="${draft['id']}" 
                        ${String(draft['id']) === String(selected_draft_id) ? 'selected' : ''}>
                        ${draft['title'] ? draft['title'] : '-- untitled draft --'}
                    </option>
                `;
            }
            $(`#${this.selector_id}`).dropdown({
                onChange: (draft_id) => {
                    this.on_change(this.drafts[draft_id]);
                }
            });
        })
    }

    get_selected_draft() {
        let draft_id = $(`#${this.selector_id}`).dropdown('get value');
        return this.drafts[draft_id];
    }

}
