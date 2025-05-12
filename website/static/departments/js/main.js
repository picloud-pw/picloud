document.addEventListener("DOMContentLoaded", function () {

    restore_state();

});

let DEPARTMENT_ID = null;
let SELECTED_CITY = null;

function save_state() {
    let state = {};
    if (DEPARTMENT_ID) {
        state = {
            "id": DEPARTMENT_ID,
        };
    }
    push_state(state);
}

function restore_state() {
    let params = new URLSearchParams(document.location.search);

    let pathname = new URL(window.location.href).pathname;
    let path_parts = pathname.split('/');

    if (path_parts.length === 4) {
        DEPARTMENT_ID = path_parts[2]
        init_child_department_page(DEPARTMENT_ID);
    } else {
        init_universities_page();
    }

}

function init_universities_page() {
    document.title = 'Universities';

    document.getElementById('hierarchy_root').innerHTML = `
        <div class="ui centered padded grid">
            <div class="six wide computer ten wide tablet sixteen wide mobile column">
                <div id="new_university_form" style="margin-top: 20px"></div>
                <h1 class="ui header" style="margin-top: 40px">Universities</h1>
                <div id="universities_list"></div>
            </div>
        </div>
    `;
    init_new_university_form('new_university_form');
    display_universities_list('universities_list');
}

function display_universities_list(container_id) {
    let container = document.getElementById(container_id);
    return axios.get(`/hierarchy/departments/search?parent_department_id=null`)
        .then((response) => {
            let departments = response.data['departments'];
            for (let d of departments) {
                container.innerHTML += `
                    <div class="ui link items segment" style="cursor: pointer">
                        <a class="item" href="/deps/${d['id']}/">
                            <div class="ui tiny avatar image">
                                <img src="${d['logo']}" alt="Not found" 
                                    onerror="this.src='/media/resources/default/u_logo.png'">
                            </div>
                            <div class="middle aligned content">
                              <div class="header">${d['name']}</div>
                            </div>
                        </a>
                    </div>
               `;
            }
        })
}

function init_new_university_form(container_id) {
    document.getElementById(container_id).innerHTML = `
        <form class="ui form segment">
            <div class="fields">
                <div class="four wide field">
                    <label>Country</label>
                    <div class="ui fluid disabled button">Russia</div>
                </div>
                <div class="twelve wide field">
                    <label>City <i style="color: #d06969" title="Required field">*</i></label>
                    <div class="ui search" id="cities_search">
                        <div class="ui left icon fluid input" style="max-width: 600px">
                            <i class="building outline icon"></i>
                            <input class="prompt" type="text" placeholder="Enter city name">
                        </div>
                        <div class="search results"></div>
                    </div>
                </div>
            </div>
            <div class="field">
                <label>New University Title<i style="color: #d06969" title="Required field">*</i></label>
                <div class="ui fluid search" id="university_search">
                    <div class="ui left icon fluid input" style="max-width: 600px">
                        <i class="university icon"></i>
                        <input class="prompt" type="text" placeholder="Add new university by name">
                    </div>
                    <div class="search results"></div>
                </div>
            </div>
            <div id="new_university_preview"></div>
        </form>
    `;
    init_cities_search_from_vk('cities_search');
    init_universities_search_from_vk('university_search');
}

function init_cities_search_from_vk(input_id) {
    $(`#${input_id}`).search({
        apiSettings: {
            url: "/hierarchy/cities/search?q={query}",
            onResponse: (response) => {
                let modified_response = [];
                for (let city of response['cities']) {
                    modified_response.push({
                        city_id: city['id'],
                        title: city['title'],
                        price: city['region'] ? `<div class="ui basic label">${city['region']}</div>` : '',
                    })
                }
                return {results: modified_response}
            },
        },
        onSelect: (result, response) => {
            document.getElementById('new_university_preview').innerHTML = '';
            SELECTED_CITY = result;
        },
        maxResults: 10,
        minCharacters: 2,
    });
}

function init_universities_search_from_vk(input_id ) {
    $(`#${input_id}`).search({
        apiSettings: {
            url: `/hierarchy/universities/search?q={query}&city_id={city_id}`,
            beforeSend: function(settings) {
                settings.urlData['city_id'] = SELECTED_CITY ? SELECTED_CITY['city_id'] : null;
                return settings;
            },
            onResponse: (response) => {
                let modified_response = [];
                for (let university of response['universities']) {
                    modified_response.push({
                        university_id: university['id'],
                        title: university['title'],
                        price: `<div class="ui basic label">${university['id']}</div>`,
                    })
                }
                return {results: modified_response}
            },
        },
        onSelect: display_university_preview,
        maxResults: 10,
        minCharacters: 2,
    });
}

