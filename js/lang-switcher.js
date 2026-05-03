/**
 * Re Hong — language / locale switcher (path-based i18n).
 *
 * Conventions for new pages:
 * - English (default): /page.html or / for home
 * - Other locales: /<locale>/page.html or /<locale>/ for home
 * - Locales: zh-TW (Traditional Chinese), ja, ko, es
 * - Add the new page under each locale folder with the same filename
 * - Register hreflang alternates on every language variant
 * - Mirror nav links with the correct locale prefix
 */
(function () {
  var LOCALES = [
    { id: "en", prefix: "", label: "English", htmlLang: "en" },
    { id: "zh-TW", prefix: "/zh-TW", label: "繁體中文", htmlLang: "zh-TW" },
    { id: "ja", prefix: "/ja", label: "日本語", htmlLang: "ja" },
    { id: "ko", prefix: "/ko", label: "한국어", htmlLang: "ko" },
    { id: "es", prefix: "/es", label: "Español", htmlLang: "es" },
  ];

  var LOCALE_PREFIX_RE = /^\/(zh-TW|ja|ko|es)(?=\/|$)/;

  function findLocaleByPrefix(prefix) {
    for (var i = 0; i < LOCALES.length; i++) {
      if (LOCALES[i].prefix === prefix) return LOCALES[i];
    }
    return LOCALES[0];
  }

  function currentLocale() {
    var path = window.location.pathname;
    var m = path.match(LOCALE_PREFIX_RE);
    if (!m) return LOCALES[0];
    return findLocaleByPrefix("/" + m[1]) || LOCALES[0];
  }

  function stripLocalePrefix(pathname) {
    return pathname.replace(LOCALE_PREFIX_RE, "") || "/";
  }

  function logicalPage() {
    var tail = stripLocalePrefix(window.location.pathname);
    if (tail === "/" || tail === "/index.html") return "index";
    if (tail === "/careers.html") return "careers";
    if (tail === "/quality.html") return "quality";
    return "index";
  }

  function buildUrl(locale) {
    var page = logicalPage();
    var p = locale.prefix || "";
    if (page === "index") {
      if (!p) return "/";
      return p + "/";
    }
    return p + "/" + page + ".html";
  }

  function initSwitcher() {
    var roots = document.querySelectorAll("[data-lang-switcher]");
    if (!roots.length) return;

    var active = currentLocale();

    roots.forEach(function (root) {
      var btn = root.querySelector(".lang-toggle");
      var menu = root.querySelector(".lang-menu");
      if (!btn || !menu) return;

      var labelSpan = btn.querySelector(".lang-toggle__label");
      if (labelSpan) labelSpan.textContent = active.label;
      btn.setAttribute("aria-label", "Language: " + active.label);

      menu.innerHTML = "";
      LOCALES.forEach(function (loc) {
        var li = document.createElement("li");
        li.setAttribute("role", "none");
        var a = document.createElement("a");
        a.setAttribute("role", "menuitem");
        a.href = buildUrl(loc);
        a.textContent = loc.label;
        if (loc.id === active.id) {
          a.setAttribute("aria-current", "true");
        }
        li.appendChild(a);
        menu.appendChild(li);
      });

      function closeMenu() {
        menu.hidden = true;
        btn.setAttribute("aria-expanded", "false");
      }

      function openMenu() {
        menu.hidden = false;
        btn.setAttribute("aria-expanded", "true");
      }

      function toggleMenu() {
        if (menu.hidden) openMenu();
        else closeMenu();
      }

      btn.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleMenu();
      });

      menu.addEventListener("click", function (e) {
        if (e.target.closest("a")) closeMenu();
      });

      document.addEventListener("click", function (e) {
        if (!root.contains(e.target)) closeMenu();
      });

      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") closeMenu();
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSwitcher);
  } else {
    initSwitcher();
  }
})();
