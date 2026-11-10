#!/usr/bin/env python3
"""
GreenGrow - Initial Educational Data & Admin Account Seeder
Seeds default administrator, educational categories, articles, FAQs, and sample resource guides.
IMPORTANT: Strictly complies with the requirement NOT to fabricate or pre-populate farmer survey data.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from app.core.config import settings
from app.core.security import hash_password
from app.database.connection import SessionLocal
from app.models.user import AdminUser
from app.models.article import ArticleCategory, Article
from app.models.faq import FAQ
from app.models.video import EducationalVideo
from app.models.resource import Resource
from app.models.announcement import Announcement
from app.models.survey import SurveyResponse


def generate_sample_pdf(dest_path: Path):
    """Generates a sample educational PDF guide for the resource library."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(dest_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("GreenGrow - Farmer Guidance Handbook", styles["Title"]),
        Spacer(1, 12),
        Paragraph("Practical Field Guide to On-Farm Composting & Organic Input Preparation", styles["Heading2"]),
        Spacer(1, 8),
        Paragraph(
            "This educational document provides smallholder farmers with practical instructions "
            "for aerobic windrow composting, vermiculture bed management, and traditional liquid inoculants "
            "(Jeevamrutham). Produced for rural agricultural development initiatives in Tholukodu village.",
            styles["BodyText"],
        ),
        Spacer(1, 12),
        Paragraph("Key Soil Health Recommendations:", styles["Heading3"]),
        Paragraph("1. Incorporate 4 to 5 tonnes of cured FYM per acre prior to pre-monsoon sowing.", styles["Normal"]),
        Paragraph("2. Treat legume seeds with Rhizobium culture (200g per 10kg seed) with rice starch slurry.", styles["Normal"]),
        Paragraph("3. Maintain 50% continuous mulch cover using dry crop residue to retain soil moisture.", styles["Normal"]),
    ]
    doc.build(story)


