/**
 * GreenGrow - Main Public JavaScript
 * Handles contact forms, dynamic interactivity, and UI notifications.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Contact & Feedback Form Handler
  const feedbackForm = document.getElementById("publicFeedbackForm");
  const feedbackNotice = document.getElementById("feedbackNoticeContainer");

  if (feedbackForm) {
    feedbackForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const submitBtn = feedbackForm.querySelector("button[type='submit']");
      const originalBtnText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span>Submitting...`;

      const payload = {
        name: document.getElementById("fbName")?.value || null,
        email: document.getElementById("fbEmail")?.value || null,
        phone: document.getElementById("fbPhone")?.value || null,
        subject: document.getElementById("fbSubject").value,
        message: document.getElementById("fbMessage").value,
      };

      try {
        const response = await fetch("/api/v1/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errData = await response.json().catch(() => ({}));
          throw new Error(errData.detail || "Feedback submission failed.");
        }

        feedbackForm.reset();
        if (feedbackNotice) {
          feedbackNotice.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show shadow-sm" role="alert">
              <i class="bi bi-check-circle-fill me-2 fs-5"></i>
              <strong>Thank You!</strong> Your feedback has been received and securely stored in our Oracle database. Our agricultural advisory team will review it shortly.
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
    });
  }
});
