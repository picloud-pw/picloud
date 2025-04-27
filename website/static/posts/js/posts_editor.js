import {PostBodyEditor} from "./editorjs.js";
import {Subjects} from "./subjects.js";


export class PostEditor {

    post = null;
    autosave = false;

    constructor(container, settings) {
        this.container = container;
        this.subjects_service = new Subjects();

        this.autosave = settings['autosave'] ? settings['autosave'] : false;
        this.on_title_change = settings['on_title_change'] ? settings['on_title_change'] : () => {};
        axios.get('/students/me').then((response) => {
            this.me = response.data;
            if (settings['post']) {
                this.display_post(settings['post']);
            } else if (settings['post_id']) {
                this.display_post_with_id(settings['post_id']);
            }
        })
    }

    get_post(post_id) {
        return axios.get(`/posts/get?id=${post_id}`);
    }

    display_post_with_id(post_id) {
        this.get_post(post_id).then((response) => {
            this.display_post(response.data);
        });
    }

    display_post(post) {
        this.post = post;
        this.el_id = random_ID();
        this.container.innerHTML = `
            <div class="ui segment" id="${this.el_id}_settings"></div>
            <div class="ui segment" style="margin-top: 20px; padding: 15px" id="${this.el_id}_body"></div>
        `;
        this.display_post_settings();
        this.display_post_body();
    }

    display_post_settings() {
        document.getElementById(`${this.el_id}_settings`).innerHTML = `
            <form class="ui form">
                <div class="fluid field" id="subject_selector_field"></div>
                <div class="fields">
                    <div class="ten wide field">
                        <label>Title</label>
                        <input type="text" id="${this.el_id}_title" placeholder="Title" value="${this.post['title']}">
                    </div>
                    <div class="six wide field">
                        <label>Post type</label>
                        <select class="ui search dropdown" id="${this.el_id}_type"></select>
                    </div>
                </div>
            </form>
        `;

        this.init_subject_selector_field(
            document.getElementById('subject_selector_field'),
            this.post['subject'] ? this.post['subject']['id'] : null
        );
        document.getElementById(`${this.el_id}_title`).onchange = () => {
            if (this.autosave) { this.save_changes(); }
            this.on_title_change();
        }
        this.display_post_types( this.post['type'] ? this.post['type']['id'] : null);
    }

    init_subject_selector_field(container, subject_id) {
        container.innerHTML = `
            <label>Subject</label>
            <div class="ui action fluid input">
                <div class="ui selection fluid search loading dropdown" id="${this.el_id}_subjects">
                    <div class="text"></div> <i class="dropdown icon"></i>
                </div>
                <div class="ui icon button" id="${this.el_id}_new_subject_btn"> <i class="plus icon"></i> </div>    
            </div>
        `;
        document.getElementById(`${this.el_id}_new_subject_btn`).onclick = () => {
            this.subjects_service.display_new_subject_modal((response) => {
                this.init_subject_selector_field(container);
            });
        }
        this.subjects_service.get_subjects_list().then(response => {
            let personal_subjects = [];
            let public_subjects = [];
            for (let subject of response.data['subjects']) {
                let sub_dict = {
                    name: subject['name'],
                    class: 'vertical item',
                    value: subject['id'],
                    description: subject['departments'] && subject['departments'].length ?
                        subject['departments'][0]['name'] : null,
                    selected: subject['id'] === subject_id,
                };
                if (subject['author_id'] === this.me.user.id) {
                    personal_subjects.push(sub_dict);
                } else {
                    public_subjects.push(sub_dict);
                }
            }
            $(`#${this.el_id}_subjects`).dropdown({
                placeholder: 'Subjects  selector...',
                values: [{name: 'Your subjects', type: 'header', icon: 'book'}]
                    .concat(personal_subjects)
                    .concat([{name: 'Public available subjects', type: 'header', icon: 'book'}])
                    .concat(public_subjects),
                onChange: () => { this.save_changes(); }
            });
            document.getElementById(`${this.el_id}_subjects`).classList.remove('loading');
        })
    }

    display_post_body() {
        this.body_editor = new PostBodyEditor(document.getElementById(`${this.el_id}_body`), {
            data: this.post['ejs_body'],
            on_change: () => { if (this.autosave) { this.save_changes(); } },
        })
    }

    display_post_types(post_type_id = null) {
        let container = document.getElementById(`${this.el_id}_type`);
        axios.get('/posts/types/get').then(response => {
            for (let type of response.data['types']) {
                container.innerHTML += `
                    <option value="${type['id']}" ${type['id'] === post_type_id ? 'selected' : ''}>
                        ${type['title']}
                    </option>
                `;
            }
            $(`#${this.el_id}_type`).dropdown({
                onChange: () => {
                    if (this.autosave) { this.save_changes(); }
                }
            });
        })
    }

    get_post_type_id() {
        return $(`#${this.el_id}_type`).dropdown('get value');
    }

    get_title() {
        return $(`#${this.el_id}_title`).val();
    }

    get_subject() {
        return $(`#${this.el_id}_subjects`).dropdown('get value');
    }

    new_draft_post() {
        let data = new FormData();
        return axios.post('/posts/create', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}});
    }

    async save_changes() {
        let data = new FormData();
        data.append('id', this.post['id']);
        data.append('title', this.get_title());
        data.append('subject_id', this.get_subject());
        data.append('post_type_id', this.get_post_type_id());
        data.append('body', JSON.stringify(await this.body_editor.save()));

        return axios.post('/posts/update', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}});
    }

    publish_draft() {
        let data = new FormData();
        data.append('id', this.post['id']);
        data.append('is_draft', 'False');
        return axios.post('/posts/submit', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
    }

    remove_post() {
        let data = new FormData();
        data.append("id", this.post['id']);
        return axios.post('/posts/delete', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
    }

}
