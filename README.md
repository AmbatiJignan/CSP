# GreenGrow – Organic Farming Awareness & Farmer Guidance Portal

**GreenGrow** is a 100% frontend-only static web portal dedicated to agricultural education, organic farming awareness, practical agronomic transition guidance, and farmer survey management.

Originally developed with a Python FastAPI and Oracle Database backend, the project has been fully decoupled and converted into a **lightweight, zero-backend, pure HTML5/CSS3/JavaScript static website**. All data persistence, agronomic calculations, survey recording, feedback management, search indexing, and administrative functions operate directly in the client browser using HTML5 `localStorage`.

---

## ✨ Key Features & Functionality

- **Preserved Design & Visual Fidelity**:
  - Exactly preserves the original responsive UI, Bootstrap 5 theme, CSS layout, gradients, typography, and Bootstrap Icons.
  - Smooth mobile responsiveness and desktop viewports.
- **Educational Agronomy Modules**:
  - Principles & definition of organic farming.
  - Soil organic carbon (SOC) and ecological advantages.
  - Balanced analysis of conventional farming risks (product, dose, timing, and management).
  - **9 Detailed Organic Farming Techniques**: Composting, Vermicomposting, FYM, Green Manuring, Crop Rotation, Biofertilisers, Mulching, IPM, and Biological Control with procedures, materials, and precautions.
  - Comprehensive comparison table (Organic vs. Conventional).
  - Phased transition guidance for smallholder farmers.
- **Input Estimation Calculator (`js/calculator.js`)**:
  - 100% client-side calculation: `Estimated Quantity = Cultivated Area × Application Rate`.
  - Supports multiple area units (Acres, Hectares, Gunthas, Sq Meters) and rate units (tonnes/acre, kg/acre, etc.).
  - Step-by-step mathematical formula and agronomic advice dynamically rendered.
- **Farmer Survey Management (Tholukodu Village Field Study)**:
  - Enter, edit, view, and filter genuine farmer questionnaire responses.
  - 100% client-side data management using `localStorage` through `js/data.js`.
  - Client-side CSV export of survey records.
  - Summary analytics and field responses directly reviewable in the browser.
- **Demonstration Admin Dashboard & Analytics (`admin/`)**:
  - Live **Chart.js** visualizations powered directly by `localStorage` data (farming method distribution, input usage, awareness, challenges, willingness).
  - Feedback inbox with status workflow (`New`, `Reviewed`, `Resolved`) and delete actions.
  - Article, FAQ, resource, and video content managers.
  - Role-based demonstration admin access and immutable audit trail.
- **Bilingual Support (`js/translations.js`)**:
  - Instant toggle between **English** and **Telugu (తెలుగు)** with persistent language preferences in `localStorage`.
- **Global Static Search (`search.html`)**:
  - Real-time client-side search query matching across all articles, techniques, and FAQ items.
- **Resource Downloads**:
  - Direct static PDF handbook downloads (`uploads/resources/greengrow_farmer_guidance_handbook.pdf`).

---

## 🚀 How to Run the Website (Using VS Code Live Server)

Because GreenGrow is now a 100% static frontend application, **no Python, FastAPI, Oracle Database, Docker, or Node.js server is needed**.

### Step 1: Open Project in VS Code
Open VS Code and choose **File > Open Folder...**, then select the `CSP-1` root folder.

### Step 2: Install Live Server Extension
1. Click the **Extensions** icon on the left sidebar (or press `Ctrl+Shift+X` / `Cmd+Shift+X`).
2. Search for **Live Server** (by Ritwick Dey).
3. Click **Install**.

### Step 3: Launch the Website
1. In the VS Code file explorer, right-click **`index.html`**.
2. Click **Open with Live Server** (or click the **Go Live** button in the bottom status bar).
3. The website will open automatically in your browser at:
   ```
   http://127.0.0.1:5500/index.html
   ```

*(Alternatively, you can double-click `index.html` to open it directly as a local file, or use Python's built-in static server with `python -m http.server 8000`).*

---

## 🔐 Demonstration Admin Portal

- **Login URL**: `admin/login.html`
- **Default Demonstration Credentials**:
  - **Username**: `admin`
  - **Password**: `admin123` (or any password; client-side simulation)
  - **Role**: `superadmin`
- All created surveys, articles, FAQs, feedback items, and users persist safely in browser `localStorage`. To reset back to default sample records, open browser DevTools Console and run `DataStore.reset()`.

---

## 📁 Project Structure

```
GreenGrow/
│
├── index.html                           # Home page
├── about.html                           # About the GreenGrow portal & field study
├── advantages.html                      # Organic farming advantages & SOC science
├── conventional-risks.html              # Conventional farming risk analysis
├── techniques.html                      # 9 Practical organic techniques
├── comparison.html                      # Organic vs Conventional comparative analysis
├── guidance.html                        # Farmer transition guidance
├── calculator.html                      # Organic input requirement calculator
├── resources.html                       # Guides, manuals, and PDF downloads
├── videos.html                          # Educational video library
├── faqs.html                            # Frequently asked questions with category filter
├── contact.html                         # Contact & farmer feedback form
├── search.html                          # Static content search
├── 404.html                             # Not found error page
│
├── admin/                               # Demonstration Admin Portal
│   ├── login.html                       # Admin sign-in demonstration
│   ├── dashboard.html                   # Analytics charts and metrics overview
│   ├── surveys.html                     # Farmer survey responses list & CSV export
│   ├── survey_form.html                 # Add/Edit farmer survey response
│   ├── survey_detail.html               # Individual survey response viewer
│   ├── articles.html                    # Manage educational articles
│   ├── article_form.html                # Add/Edit article
│   ├── resources.html                   # Manage PDF guides & documents
│   ├── videos.html                      # Manage educational video links
│   ├── faqs.html                        # Manage FAQs
│   ├── feedback.html                    # Feedback messages inbox & status manager
│   ├── users.html                       # Manage admin user accounts
│   └── audit_logs.html                  # Administrative activity audit trail
│
├── articles/                            # Static article pages
│   ├── restoring-soil-organic-carbon.html
│   ├── botanical-formulations-neemastra-agniastra.html
│   └── biofertilisers-vs-chemical-nutrients.html
│
├── css/                                 # Preserved CSS Stylesheets
│   ├── style.css                        # Public portal styling
│   └── admin.css                        # Admin dashboard & controls styling
│
├── js/                                  # Pure Client-Side JavaScript
│   ├── data.js                          # Static seed data & LocalStorage DataStore
│   ├── main.js                          # Navigation, search, i18n & feedback handling
│   ├── calculator.js                    # Agricultural input calculator engine
│   ├── admin.js                         # Admin authentication & Chart.js rendering
│   └── translations.js                  # English & Telugu translation strings
│
├── images/                              # Images and visual assets
│
├── uploads/                             # Downloadable assets
│   ├── resources/
│   │   └── greengrow_farmer_guidance_handbook.pdf
│   └── articles/
│
└── README.md                            # Documentation and setup instructions
```
