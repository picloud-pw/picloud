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
    return {
        "university_id": university_id,
        "department_id": department_id,
        "chair_id": chair_id,
        "program_id": program_id,
        "subject_id": subject_id,
        "type_id": type_id,
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
    if (data.page) components.push(`page=${data.page}`);
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
    loadMoreButton.textContent = 'Загрузка…';
    loadMoreButton.disabled = true;

    pageNumber++;
    let url = `${baseUrl}&page=${pageNumber}`;

    let request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRFToken', getCsrfToken());
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            let parser = new DOMParser();
            let posts = parser.parseFromString(request.responseText, "text/html").body.children;
            if (posts.length === 0) {
                loadMoreButton.textContent = "Больше ничего нет.";
                loadMoreButton.disabled = true;
                nothingLeft = true;
            } else {
                Array.from(posts).forEach(post => {
                    searchResults.appendChild(post);
                });
                assignOnImageLoadedHooks();
                loadMoreButton.textContent = `Загрузить ещё`;
                loadMoreButton.disabled = false;
                nothingLeft = false;
            }
            resizeAllPosts();
            updateImageModalHooks();
        } else {
            // TODO: Обработать ошибку, возвращённую сервером
        }
        loading = false;
    };
    request.onerror = function () {
        // TODO: Обработать ошибку соединения
    };
    request.send(/* FIXME: data */);
}

function search(subject_id = undefined, type_id = undefined) {
    pageNumber = 1;
    let data = {
        subject_id: subject_id,
        type_id: type_id,
        page: 1,
    };
    baseUrl = `/api/posts/?${calculateSuffix(data)}`;
    let request = new XMLHttpRequest();
    request.open('GET', baseUrl, true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('X-CSRFToken', getCsrfToken());
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            searchResults.innerHTML = request.responseText;
            // TODO: Найти лучший способ определения пустого результата
            if (searchResults.querySelector('.post')) {
                loadMoreButton.textContent = "Загрузить ещё";
                loadMoreButton.disabled = false;
                assignOnImageLoadedHooks();
                nothingLeft = false;
            } else {
                nothingLeft = true;
                loadMoreButton.textContent = "Ничего не найдено";
                loadMoreButton.disabled = true;
            }
            resizeAllPosts();
            updateImageModalHooks();
        } else {
            // TODO: Обработать ошибку, возвращённую сервером
        }
    };
    request.onerror = function () {
        // TODO: Обработать ошибку соединения
    };
    request.send(data);

    while (searchResults.lastChild) {
        searchResults.removeChild(searchResults.lastChild);
    }
    loadMoreButton.textContent = "Подождите…";
    loadMoreButton.disabled = true;
}

function newSearchRequest(data) {
    search(data.subject_id, data.type_id);
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
    ]
        .forEach(element => {
            element.addEventListener('change', function () {
                let data = getCurrentValues();
                history.pushState(data, null, `/search/?${calculateSuffix(data)}`);
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