function display_university_preview(result, response) {
    document.getElementById('new_university_preview').innerHTML = `
        <h5 class="ui dividing header">Approve your choice</h5>
        <span class="ui blue label">City: ${SELECTED_CITY['title']}</span>
        <span class="ui teal label">University: ${result['title']}</span>
        <span class="ui basic mini button" 
            onclick="this.classList.add('loading'); add_new_university('${result['university_id']}', '${result['title']}')">
            Add University
        </span>
    `;
}

function add_new_university(university_id, university_name) {
    let data = new FormData();
    data.append("university_id", university_id);
    data.append("full_university_name", university_name);
    data.append("city_id", SELECTED_CITY ? SELECTED_CITY['city_id'] : null);
    axios.post('/hierarchy/universities/add', data, {headers: {'X-CSRFToken': Cookies.get('csrftoken')}})
        .then((response) => {
            show_alert('success', 'University successfully added!');
        })
        .catch(() => {
            show_alert('warning', 'Something went wrong :( Perhaps this university is already in the database, try searching.');
        })
        .finally(() => {
            init_universities_page();
        })
}

function init_child_department_page(parent_department_id) {
    DEPARTMENT_ID = parent_department_id;

    document.getElementById('hierarchy_root').innerHTML = `
        <div class="ui padded grid">
            <div class="no-margin-padding column">
                <div id="breadcrumbs_container" style="text-align: left; margin-bottom: 20px; min-height: 70px"></div>
    
                <div class="ui centered stackable grid">
                    <div class="fourteen wide column">
                        <div id="search_container" style="margin: 30px 0"></div>
                        <div id="departments_container"></div>
                    </div>
                </div>
    
            </div>
        </div>
    `;

    init_breadcrumbs(parent_department_id);
    init_hierarchy_search(parent_department_id, (search_type, search_query) => {
        let container = document.getElementById('departments_container');
        container.innerHTML = `<div class="ui active centered inline loader"></div>`;
        display_departments_list(container, parent_department_id, search_query, search_type);
    });
}

function get_department_types(parent_department_id) {
    return axios.get(`/hierarchy/departments/types?parent_department_id=${parent_department_id}`);
}

function init_hierarchy_search(parent_department_id, on_change) {
    document.getElementById('search_container').innerHTML = `
        <div class="ui left action big input" style="min-width: 50%">
            <select class="ui compact big dropdown" id="hierarchy_search_type" style="min-width: 30%"></select>
            <input type="text" placeholder="Search..." id="hierarchy_search_query">
        </div>
    `;

    get_department_types(parent_department_id).then((response) => {
        let types = response.data;
        let search_type_container = document.getElementById('hierarchy_search_type');
        for (let tp of types) {
            search_type_container.innerHTML += `
                <option value="${tp['id']}">${tp['name']}</option>
            `;
        }
        if (!types.length) {
            search_type_container.innerHTML += `
                <option selected value="">-- no options --</option>
            `;
        }
        let get_values = () => {
            let search_type = $('#hierarchy_search_type').dropdown('get value');
            let search_query = document.getElementById('hierarchy_search_query').value;
            return [search_type, search_query];
        }
        $('#hierarchy_search_type').dropdown({
            onChange: () => { on_change(...get_values()) },
        })
        document.getElementById('hierarchy_search_query')
            .addEventListener('input', function () { on_change(...get_values()); })
        on_change(...get_values());
    })
}

function init_breadcrumbs(department_id) {

    function format_breadcrumbs(container, node) {
        container.innerHTML += `
            <a class="step ${!node['child'] ? 'active' : ''}" href="/deps/${node['id']}/" title="${node['name']}">
                <div class="content">
                    <div class="title">
                        ${node['name'].length > 50 ? node['name'].substr(0, 50) + '...' : node['name']}
                    </div>
                    <div class="description"></div>
                </div>
            </a>
        `;
        if (node['child']) {
            format_breadcrumbs(container, node['child']);
        } else {
            document.title = node['name'];
        }
    }

    document.getElementById('breadcrumbs_container').innerHTML = `
        <div class="ui fluid small steps" style="min-height: 70px" id="breadcrumbs"></div>
    `;
    let container = document.getElementById('breadcrumbs');
    container.innerText = "";

    axios.get(`/hierarchy/departments/get?id=${department_id}`)
        .then((response) => {
            let hierarchy = response.data['hierarchy'];
            format_breadcrumbs(container, hierarchy);
            $("a.section").popup({position: 'bottom center'});
        });
}
