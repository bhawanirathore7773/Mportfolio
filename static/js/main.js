(function () {
  "use strict";

  /* Sticky header shadow/border once the page scrolls */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Mobile nav toggle */
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
      document.body.style.overflow = isOpen ? "hidden" : "";
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      });
    });
  }

  /* ------------------------------------------------------------------
     Lightbox — built from [data-lightbox-group] images on the page.
     Works from any project image gallery without extra markup per page.
  ------------------------------------------------------------------ */
  var galleryImages = Array.prototype.slice.call(document.querySelectorAll("[data-lightbox-group] [data-lightbox-item]"));
  if (galleryImages.length) {
    var overlay = document.createElement("div");
    overlay.className = "lightbox";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.innerHTML =
      '<button class="lightbox-close" aria-label="Close">&times;</button>' +
      '<button class="lightbox-prev" aria-label="Previous image">&#8249;</button>' +
      '<img alt="" />' +
      '<button class="lightbox-next" aria-label="Next image">&#8250;</button>' +
      '<div class="lightbox-counter"></div>';
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

    function open(index) {
      show(index);
      overlay.classList.add("is-open");
      document.body.style.overflow = "hidden";
    }

    function close() {
      overlay.classList.remove("is-open");
      document.body.style.overflow = "";
    }

    galleryImages.forEach(function (img, index) {
      img.style.cursor = "zoom-in";
      img.addEventListener("click", function () { open(index); });
    });

    overlay.querySelector(".lightbox-close").addEventListener("click", close);
    overlay.querySelector(".lightbox-prev").addEventListener("click", function () { show(currentIndex - 1); });
    overlay.querySelector(".lightbox-next").addEventListener("click", function () { show(currentIndex + 1); });
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) close();
    });

    document.addEventListener("keydown", function (event) {
      if (!overlay.classList.contains("is-open")) return;
      if (event.key === "Escape") close();
      if (event.key === "ArrowLeft") show(currentIndex - 1);
      if (event.key === "ArrowRight") show(currentIndex + 1);
    });

    overlay.addEventListener("touchstart", function (event) {
      touchStartX = event.changedTouches[0].clientX;
    }, { passive: true });
    overlay.addEventListener("touchend", function (event) {
      if (touchStartX === null) return;
      var delta = event.changedTouches[0].clientX - touchStartX;
      if (Math.abs(delta) > 40) show(currentIndex + (delta < 0 ? 1 : -1));
      touchStartX = null;
    }, { passive: true });
  }
})();
