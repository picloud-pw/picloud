document.addEventListener("DOMContentLoaded", function () {

    init_search();

});

function init_search() {
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
                        price: post['subject'],
                        description: `Posted on ${post['created_date']} by ${post['author_username']}`,
                    })
                }
                return {results: modified_response}
            },
        },
        onSelect: (result, response) => {
            display_post(result['post_id']);
        },
        maxResults: 10,
        minCharacters: 2,
    });
}

function load_posts_list() {
    axios.get('/posts/search')
        .then((response) => {
            let posts = response.data;
        })
}

function display_post(post_id) {

}