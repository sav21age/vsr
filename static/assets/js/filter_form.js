(function () {
    ("use strict");

    /**
     * Easy selector helper function
     */
    const select = (el, all = false) => {
        el = el.trim();
        if (all) {
            return [...document.querySelectorAll(el)];
        } else {
            return document.querySelector(el);
        }
    };

    /**
     * Easy event listener function
     */
    const on = (type, el, listener, all = false) => {
        let selectEl = select(el, all);
        if (selectEl) {
            if (all) {
                selectEl.forEach((e) => e.addEventListener(type, listener));
            } else {
                selectEl.addEventListener(type, listener);
            }
        }
    };

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
    };

    let csrfToken = select('input[name=csrfmiddlewaretoken]');

    numberField = function (field, res) {
        field.disabled = false
        if (JSON.parse(res['min']) === null || JSON.parse(res['max']) === null) {
            field.setAttribute('placeholder', '')
            field.disabled = 'disabled'
        } else {
            field.setAttribute('min', res['min'])
            field.setAttribute('data-min', res['min'])
            
            field.setAttribute('max', res['max'])
            field.setAttribute('data-max', res['max'])
            
            field.setAttribute('placeholder', `от ${res['min']} до ${res['max']}`)
        }

        if (field.value !== '') {
            if ((field.value < Number(field.min) || field.value > Number(field.max))) {
                field.classList.add('is-invalid');
            }
        }

    };

    selectField = function (field, res) {
        field.disabled = false
        if (res.length == 0) {
            field.selectedIndex = 0
            field.disabled = 'disabled'
        } else {
            Object.values(field.options).forEach((el) => {
                if (el.value != '') {
                    el.removeAttribute("hidden");
                    if (!res.includes(Number(el.value))) {
                        if (el.selected) field.selectedIndex = 0
                        el.setAttribute('hidden', 'true');
                    }
                }
            })
        }
    };    

    // const cff = select('#coniferFilterForm').length;
    const cff = select('#coniferFilterForm');
    if (cff) {
        const urlSearchParams = new URLSearchParams(window.location.search);
        const showFilters = urlSearchParams.get('show_filters');
        if (showFilters == 'yes') {
            const ccff = select('#collapseConiferFilterForm');
            bootstrap.Collapse.getOrCreateInstance(ccff).show();
        }
        
        const send = function (e) {
            select('.overlay').classList.add('d-block');
            const body = {
                'csrfmiddlewaretoken': csrfToken.value
            };

            let genus = select("input[name=genus]", true);
            body['genus'] = []
            genus.forEach((el) => {
                if (el.checked) {
                    body['genus'].push(el.value)
                }
            });

            let height_from = select("input[name=height_from]");
            if (height_from.value) body['height_from'] = height_from.value
            
            let width_from = select("input[name=width_from]");
            if (width_from.value) body['width_from'] = width_from.value
            
            let container = select("select[name=container]");
            if (container.value) body['container'] = container.value
            
            let rs = select("select[name=rs]");
            if (rs.value) body['rs'] = rs.value
            
            let shtamb = select("input[name=shtamb]");
            if (shtamb.checked) body['shtamb'] = 'on'
            
            let extra = select("input[name=extra]");
            if (extra.checked) body['extra'] = 'on'

            if (!height_from.classList.contains('is-invalid') && !width_from.classList.contains('is-invalid')) {
                xhr.open("POST", '/catalog/conifers/filter-form/', true);
                xhr.setRequestHeader("X-REQUESTED-WITH", "XMLHttpRequest");
                xhr.onreadystatechange = function () {
                    
                    if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
                        let res = JSON.parse(xhr.response)
                        if (Object.keys(res).length !== 0) {

                            if (res['genus'].length > 0 && e.target.name != 'genus') {
                                genus.forEach((el) => {
                                    el.disabled = false
                                    if (!res['genus'].includes(Number(el.value))) {
                                        el.disabled = 'disabled'
                                    }
                                });
                            }

                            if (res['height_from'] && e.target.name != 'height_from') {
                                numberField(height_from, res['height_from'])
                            }

                            if (res['width_from'] && e.target.name != 'width_from') {
                                numberField(width_from, res['width_from'])
                            }

                            if (res['container'] && e.target.name != 'container') {
                                selectField(container, res['container'])
                            }

                            if (res['rs'] && e.target.name != 'rs') {
                                selectField(rs, res['rs'])
                            }

                            if (e.target.name != 'shtamb') {
                                if (res['shtamb'])
                                    shtamb.disabled = false
                                else
                                    shtamb.disabled = 'disabled'
                            }

                            if (e.target.name != 'extra') {
                                if (res['extra'])
                                    extra.disabled = false
                                else
                                    extra.disabled = 'disabled'
                            }
                        }
                        select('.overlay').classList.remove('d-block');
                    }
                };
                xhr.send(new URLSearchParams(serialize(body)));
            } else{
                select('.overlay').classList.remove('d-block');
            }
        }

        inputNumberField = function (e) {
            let field = e.target
            if ((field.value >= Number(field.min) && field.value <= Number(field.max)) || field.value === '') {
                field.classList.remove('is-invalid');
                send(e)
            } else {
                field.classList.add('is-invalid');
            }
        };

        blurNumberField = function (e) {
            let field = e.target
            if (field.value < Number(field.min) || field.value > Number(field.max)) {
                field.value = ''
            }
            field.classList.remove('is-invalid');
        };

        on("click", "input[name=genus]", send, true);
        on("input", "input[name=height_from]", inputNumberField);
        on("input", "input[name=width_from]", inputNumberField);
        on("blur", "input[name=height_from]", blurNumberField);
        on("blur", "input[name=width_from]", blurNumberField);
        on("change", "select[name=container]", send);
        on("change", "select[name=rs]", send);
        on("click", "input[name=shtamb]", send);
        on("click", "input[name=extra]", send);

        document.addEventListener("DOMContentLoaded", function () {
            let e = new Event("load");
            Object.defineProperty(e, 'target', { writable: false, value: { name: "load" } });
            send(e)
        });
    }

})();
