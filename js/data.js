/**
 * GreenGrow - Static Data Store
 * Provides offline seed data for articles, faqs, videos, resources, surveys, and admin users.
 * Automatically synchronizes with browser localStorage for realistic interactivity.
 */

const DEFAULT_ARTICLES = [
  {
    id: 1,
    title: "Restoring Soil Organic Carbon: The Biological Engine of Farm Fertility",
    slug: "restoring-soil-organic-carbon",
    category: "Soil Health & Humus",
    category_slug: "soil-health",
    summary: "Soil organic carbon is the single most critical determinant of farm productivity and water conservation in dryland agriculture.",
    content: `Soil organic carbon (SOC) represents the biological backbone of fertile land. When soils drop below 0.5% organic carbon, synthetic fertilisers lose their efficiency because there is insufficient microbial activity to hold and transform soluble nutrients.

Building SOC requires three continuous steps:
1. Return all crop residues rather than burning stubble.
2. Apply 3 to 5 tonnes of well-cured compost or FYM every year.
3. Grow short-duration green manures (Sunnhemp or Dhaincha) during fallow windows.

Within 2 to 3 years of consistent organic matter addition, farmers in dryland tracts observe improved soil aggregate stability, noticeable earthworm activity, and superior moisture retention during dry spells.`,
    author: "Dr. K. S. Rao, Agronomist",
    created_at: "2026-10-15",
    view_count: 142,
    is_published: true,
    is_featured: true,
    image_url: ""
  },
  {
    id: 2,
    title: "Botanical Formulations: Preparing Neemastra and Agniastra on the Farm",
    slug: "botanical-formulations-neemastra-agniastra",
    category: "Ecological Pest Defense",
    category_slug: "pest-defense",
    summary: "A practical recipe guide for creating effective, zero-chemical botanical pest decoctions using native ingredients.",
    content: `Botanical decoctions offer potent, eco-friendly pest suppression without destroying predatory spiders or honeybees.

Neemastra Recipe (For Sucking Pests and Small Caterpillars):
• 5 kg crushed neem leaves or 5 kg crushed neem seed powder.
• 5 litres indigenous cow urine.
• 2 kg fresh cow dung.
• 100 litres water.
Ferment for 48 hours under shade while stirring clockwise twice daily. Filter through cotton cloth and spray directly without dilution.

Agniastra Recipe (For Severe Borer and Leaf Miner Attacks):
• 1 kg crushed garlic, 500g hot green chillies, 500g ginger paste, 5 kg crushed neem leaves.
• Boil in 10 litres cow urine until reduced by half. Dilute 2 litres of filtered extract in 100 litres water for field application.`,
    author: "GreenGrow Agro-Ecology Team",
    created_at: "2026-10-22",
    view_count: 98,
    is_published: true,
    is_featured: true,
    image_url: ""
  },
  {
    id: 3,
    title: "Biofertilisers vs Chemical Nutrients: Understanding Microbial Dynamics",
    slug: "biofertilisers-vs-chemical-nutrients",
    category: "Organic Inputs & Biofertilisers",
    category_slug: "organic-inputs",
    summary: "How beneficial microbial inoculants fix atmospheric nitrogen and solubilise fixed phosphorus in the root rhizosphere.",
    content: `Unlike synthetic chemical fertilisers that provide instant soluble salts, biofertilisers are living microbial inoculants that colonise plant roots and work symbiotically throughout the crop growth cycle.

1. Rhizobium: Forms active nodules on pulse and legume roots, converting atmospheric nitrogen (N2) into plant-absorbable ammonium.
2. Azospirillum & Azotobacter: Free-living nitrogen fixers ideal for cereals such as paddy, millets, and maize.
3. Phosphobacteria (PSB): Secretes organic acids that dissolve insoluble tricalcium phosphate bound in clay soils, liberating bio-available phosphorus.

Proper application tip: Always mix biofertiliser powders with moist vermicompost or compost; avoid direct sunlight exposure, and apply to seeds or planting furrows promptly.`,
    author: "GreenGrow Scientific Desk",
    created_at: "2026-11-01",
    view_count: 76,
    is_published: true,
    is_featured: false,
    image_url: ""
  }
];

