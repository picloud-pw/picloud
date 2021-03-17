function random_ID() {
    return '_' + Math.random().toString(36).substr(2, 9);
}

Date.prototype.toPrettyString = function () {
    let dd = this.getDate();
    let mm = this.getMonth() + 1;

    let date = [
        (dd > 9 ? '' : '0') + dd,
        (mm > 9 ? '' : '0') + mm,
        this.getFullYear(),
    ].join('-');
    let time = [
        this.getHours(),
        this.getMinutes(),
    ].join(':');
    return `${date}${time === '3:0' ? '' : ' ' + time}`;
};

Date.prototype.toYYYYMMDD = function () {

    let dd = this.getDate();
    let mm = this.getMonth() + 1;

    return [
        this.getFullYear(),
        (mm > 9 ? '' : '0') + mm,
        (dd > 9 ? '' : '0') + dd,
    ].join('-');
};

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
            <div class="ui placeholder">
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
            <div class="ui placeholder">
              <div class="image header">
                <div class="line"></div><div class="line"></div>
                <div class="line"></div><div class="line"></div>
              </div>
            </div>
        `;
    }
}

function show_ad_block(type='squared'){
    if (window.CAN_RUN_ADS === undefined) {
        return ads_placeholders()
    }

    let slot = 'medium rectangle';
    let ad_id = '3230844943'

    if (type === 'horizontal') {
        ad_id = '6967388903';
        slot = 'banner';
    }
    if (type === 'vertical') {
        ad_id = '9597421672';
        slot = 'vertical rectangle';
    }
    return `
        <div class="ui ${slot} ad" style="margin: auto;">
            <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-8915976864571228"
                 data-ad-slot="${ad_id}"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>
                 (adsbygoogle = window.adsbygoogle || []).push({});
            </script>
        </div>
    `
}

function ads_placeholders() {
     return `
        <div class="ui medium rectangle" style="text-align: center">
            <img src="/static/img/sad-cat.png" alt="sad-cat :(" 
                style="margin:10px; max-width: 100%; max-height: 100%"/>
            <hr>
            <div style="margin: 10px;">
                Please <a href="https://globalnews.ca/pages/disable-ad-blocker" target="_blank">disable AdBlock</a> 
                and <a href="">refresh</a> the page. <br>
                We try not to annoy you with ads 😔
            </div>
        </div>
    `;
}