"""
whatsthepoint.to — Post Manager
Streamlit app to create, edit, preview and publish blog posts.
Run with: streamlit run app.py
"""

import streamlit as st
import os, json, re
from pathlib import Path
from datetime import date, datetime

# ── Config ──────────────────────────────────────────────────────────────────
SITE_ROOT   = Path(__file__).parent.parent
POSTS_DIR   = SITE_ROOT / "posts"
INDEX_FILE  = SITE_ROOT / "index.html"
BLOG_FILE   = SITE_ROOT / "blog.html"
POST_TMPL   = SITE_ROOT / "post.html"
META_FILE   = POSTS_DIR / "_posts.json"

POSTS_DIR.mkdir(exist_ok=True)

TAGS = ["AI Strategy", "Enterprise ML", "Leadership", "Ethics & Risk", "Governance", "Org Design"]
TAG_CLASSES = {
    "AI Strategy":   "tag",
    "Enterprise ML": "tag tag--outline",
    "Leadership":    "tag tag--navy",
    "Ethics & Risk": "tag tag--outline",
    "Governance":    "tag tag--outline",
    "Org Design":    "tag",
}
GTAG = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-B9XYVRJE07"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-B9XYVRJE07');
  </script>"""

# ── Helpers ──────────────────────────────────────────────────────────────────
def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[\s_]+', '-', text)[:60]

def load_meta():
    if META_FILE.exists():
        return json.loads(META_FILE.read_text())
    return []

def save_meta(posts):
    META_FILE.write_text(json.dumps(posts, indent=2, default=str))

def reading_time(body_html):
    words = len(re.sub('<[^>]+>', '', body_html).split())
    mins  = max(1, round(words / 200))
    return f"{mins} min read"

def format_date(d):
    if isinstance(d, str):
        d = datetime.strptime(d, "%Y-%m-%d").date()
    return d.strftime("%-d %b %Y")

def render_post_html(slug, title, standfirst, tag, pub_date, body_html, read_time):
    tag_class = TAG_CLASSES.get(tag, "tag")
    tag_slug  = slugify(tag)
    date_str  = format_date(pub_date) if pub_date else ""
    url_path  = f"posts/{slug}.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — What's The Point.</title>
  <meta name="description" content="{standfirst[:160]}" />
  <link rel="canonical" href="https://whatsthepoint.to/{url_path}" />
  <link rel="stylesheet" href="../css/style.css" />
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%230a0a0a'/><text x='16' y='22' font-size='18' text-anchor='middle' fill='%23d4380d' font-family='serif' font-weight='900'>?</text></svg>" />
{GTAG}
  <style>
    .post-hero {{background:var(--ink);color:var(--paper);padding:5rem 2rem 4rem;}}
    .post-hero__inner {{max-width:800px;margin:0 auto;}}
    .post-hero__tags {{display:flex;gap:0.5rem;margin-bottom:1.5rem;}}
    .post-hero h1 {{font-size:clamp(2rem,5vw,3.8rem);line-height:1.05;letter-spacing:-0.03em;margin-bottom:1.5rem;}}
    .post-hero .standfirst {{font-size:1.2rem;color:#bbb;line-height:1.65;max-width:58ch;}}
    .post-meta-bar {{background:var(--cream);border-bottom:2px solid var(--ink);padding:1rem 2rem;}}
    .post-meta-bar__inner {{max-width:800px;margin:0 auto;display:flex;gap:2rem;align-items:center;font-family:var(--font-mono);font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);flex-wrap:wrap;}}
    .post-body {{max-width:800px;margin:4rem auto;padding:0 2rem;}}
    .share-bar {{padding:1.5rem 0;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);display:flex;gap:1rem;align-items:center;font-family:var(--font-mono);font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);flex-wrap:wrap;}}
    .share-btn {{display:inline-flex;align-items:center;gap:0.45rem;padding:0.45rem 0.9rem;font-family:var(--font-mono);font-size:0.63rem;text-transform:uppercase;letter-spacing:0.1em;text-decoration:none;border:1px solid currentColor;transition:all 0.15s;cursor:pointer;background:transparent;}}
    .share-btn--linkedin {{color:#0077b5;border-color:#0077b5;}}
    .share-btn--linkedin:hover {{background:#0077b5;color:#fff;}}
    .share-btn--twitter {{color:#000;border-color:#000;}}
    .share-btn--twitter:hover {{background:#000;color:#fff;}}
    .share-btn--pdf {{color:var(--accent);border-color:var(--accent);}}
    .share-btn--pdf:hover {{background:var(--accent);color:#fff;}}
    .progress-bar {{position:fixed;top:0;left:0;height:3px;background:var(--accent);z-index:999;transition:width 0.1s;width:0%;}}
    @media print {{
      .masthead,.date-banner,.progress-bar,.share-bar,footer,#site-footer {{display:none!important;}}
      body {{background:#fff;}}
      .post-hero {{background:#0a0a0a!important;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
      .post-body {{margin:2rem auto;}}
      .pdf-watermark {{display:block!important;position:fixed;bottom:1.5cm;right:1.5cm;font-family:'IBM Plex Mono',monospace;font-size:8pt;color:#ccc;text-align:right;}}
    }}
    .pdf-watermark {{display:none;}}
  </style>
</head>
<body>
<div class="progress-bar" id="progress"></div>
<div class="pdf-watermark">whatsthepoint.to · Anshul Aggarwal</div>
<div id="site-header"></div>

<section class="post-hero">
  <div class="post-hero__inner">
    <div class="post-hero__tags"><span class="{tag_class}">{tag}</span></div>
    <h1 id="post-title">{title}</h1>
    <p class="standfirst">{standfirst}</p>
  </div>
</section>

<div class="post-meta-bar">
  <div class="post-meta-bar__inner">
    <span>{date_str}</span>
    <span>·</span>
    <span>{read_time}</span>
    <span>·</span>
    <span>By <a href="../about.html" style="color:var(--accent);">Anshul Aggarwal</a></span>
  </div>
</div>

<article class="post-body article-body reveal">
{body_html}

  <div class="share-bar">
    <span>Share:</span>
    <a class="share-btn share-btn--linkedin" id="share-linkedin" href="#" target="_blank" rel="noopener">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
      Share on LinkedIn
    </a>
    <a class="share-btn share-btn--twitter" id="share-twitter" href="#" target="_blank" rel="noopener">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.737-8.835L1.254 2.25H8.08l4.259 5.631 5.905-5.631zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
      Share on X
    </a>
    <button class="share-btn share-btn--pdf" onclick="window.print()">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><polyline points="9 15 12 18 15 15"/></svg>
      Download PDF
    </button>
  </div>
</article>

<section style="background:var(--cream);padding:4rem 2rem;margin-top:4rem;border-top:2px solid var(--ink);">
  <div style="max-width:var(--max-w);margin:0 auto;">
    <h3 style="font-size:1.6rem;margin-bottom:1rem;padding-bottom:1rem;border-bottom:2px solid var(--ink);">More Essays</h3>
    <a href="../blog.html" style="font-family:var(--font-mono);font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--accent);">Browse all posts →</a>
  </div>
</section>

<div id="site-footer"></div>
<script src="../js/shared.js"></script>
<script src="../js/main.js"></script>
<script>
  const bar = document.getElementById('progress');
  window.addEventListener('scroll', () => {{
    const dh = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (dh > 0 ? (window.scrollY / dh) * 100 : 0) + '%';
  }});
  document.addEventListener('DOMContentLoaded', () => {{
    const url   = encodeURIComponent(window.location.href);
    const title = encodeURIComponent(document.getElementById('post-title')?.textContent || document.title);
    document.getElementById('share-linkedin').href =
      'https://www.linkedin.com/sharing/share-offsite/?url=' + url;
    document.getElementById('share-twitter').href =
      'https://twitter.com/intent/tweet?url=' + url + '&text=' + title;
  }});
</script>
</body>
</html>"""

