/**
 * GreenGrow - Main Public JavaScript
 * Handles contact forms, dynamic search, dynamic data rendering, and UI notifications without backend.
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Contact & Feedback Form Handler (pure frontend + localStorage)
  const feedbackForm = document.getElementById("publicFeedbackForm");
  const feedbackNotice = document.getElementById("feedbackNoticeContainer");

  if (feedbackForm) {
    feedbackForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const submitBtn = feedbackForm.querySelector("button[type='submit']");
      const originalBtnText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span>Submitting...`;

      const payload = {
        id: Date.now(),
        name: document.getElementById("fbName")?.value.trim() || "Anonymous",
        email: document.getElementById("fbEmail")?.value.trim() || null,
        phone: document.getElementById("fbPhone")?.value.trim() || null,
        subject: document.getElementById("fbSubject").value.trim(),
        message: document.getElementById("fbMessage").value.trim(),
        status: "New",
        created_at: new Date().toISOString().replace('T', ' ').substring(0, 16),
        admin_notes: ""
      };

      setTimeout(() => {
        try {
          if (typeof DataStore !== "undefined") {
            const feedbacks = DataStore.getFeedback();
            feedbacks.unshift(payload);
            DataStore.saveFeedback(feedbacks);
          }

          feedbackForm.reset();
          if (feedbackNotice) {
            feedbackNotice.innerHTML = `
              <div class="alert alert-success alert-dismissible fade show shadow-sm" role="alert">
                <i class="bi bi-check-circle-fill me-2 fs-5"></i>
                <strong>Thank You!</strong> Your feedback has been received and securely stored in your browser session. Our agricultural advisory team will review it shortly.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            `;
            feedbackNotice.scrollIntoView({ behavior: "smooth", block: "nearest" });
          }
        } catch (err) {
          if (feedbackNotice) {
            feedbackNotice.innerHTML = `
              <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                <strong>Error:</strong> ${err.message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            `;
          }
        } finally {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnText;
        }
      }, 400);
    });
  }

  // 2. Dynamic Homepage Articles and Videos Injector
  initHomePage();

  // 3. Dynamic Resources Page Injector
  initResourcesPage();

  // 4. Dynamic Videos Page Injector
  initVideosPage();

  // 5. Dynamic FAQs Page Injector
  initFaqsPage();

  // 6. Dynamic Search Page
  initSearchPage();

  // 7. Dynamic Article Detail Page
  initArticleDetailPage();
});

// Helper to escape HTML to prevent injection
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function initHomePage() {
  const articlesContainer = document.getElementById("homeArticlesContainer");
  if (articlesContainer && typeof DataStore !== "undefined") {
    const articles = DataStore.getArticles().filter(a => a.is_published).slice(0, 3);
    articlesContainer.innerHTML = articles.map(art => `
      <div class="col-md-4">
        <div class="card h-100 border rounded-4 overflow-hidden shadow-sm">
          <div class="card-body p-4 d-flex flex-column">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-success-subtle text-success">${escapeHtml(art.category || 'General')}</span>
              <small class="text-muted"><i class="bi bi-eye me-1"></i>${art.view_count || 0}</small>
            </div>
            <h5 class="fw-bold mb-2">${escapeHtml(art.title)}</h5>
            <p class="text-muted small flex-grow-1">${escapeHtml(art.summary || (art.content ? art.content.substring(0, 140) + '...' : ''))}</p>
            <a href="articles/${escapeHtml(art.slug)}.html" class="btn btn-sm btn-outline-success rounded-pill mt-2">
              Read Full Article <i class="bi bi-arrow-right ms-1"></i>
            </a>
          </div>
        </div>
      </div>
    `).join("");
  }

  const videosContainer = document.getElementById("homeVideosContainer");
  if (videosContainer && typeof DataStore !== "undefined") {
    const videos = DataStore.getVideos().filter(v => v.is_published).slice(0, 3);
    videosContainer.innerHTML = videos.map(vid => `
      <div class="col-md-4">
        <div class="card h-100 border rounded-4 overflow-hidden shadow-sm">
          <div class="bg-dark text-white p-4 text-center position-relative">
            <i class="bi bi-play-circle-fill display-3 text-warning"></i>
            ${vid.duration_minutes ? `<span class="position-absolute bottom-0 end-0 m-2 badge bg-black bg-opacity-75">${vid.duration_minutes} min</span>` : ''}
          </div>
          <div class="card-body p-4">
            <span class="badge bg-secondary-subtle text-secondary mb-2">${escapeHtml(vid.category)}</span>
            <h6 class="fw-bold mb-2">${escapeHtml(vid.title)}</h6>
            <p class="text-muted small mb-3">${escapeHtml(vid.description || 'Practical demonstration of organic farming techniques.')}</p>
            <a href="${escapeHtml(vid.video_url)}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-primary rounded-pill w-100">
              <i class="bi bi-box-arrow-up-right me-1"></i>Watch Demonstration
            </a>
          </div>
        </div>
      </div>
    `).join("");
  }
}

function initResourcesPage() {
  const container = document.getElementById("resourcesGridContainer");
  if (!container || typeof DataStore === "undefined") return;

  const urlParams = new URLSearchParams(window.location.search);
  const selectedCat = urlParams.get("category");

  const resources = DataStore.getResources().filter(r => r.is_published);
  const filtered = selectedCat ? resources.filter(r => r.category === selectedCat) : resources;

  // Render filter pills
  const categories = [...new Set(resources.map(r => r.category))];
  const pillsContainer = document.getElementById("resourcesPillsContainer");
  if (pillsContainer) {
    pillsContainer.innerHTML = `
      <a href="resources.html" class="btn btn-sm ${!selectedCat ? 'btn-success' : 'btn-outline-secondary'} rounded-pill px-3">
        All Resources
      </a>
      ${categories.map(c => `
        <a href="resources.html?category=${encodeURIComponent(c)}" class="btn btn-sm ${selectedCat === c ? 'btn-success' : 'btn-outline-secondary'} rounded-pill px-3">
          ${escapeHtml(c)}
        </a>
      `).join("")}
    `;
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-12">
        <div class="p-5 text-center bg-white rounded-4 border shadow-sm">
          <i class="bi bi-folder2-open display-3 text-muted mb-3 d-block"></i>
          <h4 class="fw-bold text-dark">No Resources in this Category Yet</h4>
          <p class="text-muted small mx-auto mb-3" style="max-width: 450px;">
            Administrators can upload PDF guides, training leaflets, and policy papers from the GreenGrow Admin Dashboard.
          </p>
          <a href="resources.html" class="btn btn-outline-green rounded-pill px-4">View All Categories</a>
        </div>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(res => `
    <div class="col-md-6 col-lg-4">
      <div class="card h-100 border rounded-4 overflow-hidden shadow-sm">
        <div class="card-body p-4 d-flex flex-column">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="badge bg-success-subtle text-success">${escapeHtml(res.category)}</span>
            <small class="text-muted"><i class="bi bi-download me-1"></i>${res.download_count || 0}</small>
          </div>
          <h5 class="fw-bold mb-2 text-dark">${escapeHtml(res.title)}</h5>
          <p class="text-muted small flex-grow-1">
            ${escapeHtml(res.description || 'Comprehensive guide to organic agricultural procedures and best practices.')}
          </p>
          <div class="d-flex justify-content-between align-items-center pt-3 border-top mt-2">
            <small class="text-muted text-uppercase fw-semibold">${escapeHtml(res.file_type)} • ${(res.file_size_bytes / 1024).toFixed(1)} KB</small>
            <a href="${escapeHtml(res.file_path || 'uploads/resources/greengrow_farmer_guidance_handbook.pdf')}" download class="btn btn-sm btn-primary-green rounded-pill px-3">
              <i class="bi bi-arrow-down-circle me-1"></i>Download
            </a>
          </div>
        </div>
      </div>
    </div>
  `).join("");
}

function initVideosPage() {
  const container = document.getElementById("videosGridContainer");
  if (!container || typeof DataStore === "undefined") return;

  const urlParams = new URLSearchParams(window.location.search);
  const selectedCat = urlParams.get("category");

  const videos = DataStore.getVideos().filter(v => v.is_published);
  const filtered = selectedCat ? videos.filter(v => v.category === selectedCat) : videos;

  const categories = [...new Set(videos.map(v => v.category))];
  const pillsContainer = document.getElementById("videosPillsContainer");
  if (pillsContainer) {
    pillsContainer.innerHTML = `
      <a href="videos.html" class="btn btn-sm ${!selectedCat ? 'btn-success' : 'btn-outline-secondary'} rounded-pill px-3">
        All Videos
      </a>
      ${categories.map(c => `
        <a href="videos.html?category=${encodeURIComponent(c)}" class="btn btn-sm ${selectedCat === c ? 'btn-success' : 'btn-outline-secondary'} rounded-pill px-3">
          ${escapeHtml(c)}
        </a>
      `).join("")}
    `;
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-12">
        <div class="p-5 text-center bg-white rounded-4 border">
          <i class="bi bi-camera-video display-3 text-muted mb-3 d-block"></i>
          <h4 class="fw-bold">No Videos Available in this Category</h4>
          <p class="text-muted small">New video demonstrations will be added by the GreenGrow editorial team.</p>
        </div>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(vid => `
    <div class="col-md-6 col-lg-4">
      <div class="card h-100 border rounded-4 overflow-hidden shadow-sm">
        <div class="bg-dark text-white p-4 text-center position-relative" style="min-height: 180px; display: flex; align-items: center; justify-content: center;">
          ${vid.thumbnail_url ? `<img src="${escapeHtml(vid.thumbnail_url)}" alt="${escapeHtml(vid.title)}" class="position-absolute top-0 start-0 w-100 h-100 object-fit-cover opacity-50">` : ''}
          <a href="${escapeHtml(vid.video_url)}" target="_blank" rel="noopener noreferrer" class="text-warning text-decoration-none z-1">
            <i class="bi bi-play-circle-fill display-3"></i>
          </a>
          ${vid.duration_minutes ? `<span class="position-absolute bottom-0 end-0 m-2 badge bg-black bg-opacity-75 z-1">${vid.duration_minutes} mins</span>` : ''}
        </div>
        <div class="card-body p-4 d-flex flex-column">
          <span class="badge bg-secondary-subtle text-secondary mb-2 align-self-start">${escapeHtml(vid.category)}</span>
          <h5 class="fw-bold mb-2 text-dark">${escapeHtml(vid.title)}</h5>
          <p class="text-muted small flex-grow-1">
            ${escapeHtml(vid.description || 'Practical demonstration of organic farming techniques and field preparation.')}
          </p>
          <a href="${escapeHtml(vid.video_url)}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-primary rounded-pill mt-3 w-100">
            <i class="bi bi-box-arrow-up-right me-1"></i>Watch Demonstration
          </a>
        </div>
      </div>
    </div>
  `).join("");
}

function initFaqsPage() {
  const accordion = document.getElementById("faqAccordionContainer");
  if (!accordion || typeof DataStore === "undefined") return;

  const faqs = DataStore.getFaqs().filter(f => f.is_published);
  const categories = [...new Set(faqs.map(f => f.category))];

  const pillsContainer = document.getElementById("faqPillsContainer");
  if (pillsContainer) {
    pillsContainer.innerHTML = `
      <button class="btn btn-sm btn-success rounded-pill px-3 faq-filter-btn" data-category="all">All FAQs</button>
      ${categories.map(c => `
        <button class="btn btn-sm btn-outline-secondary rounded-pill px-3 faq-filter-btn" data-category="${escapeHtml(c)}">${escapeHtml(c)}</button>
      `).join("")}
    `;

    pillsContainer.querySelectorAll('.faq-filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        pillsContainer.querySelectorAll('.faq-filter-btn').forEach(b => {
          b.classList.remove('btn-success');
          b.classList.add('btn-outline-secondary');
        });
        btn.classList.remove('btn-outline-secondary');
        btn.classList.add('btn-success');

        const selectedCat = btn.getAttribute('data-category');
        document.querySelectorAll('.faq-item').forEach(item => {
          if (selectedCat === 'all' || item.getAttribute('data-category') === selectedCat) {
            item.style.display = 'block';
          } else {
            item.style.display = 'none';
          }
        });
      });
    });
  }

  accordion.innerHTML = faqs.map((faq, idx) => `
    <div class="accordion-item faq-item" data-category="${escapeHtml(faq.category)}">
      <h2 class="accordion-header" id="heading${faq.id}">
        <button class="accordion-button ${idx !== 0 ? 'collapsed' : ''} fw-semibold text-dark py-3" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${faq.id}" aria-expanded="${idx === 0 ? 'true' : 'false'}" aria-controls="collapse${faq.id}">
          <span class="badge bg-success-subtle text-success me-3">${escapeHtml(faq.category)}</span>
          ${escapeHtml(faq.question)}
        </button>
      </h2>
      <div id="collapse${faq.id}" class="accordion-collapse collapse ${idx === 0 ? 'show' : ''}" aria-labelledby="heading${faq.id}" data-bs-parent="#faqAccordionContainer">
        <div class="accordion-body text-muted small p-4 bg-light bg-opacity-50">
          ${escapeHtml(faq.answer)}
        </div>
      </div>
    </div>
  `).join("");
}

function initSearchPage() {
  const resultsContainer = document.getElementById("searchResultsArea");
  if (!resultsContainer || typeof DataStore === "undefined") return;

  const urlParams = new URLSearchParams(window.location.search);
  const query = (urlParams.get("q") || "").trim().toLowerCase();

  const queryDisplay = document.getElementById("searchQueryDisplay");
  const searchInput = document.getElementById("searchInputField");
  if (searchInput) searchInput.value = urlParams.get("q") || "";

  if (!query) {
    if (queryDisplay) queryDisplay.textContent = "Enter a keyword above to search across articles, FAQs, resources, and videos.";
    resultsContainer.innerHTML = `
      <div class="p-4 bg-light rounded-4 border">
        <h5 class="fw-bold mb-2">Search Suggestions</h5>
        <div class="d-flex flex-wrap gap-2">
          <a href="search.html?q=compost" class="btn btn-sm btn-white border rounded-pill">Compost</a>
          <a href="search.html?q=vermicompost" class="btn btn-sm btn-white border rounded-pill">Vermicompost</a>
          <a href="search.html?q=soil" class="btn btn-sm btn-white border rounded-pill">Soil Health</a>
          <a href="search.html?q=pest" class="btn btn-sm btn-white border rounded-pill">Pest Management</a>
          <a href="search.html?q=water" class="btn btn-sm btn-white border rounded-pill">Water Conservation</a>
          <a href="search.html?q=neem" class="btn btn-sm btn-white border rounded-pill">Neem Extract</a>
        </div>
      </div>
    `;
    return;
  }

  // Filter static contents
  const articles = DataStore.getArticles().filter(a =>
    a.is_published && (a.title.toLowerCase().includes(query) || (a.summary && a.summary.toLowerCase().includes(query)) || a.content.toLowerCase().includes(query))
  );

  const faqs = DataStore.getFaqs().filter(f =>
    f.is_published && (f.question.toLowerCase().includes(query) || f.answer.toLowerCase().includes(query))
  );

  const resources = DataStore.getResources().filter(r =>
    r.is_published && (r.title.toLowerCase().includes(query) || (r.description && r.description.toLowerCase().includes(query)))
  );

  const videos = DataStore.getVideos().filter(v =>
    v.is_published && (v.title.toLowerCase().includes(query) || (v.description && v.description.toLowerCase().includes(query)))
  );

  const totalMatches = articles.length + faqs.length + resources.length + videos.length;

  if (queryDisplay) {
    queryDisplay.innerHTML = `Showing results for: <strong>"${escapeHtml(query)}"</strong> (${totalMatches} matches found)`;
  }

  if (totalMatches === 0) {
    resultsContainer.innerHTML = `
      <div class="p-5 text-center bg-white rounded-4 border shadow-sm">
        <i class="bi bi-search display-3 text-muted mb-3 d-block"></i>
        <h4 class="fw-bold">No Matches Found</h4>
        <p class="text-muted small mx-auto" style="max-width: 450px;">
          Try searching with broader terms such as "compost", "water", "soil", "pests", or "manure".
        </p>
      </div>
    `;
    return;
  }

  let html = '';

  if (articles.length > 0) {
    html += `
      <div class="mb-5">
        <h4 class="fw-bold text-success mb-3"><i class="bi bi-file-text me-2"></i>Articles (${articles.length})</h4>
        <div class="list-group shadow-sm rounded-4 overflow-hidden border">
          ${articles.map(art => `
            <a href="articles/${escapeHtml(art.slug)}.html" class="list-group-item list-group-item-action p-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <h6 class="fw-bold mb-0 text-dark">${escapeHtml(art.title)}</h6>
                <span class="badge bg-success-subtle text-success">${escapeHtml(art.category || 'General')}</span>
              </div>
              <p class="text-muted small mb-0">${escapeHtml(art.summary || (art.content ? art.content.substring(0, 140) + '...' : ''))}</p>
            </a>
          `).join("")}
        </div>
      </div>
    `;
  }

  if (faqs.length > 0) {
    html += `
      <div class="mb-5">
        <h4 class="fw-bold text-primary mb-3"><i class="bi bi-question-circle me-2"></i>Frequently Asked Questions (${faqs.length})</h4>
        <div class="list-group shadow-sm rounded-4 overflow-hidden border">
          ${faqs.map(f => `
            <div class="list-group-item p-3">
              <span class="badge bg-primary-subtle text-primary mb-1">${escapeHtml(f.category)}</span>
              <h6 class="fw-bold mb-1 text-dark">${escapeHtml(f.question)}</h6>
              <p class="text-muted small mb-0">${escapeHtml(f.answer)}</p>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  }

  if (resources.length > 0) {
    html += `
      <div class="mb-5">
        <h4 class="fw-bold text-warning-emphasis mb-3"><i class="bi bi-folder2 me-2"></i>Resources & PDF Downloads (${resources.length})</h4>
        <div class="list-group shadow-sm rounded-4 overflow-hidden border">
          ${resources.map(r => `
            <div class="list-group-item p-3 d-flex justify-content-between align-items-center">
              <div>
                <h6 class="fw-bold mb-1 text-dark">${escapeHtml(r.title)}</h6>
                <small class="text-muted">${escapeHtml(r.category)} • ${escapeHtml(r.file_type).toUpperCase()}</small>
              </div>
              <a href="${escapeHtml(r.file_path || 'uploads/resources/greengrow_farmer_guidance_handbook.pdf')}" download class="btn btn-sm btn-outline-success rounded-pill px-3">
                <i class="bi bi-download me-1"></i>Download
              </a>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  }

  if (videos.length > 0) {
    html += `
      <div class="mb-5">
        <h4 class="fw-bold text-danger mb-3"><i class="bi bi-camera-video me-2"></i>Videos (${videos.length})</h4>
        <div class="list-group shadow-sm rounded-4 overflow-hidden border">
          ${videos.map(v => `
            <div class="list-group-item p-3 d-flex justify-content-between align-items-center">
              <div>
                <h6 class="fw-bold mb-1 text-dark">${escapeHtml(v.title)}</h6>
                <small class="text-muted">${escapeHtml(v.category)} • ${v.duration_minutes || 0} mins</small>
              </div>
              <a href="${escapeHtml(v.video_url)}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-primary rounded-pill px-3">
                <i class="bi bi-play-circle me-1"></i>Watch
              </a>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  }

  resultsContainer.innerHTML = html;
}

function initArticleDetailPage() {
  const container = document.getElementById("articleDetailDynamicContainer");
  if (!container || typeof DataStore === "undefined") return;

  const slug = container.getAttribute("data-slug");
  if (!slug) return;

  const articles = DataStore.getArticles();
  const article = articles.find(a => a.slug === slug);
  if (!article) return;

  // Increment view count in local storage
  article.view_count = (article.view_count || 0) + 1;
  DataStore.saveArticles(articles);

  const viewsEl = document.getElementById("artViewCount");
  if (viewsEl) viewsEl.textContent = `${article.view_count} views`;
}
