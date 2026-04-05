# Limelight – Homepage Options

Five Bootstrap 5 homepage designs for **Limelight** (`flaskpackages.pythonanywhere.com`), the community-driven directory of open source Flask extensions, frameworks, modules, and projects.

---

## Options

### Option 1 – Search-First (`option1-search-first.html`)
A prominent hero search bar drives the UX. Below it: a compact stats bar and a dense category icon grid, then two equal-width columns showing *Trending* and *Recently Added* packages as clean list rows.

**Best for:** Users who already know what they're looking for. Content-heavy, low friction.

---

### Option 2 – Magazine / Featured (`option2-magazine.html`)
A dark hero spotlights one editor-picked package with companion trending picks on the right. Body uses a two-column layout (main content + sidebar). Sections use editorial-style "section label" typography.

**Best for:** First-time visitors who benefit from curation and editorial feel.

---

### Option 3 – Dashboard (`option3-dashboard.html`)
Fixed left sidebar navigation. Sticky top search bar. KPI metric cards at top. Compact category icon tiles. Tabular package listing with health dots, star counts, and download figures.

**Best for:** Power users and developers who appreciate data density and quick navigation.

---

### Option 4 – Minimal / Text-Heavy (`option4-minimal-text.html`)
Serif body font with sans headings, tight ruled lines, no color blocks. Looks like a well-designed technical publication. All content visible above the fold. Full alphabetical category list in a multi-column ul.

**Best for:** Developers who distrust eye candy; strong SEO due to rich prose descriptions.

---

### Option 5 – Card Grid + Filter Sidebar (`option5-card-filter.html`)
Full package-browsing experience on the homepage: sticky filter bar (search + sort + health status dropdowns), collapsible category sidebar, Bootstrap card grid (3 columns on desktop), and pagination.

**Best for:** Returning users and discovery browsing; most interactive option.

---

## SEO features (all options)
- Semantic HTML5 (`<header>`, `<main>`, `<article>`, `<aside>`, `<footer>`, `<nav>`)
- Unique, keyword-rich `<title>` and `<meta name="description">`
- `<link rel="canonical">`
- Open Graph and Twitter Card meta tags
- `schema.org` `WebSite` JSON-LD with `SearchAction` (enables Google sitelinks search box)
- All images have `alt` text; icons are decorative and aria-hidden by default
- Clear heading hierarchy (one `<h1>` per page)
- Descriptive anchor text on all links

### Option 6 – Tabler UI (`option6-tabler.html`)
Option 5 re-implemented with **Tabler 1.4.0** instead of plain Bootstrap 5. All Bootstrap-only components are replaced with their Tabler equivalents.

**Key migrations from option 5 → option 6:**

| Component | Option 5 (Bootstrap) | Option 6 (Tabler) |
|---|---|---|
| CSS framework | `bootstrap@5.3.3` | `@tabler/core@1.4.0` |
| Icon set | Bootstrap Icons (`bi bi-*`) | Tabler Icons (`ti ti-*`) |
| Navbar | `navbar-dark` + manual bg | Tabler `navbar navbar-expand-md d-print-none` |
| Badges (health) | Custom `.hb-active` CSS | Tabler `badge bg-success-lt`, `bg-warning-lt`, `bg-danger-lt` |
| Category badges | Custom `.cnt` CSS | Tabler `badge bg-secondary-lt` |
| Color utility badges | Manual hex CSS | Tabler semantic colors (`bg-blue-lt`, `bg-purple-lt`, `bg-cyan-lt`, …) |
| Package cards | Custom `.pkg-card` div | Tabler `card` + `card-body` + `card-footer` |
| CTA card | Custom dashed div | Tabler `card` + Tabler `avatar avatar-lg` icon block |
| Pagination arrows | `«` / `»` text | Tabler SVG chevron icons |
| Footer | Custom dark `<footer>` | Tabler `footer footer-transparent` |
| Layout wrapper | Plain `<main>` | Tabler `page-wrapper` → `page-body` |
| JS | `bootstrap.bundle.min.js` | `tabler.min.js` |

**Best for:** Projects already using Tabler for their app UI; consistent look with Tabler admin dashboards.

---

## Dependencies (CDN only, no build step)

**Options 1–5**
- Bootstrap 5.3.3
- Bootstrap Icons 1.11.3

**Option 6**
- Tabler 1.4.0 (`@tabler/core@1.4.0`)
- Tabler Icons webfont (`@tabler/icons-webfont@3.19.0`)
