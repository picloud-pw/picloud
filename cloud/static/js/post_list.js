window.addEventListener("load", function () {
    resizeAllPosts();
    assignOnImageLoadedHooks();
});

window.addEventListener("resize", resizeAllPosts);

function assignOnImageLoadedHooks() {
    let allItems = document.getElementsByClassName("post");
    for (let post of allItems) {
        imagesLoaded(post, resizePostWithImagesLoaded);
    }
}

function resizePostWithImagesLoaded(instance) {
    let post = instance.elements[0];
    resizePost(post);
}

function resizeAllPosts() {
    posts = document.getElementsByClassName("post");
    for (let post of posts) {
        resizePost(post);
    }
}

function resizePost(post) {
    let postList = document.getElementsByClassName("post-list")[0];
    let rowHeight = parseInt(window.getComputedStyle(postList).getPropertyValue('grid-auto-rows'));
    let rowGap = parseInt(window.getComputedStyle(postList).getPropertyValue('grid-row-gap'));
    let fullRowHeight = rowHeight + rowGap;
    let rowsNumber = Math.ceil((post.querySelector('.post-container').getBoundingClientRect().height + rowGap) / fullRowHeight);
    post.style.gridRowEnd = "span " + rowsNumber;
}
