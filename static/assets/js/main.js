function setLocation(url) {
  window.location.href = url;
}

const popoverTriggerList = document.querySelectorAll(
  '[data-bs-toggle="popover"]'
);

const popoverList = [...popoverTriggerList].map(
  (popoverTriggerEl) =>
    new bootstrap.Popover(popoverTriggerEl, { html: true })
);

const alertList = document.querySelectorAll('.alert')
const alerts = [...alertList].map(element => new bootstrap.Alert(element))

let xhr = new XMLHttpRequest();

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

  /**
   * Easy on scroll event listener
   */
  const onscroll = (el, listener) => {
    el.addEventListener("scroll", listener);
  };

  /**
   * Mobile nav toggle
   */
  on("click", ".mobile-nav-toggle", function (e) {
    select("#navbar").classList.toggle("navbar-mobile");
    this.classList.toggle("bi-list");
    this.classList.toggle("bi-x");
  });

  /**
   * Mobile nav dropdowns activate
   */
  on(
    "click",
    ".navbar .dropdown > a",
    function (e) {
      if (select("#navbar").classList.contains("navbar-mobile")) {
        e.preventDefault();
        this.nextElementSibling.classList.toggle("dropdown-active");
      }
    },
    true
  );

  /**
   * Initiate portfolio lightbox
   */
  const lightbox = GLightbox({
    selector: ".glightbox",
  });

  /**
   * Back to top button
   */
  let backtotop = select(".back-to-top");
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add("active");
      } else {
        backtotop.classList.remove("active");
      }
    };
    window.addEventListener("load", toggleBacktotop);
    onscroll(document, toggleBacktotop);
  }

  /**
   * Animation on scroll
   */
  // AOS.init({
  //   duration: 1000,
  //   easing: "ease-in-out",
  //   once: true,
  //   mirror: false,
  // });

  on("click", "#favorites", function (e) {
    e.preventDefault();
    // let url = `/favorites/?ct_id=${this.dataset.ctId}&id=${this.dataset.id}`;

    params = {
      'ct_id': this.dataset.ctId,
      'id': this.dataset.id
    };

    xhr.open("GET", `/favorites/?${new URLSearchParams(params)}`, true);
    xhr.setRequestHeader("X-REQUESTED-WITH", "XMLHttpRequest");
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status == 200) {
        let i = document.querySelector("#favorites > i");
        if (xhr["state"] == true) {
          i.classList.toggle("fas");
          i.classList.toggle("far");
        } else {
          i.classList.toggle("fas");
          i.classList.toggle("far");
        }
      }
    };
    xhr.send();
  });


  on("click", "#addToCart", function (e) {
    e.preventDefault();
    self = this;

    let productPrice = select("input[name=productPrice]:checked", false);
    let csrfToken = select("input[name=csrfmiddlewaretoken]", false);

    body = {
      'ct_id': productPrice.dataset.ctId,
      'id': productPrice.dataset.id,
      'csrfmiddlewaretoken': csrfToken.value
    };

    xhr.open("POST", `${this.value}`, true);
    xhr.setRequestHeader("X-REQUESTED-WITH", "XMLHttpRequest");
    // xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
      if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        // self.classList.remove("btn-primary")
        self.innerHTML = 'Добавлен в корзину'
        self.disabled = true;
        setTimeout(function () {
          // self.classList.add("btn-primary")
          
          self.innerHTML = 'Добавить в корзину'
          self.disabled = false;
          shake(response['cart']);
        },
          1000);
      }
    };
    xhr.send(new URLSearchParams(body));
  });

  //--

  const shake = function (cart=null) {
    if (typeof cart === 'object' && ('total_quantity' in cart)){
      const cpq = select("#cartProductQuantity > span", false)
      console.log(cart.total_quantity)
      cpq.innerHTML = cart.total_quantity
    }
 
    const i = select("#cartProductQuantity > i", false);
    i.classList.toggle("shake");
  }

  //--

  const onEL = function () {
    on("click", "#cartContainer button.increment", increment, true);
    on("click", "#cartContainer button.decrement", decrement, true);
    on("click", "#cartContainer button.remove", remove, true);
  }

  //--

  const remove = function (e) {
    e.preventDefault();
    let parent = e.target.closest('div')
    let csrfToken = parent.querySelector('input[name=csrfmiddlewaretoken]')
    let button = parent.querySelector('.remove')

    body = {
      'ci_id': button.dataset.ciId,
      'csrfmiddlewaretoken': csrfToken.value
    };

    xhr.open("POST", `${button.value}`, true);
    xhr.setRequestHeader("X-REQUESTED-WITH", "XMLHttpRequest");
    xhr.onreadystatechange = function () {
      if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
        let html = select("#cartContainer", false)
        let response = JSON.parse(xhr.response)
        html.innerHTML = response['template'];
        onEL();
        shake(response['cart']);
      }
    };
    xhr.send(new URLSearchParams(body));
  }

  on("click", "#cartContainer button.remove", remove, true);

  //--

  const update = function (e, operation) {
    e.preventDefault();
    let parent = e.target.closest('div')
    // let input = parent.querySelector('input[name=quantity]')
    let csrfToken = parent.querySelector('input[name=csrfmiddlewaretoken]')
    let button = parent.querySelector(`.${operation}`)
    // let value = parseInt(input.value);

    // if (!isNaN(value)) {
    //   if (operation === 'increment') {
    //     value += 1;
    //   } else {
    //     if (value > 1) {
    //       value -= 1;
    //     }
    //   }
    //   input.value = value;
    // } else {
    //   input.value = 1;
    // }

    body = {
      'ci_id': button.dataset.ciId,
      'value': button.dataset.value,
      'csrfmiddlewaretoken': csrfToken.value,
    };

    xhr.open("POST", `${button.value}`, true);
    xhr.setRequestHeader("X-REQUESTED-WITH", "XMLHttpRequest");
    xhr.onreadystatechange = function () {
      if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
        let html = select("#cartContainer", false)
        let response = JSON.parse(xhr.response)
        html.innerHTML = response['template'];
        onEL();
        shake(response['cart']);
      }
    };
    xhr.send(new URLSearchParams(body));
  }


  const increment = function (e) {
    update(e, 'increment');
  }

  on("click", "#cartContainer button.increment", increment, true);

  const decrement = function (e) {
    update(e, 'decrement');
  }

  on("click", "#cartContainer button.decrement", decrement, true);

})();
