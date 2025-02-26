import Masonry from 'https://cdn.jsdelivr.net/npm/masonry-layout@4.2.2/+esm';
import imagesLoaded from 'https://cdn.jsdelivr.net/npm/imagesloaded@5.0.0/+esm';

import {Post} from "../../posts/js/post.js";


export class CloudPage {

    masonry = null;
    page = 1;

    constructor(container, settings) {
        this.container = container;
        this.restore_state();
    }

    restore_state() {
        this.container.innerHTML = `
            <div class="ui padded grid">
                <div class="no-margin-padding column">
                    <div class="ui segment" id="search_container">
                        <div class="ui stackable grid">
                            <div class="left floated sixteen wide column">
                                <div class="ui search" id="top_search">
                                    <div class="ui left icon fluid input" style="max-width: 600px">
                                        <i class="search icon"></i>
                                        <input class="prompt" id="search" type="text" placeholder="Enter search query"
                                               style="border-radius: 50px;">
                                    </div>
                                    <div class="search results"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="modal"></div>
                    <div class="ui basic segment" style="min-height: 100px; margin-top: 0; text-align: center">
                        <div id="posts_container"></div>
                        <div class="ui basic button" id="load_more_btn">load more...</div>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('load_more_btn').onclick = () => {
            this.load_posts_list();
        }
        const grid = document.querySelector('#posts_container');
        this.clear_posts_container(grid);
        this.masonry = new Masonry(grid, {
            itemSelector: ".post",
            columnWidth: ".post-size-reference",
            gutter: ".post-grid-gutter-size-reference",
            percentPosition: true,
        });
        imagesLoaded(grid).on('progress', () => {
            this.masonry.layout();
        });
        let intervalId = setInterval(() => {
            this.masonry.layout();
        }, 3000);

        this.init_posts_search(
            (result, response) => {
                window.location.href = `/posts?id=${result['post_id']}`;
            }
        );

        this.load_posts_list();
    }

    load_posts_list() {
        let btn = document.getElementById('load_more_btn');
        btn.classList.add('loading');
        let container = document.getElementById('posts_container');
        axios.get(`/posts/search?page=${this.page}`)
            .then((response) => {
                let posts = response.data['posts'];
                for (let post of posts) {
                    let rendered_post = new Post().render_post(post);
                    this.append_element(rendered_post, container);
                }
            })
            .finally(() => {
                btn.classList.remove('loading');
                this.page += 1;
            })
    }

    clear_posts_container(postsGrid) {
        postsGrid.innerHTML = '';

        let masonrySizer = document.createElement("div");
        masonrySizer.classList.add("post-size-reference");
        postsGrid.appendChild(masonrySizer);

        let gutterSizer = document.createElement("div");
        gutterSizer.classList.add("post-grid-gutter-size-reference");
        postsGrid.appendChild(gutterSizer);
    }

    append_element(element, postsContainer) {
        postsContainer.appendChild(element);
        this.masonry.appended(element);
        imagesLoaded(element).on('progress', () => {
            this.masonry.layout();
        });
    }

    init_posts_search(on_select = null) {
        $('.ui.search').search({
            apiSettings: {
                url: "/posts/search?q={query}",
                onResponse: (response) => {
                    let posts = response['posts'];
                    let modified_response = [];
                    for (let post of posts) {
                        modified_response.push({
                            post_id: post['id'],
                            title: post['title'],
                            price: post['author']['user']['username'],
                            description: `[${post['created_date_human']}] ${post['subject']['name']}`,
                        })
                    }
                    return {results: modified_response}
                },
            },
            onSelect: on_select,
            maxResults: 10,
            minCharacters: 2,
        });
    }

}