const DEFAULT_FAQS = [
  {
    id: 1,
    category: "Transition",
    question: "Will my crop yield drop if I immediately switch to organic farming?",
    answer: "A modest yield dip of 10% to 20% can occur during the first 1 to 2 transition seasons if chemical fertilisers are withdrawn abruptly without prior soil organic matter replenishment. We recommend a phased transition: convert 25% to 33% of your acreage per year while applying heavy basal compost and green manure.",
    display_order: 1,
    is_published: true
  },
  {
    id: 2,
    category: "Composting",
    question: "How can I tell when my compost pile is fully mature and safe to apply?",
    answer: "Mature compost is dark brown or black, crumbly to the touch, and possesses a pleasant earthy smell like forest soil. Its internal temperature will have cooled to ambient air temperature, and original plant stalks will be indistinguishable.",
    display_order: 2,
    is_published: true
  },
  {
    id: 3,
    category: "Pest Control",
    question: "Are organic botanical sprays safe for bees and earthworms?",
    answer: "Yes. Botanical extracts like Neem Seed Kernel Extract (NSKE) act primarily as antifeedants and oviposition deterrents for chewing and sucking crop pests. Unlike broad-spectrum synthetic organophosphates, they do not harm honeybees or earthworms when applied at recommended concentrations.",
    display_order: 3,
    is_published: true
  },
  {
    id: 4,
    category: "Certification",
    question: "What is PGS-India certification for smallholder farmers?",
    answer: "Participatory Guarantee System for India (PGS-India) is a decentralised organic certification programme implemented by the Ministry of Agriculture. It allows groups of local farmers to inspect each other's fields and certify produce without incurring costly commercial third-party audit fees.",
    display_order: 4,
    is_published: true
  },
  {
    id: 5,
    category: "Water",
    question: "Does organic farming really save water?",
    answer: "Yes. Studies demonstrate that soils rich in organic matter can retain 20% to 30% more moisture compared to degraded soils. Organic mulching also cuts surface evaporation by more than half, enabling crops to survive dry spells.",
    display_order: 5,
    is_published: true
  }
];

const DEFAULT_VIDEOS = [
  {
    id: 1,
    title: "Aerobic Windrow Composting Field Demonstration",
    description: "Step-by-step tutorial on constructing and aerating farm waste compost windrows.",
    category: "Composting",
    video_url: "https://www.youtube.com/watch?v=H_qUZaqhcPM",
    thumbnail_url: "",
    duration_minutes: 15,
    display_order: 1,
    is_published: true
  },
  {
    id: 2,
    title: "Preparing Jeevamrutham Bio-Stimulant",
    description: "Practical demonstration of mixing indigenous cow dung, urine, jaggery, and pulse flour for soil inoculation.",
    category: "Biofertilisers",
    video_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    thumbnail_url: "",
    duration_minutes: 12,
    display_order: 2,
    is_published: true
  },
  {
    id: 3,
    title: "Integrated Pest Management & Trap Crops",
    description: "How to install yellow sticky cards, pheromone traps, and border marigold plantings.",
    category: "Pest Control",
    video_url: "https://www.youtube.com/watch?v=CELaZ62mkfY",
    thumbnail_url: "",
    duration_minutes: 18,
    display_order: 3,
    is_published: true
  }
];

const DEFAULT_RESOURCES = [
  {
    id: 1,
    title: "GreenGrow Farmer Guidance Handbook (PDF)",
    description: "Comprehensive printable field manual detailing composting, vermiculture, and biological pest defense.",
    category: "Guides",
    file_name: "greengrow_farmer_guidance_handbook.pdf",
    file_path: "uploads/resources/greengrow_farmer_guidance_handbook.pdf",
    file_size_bytes: 12288,
    file_type: "pdf",
    download_count: 38,
    created_at: "2026-11-07",
    is_published: true
  }
];

