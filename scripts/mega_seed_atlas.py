import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import psycopg2
from psycopg2.extras import execute_values, Json
from src.core.config import settings


def mega_seed():
    conn = psycopg2.connect(settings.DATABASE_URL)
    cur = conn.cursor()

    print("🌍 Seeding High-Value State & National Datasets...")

    # 1. High-Value Explicit Datasets (MRSAC, IMD, CPCB, WRD, etc.)
    state_datasets = [
        # MRSAC (Maharashtra Remote Sensing Application Centre) - GIS Goldmine
        (
            "mrsac_land_use",
            "MRSAC Land Use / Land Cover (LULC)",
            "GIS",
            "MRSAC",
            "Geospatial, Computer Vision",
            "Annual",
        ),
        (
            "mrsac_watershed",
            "MRSAC Watershed & Drainage Maps",
            "Water",
            "MRSAC",
            "Geospatial, Routing",
            "Static",
        ),
        (
            "mrsac_groundwater",
            "MRSAC Groundwater Prospects Zones",
            "Water",
            "MRSAC",
            "Geospatial, Classification",
            "Annual",
        ),
        (
            "mrsac_crop_acreage",
            "MRSAC Satellite-based Crop Acreage",
            "Agriculture",
            "MRSAC",
            "Geospatial, Time-Series",
            "Seasonal",
        ),
        (
            "mrsac_drought",
            "MRSAC Agricultural Drought Assessment",
            "Disaster",
            "MRSAC",
            "Geospatial, Forecasting",
            "Weekly",
        ),
        (
            "mrsac_forest_fire",
            "MRSAC Forest Fire Hotspots (MODIS/VIIRS)",
            "Environment",
            "MRSAC",
            "Geospatial, Anomaly Detection",
            "Daily",
        ),
        (
            "mrsac_urban_sprawl",
            "MRSAC Urban Sprawl & Land Surface Temp",
            "Urban",
            "MRSAC",
            "Geospatial, Time-Series",
            "Annual",
        ),
        (
            "mrsac_wetlands",
            "MRSAC Wetlands Inventory & Mapping",
            "Environment",
            "MRSAC",
            "Geospatial",
            "Biennial",
        ),
        (
            "mrsac_wasteland",
            "MRSAC Wasteland Atlas",
            "Land",
            "MRSAC",
            "Geospatial",
            "Annual",
        ),
        (
            "mrsac_minerals",
            "MRSAC Mineral Prospecting Zones",
            "Industry",
            "MRSAC",
            "Geospatial",
            "Static",
        ),
        # Water & Environment
        (
            "maha_wrd_dam_levels",
            "WRD Live Dam & Reservoir Levels",
            "Water",
            "WRD",
            "Time-Series, Forecasting",
            "Daily",
        ),
        (
            "maha_wrd_minor_irrigation",
            "Minor Irrigation Census Data",
            "Water",
            "WRD",
            "Tabular, Analytics",
            "Quinquennial",
        ),
        (
            "mpcb_air_quality_stations",
            "MPCB CAAQM Real-Time AQI Data",
            "Environment",
            "MPCB",
            "Time-Series, Anomaly Detection",
            "Hourly",
        ),
        (
            "mpcb_river_quality",
            "MPCB River Water Quality (BOD/DO)",
            "Environment",
            "MPCB",
            "Time-Series, Classification",
            "Monthly",
        ),
        (
            "mpcb_industrial_consents",
            "MPCB Industrial Consent to Operate",
            "Environment",
            "MPCB",
            "NLP, Tabular",
            "Continuous",
        ),
        (
            "maha_forest_wildlife",
            "Maharashtra Forest Dept Wildlife Sanctuaries",
            "Environment",
            "Forest",
            "Geospatial, Tabular",
            "Static",
        ),
        (
            "maha_forest_mangroves",
            "Mangrove Cover & Health (SRTM/Sentinel)",
            "Environment",
            "Forest",
            "Geospatial, Computer Vision",
            "Annual",
        ),
        # Agriculture & Economy
        (
            "maha_apmc_daily_arrivals",
            "APMC Daily Market Arrivals & Prices",
            "Agriculture",
            "MSAMB",
            "Time-Series, Forecasting",
            "Daily",
        ),
        (
            "maha_soil_health_cards",
            "Soil Health Card NPK Data",
            "Agriculture",
            "Agriculture",
            "Geospatial, Tabular",
            "Biennial",
        ),
        (
            "maha_midc_estates",
            "MIDC Industrial Estate Boundaries",
            "Industry",
            "MIDC",
            "Geospatial, Tabular",
            "Annual",
        ),
        (
            "maha_maha_rera_projects",
            "MahaRERA Registered Real Estate Projects",
            "Urban",
            "MahaRERA",
            "NLP, Tabular, Geospatial",
            "Daily",
        ),
        (
            "maha_msedcl_feeders",
            "MSEDCL Electrical Feeder Boundaries",
            "Energy",
            "MSEDCL",
            "Geospatial, Time-Series",
            "Annual",
        ),
        (
            "maha_msedcl_outages",
            "MSEDCL Power Outage Logs",
            "Energy",
            "MSEDCL",
            "Time-Series, NLP",
            "Daily",
        ),
        (
            "maha_transport_rto",
            "RTO Vehicle Registration Statistics",
            "Transport",
            "Transport",
            "Time-Series, Tabular",
            "Monthly",
        ),
        (
            "maha_health_facilities_dir",
            "NHM Public Health Facilities Directory",
            "Health",
            "Health",
            "Geospatial, Tabular",
            "Annual",
        ),
        (
            "maha_education_schools",
            "UDISE+ School Directory & Infrastructure",
            "Education",
            "Education",
            "Geospatial, Tabular",
            "Annual",
        ),
        (
            "census_2011_village_dir",
            "Census 2011 Primary Census Abstract (Village)",
            "Demographics",
            "Census",
            "Tabular, Geospatial",
            "Decadal",
        ),
        (
            "data_gov_in_pincode",
            "India Post PIN Code Directory",
            "Citizen Services",
            "India Post",
            "Tabular, NLP",
            "Static",
        ),
    ]

    # 2. Matrix Generation: District-Level Datasets (36 Districts x 8 Facility Types = 288 Datasets)
    districts = [
        "Mumbai",
        "Mumbai Suburban",
        "Thane",
        "Palghar",
        "Raigad",
        "Ratnagiri",
        "Sindhudurg",
        "Nashik",
        "Jalgaon",
        "Dhule",
        "Nandurbar",
        "Pune",
        "Satara",
        "Sangli",
        "Kolhapur",
        "Solapur",
        "Ahmednagar",
        "Aurangabad",
        "Jalna",
        "Parbhani",
        "Hingoli",
        "Nanded",
        "Beed",
        "Latur",
        "Osmanabad",
        "Buldhana",
        "Akola",
        "Washim",
        "Amravati",
        "Yavatmal",
        "Wardha",
        "Nagpur",
        "Bhandara",
        "Gondia",
        "Chandrapur",
        "Gadchiroli",
    ]

    facility_types = [
        ("Fair Price Shops (Ration)", "Citizen Services", "Tabular, Geospatial"),
        ("Primary Health Centres (PHC)", "Health", "Tabular, Geospatial"),
        ("Zilla Parishad Schools", "Education", "Tabular, Geospatial"),
        ("Post Offices", "Citizen Services", "Tabular, Geospatial"),
        ("Police Stations", "Citizen Services", "Tabular, Geospatial"),
        ("Gram Panchayat Funds", "Public Finance", "Tabular, NLP"),
        ("Tourism / MTDC Centers", "Economy", "Tabular, NLP"),
        ("Village Roads (PMGSY)", "Infrastructure", "Geospatial, Routing"),
    ]

    dataset_records = []

    # Add State Datasets
    for d_id, d_name, d_domain, d_dept, d_ai, d_freq in state_datasets:
        dataset_records.append(
            (
                d_id,
                d_name,
                d_domain,
                d_dept,
                "Open Government License",
                "GIS/CSV",
                "https://data.gov.in",
                d_ai,
                d_freq,
            )
        )

    # Add District Datasets
    for district in districts:
        dist_slug = district.lower().replace(" ", "_")
        for fac_name, fac_domain, fac_ai in facility_types:
            d_id = f"maha_{dist_slug}_{fac_name.lower().replace(' ', '_').replace('(', '').replace(')', '')}"
            d_name = f"{district} District: {fac_name} Directory"
            dataset_records.append(
                (
                    d_id,
                    d_name,
                    fac_domain,
                    f"District Collector ({district})",
                    "Open Government License",
                    "CSV",
                    f"https://data.gov.in/catalog/{dist_slug}",
                    fac_ai,
                    "Annual",
                )
            )

    print(
        f"💾 Bulk inserting {len(dataset_records)} datasets into metadata_registry..."
    )

    execute_values(
        cur,
        """
        INSERT INTO metadata_registry 
        (dataset_id, name, domain, department, license, format, source_url, ai_readiness, refresh_frequency, quality_score, last_updated)
        VALUES %s
        ON CONFLICT (dataset_id) DO UPDATE SET
            name = EXCLUDED.name,
            domain = EXCLUDED.domain,
            ai_readiness = EXCLUDED.ai_readiness,
            source_url = EXCLUDED.source_url,
            last_updated = NOW()
    """,
        [
            (
                r[0],
                r[1],
                r[2],
                r[3],
                r[4],
                r[5],
                r[6],
                Json({"use_cases": r[7].split(", ")}),
                r[8],
                4.0,
            )
            for r in dataset_records
        ],
        template="(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())",
    )

    # 3. Seed API Registry (Real Public APIs)
    print("🔌 Seeding Public API Registry...")
    apis = [
        # Data.gov.in OData APIs
        (
            "api_data_gov_in_odata",
            "Data.gov.in OData REST API",
            "MeitY",
            "https://api.data.gov.in",
            "API Key (data.gov.in)",
            "1000/day",
            "https://data.gov.in/api-documentation",
        ),
        (
            "api_imd_forecast",
            "IMD District Weather Forecast",
            "IMD",
            "https://mausam.imd.gov.in/api",
            "Public",
            "Unlimited",
            "https://mausam.imd.gov.in",
        ),
        (
            "api_cpcb_aqi",
            "CPCB National AQI Feed",
            "CPCB",
            "https://app.cpcbccr.com/ccr/docs/Api_consent_correction.pdf",
            "API Key",
            "Strict",
            "https://cpcb.nic.in",
        ),
        (
            "api_bhuvan_wms",
            "ISRO Bhuvan WMS/WFS Services",
            "ISRO/NRSC",
            "https://bhuvan-app1.nrsc.gov.in/api/wms",
            "Public",
            "Unlimited",
            "https://bhuvan.nrsc.gov.in",
        ),
        (
            "api_osm_overpass",
            "OpenStreetMap Overpass API (Maharashtra)",
            "OSM",
            "https://overpass-api.de/api/interpreter",
            "Public",
            "Fair Use",
            "https://wiki.openstreetmap.org/wiki/Overpass_API",
        ),
        (
            "api_parivahan_vahan",
            "Parivahan VAHAN (Vehicle Registration)",
            "MoRTH",
            "https://vahan.parivahan.gov.in/vahanservice/v4/ui/",
            "OAuth2",
            "Restricted",
            "https://parivahan.gov.in",
        ),
        (
            "api_parivahan_sarathi",
            "Parivahan SARATHI (Driving License)",
            "MoRTH",
            "https://sarathi.parivahan.gov.in/sarathiservice",
            "OAuth2",
            "Restricted",
            "https://parivahan.gov.in",
        ),
        (
            "api_gst_system",
            "GST System Public API (GSTR)",
            "GSTN",
            "https://www.gst.gov.in/api",
            "OAuth2/Gstin",
            "Strict",
            "https://developer.gst.gov.in",
        ),
        (
            "api_epfo_uan",
            "EPFO UAN Verification",
            "EPFO",
            "https://unifiedportal-mem.epfindia.gov.in/externalAPI/",
            "API Key",
            "Strict",
            "https://www.epfindia.gov.in",
        ),
        (
            "api_fssai_license",
            "FSSAI License Verification",
            "FSSAI",
            "https://foscos.fssai.gov.in/api",
            "Public",
            "Fair Use",
            "https://foscos.fssai.gov.in",
        ),
        (
            "api_mahabhulekh_ror",
            "Mahabhulekh 7/12 Extract API",
            "Revenue (MH)",
            "https://bhulekh.mahabhumi.gov.in",
            "OAuth2",
            "Restricted",
            "https://mahabhumi.gov.in",
        ),
        (
            "api_maha_rera",
            "MahaRERA Project Search API",
            "MahaRERA",
            "https://maharera.mahaonline.gov.in",
            "Public",
            "Fair Use",
            "https://maharera.mahaonline.gov.in",
        ),
        (
            "api_pincode_india",
            "India Post PIN Code Search",
            "India Post",
            "https://api.postalpincode.in/pincode/{pin}",
            "Public",
            "Unlimited",
            "https://www.postalpincode.in/api",
        ),
        (
            "api_india_post_tracking",
            "India Post Article Tracking",
            "India Post",
            "https://api.postalpincode.in/item/{item}",
            "Public",
            "Unlimited",
            "https://www.postalpincode.in/api",
        ),
        (
            "api_ngt_orders",
            "National Green Tribunal Orders (NLP)",
            "NGT",
            "https://greentribunal.gov.in",
            "Public",
            "Fair Use",
            "https://greentribunal.gov.in",
        ),
        (
            "api_supreme_court",
            "Supreme Court Daily Orders",
            "SCI",
            "https://main.sci.gov.in",
            "Public",
            "Fair Use",
            "https://main.sci.gov.in",
        ),
        (
            "api_mca_charges",
            "MCA Corporate Charges Search",
            "MCA",
            "https://www.mca.gov.in/mcafoportal/showCheckSignatory.do",
            "Public",
            "Fair Use",
            "https://www.mca.gov.in",
        ),
    ]

    execute_values(
        cur,
        """
        INSERT INTO api_registry (api_id, name, department, base_url, auth_method, rate_limit, documentation_url)
        VALUES %s ON CONFLICT (api_id) DO NOTHING
    """,
        apis,
    )

    conn.commit()
    cur.close()
    conn.close()
    print(
        f"🎉 MEGA-SEED COMPLETE! Ingested {len(dataset_records)} Datasets and {len(apis)} APIs."
    )


if __name__ == "__main__":
    mega_seed()
