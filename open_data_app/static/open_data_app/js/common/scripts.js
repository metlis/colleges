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

function initFilterGMap(center, zoom) {
    var mapCenter = center || {
        lat: 39.589931,
        lng: -95.009003
    };
    var mapZoom = zoom || 3;
    window.map = new google.maps.Map(document.getElementById('map'), {
        center: mapCenter,
        zoom: mapZoom
    });
}

function initFilterYMap(center, zoom) {
    var mapCenter = center || [
        39.589931,
        -95.009003
    ];
    var mapZoom = zoom || 3;
    window.map = new ymaps.Map('map', {
        center: mapCenter,
        zoom: mapZoom,
    });
}

function createLabelText(label) {
    var text = '<h3>' + label[4] + '</h3>' +
               '<p><span class="icon-container"><i class="fab fa-internet-explorer" data-toggle="tooltip" data-placement="top"></i></span>: <a href="' + '/institution/' + label[2] + '/' + label[3] + '/' + '">College page</a></p>' +
               '<p><span class="icon-container"><i class="fas fa-map-marker-alt" data-toggle="tooltip" data-placement="top"></i></span>: ' + label[5] + ', ' + label[6] + '</p>' +
               '<p><span class="icon-container"><i class="fas fa-city" data-toggle="tooltip" data-placement="top"></i></span>: ' + label[8] + '</p>' +
               '<p><span class="icon-container"><i class="fas fa-user-graduate" data-toggle="tooltip" data-placement="top"></i></span>: ' + label[7] + '</p>' +
               '<p><span class="icon-container"><i class="fas fa-home" data-toggle="tooltip" data-placement="top"></i></span>: ' + label[9] + '</p>';
    return text;
}

function getGMapLabels(url) {
    axios.get('/api/request_map_labels/?' + url)
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
                    initFilterGMap({
                        lat: Number(mapLabels[0][0]),
                        lng: Number(mapLabels[0][1])
                    }, 6)
                } else {
                    initFilterGMap();
                }
                var markers = mapLabels.map(function (label, i) {
                    var contentString = '<div class="mapInfo">' +
                        createLabelText(label) +
                        '</div>';
                    var infowindow = new google.maps.InfoWindow({
                        content: contentString
                    });
                    var marker = new google.maps.Marker({
                        position: {
                            lat: Number(label[0]),
                            lng: Number(label[1])
                        },
                        title: label[4] + '\n' + label[5] + ', ' + label[6]
                    });
                    google.maps.event.addListener(marker, 'click', function () {
                        infowindow.open(map, marker);
                    });
                    return marker;
                });
                var markerCluster = new MarkerClusterer(map, markers,
                    {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
            }
        })
        .catch(function (error) {
            initFilterGMap();
            console.log(error);
        })
}

function getYMapLabels(url) {
    axios.get('/api/request_map_labels/?' + url)
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
                    initFilterYMap([
                        Number(mapLabels[0][0]),
                        Number(mapLabels[0][1])
                    ], 6)
                } else {
                    initFilterYMap();
                }
                var clusterer = new ymaps.Clusterer({
                    preset: 'islands#invertedBlueClusterIcons',
                    clusterHideIconOnBalloonOpen: false,
                    geoObjectHideIconOnBalloonOpen: false
                });
                var geoObjects = mapLabels.map(function(label) {
                    var point = [Number(label[0]), Number(label[1])];
                    var pointData = {
                        balloonContentBody: createLabelText(label),
                        clusterCaption: '<strong>' + label[4] + '</strong>'
                    };
                    return new ymaps.Placemark(point, pointData);
                });
                clusterer.add(geoObjects);
                map.geoObjects.add(clusterer);
            }
        })
        .catch(function (error) {
            initFilterGMap();
            console.log(error);
        })
}

function initCollegeGMap(college) {
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

function initCollegeYmap(lat, long, city, state, zip) {
    var map, maker, title = '';

    map = new ymaps.Map('map', {
        center: [lat, long],
        zoom: 8,
    });

    maker = new ymaps.GeoObject({
        geometry: {
            type: 'Point',
            coordinates: [lat, long],
        },
        properties: {
            balloonContent: city + ', ' + state + ', ' + zip,
        }
    });

    map.geoObjects.add(maker);

}

function modifyFavourites(el, collegeId) {
    axios.get('/api/toggle_favourite/?college_id=' + collegeId)
        .then(function (response) {
            var favBadge = document.getElementById('favourite-badge');
            if (response.data && response.data == 'Added') {
                favBadge.innerText =  Number(favBadge.innerText) + 1;
                el.classList.remove('far');
                el.classList.add('fas');
                if (el.parentNode.className == 'card-header') {
                    el.parentNode.parentNode.classList.remove('card');
                    el.parentNode.parentNode.classList.add('card-favourite');
                }
            } else if (response.data && response.data == 'Removed') {
                favBadge.innerText = Number(favBadge.innerText) - 1;
                el.classList.remove('fas');
                el.classList.add('far')
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

$(".card-header, .sort").click(function () {
    var icon =  $(this).find(".rotate");
    $(icon).toggleClass('down');
});

$('.cookie-agreement').on('click', function(e) {
    axios.get('/api/agree_on_cookies/')
        .then(function (response) {
            $('.v-snack').css('display', 'none');
        })
        .catch(function (error) {
            console.log(error);
    })
});