import {PostEditor} from "./posts_editor.js";

export class PostsEditorPage {

    me = null;
    post_id = null;

    constructor(container) {
        let pathname = new URL(window.location.href).pathname;
        let path_parts = pathname.split('/');
        if (path_parts.length !== 4) {
            console.error("Incorrect path format.")
        }
        this.post_id = path_parts[2];

        axios.get('/students/me').then(response => {
            this.me = response.data;
            this.restore_state(container);
        })
    }

    restore_state(container) {
        let el_id = random_ID();
        container.innerHTML = `
            <div class="ui centered stackable grid" style="padding-top: 100px; text-align: left">
                <div class="ten wide computer twelve wide tablet sixteen wide mobile column">
                    <div class="ui segment">
                        <span class="ui right floated button" id="${el_id}_save_btn">Save changes</span>
                        <span class="ui basic red button" id="${el_id}_remove_post_btn">Delete post</span>
                    </div>
                    <div id="${el_id}_post_container"></div>
                </div>
            </div>
        `;
        this.remove_post_btn = document.getElementById(`${el_id}_remove_post_btn`);
        this.save_post_btn = document.getElementById(`${el_id}_save_btn`);

        this.post_editor = new PostEditor(document.getElementById(`${el_id}_post_container`), {
            'autosave': false,
            'post_id': this.post_id,
        });

        this.save_post_btn.onclick = () => {
            this.post_editor.save_changes().then(() => { show_alert('success', 'Changes saved!') });
        }
        this.remove_post_btn.onclick = () => {
            this.post_editor.remove_post().then(() => { window.location.replace('/'); });
        }
    }

}