def build_post_card_list_item(p):
    """HTML for one post in blog.html archive list."""
    tag_class = TAG_CLASSES.get(p['tag'], 'tag')
    return f"""
      <a class="archive-post-item" href="posts/{p['slug']}.html" data-tags="{slugify(p['tag'])}">
        <div class="archive-post-item__date">{format_date(p['date'])}</div>
        <div>
          <span class="{tag_class}" style="margin-bottom:0.5rem;display:inline-block;">{p['tag']}</span>
          <h3>{p['title']}</h3>
          <p class="excerpt">{p['standfirst'][:180]}{'…' if len(p['standfirst']) > 180 else ''}</p>
          <div style="font-family:var(--font-mono);font-size:0.63rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);">
            <span>{p['read_time']}</span>
          </div>
        </div>
      </a>"""

def build_post_card_featured(p):
    """HTML for a featured card on index.html."""
    tag_class = TAG_CLASSES.get(p['tag'], 'tag')
    return f"""
    <article class="post-card">
      <div class="post-card__number">
        <span class="{tag_class}">{p['tag']}</span>
        <span>{format_date(p['date'])}</span>
      </div>
      <h3><a href="posts/{p['slug']}.html">{p['title']}</a></h3>
      <p class="excerpt">{p['standfirst'][:160]}{'…' if len(p['standfirst']) > 160 else ''}</p>
      <div class="post-card__footer">
        <span>{format_date(p['date'])}</span>
        <span>{p['read_time']}</span>
      </div>
    </article>"""

