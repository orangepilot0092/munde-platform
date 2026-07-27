"""
KrishiSetu: Agriculture Intelligence Prompt Library
50 carefully crafted prompts covering all agriculture-related scenarios in Maharashtra.
"""
from munde.prompts.base import Prompt, PromptCategory, PromptDifficulty

KRISHISETU_PROMPTS = [
    # === SITUATIONAL (Current State) - 10 Prompts ===
    Prompt(
        id="krishisetu_001",
        agent="krishisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current sowing progress for soybean in Maharashtra?",
        expected_data_sources=["MSAMB Sowing Data"],
        tags=["sowing", "soybean", "progress"],
        marathi_translation="महाराष्ट्रातील सोयाबीन पेरणीची सध्याची प्रगती काय आहे?",
        showcase=True
    ),
    Prompt(
        id="krishisetu_002",
        agent="krishisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What are today's onion prices in Lasalgaon APMC?",
        expected_data_sources=["Enam Market Data"],
        tags=["prices", "onion", "lasalgaon", "market"],
        marathi_translation="लासलगाव APMC मध्ये आज कांद्याचे भाव काय आहेत?",
        showcase=True
    ),
    Prompt(
        id="krishisetu_003",
        agent="krishisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Show me the current soil health status for all districts in Vidarbha.",
        expected_data_sources=["Soil Health Card Database"],
        tags=["soil", "vidarbha", "health"],
        marathi_translation="विदर्भातील सर्व जिल्ह्यांची सध्याची माती आरोग्य स्थिती दाखवा."
    ),
    Prompt(
        id="krishisetu_004",
        agent="krishisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the total area under organic farming in Maharashtra?",
        expected_data_sources=["Agriculture Dept Data"],
        tags=["organic", "area", "state"]
    ),
    Prompt(
        id="krishisetu_005",
        agent="krishisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current stock position of food grains in Maharashtra?",
        expected_data_sources=["FCI Data", "Civil Supplies Dept"],
        tags=["stock", "food-grains", "fci"]
    ),
    Prompt(
        id="krishisetu_006",
        agent="krishisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current horticulture production in Maharashtra?",
        expected_data_sources=["Horticulture Dept Data"],
        tags=["horticulture", "production", "state"]
    ),
    Prompt(
        id="krishisetu_007",
        agent="krishisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Show me the status of Fasal Bima Yojana claims in my district.",
        expected_data_sources=["PMFBY Portal Data"],
        tags=["insurance", "pmfby", "claims"]
    ),
    Prompt(
        id="krishisetu_008",
        agent="krishisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current status of agricultural exports from Maharashtra?",
        expected_data_sources=["MSAMB Export Data"],
        tags=["exports", "agriculture", "state"]
    ),
    Prompt(
        id="krishisetu_009",
        agent="krishisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Show me the distribution of land holdings across Maharashtra.",
        expected_data_sources=["Agriculture Census"],
        tags=["land-holdings", "distribution", "state"]
    ),
    Prompt(
        id="krishisetu_010",
        agent="krishisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the status of soil health card distribution in my district?",
        expected_data_sources=["Soil Health Card Portal"],
        tags=["soil-card", "distribution", "district"]
    ),
    
    # === PREDICTIVE (Forecasting & Risk) - 10 Prompts ===
    Prompt(
        id="krishisetu_011",
        agent="krishisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict cotton yield for Nagpur district this season based on current conditions.",
        expected_data_sources=["Historical Yield", "Weather Data", "Soil Data"],
        tags=["prediction", "cotton", "nagpur", "yield"]
    ),
    Prompt(
        id="krishisetu_012",
        agent="krishisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict the impact of climate change on rice cultivation in Konkan.",
        expected_data_sources=["Climate Models", "Historical Data"],
        tags=["climate", "rice", "konkan", "prediction"]
    ),
    Prompt(
        id="krishisetu_013",
        agent="krishisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast wheat production for Rabi season based on current sowing.",
        expected_data_sources=["Sowing Data", "Weather Forecast"],
        tags=["wheat", "rabi", "forecast"]
    ),
    Prompt(
        id="krishisetu_014",
        agent="krishisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict grape production in Nashik for export this season.",
        expected_data_sources=["Historical Data", "Market Intelligence"],
        tags=["grape", "nashik", "export", "prediction"]
    ),
    Prompt(
        id="krishisetu_015",
        agent="krishisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict the impact of COVID-19 recovery on agricultural labor availability.",
        expected_data_sources=["Labor Data", "Migration Patterns"],
        tags=["covid", "labor", "prediction"]
    ),
    Prompt(
        id="krishisetu_016",
        agent="krishisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict the adoption rate of drone technology in Maharashtra agriculture.",
        expected_data_sources=["Technology Surveys", "Pilot Projects"],
        tags=["drone", "technology", "adoption"]
    ),
    Prompt(
        id="krishisetu_017",
        agent="krishisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the risk of pest attack on cotton crops in Vidarbha this season?",
        expected_data_sources=["Historical Pest Data", "Weather Conditions"],
        tags=["pest", "cotton", "vidarbha", "risk"]
    ),
    Prompt(
        id="krishisetu_018",
        agent="krishisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict onion prices for the next 3 months based on current sowing area.",
        expected_data_sources=["Sowing Data", "Historical Prices"],
        tags=["onion", "prices", "prediction"]
    ),
    Prompt(
        id="krishisetu_019",
        agent="krishisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast sugarcane production in Western Maharashtra considering water availability.",
        expected_data_sources=["WRD Data", "Historical Yield"],
        tags=["sugarcane", "western-maharashtra", "forecast"]
    ),
    Prompt(
        id="krishisetu_020",
        agent="krishisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the likelihood of unseasonal rainfall affecting Rabi crops?",
        expected_data_sources=["IMD Forecast", "Crop Calendar"],
        tags=["rainfall", "rabi", "risk"]
    ),
    
    # === PRESCRIPTIVE (Recommendations) - 10 Prompts ===
    Prompt(
        id="krishisetu_021",
        agent="krishisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Which crop is best suited for my black cotton soil in Vidarbha with limited irrigation?",
        expected_data_sources=["Soil Health Cards", "MSAMB Recommendations"],
        tags=["recommendation", "soil", "vidarbha", "crop"],
        marathi_translation="मर्यादित सिंचन असलेल्या विदर्भातील माझ्या काळ्या कसदार मातीसाठी कोणते पीक योग्य आहे?",
        showcase=True
    ),
    Prompt(
        id="krishisetu_022",
        agent="krishisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="My sugarcane crop is showing yellowing leaves. What could be the cause and solution?",
        expected_data_sources=["Plant Protection Guides", "Soil Health Data"],
        tags=["disease", "sugarcane", "diagnosis"],
        marathi_translation="माझ्या ऊसाच्या पिकाची पाने पिवळी होत आहेत. कारण आणि उपाय काय असेल?"
    ),
    Prompt(
        id="krishisetu_023",
        agent="krishisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Which fertilizer is recommended for turmeric in my soil type?",
        expected_data_sources=["Soil Test Results", "Fertilizer Guidelines"],
        tags=["fertilizer", "turmeric", "soil"]
    ),
    Prompt(
        id="krishisetu_024",
        agent="krishisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Recommend integrated pest management for cotton crop.",
        expected_data_sources=["IPM Guidelines", "Pest Surveillance Data"],
        tags=["ipm", "cotton", "pest"]
    ),
    Prompt(
        id="krishisetu_025",
        agent="krishisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Best practices for mango orchard management in Konkan?",
        expected_data_sources=["Horticulture Guides", "Regional Practices"],
        tags=["mango", "konkan", "practices"]
    ),
    Prompt(
        id="krishisetu_026",
        agent="krishisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Recommend organic farming practices for vegetable cultivation.",
        expected_data_sources=["Organic Farming Manuals"],
        tags=["organic", "vegetables", "practices"]
    ),
    Prompt(
        id="krishisetu_027",
        agent="krishisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Best water-efficient crops for drought-prone regions?",
        expected_data_sources=["Crop Water Requirement Data"],
        tags=["water-efficient", "drought", "crops"]
    ),
    Prompt(
        id="krishisetu_028",
        agent="krishisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a crop diversification plan for water-stressed farmers.",
        expected_data_sources=["Crop Suitability Maps", "Water Availability Data"],
        tags=["diversification", "water-stress", "plan"]
    ),
    Prompt(
        id="krishisetu_029",
        agent="krishisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a climate-resilient agriculture plan for coastal Konkan.",
        expected_data_sources=["Climate Data", "Crop Adaptation Studies"],
        tags=["climate-resilient", "konkan", "plan"]
    ),
    Prompt(
        id="krishisetu_030",
        agent="krishisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="How to implement precision agriculture on a 10-acre farm?",
        expected_data_sources=["Precision Ag Guidelines", "Technology Providers"],
        tags=["precision", "technology", "farm"]
    ),
    
    # === COMPARATIVE (Historical Analysis) - 5 Prompts ===
    Prompt(
        id="krishisetu_031",
        agent="krishisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare agricultural productivity across all districts of Maharashtra.",
        expected_data_sources=["Agriculture Census", "MSAMB Data"],
        tags=["comparison", "districts", "productivity"]
    ),
    Prompt(
        id="krishisetu_032",
        agent="krishisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare MSP effectiveness across different crops in Maharashtra.",
        expected_data_sources=["MSP Data", "Market Prices"],
        tags=["msp", "comparison", "crops"]
    ),
    Prompt(
        id="krishisetu_033",
        agent="krishisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare farmer suicide rates across districts and identify root causes.",
        expected_data_sources=["NCRB Data", "District Reports"],
        tags=["comparison", "suicide", "analysis"]
    ),
    Prompt(
        id="krishisetu_034",
        agent="krishisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare Maharashtra's agricultural performance with other major states.",
        expected_data_sources=["National Agriculture Statistics"],
        tags=["comparison", "states", "performance"]
    ),
    Prompt(
        id="krishisetu_035",
        agent="krishisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="How has soybean cultivation area changed in Maharashtra over the last decade?",
        expected_data_sources=["Historical Sowing Data"],
        tags=["soybean", "trend", "historical"]
    ),
    
    # === CROSS-DOMAIN (Multi-Agent) - 5 Prompts ===
    Prompt(
        id="krishisetu_036",
        agent="krishisetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How will water scarcity in Marathwada affect cotton production and market prices?",
        expected_data_sources=["WRD Data", "MSAMB Data", "Market Intelligence"],
        tags=["cross-domain", "jalsetu", "cotton", "marathwada"],
        showcase=True
    ),
    Prompt(
        id="krishisetu_037",
        agent="krishisetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How can urban waste composting benefit peri-urban farmers?",
        expected_data_sources=["Urban Waste Data", "Agriculture Extension"],
        tags=["cross-domain", "nagarsetu", "compost", "urban"]
    ),
    Prompt(
        id="krishisetu_038",
        agent="krishisetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How can renewable energy adoption benefit farmers economically?",
        expected_data_sources=["Energy Dept Data", "Solar Pump Schemes"],
        tags=["cross-domain", "urjasetu", "renewable", "farmers"]
    ),
    Prompt(
        id="krishisetu_039",
        agent="krishisetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How can better rural roads improve agricultural market access?",
        expected_data_sources=["Rural Development Data", "Market Connectivity"],
        tags=["cross-domain", "margsetu", "roads", "market"]
    ),
    Prompt(
        id="krishisetu_040",
        agent="krishisetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How can agricultural data improve disaster response planning?",
        expected_data_sources=["Agriculture Data", "Disaster Management Plans"],
        tags=["cross-domain", "aapattisetu", "disaster", "planning"],
        showcase=True
    ),
    
    # === CITIZEN-FACING - 5 Prompts ===
    Prompt(
        id="krishisetu_041",
        agent="krishisetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to apply for soil health card for my farm?",
        expected_data_sources=["Soil Health Scheme Guidelines"],
        tags=["citizen", "soil-card", "application"],
        marathi_translation="माझ्या शेतसाठी माती आरोग्य कार्ड कसे मिळवावे?"
    ),
    Prompt(
        id="krishisetu_042",
        agent="krishisetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to get compensation for crop damage due to unseasonal rainfall?",
        expected_data_sources=["Relief Guidelines", "Revenue Dept"],
        tags=["citizen", "compensation", "rainfall"],
        marathi_translation="अवेळी पावसामुळे पिकांचे नुकसान झाल्यास भरपाई कशी मिळवावी?"
    ),
    Prompt(
        id="krishisetu_043",
        agent="krishisetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="Where is the nearest KVK (Krishi Vigyan Kendra) to my location?",
        expected_data_sources=["KVK Directory"],
        tags=["citizen", "kvk", "location"]
    ),
    Prompt(
        id="krishisetu_044",
        agent="krishisetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="What subsidies are available for purchasing farm machinery?",
        expected_data_sources=["Subsidy Schemes", "Agriculture Dept"],
        tags=["citizen", "subsidy", "machinery"]
    ),
    Prompt(
        id="krishisetu_045",
        agent="krishisetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to register as a farmer on the Mahadbt portal?",
        expected_data_sources=["Mahadbt Guidelines"],
        tags=["citizen", "mahadbt", "registration"],
        marathi_translation="महाडीबीटी पोर्टलवर शेतकरी म्हणून नोंदणी कशी करावी?"
    ),
    
    # === OFFICER-FACING (Decision Support) - 5 Prompts ===
    Prompt(
        id="krishisetu_046",
        agent="krishisetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a crop loss assessment report for flood-affected farmers in Kolhapur.",
        expected_data_sources=["Revenue Dept Data", "MSAMB Data", "Satellite Imagery"],
        tags=["officer", "loss-assessment", "kolhapur", "flood"],
        showcase=True
    ),
    Prompt(
        id="krishisetu_047",
        agent="krishisetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the impact of farm loan waiver on agricultural credit in Maharashtra.",
        expected_data_sources=["Banking Data", "Credit Reports"],
        tags=["officer", "loan-waiver", "credit", "analysis"]
    ),
    Prompt(
        id="krishisetu_048",
        agent="krishisetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a strategy to double farmers' income by 2030 in Maharashtra.",
        expected_data_sources=["Economic Survey", "Agriculture Plans"],
        tags=["officer", "strategy", "income", "vision"]
    ),
    Prompt(
        id="krishisetu_049",
        agent="krishisetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the effectiveness of e-NAM platform for Maharashtra farmers.",
        expected_data_sources=["e-NAM Data", "Market Integration Reports"],
        tags=["officer", "e-nam", "analysis"]
    ),
    Prompt(
        id="krishisetu_050",
        agent="krishisetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Develop a strategy to reduce post-harvest losses in Maharashtra.",
        expected_data_sources=["Post-Harvest Studies", "Infrastructure Data"],
        tags=["officer", "post-harvest", "losses", "strategy"]
    ),
]

def register_krishisetu_prompts(library):
    """Register all KrishiSetu prompts in the library."""
    for prompt in KRISHISETU_PROMPTS:
        library.register(prompt)
