function format_post_links(links) {
    if (!links.length)
        return '';
    let links_list = ``;
    for (let link of links) {
        links_list += `
          <div class="item">
            <i class="linkify icon"></i>
            <div class="content">
                <a href="${link}" target="_blank">${link}</a>
            </div>
          </div>
        `;
    }
    return `<div class="ui list">${links_list}</div><hr/>`;
}

function format_post_images(images) {
    let template = '';
    for (let image of images) {
        template += `
            <a href="${image['url']}" target="_blank">
                <img class="post-img" src="${image['url']}"  alt="${image['url']}"
                    ratio="${image['width']}x${image['height']}"/>
                <hr/>
            </a>
        `;
    }
    return template;
}

function format_post_files(files) {
    let template = '';
    for (let file of files) {
        template += `
            <a class="ui green right basic labeled icon mini fluid button" href="${file['url']}" target="_blank">
                Download '<strong>${file['extension']}</strong>' file <i class="download icon"></i>
            </a>
            <hr/>
        `
    }
    return template;
}

function render_post(post) {
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
            ${post['html'] ? `<div class="text">${post['html']}</div> <hr/>` : ''}
            
            ${format_post_images(post['attachments']['images'])}
            
            ${format_post_links(post['attachments']['links'])}

            ${format_post_files(post['attachments']['files'])}
            
            ${post['is_parent'] ? `
                <br> <a class="ui button" href="">Child posts</a>
            ` : ''}
            
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
