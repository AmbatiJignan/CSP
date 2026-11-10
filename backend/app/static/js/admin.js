/**
 * GreenGrow - Admin Portal JavaScript & Chart.js Analytics
 * Uses strictly actual database records for all visualisations.
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Admin Login Form Handler
  const loginForm = document.getElementById("adminLoginForm");
  const loginNotice = document.getElementById("loginNotice");

  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const submitBtn = loginForm.querySelector("button[type='submit']");
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Authenticating...`;

      const username = document.getElementById("adminUsername").value;
      const password = document.getElementById("adminPassword").value;

      try {
        const resp = await fetch("/api/v1/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });

        const data = await resp.json();
        if (!resp.ok) {
          throw new Error(data.detail || "Authentication failed");
        }

        // Store token in localStorage for API calls
        localStorage.setItem("greengrow_token", data.access_token);
        localStorage.setItem("greengrow_admin", JSON.stringify(data));

        // Redirect to dashboard
        window.location.href = "/admin/dashboard";
      } catch (err) {
        if (loginNotice) {
          loginNotice.innerHTML = `
            <div class="alert alert-danger py-2 small" role="alert">
              <i class="bi bi-shield-x me-2"></i>${err.message}
            </div>
          `;
        }
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }

  // 2. Admin Logout Handler
  document.querySelectorAll(".admin-logout-btn").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      try {
        await fetch("/api/v1/auth/logout", { method: "POST" });
      } catch (err) {}
      localStorage.removeItem("greengrow_token");
      localStorage.removeItem("greengrow_admin");
      window.location.href = "/admin/login";
    });
  });

  // 3. Initialize Analytics Visualizations on Dashboard
  initDashboardAnalytics();
});

async function initDashboardAnalytics() {
  const chartContainers = document.querySelectorAll("[data-analytics-chart]");
  if (chartContainers.length === 0) return;

  try {
    const token = localStorage.getItem("greengrow_token");
    const headers = token ? { Authorization: `Bearer ${token}` } : {};

    const resp = await fetch("/api/v1/analytics/overview", { headers });
    if (!resp.ok) return;

    const data = await resp.json();
    renderCharts(data);
  } catch (err) {
    console.error("Failed to load analytics data:", err);
  }
}

function renderCharts(data) {
  const hasData = data.has_real_survey_data;
  const noDataPlaceholder = document.getElementById("noSurveyDataAlert");
  if (noDataPlaceholder) {
    noDataPlaceholder.style.display = hasData ? "none" : "block";
  }

  if (!hasData) return;

  // 1. Farming Method Distribution (Doughnut)
  const methodCtx = document.getElementById("chartFarmingMethods");
  if (methodCtx && data.farming_methods.length > 0) {
    new Chart(methodCtx, {
      type: "doughnut",
      data: {
        labels: data.farming_methods.map((d) => d.label),
        datasets: [
          {
            data: data.farming_methods.map((d) => d.count),
            backgroundColor: ["#2e7d32", "#4caf50", "#81c784", "#ffb74d", "#ef5350"],
            borderWidth: 2,
            borderColor: "#ffffff",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom" },
          tooltip: {
            callbacks: {
              label: (item) => `${item.label}: ${item.raw} (${data.farming_methods[item.dataIndex].percentage}%)`,
            },
          },
        },
      },
    });
  }

  // 2. Organic Input Usage (Bar)
  const inputsCtx = document.getElementById("chartOrganicInputs");
  if (inputsCtx && data.organic_inputs.length > 0) {
    new Chart(inputsCtx, {
      type: "bar",
      data: {
        labels: data.organic_inputs.map((d) => d.label),
        datasets: [
          {
            label: "Farmers Using Input",
            data: data.organic_inputs.map((d) => d.count),
            backgroundColor: "#388e3c",
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    });
  }

  // 3. Organic Farming Awareness (Pie)
  const awarenessCtx = document.getElementById("chartAwareness");
  if (awarenessCtx && data.awareness_levels.length > 0) {
    new Chart(awarenessCtx, {
      type: "pie",
      data: {
        labels: data.awareness_levels.map((d) => d.label),
        datasets: [
          {
            data: data.awareness_levels.map((d) => d.count),
            backgroundColor: ["#1b5e20", "#388e3c", "#81c784", "#c8e6c9"],
            borderWidth: 2,
            borderColor: "#ffffff",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom" },
        },
      },
    });
  }

  // 4. Farmer Challenges (Horizontal Bar)
  const challengesCtx = document.getElementById("chartChallenges");
  if (challengesCtx && data.challenges.length > 0) {
    new Chart(challengesCtx, {
      type: "bar",
      data: {
        labels: data.challenges.map((d) => d.label),
        datasets: [
          {
            label: "Reported Constraints",
            data: data.challenges.map((d) => d.count),
            backgroundColor: "#f57c00",
            borderRadius: 6,
          },
        ],
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    });
  }

  // 5. Willingness to Adopt Organic (Bar)
  const willingnessCtx = document.getElementById("chartWillingness");
  if (willingnessCtx && data.willingness_levels.length > 0) {
    new Chart(willingnessCtx, {
      type: "bar",
      data: {
        labels: data.willingness_levels.map((d) => d.label),
        datasets: [
          {
            label: "Respondent Count",
            data: data.willingness_levels.map((d) => d.count),
            backgroundColor: ["#2e7d32", "#66bb6a", "#ffa726", "#e53935"],
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    });
  }

  // 6. Primary Crops (Bar)
  const cropsCtx = document.getElementById("chartCrops");
  if (cropsCtx && data.crops.length > 0) {
    new Chart(cropsCtx, {
      type: "bar",
      data: {
        labels: data.crops.map((d) => d.label),
        datasets: [
          {
            label: "Cultivating Farmers",
            data: data.crops.map((d) => d.count),
            backgroundColor: "#5d4037",
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    });
  }

  // 7. Survey Responses Over Time (Line)
  const timelineCtx = document.getElementById("chartTimeline");
  if (timelineCtx && data.timeline.length > 0) {
    new Chart(timelineCtx, {
      type: "line",
      data: {
        labels: data.timeline.map((d) => d.label),
        datasets: [
          {
            label: "Daily Survey Submissions",
            data: data.timeline.map((d) => d.count),
            borderColor: "#2e7d32",
            backgroundColor: "rgba(46, 125, 50, 0.1)",
            fill: true,
            tension: 0.3,
            pointRadius: 5,
            pointBackgroundColor: "#1b5e20",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    });
  }
}
