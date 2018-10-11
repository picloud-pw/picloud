function display_options(text_request) {

    let xhr = new XMLHttpRequest();
    xhr.open('GET', "/search?request=" + text_request, true);
    xhr.send();

    xhr.onreadystatechange = function () {
        if (4 !== xhr.readyState) return;

        if (xhr.status === 200) {
            let options = JSON.parse(xhr.responseText);

            console.log(options);
        }

    };

}