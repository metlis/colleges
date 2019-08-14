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

function initFilterMap() {
    window.map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 46.589931,
            lng: -95.009003
        },
        zoom: 3
    });
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

function getMapLabels(url) {
    axios.get('/api/get_labels/?' + url)
        .then(function (response) {
            if (response.data.data) {
                initFilterMap();
                var mapLabels = response.data.data;
                var locations = [];
                for (var i = 0; i < mapLabels.length; i++) {
                    locations.push(mapLabels[i])
                }
                for (var i = 0; i < locations.length; i++) {
                    var lat = Number(locations[i][0]);
                    var lng = Number(locations[i][1]);
                    locations[i][1] = Number(locations[i][1]);
                    var maker = new google.maps.Marker({
                        position: {
                            lat: lat,
                            lng: lng
                        },
                        map: window.map,
                        title: locations[i][2] + '\n' + locations[i][3] + ', ' + locations[i][4]
                    });
                }

            }
        })
        .catch(function (error) {
            initFilterMap();
            console.log(error);
        })
}

function modifyFavourites(el, key, collegeId) {
    axios.get('/api/modify_favourites/?session_key=' + key + '&college_id=' + collegeId)
        .then(function (response) {
            if (response.data && response.data == 'Added') {
                el.classList.remove('far');
                el.classList.add('fas');
            } else if (response.data && response.data == 'Removed') {
                el.classList.remove('fas');
                el.classList.add('far');
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

$('#college-star').on('click', function(e) {
    var key = this.getAttribute('data-session-key');
    var id = this.getAttribute('data-college-id');
    if (key && id) modifyFavourites(this, key, id);
});