def rebuild_index(posts):
    published = [p for p in posts if p.get('published')]
    published.sort(key=lambda x: x['date'], reverse=True)
    recent = published[:6]

    if not recent:
        grid_html = """<div class="posts-grid--list" style="border:2px solid var(--ink);">
    <p style="padding:3rem 2rem;font-family:var(--font-mono);font-size:0.85rem;color:var(--muted);text-align:center;letter-spacing:0.05em;">
      No posts yet — check back soon.
    </p>
  </div>"""
    else:
        featured = recent[:3]
        rest     = recent[3:]
        featured_html = '\n'.join(build_post_card_featured(p) for p in featured)
        list_html     = '\n'.join(f"""
      <article class="post-card post-card--list" data-tags="{slugify(p['tag'])}">
        <div class="post-date">{format_date(p['date'])[:6]}</div>
        <div>
          <span class="{TAG_CLASSES.get(p['tag'],'tag')}">{p['tag']}</span>
          <h3><a href="posts/{p['slug']}.html">{p['title']}</a></h3>
          <p class="excerpt">{p['standfirst'][:140]}…</p>
        </div>
        <span class="read-time">{p['read_time']}</span>
      </article>""" for p in rest) if rest else ''
        grid_html = f"""<div class="posts-grid--featured">{featured_html}</div>
  {'<div class="posts-grid--list">' + list_html + '</div>' if list_html else ''}"""

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>What's The Point. — AI Strategy & Consulting Insights by Anshul Aggarwal</title>
  <meta name="description" content="Direct, honest writing on AI strategy, enterprise transformation, and the things that actually matter." />
  <link rel="canonical" href="https://whatsthepoint.to/" />
  <link rel="stylesheet" href="css/style.css" />
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%230a0a0a'/><text x='16' y='22' font-size='18' text-anchor='middle' fill='%23d4380d' font-family='serif' font-weight='900'>?</text></svg>" />
{GTAG}
</head>
<body>
<div id="site-header"></div>
<section class="hero">
  <div class="hero__inner">
    <div class="hero__copy">
      <p class="hero__label">AI Consulting Perspectives · Anshul Aggarwal</p>
      <h1 class="hero__title">Sharp takes<br>on <em>AI</em> that<br>actually matter.</h1>
      <p class="hero__subtitle">No hype cycles. No breathless predictions. Just honest, experienced thinking on how organisations can navigate AI — written by someone who's in the room when the hard decisions get made.</p>
    </div>
  </div>
</section>
<div class="section-header reveal">
  <div class="section-header__inner">
    <h2>Essays</h2>
    <a href="blog.html" class="view-all">All posts →</a>
  </div>
</div>
<div class="posts-grid reveal">
  {grid_html}
