function addParam(param) {
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

function initFilterMap(center, zoom) {
    var mapCenter = center || {
        lat: 46.589931,
        lng: -95.009003
    };
    var mapZoom = zoom || 3;
    window.map = new google.maps.Map(document.getElementById('map'), {
        center: mapCenter,
        zoom: mapZoom
    });
}

function getMapLabels(url) {
    axios.get('/api/get_labels/?' + url)
        .then(function (response) {
            if (response.data.data) {
                var mapLabels = response.data.data;
                var mapContainer = document.getElementById('map');
                // hide an empty map
                if (mapLabels.length == 0) {
                    mapContainer.style.display = 'none';
                    return;
                // center on a single label
                } else if (mapLabels.length == 1) {
                    initFilterMap({
                        lat: Number(mapLabels[0][0]),
                        lng: Number(mapLabels[0][1])
                    }, 6)
                } else {
                    initFilterMap();
                }
                for (var i = 0; i < mapLabels.length; i++) {
                    var lat = Number(mapLabels[i][0]);
                    var lng = Number(mapLabels[i][1]);
                    mapLabels[i][1] = Number(mapLabels[i][1]);
                    var maker = new google.maps.Marker({
                        position: {
                            lat: lat,
                            lng: lng
                        },
                        map: window.map,
                        title: mapLabels[i][2] + '\n' + mapLabels[i][3] + ', ' + mapLabels[i][4]
                    });
                }

            }
        })
        .catch(function (error) {
            initFilterMap();
            console.log(error);
        })
}

function initCollegeMap(college) {
    var map, maker, title = '';

    if (college.city && college.state && college.zip) {
        title = college.city + ', ' + college.state + ', ' + college.zip;
    }

    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: college.latitude,
            lng: college.longitude
        },
        zoom: 17
    });
    maker = new google.maps.Marker({
        position: {
            lat: college.latitude,
            lng: college.longitude
        },
        map: map,
        title: title
    });

}

function modifyFavourites(el, collegeId) {
    axios.get('/api/modify_favourites/?college_id=' + collegeId)
        .then(function (response) {
            if (response.data && response.data == 'Added') {
                el.classList.remove('far');
                el.classList.add('fas');
                if (el.parentNode.className == 'card-header') {
                    el.parentNode.parentNode.classList.remove('card');
                    el.parentNode.parentNode.classList.add('card-favourite');
                }
            } else if (response.data && response.data == 'Removed') {
                el.classList.remove('fas');
                el.classList.add('far');
                if (el.parentNode.className == 'card-header') {
                    el.parentNode.parentNode.classList.remove('card-favourite');
                    el.parentNode.parentNode.classList.add('card');
                }
            }
        })
        .catch(function (error) {
            console.log(error);
        })
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

$('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
  if (!$(this).next().hasClass('show')) {
    $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
  }
  var $subMenu = $(this).next(".dropdown-menu");
  $subMenu.toggleClass('show');

  $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
    $('.dropdown-submenu .show').removeClass("show");
  });

  return false;
});

$('.favourite-button').on('click', function(e) {
    var id = this.getAttribute('data-college-id');
    if (id) modifyFavourites(this, id);
});