/**
 * GreenGrow - Admin Portal JavaScript & Interactive Demonstration
 * Handles demonstration login, dynamic CRUD with browser localStorage, and Chart.js analytics.
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Admin Login Form Handler (Demonstration Mode)
  const loginForm = document.getElementById("adminLoginForm");
  const loginNotice = document.getElementById("loginNotice");

  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const submitBtn = loginForm.querySelector("button[type='submit']");
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Authenticating...`;

      const username = document.getElementById("adminUsername").value.trim();
      const password = document.getElementById("adminPassword").value.trim();

      setTimeout(() => {
        // Frontend demo authentication: Accept demo credentials or any non-empty input
        if (username) {
          const adminSession = {
            username: username || "admin",
            full_name: username === "admin" ? "GreenGrow Project Administrator" : username,
            role: username === "admin" ? "superadmin" : "admin",
            access_token: "frontend-demo-token-" + Date.now()
          };
          localStorage.setItem("greengrow_token", adminSession.access_token);
          localStorage.setItem("greengrow_admin", JSON.stringify(adminSession));

          if (typeof DataStore !== "undefined") {
            DataStore.logAudit("LOGIN", "AUTH", "1", `Admin '${username}' signed in (Frontend Demo)`);
          }

          window.location.href = "dashboard.html";
        } else {
          if (loginNotice) {
            loginNotice.innerHTML = `
              <div class="alert alert-danger py-2 small" role="alert">
                <i class="bi bi-shield-x me-2"></i>Please enter an admin username.
              </div>
            `;
          }
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalText;
        }
      }, 350);
    });
  }

  // 2. Admin Logout Handler
  document.querySelectorAll(".admin-logout-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("greengrow_token");
      localStorage.removeItem("greengrow_admin");
      window.location.href = "login.html";
    });
  });

  // 3. Populate current admin user pill if present
  const adminPill = document.querySelector(".admin-user-pill");
  if (adminPill) {
    const rawAdmin = localStorage.getItem("greengrow_admin");
    if (rawAdmin) {
      try {
        const adminData = JSON.parse(rawAdmin);
        const nameSpan = adminPill.querySelector(".admin-user-name");
        if (nameSpan) nameSpan.textContent = adminData.full_name || adminData.username;
        const roleBadge = adminPill.querySelector(".admin-user-role");
        if (roleBadge) roleBadge.textContent = adminData.role;
      } catch (e) {}
    }
  }

  // 4. Initialize Analytics Visualizations on Dashboard
  initDashboardAnalytics();
});

function initDashboardAnalytics() {
  const chartContainers = document.querySelectorAll("[data-analytics-chart]");
  if (chartContainers.length === 0 || typeof DataStore === "undefined") return;

  const surveys = DataStore.getSurveys();
  const feedback = DataStore.getFeedback();
  const articles = DataStore.getArticles();
  const resources = DataStore.getResources();
  const faqs = DataStore.getFaqs();

  // Update Metric Card numbers
  const countSurveys = document.getElementById("statTotalSurveys");
  if (countSurveys) countSurveys.textContent = surveys.length;

  const countArticles = document.getElementById("statTotalArticles");
  if (countArticles) countArticles.textContent = articles.length;

  const countResources = document.getElementById("statTotalResources");
  if (countResources) countResources.textContent = resources.length;

  const countFaqs = document.getElementById("statTotalFaqs");
  if (countFaqs) countFaqs.textContent = faqs.length;

  const countFeedbackTotal = document.getElementById("statFeedbackTotal");
  if (countFeedbackTotal) countFeedbackTotal.textContent = feedback.length;

  const countFeedbackNew = document.getElementById("statFeedbackNew");
  if (countFeedbackNew) countFeedbackNew.textContent = feedback.filter(f => f.status === 'New').length;

  const countFeedbackReviewed = document.getElementById("statFeedbackReviewed");
  if (countFeedbackReviewed) countFeedbackReviewed.textContent = feedback.filter(f => f.status === 'Reviewed').length;

  const countFeedbackResolved = document.getElementById("statFeedbackResolved");
  if (countFeedbackResolved) countFeedbackResolved.textContent = feedback.filter(f => f.status === 'Resolved').length;

  const noDataPlaceholder = document.getElementById("noSurveyDataAlert");
  if (noDataPlaceholder) {
    noDataPlaceholder.style.display = surveys.length > 0 ? "none" : "block";
  }

  // Populate Dashboard Recent Survey Table
  const recentSurveyTbody = document.getElementById("dashboardRecentSurveys");
  if (recentSurveyTbody) {
    if (surveys.length === 0) {
      recentSurveyTbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-4">No survey records present in database yet.</td></tr>`;
    } else {
      recentSurveyTbody.innerHTML = surveys.slice(0, 5).map(s => `
        <tr>
          <td class="fw-bold">${s.respondent_code}</td>
          <td>${s.village}</td>
          <td><span class="badge bg-light text-dark border">${s.farming_method}</span></td>
          <td>${s.awareness_level}</td>
          <td><span class="badge bg-success-subtle text-success">${s.willingness_to_adopt}</span></td>
          <td>
            <a href="survey_detail.html?id=${s.id}" class="btn btn-sm btn-outline-primary py-0 px-2 rounded-pill">
              View
            </a>
          </td>
        </tr>
      `).join("");
    }
  }

  // Populate Dashboard Recent Feedback Table
  const recentFeedbackTbody = document.getElementById("dashboardRecentFeedback");
  if (recentFeedbackTbody) {
    if (feedback.length === 0) {
      recentFeedbackTbody.innerHTML = `<tr><td colspan="3" class="text-center text-muted py-4">No user feedback messages recorded yet.</td></tr>`;
    } else {
      recentFeedbackTbody.innerHTML = feedback.slice(0, 5).map(fb => `
        <tr>
          <td><strong>${fb.name || 'Anonymous'}</strong></td>
          <td>${(fb.subject || '').substring(0, 25)}...</td>
          <td>
            <span class="badge-status badge-${(fb.status || 'new').toLowerCase()}">${fb.status}</span>
          </td>
        </tr>
      `).join("");
    }
  }

  if (surveys.length === 0) return;

  // Process data for charts
  const methodCounts = {};
  const inputCounts = {};
  const awarenessCounts = {};
  const challengeCounts = {};
  const willingnessCounts = {};
  const cropCounts = {};
  const timelineCounts = {};

  surveys.forEach(s => {
    // Methods
    methodCounts[s.farming_method] = (methodCounts[s.farming_method] || 0) + 1;
    // Awareness
    awarenessCounts[s.awareness_level] = (awarenessCounts[s.awareness_level] || 0) + 1;
    // Willingness
    willingnessCounts[s.willingness_to_adopt] = (willingnessCounts[s.willingness_to_adopt] || 0) + 1;
    // Timeline
    if (s.survey_date) {
      timelineCounts[s.survey_date] = (timelineCounts[s.survey_date] || 0) + 1;
    }
    // Inputs
    if (s.organic_input_usage) {
      s.organic_input_usage.split(',').forEach(item => {
        const trimmed = item.trim();
        if (trimmed && trimmed.toLowerCase() !== 'none') {
          inputCounts[trimmed] = (inputCounts[trimmed] || 0) + 1;
        }
      });
    }
    // Challenges
    if (s.primary_challenges) {
      s.primary_challenges.split(',').forEach(item => {
        const trimmed = item.trim();
        if (trimmed) {
          challengeCounts[trimmed] = (challengeCounts[trimmed] || 0) + 1;
        }
      });
    }
    // Crops
    if (s.primary_crops) {
      s.primary_crops.split(',').forEach(item => {
        const trimmed = item.trim();
        if (trimmed) {
          cropCounts[trimmed] = (cropCounts[trimmed] || 0) + 1;
        }
      });
    }
  });

  // Render Chart 1: Farming Methods
  const methodCtx = document.getElementById("chartFarmingMethods");
  if (methodCtx && typeof Chart !== "undefined") {
    new Chart(methodCtx, {
      type: "doughnut",
      data: {
        labels: Object.keys(methodCounts),
        datasets: [{
          data: Object.values(methodCounts),
          backgroundColor: ["#2e7d32", "#4caf50", "#81c784", "#ffb74d", "#ef5350"],
          borderWidth: 2,
          borderColor: "#ffffff",
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: "bottom" } },
      },
    });
  }

  // Render Chart 2: Organic Inputs
  const inputsCtx = document.getElementById("chartOrganicInputs");
  if (inputsCtx && typeof Chart !== "undefined") {
    new Chart(inputsCtx, {
      type: "bar",
      data: {
        labels: Object.keys(inputCounts),
        datasets: [{
          label: "Farmers Using Input",
          data: Object.values(inputCounts),
          backgroundColor: "#388e3c",
          borderRadius: 6,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });
  }

  // Render Chart 3: Awareness Levels
  const awarenessCtx = document.getElementById("chartAwareness");
  if (awarenessCtx && typeof Chart !== "undefined") {
    new Chart(awarenessCtx, {
      type: "pie",
      data: {
        labels: Object.keys(awarenessCounts),
        datasets: [{
          data: Object.values(awarenessCounts),
          backgroundColor: ["#1b5e20", "#388e3c", "#81c784", "#c8e6c9"],
          borderWidth: 2,
          borderColor: "#ffffff",
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: "bottom" } },
      },
    });
  }

  // Render Chart 4: Challenges
  const challengesCtx = document.getElementById("chartChallenges");
  if (challengesCtx && typeof Chart !== "undefined") {
    new Chart(challengesCtx, {
      type: "bar",
      data: {
        labels: Object.keys(challengeCounts),
        datasets: [{
          label: "Reported Constraints",
          data: Object.values(challengeCounts),
          backgroundColor: "#f57c00",
          borderRadius: 6,
        }],
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        scales: { x: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });
  }

  // Render Chart 5: Willingness
  const willingnessCtx = document.getElementById("chartWillingness");
  if (willingnessCtx && typeof Chart !== "undefined") {
    new Chart(willingnessCtx, {
      type: "bar",
      data: {
        labels: Object.keys(willingnessCounts),
        datasets: [{
          label: "Respondent Count",
          data: Object.values(willingnessCounts),
          backgroundColor: ["#2e7d32", "#66bb6a", "#ffa726", "#e53935"],
          borderRadius: 6,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });
  }

  // Render Chart 6: Crops
  const cropsCtx = document.getElementById("chartCrops");
  if (cropsCtx && typeof Chart !== "undefined") {
    new Chart(cropsCtx, {
      type: "bar",
      data: {
        labels: Object.keys(cropCounts),
        datasets: [{
          label: "Cultivating Farmers",
          data: Object.values(cropCounts),
          backgroundColor: "#5d4037",
          borderRadius: 6,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });
  }

  // Render Chart 7: Timeline
  const timelineCtx = document.getElementById("chartTimeline");
  if (timelineCtx && typeof Chart !== "undefined") {
    const sortedDates = Object.keys(timelineCounts).sort();
    new Chart(timelineCtx, {
      type: "line",
      data: {
        labels: sortedDates,
        datasets: [{
          label: "Daily Survey Submissions",
          data: sortedDates.map(d => timelineCounts[d]),
          borderColor: "#2e7d32",
          backgroundColor: "rgba(46, 125, 50, 0.1)",
          fill: true,
          tension: 0.3,
          pointRadius: 5,
          pointBackgroundColor: "#1b5e20",
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
      },
    });
  }
}

// Client-side CSV Exporter for Surveys
function exportSurveysToCSV() {
  if (typeof DataStore === "undefined") return;
  const surveys = DataStore.getSurveys();
  if (surveys.length === 0) {
    alert("No survey records to export.");
    return;
  }

  const headers = ["ID", "Code", "Village", "Date", "Experience(Years)", "Land(Acres)", "Method", "Primary Crops", "Awareness", "Willingness", "Inputs Used", "Challenges"];
  const rows = surveys.map(s => [
    s.id,
    `"${s.respondent_code}"`,
    `"${s.village}"`,
    `"${s.survey_date}"`,
    s.farming_experience_years || "",
    s.land_holding_acres || "",
    `"${s.farming_method}"`,
    `"${(s.primary_crops || '').replace(/"/g, '""')}"`,
    `"${s.awareness_level}"`,
    `"${s.willingness_to_adopt}"`,
    `"${(s.organic_input_usage || '').replace(/"/g, '""')}"`,
    `"${(s.primary_challenges || '').replace(/"/g, '""')}"`
  ]);

  const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `greengrow_farmer_surveys_${new Date().toISOString().slice(0,10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
