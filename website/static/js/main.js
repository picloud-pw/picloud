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
