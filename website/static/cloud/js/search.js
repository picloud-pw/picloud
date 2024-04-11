function init_posts_search(on_select = null) {
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
