// Signal that JS is available (used to gate reveal animations).
document.documentElement.classList.remove('no-js');

(function () {
  'use strict';

  /* ---- Theme toggle (light/dark, persisted) ---- */
  var themeBtn = document.getElementById('theme-toggle');

  function currentTheme() {
    var attr = document.documentElement.getAttribute('data-theme');
    if (attr) return attr;
    // Fall back to the system preference when nothing is set.
    return (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches)
      ? 'light' : 'dark';
  }

  function updateThemeIcon() {
    var icon = themeBtn && themeBtn.querySelector('.theme-toggle__icon');
    if (icon) icon.textContent = currentTheme() === 'light' ? '🌙' : '☀️';
  }

  if (themeBtn) {
    updateThemeIcon();
    themeBtn.addEventListener('click', function () {
      var next = currentTheme() === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      updateThemeIcon();
    });
  }

  /* ---- Hero role typing effect ---- */
  // EDIT: change/reorder the roles that cycle in the hero.
  var ROLES = ['AI/ML Engineer', 'Data Scientist', 'NLP Specialist', 'LLM Engineer'];
  var typedEl = document.getElementById('role-typed');
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (typedEl && !reduceMotion) {
    var roleIndex = 0, charIndex = ROLES[0].length, deleting = false;

    function tick() {
      var word = ROLES[roleIndex];
      charIndex += deleting ? -1 : 1;
      typedEl.textContent = word.slice(0, charIndex);

      var delay = deleting ? 45 : 90;
      if (!deleting && charIndex === word.length) {
        delay = 1600;            // pause on the full word
        deleting = true;
      } else if (deleting && charIndex === 0) {
        deleting = false;
        roleIndex = (roleIndex + 1) % ROLES.length;
        delay = 350;
      }
      setTimeout(tick, delay);
    }
    setTimeout(tick, 1600);      // start after showing the first role briefly
  }

  /* ---- Mobile nav toggle ---- */
  var toggle = document.querySelector('.nav__toggle');
  var menu = document.getElementById('nav-menu');

  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });

    // Close the menu after choosing a link (mobile).
    menu.addEventListener('click', function (e) {
      if (e.target.closest('.nav__link')) {
        menu.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---- Scroll-reveal via IntersectionObserver ---- */
  var revealEls = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    // Fallback: reveal everything immediately.
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---- Active nav link highlighting ---- */
  var sections = document.querySelectorAll('main section[id]');
  var navLinks = document.querySelectorAll('.nav__link');

  if ('IntersectionObserver' in window && sections.length) {
    var linkObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var id = entry.target.getAttribute('id');
          navLinks.forEach(function (link) {
            link.classList.toggle('is-active', link.getAttribute('href') === '#' + id);
          });
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });

    sections.forEach(function (section) { linkObserver.observe(section); });
  }

  /* ---- Contact form (submits to Formspree via AJAX) ---- */
  var form = document.getElementById('contact-form');
  var status = document.getElementById('form-status');

  if (form && status) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Not configured yet? Tell the user kindly instead of failing silently.
      if (form.action.indexOf('YOUR_FORM_ID') !== -1) {
        status.textContent = 'The contact form isn\'t connected yet. Please check back soon!';
        status.className = 'form-status is-error';
        return;
      }

      var btn = form.querySelector('button[type="submit"]');
      var original = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Sending…';
      status.textContent = '';
      status.className = 'form-status';

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      })
        .then(function (res) {
          if (res.ok) {
            status.textContent = 'Thanks! Your message has been sent. 🎉';
            status.className = 'form-status is-success';
            form.reset();
          } else {
            return res.json().then(function (data) {
              var msg = (data && data.errors)
                ? data.errors.map(function (x) { return x.message; }).join(', ')
                : 'Something went wrong. Please try again.';
              throw new Error(msg);
            });
          }
        })
        .catch(function (err) {
          status.textContent = err.message || 'Network error — please try again later.';
          status.className = 'form-status is-error';
        })
        .then(function () {
          btn.disabled = false;
          btn.textContent = original;
        });
    });
  }

  /* ---- Live GitHub projects feed ---- */
  // EDIT: change this to a different GitHub username to show someone else's repos.
  var GITHUB_USER = 'hyalamanchi';
  // EDIT: repo names to hide from the feed (e.g. coursework). Case-insensitive.
  var HIDE_REPOS = ['hds5210-2023', 'ORES'];
  var ghGrid = document.getElementById('gh-grid');
  var ghStatus = document.getElementById('gh-status');

  function ghPrettyName(name) {
    return name.replace(/[-_]+/g, ' ').replace(/\s+/g, ' ').trim()
      .replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  }

  function ghMonthYear(iso) {
    try {
      return new Date(iso).toLocaleDateString(undefined, { month: 'short', year: 'numeric' });
    } catch (e) { return ''; }
  }

  function ghMakeLink(href, text) {
    var a = document.createElement('a');
    a.href = href; a.target = '_blank'; a.rel = 'noopener'; a.className = 'link';
    a.textContent = text;
    return a;
  }

  function ghCard(repo) {
    var article = document.createElement('article');
    article.className = 'card reveal is-visible';

    var body = document.createElement('div');
    body.className = 'card__body';

    var title = document.createElement('h4');
    title.className = 'card__title';
    title.appendChild(ghMakeLink(repo.html_url, ghPrettyName(repo.name)));
    body.appendChild(title);

    var desc = document.createElement('p');
    desc.className = 'card__desc';
    if (repo.description) {
      desc.textContent = repo.description;
    } else {
      desc.className += ' card__desc--empty';
      desc.textContent = 'A ' + (repo.language || 'code') + ' project — details on GitHub.';
    }
    body.appendChild(desc);

    // Topic tags (add topics to your repos on GitHub to show them here)
    if (repo.topics && repo.topics.length) {
      var tags = document.createElement('ul');
      tags.className = 'tag-list tag-list--sm';
      repo.topics.slice(0, 4).forEach(function (t) {
        var li = document.createElement('li');
        li.className = 'tag';
        li.textContent = t;
        tags.appendChild(li);
      });
      body.appendChild(tags);
    }

    var meta = document.createElement('div');
    meta.className = 'repo-meta';
    if (repo.language) {
      var lang = document.createElement('span');
      lang.className = 'repo-lang';
      lang.textContent = repo.language;
      meta.appendChild(lang);
    }
    if (repo.stargazers_count > 0) {
      var stars = document.createElement('span');
      stars.textContent = '★ ' + repo.stargazers_count;
      meta.appendChild(stars);
    }
    var updated = document.createElement('span');
    updated.textContent = 'Updated ' + ghMonthYear(repo.pushed_at);
    meta.appendChild(updated);
    body.appendChild(meta);

    var links = document.createElement('div');
    links.className = 'card__links';
    links.appendChild(ghMakeLink(repo.html_url, 'View on GitHub ↗'));
    if (repo.homepage) links.appendChild(ghMakeLink(repo.homepage, 'Live ↗'));
    body.appendChild(links);

    article.appendChild(body);
    return article;
  }

  if (ghGrid && ghStatus) {
    fetch('https://api.github.com/users/' + GITHUB_USER + '/repos?sort=updated&per_page=100')
      .then(function (res) {
        if (!res.ok) throw new Error('GitHub API returned ' + res.status);
        return res.json();
      })
      .then(function (repos) {
        var hideSet = HIDE_REPOS.map(function (n) { return n.toLowerCase(); });
        var visible = repos
          .filter(function (r) {
            return !r.fork && !r.archived && hideSet.indexOf(r.name.toLowerCase()) === -1;
          })
          .sort(function (a, b) {
            // Repos with a description lead, then by stars, then most recent.
            return ((b.description ? 1 : 0) - (a.description ? 1 : 0)) ||
                   (b.stargazers_count - a.stargazers_count) ||
                   (new Date(b.pushed_at) - new Date(a.pushed_at));
          });

        if (!visible.length) {
          ghStatus.textContent = 'No public repositories to show yet.';
          return;
        }

        var frag = document.createDocumentFragment();
        visible.forEach(function (r) { frag.appendChild(ghCard(r)); });
        ghGrid.appendChild(frag);
        ghStatus.className = 'gh__status is-hidden';
      })
      .catch(function () {
        ghStatus.className = 'gh__status is-error';
        ghStatus.textContent = 'Couldn’t load live projects right now — ';
        ghStatus.appendChild(ghMakeLink('https://github.com/' + GITHUB_USER, 'visit my GitHub →'));
      });
  }

  /* ---- Footer year ---- */
  var yearEl = document.getElementById('year');
  if (yearEl) { yearEl.textContent = new Date().getFullYear(); }
})();