</div>
<div id="site-footer"></div>
<script src="js/shared.js"></script>
<script src="js/main.js"></script>
</body>
</html>"""
    INDEX_FILE.write_text(content)

def rebuild_blog(posts):
    published = [p for p in posts if p.get('published')]
    published.sort(key=lambda x: x['date'], reverse=True)

    if not published:
        list_html = '<p style="padding:3rem 0;font-family:var(--font-mono);font-size:0.85rem;color:var(--muted);letter-spacing:0.05em;">No posts yet — check back soon.</p>'
    else:
        list_html = '\n'.join(build_post_card_list_item(p) for p in published)

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>All Essays — What's The Point.</title>
  <meta name="description" content="Every essay on AI strategy, enterprise ML, leadership, and consulting reality by Anshul Aggarwal." />
  <link rel="canonical" href="https://whatsthepoint.to/blog.html" />
  <link rel="stylesheet" href="css/style.css" />
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%230a0a0a'/><text x='16' y='22' font-size='18' text-anchor='middle' fill='%23d4380d' font-family='serif' font-weight='900'>?</text></svg>" />
{GTAG}
</head>
<body>
<div id="site-header"></div>
<section class="page-hero">
  <div class="page-hero__inner">
    <p class="page-hero__label">Archive</p>
    <h1>All <em>Essays.</em></h1>
  </div>
</section>
<div class="archive-layout">
  <main>
    <div class="archive-filters">
      <button class="filter-btn active" data-tag="all">All</button>
      <button class="filter-btn" data-tag="ai-strategy">AI Strategy</button>
      <button class="filter-btn" data-tag="enterprise-ml">Enterprise ML</button>
      <button class="filter-btn" data-tag="leadership">Leadership</button>
      <button class="filter-btn" data-tag="ethics-risk">Ethics &amp; Risk</button>
    </div>
    <div class="archive-post-list">
      {list_html}
    </div>
  </main>
  <aside class="archive-sidebar">
    <div class="sidebar-block">
      <h4>Topics</h4>
      <div class="tag-cloud">
        <span class="tag">AI Strategy</span>
        <span class="tag tag--navy">Leadership</span>
        <span class="tag tag--outline">Enterprise ML</span>
        <span class="tag tag--outline">Ethics &amp; Risk</span>
        <span class="tag tag--outline">Governance</span>
        <span class="tag">Org Design</span>
      </div>
    </div>
    <div class="sidebar-block">
      <h4>About the Author</h4>
      <p style="font-size:0.88rem;color:var(--muted);line-height:1.6;margin-bottom:1rem;">
        Anshul Aggarwal — AI consulting manager writing what the industry needs to hear, not what it wants to.
      </p>
      <a href="about.html" style="font-family:var(--font-mono);font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--accent);">Read the full bio →</a>
    </div>
  </aside>
</div>
<div id="site-footer"></div>
<script src="js/shared.js"></script>
<script src="js/main.js"></script>
</body>
</html>"""
    BLOG_FILE.write_text(content)

