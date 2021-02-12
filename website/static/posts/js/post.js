function render_post(post) {
    let element = document.createElement("article");
    element.classList.add("post");
    element.innerHTML = `
            <div class="post-container" id="post-${post['id']}">
                <header>
                    <h2>
                        <a href="/posts?id=${post['id']}" style="cursor: pointer;">${post['title']}</a>
                        ${post['parent_post'] ? '<i class="ui archive icon" title="There is parent post"></i>' : ''}
                    </h2>
                    <p class="subject">
                        <span class="type">${post['type']['title']}</span>
                        |
                        <a class="subject" href="/subjects?id=${post['subject']['id']}" title="${post['subject']['name']}">
                            ${post['subject']['name']} 
                            <sup>${post['subject']['semester'] > 0 ? post['subject']['semester'] : ''}</sup>
                        </a>
                    </p>
                </header>
                <hr/>
                ${post['html'] ? `<div class="text">${post['html']}</div> <hr/>` : ''}
                
                ${post['image']['url'] ? `
                    <img class="post-img" 
                         ratio="${post['image']['width']}x${post['image']['height']}"
                         src="${post['image']['url']}" 
                         alt="${post['image']['url']}">
                ` : ''}
                
                ${post['link'] ? `
                    <a class="ui primary right labeled icon button btn-follow-link" href="${post['link']}" target="_blank">
                        Open link <i class="angle double right icon"></i>
                    </a>
                    <hr/>
                ` : ''}

                ${post['file']['url'] ? `
                    <a class="ui green right labeled icon button btn-download" href="${post['file']['url']}">
                        Download '<strong>${post['file']['extension']}</strong>' file <i class="download icon"></i>
                    </a>
                    <hr/>
                ` : ''}
                
                ${post['is_parent'] ? `
                    <br> <a class="ui button" href="">Child posts</a>
                ` : ''}
                
                <footer>
                    <a class="post-author" title="Author" href="/students?id=${post['author']['id']}">
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
                            <a class="comments-counter" href="">
                                <i class="comment icon" title="Comments count"></i> ${post['comments']}
                            </a>
                        ` : ''}
                    </span>
                </footer>
            </div>
    `;
    return element;
}
