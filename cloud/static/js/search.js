function postToHtml(post) {
    let request = new XMLHttpRequest();
    request.open('GET', '/post/' + post.id + '/render/', false);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRFToken', getCsrfToken());
    request.send();
    let html = request.responseText;
    return new DOMParser().parseFromString(html, 'text/xml');
}

function getElementValueIfEnabled(element_id) {
    let subject_elem = document.getElementById(element_id);
    return subject_elem.disabled === false ? subject_elem.value : null;
}

function getCurrentValues() {
    let university_id = getElementValueIfEnabled('id_university');
    let department_id = getElementValueIfEnabled('id_department');
    let chair_id = getElementValueIfEnabled('id_chair');
    let program_id = getElementValueIfEnabled('id_program');
    let subject_id = getElementValueIfEnabled('id_subject');
    let type_id = getElementValueIfEnabled('id_type');
    let sort_type = getElementValueIfEnabled('id_sort_type');
    return {
        "university_id": university_id,
        "department_id": department_id,
        "chair_id": chair_id,
        "program_id": program_id,
        "subject_id": subject_id,
        "type_id": type_id,
        "sort_type": sort_type,
    };
}

function setType(id) {
    setOption('id_type', id);
    return Promise.resolve();
}

window.addEventListener('popstate', event => {
    let data = event.state;
    if (!data) return;
    Promise.resolve()
        .then(() => setUniversity(data.university_id))
        .then(() => setDepartment(data.department_id))
        .then(() => setChair(data.chair_id))
        .then(() => setProgram(data.program_id))
        .then(() => setSubject(data.subject_id));
    document.getElementById("id_type").value = data.type_id;
    newSearchRequest(data);
});

function calculateSuffix(data) {
    let components = [];
    if (data.type_id) components.push(`type_id=${data.type_id ? data.type_id : ''}`);
    if (data.subject_id) components.push(`subject_id=${data.subject_id}`);
    if (data.sort_type) components.push(`sort_type=${data.sort_type}`);
    return components.join('&');
}

let baseUrl = null;
let loading = false;
let pageNumber = 1;
let nothingLeft = true;

let loadMoreButton = document.getElementById('btn-load-more');
let searchResults = document.getElementById("search_results");

function loadMore() {
    if (baseUrl === null) return;
    if (loading) return;

    loading = true;
    loadMoreButton.className = 'ui loading primary button';
    loadMoreButton.disabled = true;

    pageNumber++;
    let url = `${baseUrl}&page=${pageNumber}`;

    let request = new Request(url, {
        method: 'GET',
        credentials: "same-origin",
    });

    return fetch(request)
        .then(response => response.ok ? response.json() : Response.error())
        .then(json => {
            let posts = new DOMParser().parseFromString(json['html'], "text/html").body.children;
            if (posts.length > 0) {
                Array.from(posts).forEach(post => {
                    searchResults.appendChild(post);
                    resizePost(post);
                    imagesLoaded(post, resizePostWithImagesLoaded);
                });
            }

            assignOnImageLoadedHooks();

            loadMoreButton.className = 'ui primary button';
            if (json['has_next']) {
                loadMoreButton.textContent = `Загрузить ещё`;
                loadMoreButton.disabled = false;
                nothingLeft = false;
            } else {
                loadMoreButton.textContent = 'Больше ничего нет.';
                loadMoreButton.disabled = true;
                nothingLeft = true;
            }

            resizeAllPosts();
            updateImageModalHooks();
        })
        .catch(() => {
            loadMoreButton.className = 'ui primary button';
            loadMoreButton.textContent = "Не удалось загрузить результаты.";
            loadMoreButton.disabled = true;
        })
        .finally(() => {
            loading = false;
        });
}

function search(subject_id = undefined, type_id = undefined, sort_type = undefined) {
    pageNumber = 1;
    let data = {
        subject_id: subject_id,
        type_id: type_id,
        sort_type: sort_type,
        page: 1,
    };
    baseUrl = `/api/posts/?${calculateSuffix(data)}`;
    let url = `${baseUrl}&page=${data.page}`;

    while (searchResults.lastChild) {
        searchResults.removeChild(searchResults.lastChild);
    }

    loadMoreButton.className = 'ui loading primary button';
    loadMoreButton.textContent = "Подождите…";
    loadMoreButton.disabled = true;

    let request = new Request(baseUrl, {
        method: 'GET',
        credentials: "same-origin",
    });

    return fetch(request)
        .then(response => response.ok ? response.json() : Response.error())
        .then(json => {
            let document = new DOMParser().parseFromString(json['html'], "text/html");
            let posts = Array.from(document.body.children);
            posts.forEach(post => {
                searchResults.appendChild(post);
                resizePost(post);
                imagesLoaded(post, resizePostWithImagesLoaded);
            });

            loadMoreButton.className = 'ui primary button';
            if (json['has_next']) {
                loadMoreButton.textContent = `Загрузить ещё`;
                loadMoreButton.disabled = false;
                nothingLeft = false;
            } else {
                loadMoreButton.textContent = posts.length > 0
                    ? "Больше ничего нет."
                    : "Ничего не найдено.";
                loadMoreButton.disabled = true;
                nothingLeft = true;
            }

            resizeAllPosts();
            updateImageModalHooks();
        })
        .catch(() => {
            loadMoreButton.className = 'ui primary button';
            loadMoreButton.textContent = "Не удалось загрузить результаты.";
            loadMoreButton.disabled = true;
        })
        .finally(() => {
            loading = false;
        });
}

function newSearchRequest(data) {
    search(data.subject_id, data.type_id, data.sort_type);
}

function updateImageModalHooks() {
    let modal = document.getElementById('modal');
    let modalImg = document.getElementById("modalImg");
    let showFullBtn = document.getElementById("show-full-btn");

    for (let img of document.getElementsByClassName('post-img')) {
        img.addEventListener('click', function () {
            modal.style.display = "grid";
            modalImg.src = this.src;
            showFullBtn.href = this.src;
        });
    }
}

ready(() => {
    [
        document.getElementById('id_subject'),
        document.getElementById('id_type'),
        document.getElementById('id_sort_type'),
    ]
        .forEach(element => {
            element.addEventListener('change', function () {
                let data = getCurrentValues();
                history.pushState(data, null, `/feed/?${calculateSuffix(data)}`);
                newSearchRequest(data);
            });
        });

    document.getElementById("id_university").addEventListener("change", () => {
        universityChanged(document.getElementById("id_university").value);
    });
    document.getElementById("id_department").addEventListener("change", () => {
        departmentChanged(document.getElementById("id_department").value);
    });
    document.getElementById("id_chair").addEventListener("change", () => {
        chairChanged(document.getElementById("id_chair").value);
    });
    document.getElementById("id_program").addEventListener("change", () => {
        programChanged(document.getElementById("id_program").value);
    });
    document.getElementById("id_type").options[0].textContent = "Любого типа";

    window.addEventListener('scroll', function (event) {
        if (nothingLeft) return;
        let scrElem = event.target.scrollingElement;
        let scrolledToTheEnd = scrElem.scrollHeight - scrElem.scrollTop <= scrElem.clientHeight;
        if (scrolledToTheEnd) {
            loadMore();
        }
    });
});
