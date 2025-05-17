import {PostBodyParser} from "./editorjs.js";


export class Post {

    styles_path = '/static/posts/css/post.css';

    user = null;

    constructor(settings = {}) {
        load_styles(this.styles_path);
        this.ejs_parser = new PostBodyParser();
    }

    render_post(post) {
        let element = document.createElement("article");
        element.classList.add("post");
        element.innerHTML = `
            <div class="post-container" id="post-${post['id']}">
                <header>
                    <h3>
                        <a href="/posts/${post['id']}/" style="cursor: pointer;">${post['title']}</a>
                        ${post['parent_post'] ? '<i class="ui archive icon" title="There is parent post"></i>' : ''}
                    </h3>
                    <p class="subject">
                        <span class="type">${post['type']['title']}</span>
                        |
                        <a class="subject" href="/subs/${post['subject']['id']}/" title="${post['subject']['name']}">
                            ${post['subject']['name']} 
                            <sup>${post['subject']['semester'] > 0 ? post['subject']['semester'] : ''}</sup>
                        </a>
                    </p>
                </header>
                <hr/>
                
                ${this.ejs_parser.parse(post['ejs_body'])}
                
                <hr/>
                <footer>
                    <a class="post-author" title="Author" href="/profile/${post['author']['user']['username']}/">
                        ${post['author']['user']['username']}
                    </a>
                    <span class="post-created-date">
                        • <span title="Created date and time">${post['created_date_human']}</span>
                    </span>
                    <span class="post-footer-badges">
                        <span class="ui" style="color: #999999" title="Views count">
                            <i class="eye icon"></i>${post['views']}
                        </span>
                        ${post['comments'] ? `
                            <span class="comments-counter">
                                <i class="comment icon" title="Comments count"></i> ${post['comments']}
                            </span>
                        ` : ''}
                    </span>
                </footer>
            </div>
        `;
        return element;
    }

}
