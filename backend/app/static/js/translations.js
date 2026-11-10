/**
 * GreenGrow - Bilingual Language Support (English & Telugu)
 * Provides comprehensive translations with persistent local storage.
 */

const translations = {
  en: {
    // Navigation
    nav_home: "Home",
    nav_about: "About Organic",
    nav_advantages: "Advantages",
    nav_risks: "Conventional Risks",
    nav_techniques: "Techniques",
    nav_comparison: "Comparison",
    nav_guidance: "Farmer Guidance",
    nav_calculator: "Input Calculator",
    nav_resources: "Resources",
    nav_faqs: "FAQs",
    nav_videos: "Video Library",
    nav_contact: "Contact & Feedback",
    nav_admin: "Admin Portal",
    nav_search_placeholder: "Search articles, guides...",

    // Hero
    hero_badge: "Sustainable Agriculture & Farmer Guidance",
    hero_title: "Cultivating Healthy Soils, Sustaining Future Generations",
    hero_subtitle: "GreenGrow is an educational portal dedicated to organic farming awareness, soil health rejuvenation, water conservation, and actionable guidance for rural farmers.",
    hero_btn_explore: "Explore Techniques",
    hero_btn_calculator: "Input Calculator",

    // Home highlights
    hl_soil_title: "Soil Vitality Rebuilding",
    hl_soil_desc: "Nurturing microbial diversity, organic carbon, and earthworm activity with natural organic inputs.",
    hl_water_title: "Water Conservation",
    hl_water_desc: "Enhancing soil water retention capacity by up to 30%, mitigating drought impacts and runoff erosion.",
    hl_health_title: "Chemical-Free Harvest",
    hl_health_desc: "Safeguarding farm families and consumers from synthetic residues while preserving pollinator biodiversity.",
    hl_fair_title: "Practical & Fair Education",
    hl_fair_desc: "Balanced agro-ecological insights grounded in real village field experiences from Tholukodu.",

    // Calculator
    calc_title: "Organic Input Estimation Calculator",
    calc_subtitle: "Calculate estimated organic manure, compost, or biofertiliser quantity needed based on your crop-specific application rate.",
    calc_area_label: "Cultivated Area",
    calc_unit_label: "Area Unit",
    calc_rate_label: "Recommended Application Rate",
    calc_rate_unit_label: "Rate Unit",
    calc_input_type: "Input Type",
    calc_btn: "Calculate Estimated Quantity",
    calc_result_heading: "Estimated Organic Input Requirement",
    calc_disclaimer: "Disclaimer: Application rates must follow trusted crop and soil test recommendations.",

    // Footer
    footer_tagline: "Empowering communities through sustainable agriculture and genuine field research.",
    footer_quick_links: "Quick Navigation",
    footer_resources: "Knowledge Library",
    footer_contact_info: "Field Research Office",
    footer_copyright: "All rights reserved. Dedicated to the farmers of Tholukodu village.",
  },
  te: {
    // Navigation
    nav_home: "హోమ్ (Home)",
    nav_about: "సేంద్రియ వ్యవసాయం గురించి",
    nav_advantages: "ప్రయోజనాలు",
    nav_risks: "రసాయన సేద్య నష్టాలు",
    nav_techniques: "పద్ధతులు & విధానాలు",
    nav_comparison: "పోలిక పట్టిక",
    nav_guidance: "రైతు మార్గదర్శి",
    nav_calculator: "ఎరువుల కాలిక్యులేటర్",
    nav_resources: "వనరులు & పీడీఎఫ్",
    nav_faqs: "ప్రశ్నోత్తరాలు (FAQs)",
    nav_videos: "వీడియోల లైబ్రరీ",
    nav_contact: "సంప్రదించండి & అభిప్రాయం",
    nav_admin: "అడ్మిన్ పోర్టల్",
    nav_search_placeholder: "వ్యాసాలు, సమాచారం వెతకండి...",

    // Hero
    hero_badge: "సుస్థిర వ్యవసాయం మరియు రైతు మార్గదర్శి",
    hero_title: "ఆరోగ్యకరమైన నేలలు - సుసంపన్నమైన భవిష్యత్ తరాలు",
    hero_subtitle: "గ్రీన్ గ్రో అనేది సేంద్రియ వ్యవసాయ అవగాహన, నేల ఆరోగ్యం, నీటి సంరక్షణ మరియు గ్రామీణ రైతుల మార్గదర్శనం కోసం రూపొందించబడిన విద్యా పోర్టల్.",
    hero_btn_explore: "పద్ధతులు చూడండి",
    hero_btn_calculator: "ఎరువుల కాలిక్యులేటర్",

    // Home highlights
    hl_soil_title: "నేల జీవకళ పెంపు",
    hl_soil_desc: "సహజ ఎరువులతో నేలలో సూక్ష్మజీవులు, సేంద్రియ కర్బనం మరియు వానపాముల సంఖ్యను పెంచుతుంది.",
    hl_water_title: "నీటి సంరక్షణ సామర్థ్యం",
    hl_water_desc: "నేలలో తేమ నిల్వ సామర్థ్యాన్ని 30% వరకు పెంచి, వర్షాభావ పరిస్థితులను తట్టుకునేలా చేస్తుంది.",
    hl_health_title: "రసాయన రహిత పంటలు",
    hl_health_desc: "రైతులు మరియు వినియోగదారుల ఆరోగ్యాన్ని కాపాడుతూ, మిత్ర పురుగులను సంరక్షిస్తుంది.",
    hl_fair_title: "ప్రాక్టికల్ సమాచారం",
    hl_fair_desc: "తోలుకోడు గ్రామ క్షేత్రస్థాయి అనుభవాలతో కూడిన వాస్తవ మరియు శాస్త్రీయ మార్గదర్శనం.",

    // Calculator
    calc_title: "సేంద్రియ ఎరువుల అంచనా కాలిక్యులేటర్",
    calc_subtitle: "మీ పొలం విస్తీర్ణం మరియు సిఫార్సు చేసిన మోతాదు ఆధారంగా అవసరమైన సేంద్రియ ఎరువుల పరిమాణాన్ని లెక్కించండి.",
    calc_area_label: "సాగు విస్తీర్ణం",
    calc_unit_label: "విస్తీర్ణ కొలత",
    calc_rate_label: "సిఫార్సు మోతాదు (ఎకరాకు/హెక్టారుకు)",
    calc_rate_unit_label: "మోతాదు కొలత",
    calc_input_type: "ఎరువు రకం",
    calc_btn: "అవసరమైన పరిమాణం లెక్కించు",
    calc_result_heading: "అవసరమైన సేంద్రియ ఎరువుల అంచనా",
    calc_disclaimer: "గమనిక: పంట రకం మరియు భూసార పరీక్ష ఆధారంగా మాత్రమే సిఫార్సు మోతాదులను నిర్ణయించుకోవాలి.",

    // Footer
    footer_tagline: "సుస్థిర వ్యవసాయం మరియు గ్రామీణ విజ్ఞాన వ్యాప్తికి అంకితం.",
    footer_quick_links: "ముఖ్యమైన లింకులు",
    footer_resources: "విజ్ఞాన వనరులు",
    footer_contact_info: "క్షేత్ర పరిశోధన విభాగం",
    footer_copyright: "సర్వహక్కులు ప్రత్యేకించబడ్డాయి. తోలుకోడు గ్రామ రైతులకు అంకితం.",
  }
};

function getCurrentLanguage() {
  return localStorage.getItem("greengrow_lang") || "en";
}

function setLanguage(lang) {
  if (!translations[lang]) lang = "en";
  localStorage.setItem("greengrow_lang", lang);

  // Update text of elements with data-i18n attribute
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (translations[lang][key]) {
      el.textContent = translations[lang][key];
    }
  });

  // Update placeholders
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (translations[lang][key]) {
      el.placeholder = translations[lang][key];
    }
  });

  // Update button active state
  document.querySelectorAll(".lang-switch-btn").forEach((btn) => {
    if (btn.getAttribute("data-lang") === lang) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const currentLang = getCurrentLanguage();
  setLanguage(currentLang);

  document.querySelectorAll(".lang-switch-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const selectedLang = btn.getAttribute("data-lang");
      setLanguage(selectedLang);
    });
  });
});
