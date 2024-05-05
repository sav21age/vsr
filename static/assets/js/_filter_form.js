const cff = document.getElementById('coniferFilterForm').length;
if (cff) {
    const urlSearchParams = new URLSearchParams(window.location.search);
    const showFilters = urlSearchParams.get('show_filters');
    if (showFilters == 'yes') {
        const ccff = document.getElementById('collapseConiferFilterForm');
        bootstrap.Collapse.getOrCreateInstance(ccff).show();
    }

    let xhr = new XMLHttpRequest();

    // function formatParams(params) {
    //     return "?" + Object
    //         .keys(params)
    //         .map(function (key) {
    //             return key + "=" + encodeURIComponent(params[key])
    //         })
    //         .join("&")
    // }

    let csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]')

    const data = {
        // 'genus': [1,7],
        // 'height_from': 220,
        // 'width_from': 60,
        'extra': 'on',
        'csrfmiddlewaretoken': csrfToken.value
    };

    // console.log(JSON.stringify(data['genus']))

    // const ps = new URLSearchParams();
    // ps.set('genus', [1,3]);
    // console.log(ps.toString());

    // serialize = function (obj, prefix) {
    //     var str = [],
    //         p;
    //     for (p in obj) {
    //         if (obj.hasOwnProperty(p)) {
    //             var k = prefix ? prefix + "[" + p + "]" : p,
    //                 v = obj[p];
    //             str.push((v !== null && typeof v === "object") ?
    //                 serialize(v, k) :
    //                 encodeURIComponent(k) + "=" + encodeURIComponent(v));
    //         }
    //     }
    //     return str.join("&");
    // }

    serialize = function (obj, prefix) {
        let str = [], p;
        for (p in obj) {
            if (obj.hasOwnProperty(p)) {
                let k = prefix ? prefix : p, v = obj[p];
                str.push((v !== null && typeof v === "object") ?
                    serialize(v, k) :
                    encodeURIComponent(k) + "=" + encodeURIComponent(v));
            }
        }
        return str.join("&");
    }

    // console.log(serialize({
    //     foo: "hi there",
    //     'genus': [1, 3]
    // }));


    // console.log(new URLSearchParams(data).toString())

    const target = new URL('http://127.0.0.1/catalog/conifers/filter-form/');
    target.search = new URLSearchParams(data).toString();
    let p = new URLSearchParams(data).toString();

    let params = JSON.stringify(data);

    // console.log(params)
    // console.log(p)

    // xhr.open("GET", `/catalog/conifers/filter-form/?${p}`, true);
    // xhr.open("GET", `/catalog/conifers/filter-form/?genus=1&genus=3`, true);
    xhr.open("POST", `/catalog/conifers/filter-form/`, true);
    xhr.setRequestHeader("X-REQUESTED-WITH", "XMLHttpRequest");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
        }
    };
    xhr.send(new URLSearchParams(serialize(data)));



    // const searchParams = new URLSearchParams();
    // const s = {foo: "hi there", bar: [1,3] };
    // Object.keys(s).forEach(key => searchParams.append(key, s[key]));
    // console.log(searchParams.toString())


    // function jsonToQueryString(json) {
    //     return '?' +
    //         Object.keys(json).map(function (key) {
    //             return encodeURIComponent(key) + '=' +
    //                 encodeURIComponent(json[key]);
    //         }).join('&');
    // }

    // console.log(jsonToQueryString(data));
}