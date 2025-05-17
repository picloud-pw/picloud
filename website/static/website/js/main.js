function random_ID() {
    return '_' + Math.random().toString(36).substr(2, 9);
}

Date.prototype.toHHMM = function () {
    let hour = this.getHours();
    let minute = this.getMinutes();
    return [(hour > 9 ? '' : '0') + hour, (minute > 9 ? '' : '0') + minute].join(':');
}

Date.prototype.toYYYYMMDD = function () {
    let day = this.getDate();
    let month = this.getMonth() + 1;
    return [this.getFullYear(), (month > 9 ? '' : '0') + month, (day > 9 ? '' : '0') + day].join('-');
};

Date.prototype.toPrettyString = function () {
    return `${this.toYYYYMMDD()} ${this.toHHMM()}`;
};

function load_styles(styles_path) {
    let style = document.querySelectorAll(`[href="${styles_path}"]`);
    if (style.length === 0) {
        let style_el = document.createElement('link');
        style_el.rel = 'stylesheet';
        style_el.href = styles_path;
        document.head.appendChild(style_el);
    }
}

function push_state(dict) {
    let kvp = [];

    for (let i in Object.keys(dict)) {
        let key = Object.keys(dict)[i];
        let value = encodeURI(dict[key]);
        key = encodeURI(key);
        kvp.push([key, value].join('='));
    }

    let new_search = "?" + kvp.join('&');
    history.pushState(null, null, new_search);
}

function isScrolledIntoView(elem) {
    let docViewTop = $(window).scrollTop();
    let docViewBottom = docViewTop + $(window).height();

    let elemTop = $(elem).offset().top;
    let elemBottom = elemTop + $(elem).height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}

function render_placeholder(icon, message) {
    return `
        <div class="ui basic placeholder segment" style="min-height: 100px">
          <div class="ui icon header">
            <i class="${icon} icon"></i>
            ${message}
          </div>
        </div>
    `;
}

function render_loader(type = 'paragraph') {
    if (type === 'paragraph') {
        return `
            <div class="ui fluid placeholder">
              <div class="paragraph">
                <div class="line"></div><div class="line"></div>
                <div class="line"></div><div class="line"></div>
                <div class="line"></div><div class="line"></div>
              </div>
            </div>
            </div>
        `;
    } else if (type === 'avatar') {
        return `
            <div class="ui fluid placeholder">
              <div class="image header">
                <div class="line"></div><div class="line"></div>
                <div class="line"></div><div class="line"></div>
              </div>
            </div>
        `;
    }
}

function show_alert(type, message, time = 2) {
    let color_class = '';
    let icon = '';
    if (type === "success") {
        color_class = 'teal';
        icon = 'checkmark box';
    }
    if (type === "info") {
        color_class = 'blue';
        icon = 'info circle';
    }
    if (type === "warning") {
        color_class = 'yellow';
        icon = 'warning sign';
    }
    if (type === "error") {
        color_class = 'error';
        icon = 'remove circle';
    }

    $.toast({
        title: type.charAt(0).toUpperCase() + type.slice(1),
        message: String(message),
        class: color_class,
        showProgress: 'bottom',
        showIcon: icon,
        displayTime: Number(time) * 1000,
    });
}