const DEFAULT_SURVEYS = [
  {
    id: 1,
    respondent_code: "TK-01",
    village: "Tholukodu",
    survey_date: "2026-10-18",
    farming_experience_years: 22,
    land_holding_acres: 3.5,
    primary_crops: "Paddy, Groundnut",
    farming_method: "Partially Organic",
    awareness_level: "Moderate",
    willingness_to_adopt: "Highly Willing",
    organic_input_usage: "FYM, Neem Oil",
    knowledge_of_advantages: "Improves soil softness, reduces fertilizer bills",
    primary_challenges: "Availability of quality organic manure in peak season",
    support_needed: "Training on on-farm composting & bio-control",
    surveyor_name: "Field Team A",
    additional_comments: "Keen to establish vermicompost bed if technical support is provided.",
    consent_confirmed: true
  },
  {
    id: 2,
    respondent_code: "TK-02",
    village: "Tholukodu",
    survey_date: "2026-10-19",
    farming_experience_years: 15,
    land_holding_acres: 5.0,
    primary_crops: "Cotton, Red Gram",
    farming_method: "Conventional",
    awareness_level: "Basic",
    willingness_to_adopt: "Willing with Support",
    organic_input_usage: "None",
    knowledge_of_advantages: "Aware of health benefits for farm workers",
    primary_challenges: "Pest attack vulnerability during bollworm season",
    support_needed: "Biopesticide formulation demonstrations",
    surveyor_name: "Field Team A",
    additional_comments: "Concerned about initial yield reduction in year 1.",
    consent_confirmed: true
  },
  {
    id: 3,
    respondent_code: "TK-03",
    village: "Tholukodu",
    survey_date: "2026-10-21",
    farming_experience_years: 30,
    land_holding_acres: 2.0,
    primary_crops: "Millets, Vegetables",
    farming_method: "Fully Organic",
    awareness_level: "High",
    willingness_to_adopt: "Highly Willing",
    organic_input_usage: "FYM, Vermicompost, Jeevamrutham, Neemastra",
    knowledge_of_advantages: "Zero chemical expenses, premium vegetable prices in local weekly market",
    primary_challenges: "Labor requirement for continuous weeding",
    support_needed: "Mulch sheet subsidy & seed saver network",
    surveyor_name: "Field Team B",
    additional_comments: "Successfully practicing organic farming for over 4 years.",
    consent_confirmed: true
  },
  {
    id: 4,
    respondent_code: "TK-04",
    village: "Tholukodu",
    survey_date: "2026-10-22",
    farming_experience_years: 10,
    land_holding_acres: 4.2,
    primary_crops: "Paddy, Black Gram",
    farming_method: "Partially Organic",
    awareness_level: "Moderate",
    willingness_to_adopt: "Willing with Support",
    organic_input_usage: "Compost, Panchagavya",
    knowledge_of_advantages: "Better grain storage longevity without insect damage",
    primary_challenges: "Market access and certification process",
    support_needed: "PGS-India group registration guidance",
    surveyor_name: "Field Team B",
    additional_comments: "Wants to form a farmers' collective with adjacent plot owners.",
    consent_confirmed: true
  },
  {
    id: 5,
    respondent_code: "TK-05",
    village: "Tholukodu",
    survey_date: "2026-10-24",
    farming_experience_years: 18,
    land_holding_acres: 6.0,
    primary_crops: "Chilli, Groundnut",
    farming_method: "Conventional",
    awareness_level: "Basic",
    willingness_to_adopt: "Undecided",
    organic_input_usage: "Occasional FYM",
    knowledge_of_advantages: "Soil health rejuvenation",
    primary_challenges: "High cost of manual labor, fear of pest epidemics",
    support_needed: "Demonstration plot in village",
    surveyor_name: "Field Team A",
    additional_comments: "Willing to convert 0.5 acre as trial if inputs are supplied.",
    consent_confirmed: true
  }
];

const DEFAULT_FEEDBACK = [
  {
    id: 1,
    name: "Ramesh Naidu",
    email: "ramesh.farmer@example.com",
    phone: "+91 98480 12345",
    subject: "Guidance on Jeevamrutham application schedule",
    message: "I have prepared 200L of Jeevamrutham for 2 acres of groundnut. Please advise the best time of day and frequency for flow irrigation.",
    status: "New",
    created_at: "2026-11-08 09:30",
    admin_notes: ""
  },
  {
    id: 2,
    name: "Anitha Devi",
    email: "anitha.d@example.com",
    phone: "+91 94401 54321",
    subject: "Request for PGS Certification training in Tholukodu",
    message: "A group of 8 women farmers in our self-help group wish to register for PGS-India organic certification. Can you conduct an orientation?",
    status: "Reviewed",
    created_at: "2026-11-06 14:15",
    admin_notes: "Connected with District Agricultural Extension Coordinator."
  }
];

const DEFAULT_USERS = [
  {
    id: 1,
    username: "admin",
    full_name: "GreenGrow Project Administrator",
    email: "admin@greengrow.org",
    role: "superadmin",
    is_active: true,
    last_login: "2026-11-10 18:30"
  },
  {
    id: 2,
    username: "editor1",
    full_name: "Dr. K. S. Rao",
    email: "editor@greengrow.org",
    role: "editor",
    is_active: true,
    last_login: "2026-11-09 11:20"
  }
];

