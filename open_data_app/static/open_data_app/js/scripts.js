function addParam(param) {
    debugger
    if (window.location.href.indexOf(param) > -1) return;
    if (window.location.href.indexOf('?') > 0) {
        var parsedData = /(.*)\=(.*)/.exec(param);
        var parsedParam = parsedData[1];
        var parsedValue = parsedData[2];
        updateURLParameter(window.location.href, parsedParam, parsedValue)
    } else {
        window.location.href += '?' + param;
    }
}

function updateURLParameter(url, param, paramVal) {
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";
    if (additionalURL) {
        tempArray = additionalURL.split("&");
        for (var i = 0; i < tempArray.length; i++) {
            if (tempArray[i].split('=')[0] != param) {
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }
    }

    var rows_txt = temp + "" + param + "=" + paramVal;
    url = baseURL + "?" + newAdditionalURL + rows_txt;
    window.location.href = url.replace(/(.*)(page\=\d+&)(.*)/, '$1$3');
}