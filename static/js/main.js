(function () {
  "use strict";

  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      if (!header.classList.contains("menu-open")) {
        header.classList.toggle("is-scrolled", window.scrollY > 8);
      }
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".main-nav");
  var mobileQuery = window.matchMedia("(max-width: 860px)");

  if (toggle && nav) {
    var closeMenu = function () {
      nav.classList.remove("is-open");
      if (header) header.classList.remove("menu-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open menu");
      document.documentElement.classList.remove("menu-open");
      document.body.classList.remove("menu-open");
      document.body.style.overflow = "";
    };

    var openMenu = function () {
      if (!mobileQuery.matches) return;
      nav.classList.add("is-open");
      if (header) header.classList.add("menu-open");
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Close menu");
      document.documentElement.classList.add("menu-open");
      document.body.classList.add("menu-open");
      document.body.style.overflow = "hidden";
    };

    toggle.addEventListener("click", function (event) {
      event.preventDefault();
      if (nav.classList.contains("is-open")) closeMenu();
      else openMenu();
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeMenu);
      link.addEventListener("touchend", closeMenu, { passive: true });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        closeMenu();
        toggle.focus();
      }
    });

    var handleOutside = function (event) {
      if (!nav.classList.contains("is-open")) return;
      var target = event.target;
      if (target && target.closest && (target.closest(".main-nav") || target.closest(".menu-toggle"))) return;
      closeMenu();
    };

    document.addEventListener("click", handleOutside);
    document.addEventListener("touchend", handleOutside, { passive: true });

    var resetDesktop = function (event) {
      if (!event.matches) closeMenu();
    };
    if (mobileQuery.addEventListener) mobileQuery.addEventListener("change", resetDesktop);
    else mobileQuery.addListener(resetDesktop);
  }

  var galleryImages = Array.prototype.slice.call(document.querySelectorAll("[data-lightbox-group] [data-lightbox-item]"));
  if (galleryImages.length) {
    var overlay = document.createElement("div");
    overlay.className = "lightbox";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.innerHTML = '<button class="lightbox-close" aria-label="Close">&times;</button><button class="lightbox-prev" aria-label="Previous image">&#8249;</button><img alt="" /><button class="lightbox-next" aria-label="Next image">&#8250;</button><div class="lightbox-counter"></div>';
    document.body.appendChild(overlay);
    var imgEl = overlay.querySelector("img");
    var counterEl = overlay.querySelector(".lightbox-counter");
    var currentIndex = 0;
    var touchStartX = null;

    function show(index) {
      currentIndex = (index + galleryImages.length) % galleryImages.length;
      var target = galleryImages[currentIndex];
      imgEl.src = target.getAttribute("data-full") || target.src;
      imgEl.alt = target.alt || "";
      counterEl.textContent = (currentIndex + 1) + " / " + galleryImages.length;
    }
    function open(index) { show(index); overlay.classList.add("is-open"); document.body.style.overflow = "hidden"; }
    function close() { overlay.classList.remove("is-open"); document.body.style.overflow = ""; }
    galleryImages.forEach(function (img, index) { img.style.cursor = "zoom-in"; img.addEventListener("click", function () { open(index); }); });
    overlay.querySelector(".lightbox-close").addEventListener("click", close);
    overlay.querySelector(".lightbox-prev").addEventListener("click", function () { show(currentIndex - 1); });
    overlay.querySelector(".lightbox-next").addEventListener("click", function () { show(currentIndex + 1); });
    overlay.addEventListener("click", function (event) { if (event.target === overlay) close(); });
    document.addEventListener("keydown", function (event) {
      if (!overlay.classList.contains("is-open")) return;
      if (event.key === "Escape") close();
      if (event.key === "ArrowLeft") show(currentIndex - 1);
      if (event.key === "ArrowRight") show(currentIndex + 1);
    });
    overlay.addEventListener("touchstart", function (event) { touchStartX = event.changedTouches[0].clientX; }, { passive: true });
    overlay.addEventListener("touchend", function (event) {
      if (touchStartX === null) return;
      var delta = event.changedTouches[0].clientX - touchStartX;
      if (Math.abs(delta) > 40) show(currentIndex + (delta < 0 ? 1 : -1));
      touchStartX = null;
    }, { passive: true });
  }
})();