const DEFAULT_AUDIT_LOGS = [
  {
    id: 1,
    created_at: "2026-11-10 18:30:15",
    admin_username: "admin",
    action: "LOGIN",
    target_entity: "AUTH",
    target_id: "1",
    details: "Superadmin logged in successfully",
    ip_address: "127.0.0.1"
  },
  {
    id: 2,
    created_at: "2026-11-08 14:22:40",
    admin_username: "admin",
    action: "CREATE",
    target_entity: "SURVEY",
    target_id: "TK-05",
    details: "New farmer survey record TK-05 saved",
    ip_address: "127.0.0.1"
  },
  {
    id: 3,
    created_at: "2026-11-07 10:15:00",
    admin_username: "admin",
    action: "UPLOAD",
    target_entity: "RESOURCE",
    target_id: "1",
    details: "Uploaded GreenGrow Farmer Guidance Handbook (PDF)",
    ip_address: "127.0.0.1"
  }
];

// Helper functions for LocalStorage Data Management
const DataStore = {
  getArticles() {
    const raw = localStorage.getItem("greengrow_articles");
    if (!raw) {
      localStorage.setItem("greengrow_articles", JSON.stringify(DEFAULT_ARTICLES));
      return DEFAULT_ARTICLES;
    }
    return JSON.parse(raw);
  },
  saveArticles(items) {
    localStorage.setItem("greengrow_articles", JSON.stringify(items));
  },

  getFaqs() {
    const raw = localStorage.getItem("greengrow_faqs");
    if (!raw) {
      localStorage.setItem("greengrow_faqs", JSON.stringify(DEFAULT_FAQS));
      return DEFAULT_FAQS;
    }
    return JSON.parse(raw);
  },
  saveFaqs(items) {
    localStorage.setItem("greengrow_faqs", JSON.stringify(items));
  },

  getVideos() {
    const raw = localStorage.getItem("greengrow_videos");
    if (!raw) {
      localStorage.setItem("greengrow_videos", JSON.stringify(DEFAULT_VIDEOS));
      return DEFAULT_VIDEOS;
    }
    return JSON.parse(raw);
  },
  saveVideos(items) {
    localStorage.setItem("greengrow_videos", JSON.stringify(items));
  },

  getResources() {
    const raw = localStorage.getItem("greengrow_resources");
    if (!raw) {
      localStorage.setItem("greengrow_resources", JSON.stringify(DEFAULT_RESOURCES));
      return DEFAULT_RESOURCES;
    }
    return JSON.parse(raw);
  },
  saveResources(items) {
    localStorage.setItem("greengrow_resources", JSON.stringify(items));
  },

  getSurveys() {
    const raw = localStorage.getItem("greengrow_surveys");
    if (!raw) {
      localStorage.setItem("greengrow_surveys", JSON.stringify(DEFAULT_SURVEYS));
      return DEFAULT_SURVEYS;
    }
    return JSON.parse(raw);
  },
  saveSurveys(items) {
    localStorage.setItem("greengrow_surveys", JSON.stringify(items));
  },

  getFeedback() {
    const raw = localStorage.getItem("greengrow_feedback");
    if (!raw) {
      localStorage.setItem("greengrow_feedback", JSON.stringify(DEFAULT_FEEDBACK));
      return DEFAULT_FEEDBACK;
    }
    return JSON.parse(raw);
  },
  saveFeedback(items) {
    localStorage.setItem("greengrow_feedback", JSON.stringify(items));
  },

  getUsers() {
    const raw = localStorage.getItem("greengrow_users");
    if (!raw) {
      localStorage.setItem("greengrow_users", JSON.stringify(DEFAULT_USERS));
      return DEFAULT_USERS;
    }
    return JSON.parse(raw);
  },
  saveUsers(items) {
    localStorage.setItem("greengrow_users", JSON.stringify(items));
  },

  getAuditLogs() {
    const raw = localStorage.getItem("greengrow_audit_logs");
    if (!raw) {
      localStorage.setItem("greengrow_audit_logs", JSON.stringify(DEFAULT_AUDIT_LOGS));
      return DEFAULT_AUDIT_LOGS;
    }
    return JSON.parse(raw);
  },
  logAudit(action, entity, targetId, details) {
    const logs = this.getAuditLogs();
    const newEntry = {
      id: Date.now(),
      created_at: new Date().toISOString().replace('T', ' ').substring(0, 19),
      admin_username: "admin",
      action: action,
      target_entity: entity,
      target_id: String(targetId || '-'),
      details: details,
      ip_address: "127.0.0.1 (Frontend Demo)"
    };
    logs.unshift(newEntry);
    localStorage.setItem("greengrow_audit_logs", JSON.stringify(logs));
  }
};