# ── Streamlit UI ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WTP Post Manager",
    page_icon="✏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
  [data-testid="stSidebar"] { min-width: 240px; }
  .stButton > button { border-radius: 0; }
  h1 { font-size: 1.6rem !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar nav
with st.sidebar:
    st.markdown("## ✏️ WTP Manager")
    st.markdown("**whatsthepoint.to**")
    st.divider()
    page = st.radio("", ["📝 New Post", "📋 All Posts", "⚙️ Settings"], label_visibility="collapsed")
    st.divider()
    st.caption(f"Site root: `{SITE_ROOT}`")

posts = load_meta()

# ════════════════════════════════════════════════════════════
# PAGE: NEW POST
# ════════════════════════════════════════════════════════════
if page == "📝 New Post":
    st.title("New Post")

    # Check if editing
    edit_slug = st.session_state.get("edit_slug")
    editing   = None
    if edit_slug:
        editing = next((p for p in posts if p['slug'] == edit_slug), None)

    if editing:
        st.info(f"Editing: **{editing['title']}**  ·  [Cancel](?)")
        if st.button("Cancel Edit"):
            del st.session_state["edit_slug"]
            st.rerun()

    with st.form("post_form", clear_on_submit=not editing):
        col1, col2 = st.columns([3, 1])
        with col1:
            title = st.text_input("Title *", value=editing['title'] if editing else "")
        with col2:
            tag = st.selectbox("Tag *", TAGS,
                               index=TAGS.index(editing['tag']) if editing and editing['tag'] in TAGS else 0)

        standfirst = st.text_area("Standfirst (subtitle / excerpt) *",
                                  value=editing.get('standfirst','') if editing else "",
                                  height=80,
                                  help="1–2 sentences shown in post listings and the post header.")

        st.markdown("**Body** — write in HTML (headings, `<p>`, `<h2>`, `<blockquote>`, `<ul>`, etc.)")
        body = st.text_area("Body HTML *",
                             value=editing.get('body','') if editing else "",
                             height=420,
                             label_visibility="collapsed")

        col3, col4 = st.columns(2)
        with col3:
            pub_date = st.date_input("Publish date", value=datetime.strptime(editing['date'], "%Y-%m-%d").date() if editing and editing.get('date') else date.today())
        with col4:
            published = st.checkbox("Published (visible on site)", value=editing.get('published', False) if editing else False)

        submitted = st.form_submit_button("💾 Save & Publish" if published else "💾 Save Draft",
                                           use_container_width=True, type="primary")

    if submitted:
        if not title or not standfirst or not body:
            st.error("Title, standfirst and body are required.")
        else:
            slug      = editing['slug'] if editing else slugify(title)
            read_time = reading_time(body)
            post_html = render_post_html(slug, title, standfirst, tag, pub_date, body, read_time)

            # Write the HTML file
            (POSTS_DIR / f"{slug}.html").write_text(post_html)

            # Update meta
            entry = {
                "slug":       slug,
                "title":      title,
                "standfirst": standfirst,
                "tag":        tag,
                "date":       str(pub_date),
                "read_time":  read_time,
                "published":  published,
                "body":       body,
            }
            if editing:
                idx = next(i for i, p in enumerate(posts) if p['slug'] == slug)
                posts[idx] = entry
            else:
                posts.insert(0, entry)

            save_meta(posts)
            rebuild_index(posts)
            rebuild_blog(posts)

            if "edit_slug" in st.session_state:
                del st.session_state["edit_slug"]

            st.success(f"✅ Post saved: `posts/{slug}.html`  |  index.html and blog.html updated.")
            if published:
                st.balloons()

# ════════════════════════════════════════════════════════════
# PAGE: ALL POSTS
# ════════════════════════════════════════════════════════════
elif page == "📋 All Posts":
    st.title("All Posts")

    if not posts:
        st.info("No posts yet. Use **New Post** to write your first essay.")
    else:
        for p in sorted(posts, key=lambda x: x['date'], reverse=True):
            status = "🟢 Published" if p.get('published') else "⚫ Draft"
            with st.expander(f"{status}  ·  **{p['title']}**  ·  {format_date(p['date'])}  ·  {p['tag']}"):
                col_a, col_b, col_c = st.columns([2, 1, 1])
                with col_a:
                    st.markdown(f"**Standfirst:** {p.get('standfirst','')[:120]}…")
                    st.caption(f"Slug: `posts/{p['slug']}.html`  ·  {p.get('read_time','')}")
                with col_b:
                    if st.button("✏️ Edit", key=f"edit_{p['slug']}"):
                        st.session_state["edit_slug"] = p['slug']
                        st.rerun()
                with col_c:
                    if st.button("🗑️ Delete", key=f"del_{p['slug']}"):
                        posts = [x for x in posts if x['slug'] != p['slug']]
                        post_file = POSTS_DIR / f"{p['slug']}.html"
                        if post_file.exists():
                            post_file.unlink()
                        save_meta(posts)
                        rebuild_index(posts)
                        rebuild_blog(posts)
                        st.rerun()

                # Toggle publish
                new_state = not p.get('published')
                label = "📤 Publish" if new_state else "📥 Unpublish"
                if st.button(label, key=f"pub_{p['slug']}"):
                    idx = next(i for i, x in enumerate(posts) if x['slug'] == p['slug'])
                    posts[idx]['published'] = new_state
                    save_meta(posts)
                    rebuild_index(posts)
                    rebuild_blog(posts)
                    st.rerun()

# ════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ════════════════════════════════════════════════════════════
elif page == "⚙️ Settings":
    st.title("Settings")
    st.markdown("**Rebuild site files** — regenerates `index.html` and `blog.html` from current post metadata.")

    if st.button("🔄 Rebuild index.html & blog.html", type="primary"):
        rebuild_index(posts)
        rebuild_blog(posts)
        st.success("✅ Site files rebuilt.")

    st.divider()
    st.markdown(f"**Post count:** {len(posts)}  ·  **Published:** {sum(1 for p in posts if p.get('published'))}")
    st.markdown(f"**Site root:** `{SITE_ROOT}`")
    st.markdown(f"**Posts directory:** `{POSTS_DIR}`")