def seed():
    db = SessionLocal()
    print("=" * 65)
    print("Seeding Initial GreenGrow Data into Oracle Database 23ai...")
    print("=" * 65)

    try:
        # 1. Seed Superadmin User
        admin_user = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        if not admin_user:
            admin_user = AdminUser(
                username="admin",
                email="admin@greengrow.org",
                hashed_password=hash_password("AdminPass123!"),
                full_name="GreenGrow Project Administrator",
                role="superadmin",
                is_active=True,
            )
            db.add(admin_user)
            db.commit()
            print("[✓] Created default superadmin account: admin / AdminPass123!")
        else:
            print("[i] Superadmin account 'admin' already exists.")

        # 2. Seed Article Categories
        categories_data = [
            ("Soil Health & Humus", "soil-health", "Techniques for restoring soil organic carbon and microflora.", 1),
            ("Organic Inputs & Biofertilisers", "organic-inputs", "Preparation and usage of composts, biofertilisers, and liquid manure.", 2),
            ("Ecological Pest Defense", "pest-defense", "Natural pest repellents, trap crops, and biological controls.", 3),
            ("Water & Climate Resilience", "water-resilience", "Water conservation, mulching, and drought mitigation.", 4),
            ("Crop Advisory & Transition", "crop-advisory", "Phased transition schedules and crop rotation planning.", 5),
        ]

        cat_map = {}
        for name, slug, desc, order in categories_data:
            cat = db.query(ArticleCategory).filter(ArticleCategory.slug == slug).first()
            if not cat:
                cat = ArticleCategory(name=name, slug=slug, description=desc, display_order=order)
                db.add(cat)
                db.commit()
                db.refresh(cat)
            cat_map[slug] = cat.id
        print(f"[✓] Verified {len(categories_data)} article categories.")

        # 3. Seed Educational Articles
        articles_data = [
            {
                "title": "Restoring Soil Organic Carbon: The Biological Engine of Farm Fertility",
                "slug": "restoring-soil-organic-carbon",
                "category_id": cat_map.get("soil-health"),
                "summary": "Soil organic carbon is the single most critical determinant of farm productivity and water conservation in dryland agriculture.",
                "content": (
                    "Soil organic carbon (SOC) represents the biological backbone of fertile land. When soils drop below 0.5% organic carbon, synthetic fertilisers lose their efficiency because there is insufficient microbial activity to hold and transform soluble nutrients.\n\n"
                    "Building SOC requires three continuous steps:\n"
                    "1. Return all crop residues rather than burning stubble.\n"
                    "2. Apply 3 to 5 tonnes of well-cured compost or FYM every year.\n"
                    "3. Grow short-duration green manures (Sunnhemp or Dhaincha) during fallow windows.\n\n"
                    "Within 2 to 3 years of consistent organic matter addition, farmers in dryland tracts observe improved soil aggregate stability, noticeable earthworm activity, and superior moisture retention during dry spells."
                ),
                "author": "Dr. K. S. Rao, Agronomist",
                "is_published": True,
                "is_featured": True,
            },
            {
                "title": "Botanical Formulations: Preparing Neemastra and Agniastra on the Farm",
                "slug": "botanical-formulations-neemastra-agniastra",
                "category_id": cat_map.get("pest-defense"),
                "summary": "A practical recipe guide for creating effective, zero-chemical botanical pest decoctions using native ingredients.",
                "content": (
                    "Botanical decoctions offer potent, eco-friendly pest suppression without destroying predatory spiders or honeybees.\n\n"
                    "Neemastra Recipe (For Sucking Pests and Small Caterpillars):\n"
                    "• 5 kg crushed neem leaves or 5 kg crushed neem seed powder.\n"
                    "• 5 litres indigenous cow urine.\n"
                    "• 2 kg fresh cow dung.\n"
                    "• 100 litres water.\n"
                    "Ferment for 48 hours under shade while stirring clockwise twice daily. Filter through cotton cloth and spray directly without dilution.\n\n"
                    "Agniastra Recipe (For Severe Borer and Leaf Miner Attacks):\n"
                    "• 1 kg crushed garlic, 500g hot green chillies, 500g ginger paste, 5 kg crushed neem leaves.\n"
                    "• Boil in 10 litres cow urine until reduced by half. Dilute 2 litres of filtered extract in 100 litres water for field application."
                ),
                "author": "GreenGrow Agro-Ecology Team",
                "is_published": True,
                "is_featured": True,
            },
            {
                "title": "Biofertilisers vs Chemical Nutrients: Understanding Microbial Dynamics",
                "slug": "biofertilisers-vs-chemical-nutrients",
                "category_id": cat_map.get("organic-inputs"),
                "summary": "How beneficial microbial inoculants fix atmospheric nitrogen and solubilise fixed phosphorus in the root rhizosphere.",
                "content": (
                    "Unlike synthetic chemical fertilisers that provide instant soluble salts, biofertilisers are living microbial inoculants that colonise plant roots and work symbiotically throughout the crop growth cycle.\n\n"
                    "1. Rhizobium: Forms active nodules on pulse and legume roots, converting atmospheric nitrogen (N2) into plant-absorbable ammonium.\n"
                    "2. Azospirillum & Azotobacter: Free-living nitrogen fixers ideal for cereals such as paddy, millets, and maize.\n"
                    "3. Phosphobacteria (PSB): Secretes organic acids that dissolve insoluble tricalcium phosphate bound in clay soils, liberating bio-available phosphorus.\n\n"
                    "Proper application tip: Always mix biofertiliser powders with moist vermicompost or compost; avoid direct sunlight exposure, and apply to seeds or planting furrows promptly."
                ),
                "author": "GreenGrow Scientific Desk",
                "is_published": True,
                "is_featured": False,
            },
        ]

        for art in articles_data:
            existing = db.query(Article).filter(Article.slug == art["slug"]).first()
            if not existing:
                new_art = Article(**art)
                db.add(new_art)
                db.commit()
        print(f"[✓] Verified {len(articles_data)} educational articles.")

        # 4. Seed FAQs
        faqs_data = [
            ("Transition", "Will my crop yield drop if I immediately switch to organic farming?", "A modest yield dip of 10% to 20% can occur during the first 1 to 2 transition seasons if chemical fertilisers are withdrawn abruptly without prior soil organic matter replenishment. We recommend a phased transition: convert 25% to 33% of your acreage per year while applying heavy basal compost and green manure.", 1),
            ("Composting", "How can I tell when my compost pile is fully mature and safe to apply?", "Mature compost is dark brown or black, crumbly to the touch, and possesses a pleasant earthy smell like forest soil. Its internal temperature will have cooled to ambient air temperature, and original plant stalks will be indistinguishable.", 2),
            ("Pest Control", "Are organic botanical sprays safe for bees and earthworms?", "Yes. Botanical extracts like Neem Seed Kernel Extract (NSKE) act primarily as antifeedants and oviposition deterrents for chewing and sucking crop pests. Unlike broad-spectrum synthetic organophosphates, they do not harm honeybees or earthworms when applied at recommended concentrations.", 3),
            ("Certification", "What is PGS-India certification for smallholder farmers?", "Participatory Guarantee System for India (PGS-India) is a decentralised organic certification programme implemented by the Ministry of Agriculture. It allows groups of local farmers to inspect each other's fields and certify produce without incurring costly commercial third-party audit fees.", 4),
            ("Water", "Does organic farming really save water?", "Yes. Studies demonstrate that soils rich in organic matter can retain 20% to 30% more moisture compared to degraded soils. Organic mulching also cuts surface evaporation by more than half, enabling crops to survive dry spells.", 5),
        ]

        for cat, q, a, order in faqs_data:
            existing = db.query(FAQ).filter(FAQ.question == q).first()
            if not existing:
                new_faq = FAQ(category=cat, question=q, answer=a, display_order=order, is_published=True)
                db.add(new_faq)
                db.commit()
        print(f"[✓] Verified {len(faqs_data)} database FAQs.")

        # 5. Seed Educational Videos
        videos_data = [
            ("Aerobic Windrow Composting Field Demonstration", "Step-by-step tutorial on constructing and aerating farm waste compost windrows.", "Composting", "https://www.youtube.com/watch?v=0k1L2b4-G_g", 15, 1),
            ("Preparing Jeevamrutham Bio-Stimulant", "Practical demonstration of mixing indigenous cow dung, urine, jaggery, and pulse flour for soil inoculation.", "Biofertilisers", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 12, 2),
            ("Integrated Pest Management & Trap Crops", "How to install yellow sticky cards, pheromone traps, and border marigold plantings.", "Pest Control", "https://www.youtube.com/watch?v=ScMzIvxBSi4", 18, 3),
        ]

        for title, desc, cat, url, duration, order in videos_data:
            existing = db.query(EducationalVideo).filter(EducationalVideo.title == title).first()
            if not existing:
                new_vid = EducationalVideo(
                    title=title,
                    description=desc,
                    category=cat,
                    video_url=url,
                    duration_minutes=duration,
                    display_order=order,
                    is_published=True,
                )
                db.add(new_vid)
                db.commit()
        print(f"[✓] Verified {len(videos_data)} educational videos.")

        # 6. Seed Sample PDF Resource
        pdf_filename = "greengrow_farmer_guidance_handbook.pdf"
        pdf_path = Path(settings.UPLOAD_DIR) / "resources" / pdf_filename
        if not pdf_path.exists():
            generate_sample_pdf(pdf_path)

        existing_res = db.query(Resource).filter(Resource.file_name == pdf_filename).first()
        if not existing_res:
            res_item = Resource(
                title="GreenGrow Farmer Guidance Handbook (PDF)",
                description="Comprehensive printable field manual detailing composting, vermiculture, and biological pest defense.",
                category="Guides",
                file_path=str(pdf_path),
                file_name=pdf_filename,
                file_size_bytes=pdf_path.stat().st_size if pdf_path.exists() else 10240,
                file_type="pdf",
                is_published=True,
            )
            db.add(res_item)
            db.commit()
            print("[✓] Seeded printable PDF resource handbook.")

        # 7. Seed Active Announcement
        ann_title = "Tholukodu Village Field Study Desk Active"
        existing_ann = db.query(Announcement).filter(Announcement.title == ann_title).first()
        if not existing_ann:
            ann = Announcement(
                title=ann_title,
                content="Field research on soil organic carbon restoration and farmer transition guidance is underway in Tholukodu village.",
                link_url="/about",
                priority="High",
                is_active=True,
            )
            db.add(ann)
            db.commit()
            print("[✓] Seeded portal announcement.")

        # 8. VERIFY SURVEY RESPONSES TABLE INTEGRITY
        survey_count = db.query(SurveyResponse).count()
        print("-" * 65)
        print(f"[IMPORTANT] Total Farmer Survey Records in Oracle: {survey_count}")
        if survey_count == 0:
            print("[✓] STRICT COMPLIANCE: No fabricated survey responses have been generated.")
            print("    The project owner can enter genuine field questionnaire data via Admin Dashboard.")
        print("-" * 65)
        print("[SUCCESS] All initial portal data seeded successfully!")
        print("=" * 65)

    except Exception as exc:
        db.rollback()
        print(f"[ERROR] Seeding failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
