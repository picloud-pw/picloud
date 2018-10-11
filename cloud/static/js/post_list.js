function assignOnImageLoadedHooks() {
    let allItems = document.getElementsByClassName("post");
    for (let post of allItems) {
        imagesLoaded(post, resizePostWithImagesLoaded);
    }
}

window.addEventListener("load", function () {
    resizeAllPosts();
    assignOnImageLoadedHooks();
});

window.addEventListener("resize", resizeAllPosts);

function resizePostWithImagesLoaded(instance) {
    let post = instance.elements[0];
    resizePost(post);
}

function resizeAllPosts() {
    let posts = document.getElementsByClassName("post");
    for (let post of posts) {
        resizePost(post);
    }
}

function resizePost(post) {
    let image = post.querySelector('img.post-img');
    let ratio = image ? image.attributes['ratio'] : undefined;
    if (ratio) {
        let [origWidth, origHeight] = ratio.value.split('x');
        image.style.height = `${image.width * origHeight / origWidth}px`;

        // Forcibly redraw the post
        let oldPostDisplay = post.style.display;
        post.style.display = 'none';
        post.style.display = oldPostDisplay;

        // Forcibly redraw the image
        let oldImageDisplay = image.style.display;
        image.style.display = 'none';
        image.style.display = oldImageDisplay;

        image.style.height = `${image.width * origHeight / origWidth}px`;
    }

    let postList = document.getElementsByClassName("post-list")[0];
    let rowHeight = parseInt(window.getComputedStyle(postList).getPropertyValue('grid-auto-rows'));
    let rowGap = parseInt(window.getComputedStyle(postList).getPropertyValue('grid-row-gap'));
    let fullRowHeight = rowHeight + rowGap;
    let rowsNumber = Math.ceil((post.querySelector('.post-container').getBoundingClientRect().height + rowGap) / fullRowHeight);
    post.style.gridRowEnd = "span " + rowsNumber;
}
