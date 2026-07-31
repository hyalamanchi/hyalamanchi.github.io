/* ============================================================
   Tiny self-contained blog engine (no external dependencies)
   - Reads blog/posts.json for the post index
   - Renders the list, or a single post when ?p=<slug> is present
   - Includes a minimal, safe Markdown -> HTML renderer
   ============================================================ */
(function () {
  "use strict";

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function mdInline(s) {
    s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
    s = s.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img alt="$1" src="$2" loading="lazy">');
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/\*([^*]+)\*/g, "<em>$1</em>");
    return s;
  }

  function renderMarkdown(md) {
    md = md.replace(/^---[\s\S]*?---\s*/, ""); // strip frontmatter
    var lines = escapeHtml(md).split(/\r?\n/);
    var html = "", i = 0, inCode = false, listType = null;
    function closeList() { if (listType) { html += "</" + listType + ">"; listType = null; } }

    while (i < lines.length) {
      var line = lines[i];
      if (/^```/.test(line)) {
        if (!inCode) { closeList(); html += "<pre><code>"; inCode = true; }
        else { html += "</code></pre>"; inCode = false; }
        i++; continue;
      }
      if (inCode) { html += line + "\n"; i++; continue; }
      if (/^\s*$/.test(line)) { closeList(); i++; continue; }

      var h = line.match(/^(#{1,4})\s+(.*)$/);
      if (h) { closeList(); var lvl = h[1].length; html += "<h" + lvl + ">" + mdInline(h[2]) + "</h" + lvl + ">"; i++; continue; }
      if (/^>\s?/.test(line)) { closeList(); html += "<blockquote>" + mdInline(line.replace(/^>\s?/, "")) + "</blockquote>"; i++; continue; }
      if (/^(-|\*)\s+/.test(line)) { if (listType !== "ul") { closeList(); html += "<ul>"; listType = "ul"; } html += "<li>" + mdInline(line.replace(/^(-|\*)\s+/, "")) + "</li>"; i++; continue; }
      if (/^\d+\.\s+/.test(line)) { if (listType !== "ol") { closeList(); html += "<ol>"; listType = "ol"; } html += "<li>" + mdInline(line.replace(/^\d+\.\s+/, "")) + "</li>"; i++; continue; }
      if (/^(---|\*\*\*)\s*$/.test(line)) { closeList(); html += "<hr>"; i++; continue; }

      closeList(); html += "<p>" + mdInline(line) + "</p>"; i++;
    }
    closeList();
    if (inCode) html += "</code></pre>";
    return html;
  }

  function fmtDate(iso) {
    try { return new Date(iso + "T00:00:00").toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" }); }
    catch (e) { return iso; }
  }

  function tagChips(tags) {
    if (!tags || !tags.length) return "";
    return '<ul class="tag-list tag-list--sm">' +
      tags.map(function (t) { return '<li class="tag">' + escapeHtml(t) + "</li>"; }).join("") + "</ul>";
  }

  function getParam(name) {
    return new URLSearchParams(window.location.search).get(name);
  }

  var CAT_ICON = {
    "Roadmap": "🧭",
    "Document AI": "📄",
    "Finance & Fintech": "💰",
    "Healthcare AI": "🏥",
    "Security & MLOps": "🔒",
    "Career & Craft": "🎯",
    "DevOps & Monitoring": "🔔"
  };
  function catGlyph(cat) { return CAT_ICON[cat] || "📝"; }

  function blogCard(p, featured) {
    var hasCover = !!p.cover;
    var coverStyle = hasCover ? ' style="background-image:url(' + encodeURI(p.cover) + ')"' : "";
    var placeholder = hasCover ? "" : " blog-card__media--placeholder";
    var glyph = hasCover ? "" : '<span class="blog-card__glyph" aria-hidden="true">' + catGlyph(p.category) + "</span>";
    var cat = p.category ? '<span class="blog-card__cat">✎ ' + escapeHtml(p.category) + "</span>" : "";
    return '<article class="blog-card' + (featured ? " blog-card--wide" : "") + '" data-cat="' + escapeHtml(p.category || "") + '">' +
      '<a class="blog-card__link" href="blog.html?p=' + encodeURIComponent(p.slug) + '">' +
        '<div class="blog-card__media' + placeholder + '"' + coverStyle + ">" + glyph + cat + "</div>" +
        '<div class="blog-card__body">' +
          '<span class="blog-card__date">' + fmtDate(p.date) + (p.readMinutes ? " · " + p.readMinutes + " min" : "") + "</span>" +
          '<h3 class="blog-card__title">' + escapeHtml(p.title) + "</h3>" +
          '<p class="blog-card__excerpt">' + escapeHtml(p.summary || "") + "</p>" +
        "</div>" +
      "</a></article>";
  }

  var listEl = document.getElementById("post-list");
  var postEl = document.getElementById("post-view");
  if (!listEl && !postEl) return;

  fetch("blog/posts.json")
    .then(function (r) { if (!r.ok) throw new Error("posts.json " + r.status); return r.json(); })
    .then(function (posts) {
      posts.sort(function (a, b) { return a.date < b.date ? 1 : -1; }); // newest first
      var slug = getParam("p");

      if (slug && postEl) {
        var post = posts.filter(function (p) { return p.slug === slug; })[0];
        if (!post) { postEl.innerHTML = "<p>Post not found. <a class='link' href='blog.html'>Back to all posts</a></p>"; return; }
        document.title = post.title + " — Hemalatha Yalamanchi";
        if (listEl) listEl.style.display = "none";
        fetch("blog/posts/" + post.slug + ".md")
          .then(function (r) { if (!r.ok) throw new Error("md " + r.status); return r.text(); })
          .then(function (md) {
            postEl.innerHTML =
              '<a class="link post__back" href="blog.html">← All posts</a>' +
              '<p class="post__meta">' + fmtDate(post.date) +
                (post.readMinutes ? " · " + post.readMinutes + " min read" : "") + "</p>" +
              "<h1 class=\"post__title\">" + escapeHtml(post.title) + "</h1>" +
              tagChips(post.tags) +
              '<div class="post__body">' + renderMarkdown(md) + "</div>" +
              '<a class="link post__back" href="blog.html">← All posts</a>';
          })
          .catch(function () { postEl.innerHTML = "<p>Couldn't load this post.</p>"; });
        return;
      }

      // List view — filter pills + featured card + card grid
      if (listEl) {
        if (postEl) postEl.style.display = "none";
        if (!posts.length) { listEl.innerHTML = "<p class='section__lead'>No posts yet — check back soon!</p>"; return; }

        var cats = [];
        posts.forEach(function (p) { if (p.category && cats.indexOf(p.category) === -1) cats.push(p.category); });

        var pills = '<button class="blog-filter is-active" data-filter="all">All</button>' +
          cats.map(function (c) {
            return '<button class="blog-filter" data-filter="' + escapeHtml(c) + '">' + escapeHtml(c) + "</button>";
          }).join("");

        var cards = posts.map(function (p, idx) { return blogCard(p, idx === 0); }).join("");

        listEl.innerHTML =
          '<div class="blog-filters" id="blog-filters">' + pills + "</div>" +
          '<div class="blog-bento" id="blog-bento">' + cards + "</div>";

        // Filter behaviour
        var filterBtns = listEl.querySelectorAll(".blog-filter");
        var allCards = listEl.querySelectorAll(".blog-card");
        filterBtns.forEach(function (btn) {
          btn.addEventListener("click", function () {
            var f = btn.getAttribute("data-filter");
            filterBtns.forEach(function (b) { b.classList.toggle("is-active", b === btn); });
            allCards.forEach(function (c) {
              c.style.display = (f === "all" || c.getAttribute("data-cat") === f) ? "" : "none";
            });
          });
        });
      }
    })
    .catch(function () {
      var target = postEl || listEl;
      if (target) target.innerHTML = "<p>Couldn't load the blog right now.</p>";
    });
})();
