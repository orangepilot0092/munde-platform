"""
JalSetu: Water Intelligence Prompt Library
50 carefully crafted prompts covering all water-related scenarios in Maharashtra.
"""
from munde.prompts.base import Prompt, PromptCategory, PromptDifficulty

JALSETU_PROMPTS = [
    # === SITUATIONAL (Current State) - 10 Prompts ===
    Prompt(
        id="jalsetu_001",
        agent="jalsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current water level in Khadakwasla reservoir?",
        expected_data_sources=["WRD Daily Reservoir Report"],
        tags=["reservoir", "pune", "basic"],
        marathi_translation="खडकवासला धरणातील सध्याची पाणी पातळी काय आहे?",
        showcase=True,
        notes="Most common query - must respond in <2s"
    ),
    Prompt(
        id="jalsetu_002",
        agent="jalsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me all reservoirs in Pune district with their current storage percentage.",
        expected_data_sources=["WRD Reservoir Dashboard"],
        tags=["reservoir", "pune", "dashboard"],
        marathi_translation="पुणे जिल्ह्यातील सर्व धरणांची सध्याची साठवण क्षमता टक्केवारीत दाखवा.",
        showcase=True
    ),
    Prompt(
        id="jalsetu_003",
        agent="jalsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Which districts in Maharashtra have reservoir levels below 30% capacity?",
        expected_data_sources=["WRD State Dashboard", "District-wise Data"],
        tags=["reservoir", "critical", "state-wide"],
        marathi_translation="महाराष्ट्रातील कोणत्या जिल्ह्यांमध्ये धरणांची पातळी ३०% क्षमतेपेक्षा कमी आहे?",
        showcase=True
    ),
    Prompt(
        id="jalsetu_004",
        agent="jalsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the total water storage capacity of Maharashtra's major dams?",
        expected_data_sources=["WRD Annual Report"],
        tags=["state", "capacity", "overview"]
    ),
    Prompt(
        id="jalsetu_005",
        agent="jalsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare current reservoir levels in Marathwada with the same period last year.",
        expected_data_sources=["WRD Historical Data", "Current Dashboard"],
        tags=["comparison", "marathwada", "historical"],
        marathi_translation="मराठवाड्यातील सध्याची धरण पातळी मागील वर्षीच्या तुलनेत कशी आहे?"
    ),
    Prompt(
        id="jalsetu_006",
        agent="jalsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="List all major rivers in Maharashtra and their current flow status.",
        tags=["rivers", "state", "overview"]
    ),
    Prompt(
        id="jalsetu_007",
        agent="jalsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the water quality status of Mula-Mutha river in Pune?",
        tags=["quality", "river", "pune", "pollution"]
    ),
    Prompt(
        id="jalsetu_008",
        agent="jalsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the status of Jalyukt Shivar projects in my taluka?",
        tags=["scheme", "jalyukt-shivar", "status"]
    ),
    Prompt(
        id="jalsetu_009",
        agent="jalsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Show me a map of water-stressed blocks in Maharashtra.",
        tags=["map", "stress", "blocks", "gis"]
    ),
    Prompt(
        id="jalsetu_010",
        agent="jalsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current status of inter-state water disputes involving Maharashtra?",
        tags=["dispute", "inter-state", "legal"]
    ),
    
    # === PREDICTIVE (Forecasting & Risk) - 10 Prompts ===
    Prompt(
        id="jalsetu_011",
        agent="jalsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="What is the drought risk assessment for Beed district for the next 30 days?",
        expected_data_sources=["IMD Forecast", "WRD Reservoir Data", "Soil Moisture"],
        tags=["drought", "prediction", "beed", "risk"],
        marathi_translation="बीड जिल्ह्यासाठी पुढील ३० दिवसांचे दुष्काळ जोखीम मूल्यांकन काय आहे?",
        showcase=True,
        notes="Critical for rural Maharashtra - combines multiple data sources"
    ),
    Prompt(
        id="jalsetu_012",
        agent="jalsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Based on current monsoon patterns, which talukas are at risk of flooding?",
        expected_data_sources=["IMD Rainfall", "CWC Flood Forecast", "Topography"],
        tags=["flood", "monsoon", "prediction"],
        marathi_translation="सध्याच्या पावसाच्या पॅटर्ननुसार, कोणते तालुके पूरग्रस्त होण्याचा धोका आहे?"
    ),
    Prompt(
        id="jalsetu_013",
        agent="jalsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict water availability in Mumbai for the next 6 months considering current consumption trends.",
        expected_data_sources=["BMC Water Dept", "WRD Data", "Population Data"],
        tags=["mumbai", "prediction", "urban", "consumption"]
    ),
    Prompt(
        id="jalsetu_014",
        agent="jalsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Will Pune face water scarcity this summer? Provide evidence-based analysis.",
        expected_data_sources=["WRD Historical", "IMD Forecast", "PMC Data"],
        tags=["pune", "summer", "scarcity", "analysis"],
        showcase=True
    ),
    Prompt(
        id="jalsetu_015",
        agent="jalsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the impact of climate change on Maharashtra's water resources over the next decade.",
        expected_data_sources=["Climate Models", "WRD Historical", "Research Papers"],
        tags=["climate", "long-term", "analysis"]
    ),
    Prompt(
        id="jalsetu_016",
        agent="jalsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict groundwater depletion trends in Pune district over the next 5 years.",
        tags=["groundwater", "pune", "prediction"]
    ),
    Prompt(
        id="jalsetu_017",
        agent="jalsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Will the upcoming cyclone affect water quality in coastal districts?",
        tags=["cyclone", "coastal", "quality", "prediction"]
    ),
    Prompt(
        id="jalsetu_018",
        agent="jalsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict the impact of El Niño on Maharashtra's monsoon this year.",
        tags=["el-nino", "monsoon", "prediction"]
    ),
    Prompt(
        id="jalsetu_019",
        agent="jalsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast wheat production for Rabi season based on current sowing.",
        tags=["wheat", "rabi", "forecast"]
    ),
    Prompt(
        id="jalsetu_020",
        agent="jalsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict the adoption rate of drone technology in Maharashtra agriculture.",
        tags=["drone", "technology", "adoption"]
    ),
    
    # === PRESCRIPTIVE (Recommendations) - 10 Prompts ===
    Prompt(
        id="jalsetu_021",
        agent="jalsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What irrigation schedule do you recommend for sugarcane farmers in Kolhapur given current water levels?",
        expected_data_sources=["WRD Data", "MSAMB Crop Data", "Soil Health"],
        tags=["irrigation", "sugarcane", "kolhapur", "recommendation"],
        marathi_translation="सध्याच्या पाणी पातळीनुसार कोल्हापूरतील ऊस शेतकऱ्यांसाठी कोणते सिंचन वेळापत्रक योग्य आहे?",
        showcase=True
    ),
    Prompt(
        id="jalsetu_022",
        agent="jalsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="As District Collector, what immediate actions should I take to address water scarcity in Latur?",
        expected_data_sources=["WRD Data", "District Admin Reports", "Scheme Data"],
        tags=["policy", "latur", "emergency", "action"],
        marathi_translation="जिल्हाधिकारी म्हणून, लातूरमधील पाणी टंचाईवर तातडीने उपाय म्हणून मी काय करावे?"
    ),
    Prompt(
        id="jalsetu_023",
        agent="jalsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Which government schemes can drought-affected farmers in Osmanabad apply for?",
        expected_data_sources=["Agriculture Dept Schemes", "Revenue Dept Guidelines"],
        tags=["schemes", "osmanabad", "drought", "farmers"],
        marathi_translation="उस्मानाबादमधील दुष्काळग्रस्त शेतकरी कोणत्या सरकारी योजनांसाठी अर्ज करू शकतात?"
    ),
    Prompt(
        id="jalsetu_024",
        agent="jalsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a 5-year water conservation plan for water-stressed villages in Jalna district.",
        expected_data_sources=["Census Data", "WRD Data", "Jalyukt Shivar Guidelines"],
        tags=["planning", "jalna", "conservation", "long-term"]
    ),
    Prompt(
        id="jalsetu_025",
        agent="jalsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.BASIC,
        query="What is the best time to release water from Ujani dam for Rabi crops?",
        expected_data_sources=["WRD Operations Manual", "Crop Calendar"],
        tags=["operations", "ujani", "rabi"]
    ),
    Prompt(
        id="jalsetu_026",
        agent="jalsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Recommend rainwater harvesting structures for a school in drought-prone area.",
        tags=["harvesting", "school", "recommendation"]
    ),
    Prompt(
        id="jalsetu_027",
        agent="jalsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design an inter-basin water transfer plan to address Mumbai's water needs.",
        tags=["planning", "mumbai", "inter-basin"]
    ),
    Prompt(
        id="jalsetu_028",
        agent="jalsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What drip irrigation subsidy is available for farmers in Solapur?",
        tags=["subsidy", "drip", "solapur", "farmer"]
    ),
    Prompt(
        id="jalsetu_029",
        agent="jalsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Suggest flood management strategies for Mumbai considering climate change.",
        tags=["flood", "mumbai", "climate", "strategy"]
    ),
    Prompt(
        id="jalsetu_030",
        agent="jalsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend a watershed development plan for a tribal block in Nandurbar.",
        tags=["watershed", "tribal", "nandurbar", "development"]
    ),
    
    # === COMPARATIVE (Historical Analysis) - 5 Prompts ===
    Prompt(
        id="jalsetu_031",
        agent="jalsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare the 2016 Maharashtra drought with current conditions. What lessons were applied?",
        expected_data_sources=["Historical WRD Data", "Disaster Reports", "Policy Documents"],
        tags=["historical", "2016", "drought", "lessons"],
        marathi_translation="२०१६ च्या महाराष्ट्र दुष्काळाची सध्याच्या परिस्थितीशी तुलना करा. कोणते धडे लागू केले?"
    ),
    Prompt(
        id="jalsetu_032",
        agent="jalsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.BASIC,
        query="How has water consumption in Mumbai changed over the last 10 years?",
        expected_data_sources=["BMC Historical Data"],
        tags=["mumbai", "consumption", "trend"]
    ),
    Prompt(
        id="jalsetu_033",
        agent="jalsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Compare water availability per capita across all 36 districts of Maharashtra.",
        expected_data_sources=["Census", "WRD Data", "Population Data"],
        tags=["district", "comparison", "per-capita"],
        showcase=True
    ),
    Prompt(
        id="jalsetu_034",
        agent="jalsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare water tariffs across major cities in Maharashtra.",
        tags=["tariff", "comparison", "cities"]
    ),
    Prompt(
        id="jalsetu_035",
        agent="jalsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare Maharashtra's per capita water availability with national average.",
        tags=["comparison", "per-capita", "national"]
    ),
    
    # === CROSS-DOMAIN (Multi-Agent) - 5 Prompts ===
    Prompt(
        id="jalsetu_036",
        agent="jalsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How will the current water situation affect sugarcane production in Kolhapur this season?",
        expected_data_sources=["WRD Data", "MSAMB Crop Data", "Market Intelligence"],
        tags=["cross-domain", "krishisetu", "sugarcane", "kolhapur"],
        marathi_translation="सध्याची पाणी परिस्थिती या हंगामात कोल्हापूरतील ऊस उत्पादनावर कसा परिणाम करेल?",
        showcase=True,
        notes="Requires coordination with KrishiSetu"
    ),
    Prompt(
        id="jalsetu_037",
        agent="jalsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the impact of urban expansion in Pune on groundwater levels and suggest mitigation.",
        expected_data_sources=["Urban Planning Data", "CGWB Groundwater", "WRD Data"],
        tags=["cross-domain", "nagarsetu", "groundwater", "pune"]
    ),
    Prompt(
        id="jalsetu_038",
        agent="jalsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.ADVANCED,
        query="What is the relationship between deforestation in Western Ghats and water availability in Konkan?",
        expected_data_sources=["Forest Dept Data", "WRD Data", "Research Studies"],
        tags=["cross-domain", "forest", "konkan", "ecology"]
    ),
    Prompt(
        id="jalsetu_039",
        agent="jalsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How does industrial water usage in MIDC areas affect agricultural water availability?",
        tags=["industry", "agriculture", "conflict"]
    ),
    Prompt(
        id="jalsetu_040",
        agent="jalsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How does water availability affect migration patterns from Marathwada to Mumbai?",
        tags=["migration", "marathwada", "mumbai", "social"]
    ),
    
    # === CITIZEN-FACING - 5 Prompts ===
    Prompt(
        id="jalsetu_041",
        agent="jalsetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="When will water supply resume in my area? I live in Kothrud, Pune.",
        expected_data_sources=["PMC Water Dept", "Supply Schedule"],
        tags=["citizen", "supply", "pune", "kothrud"],
        marathi_translation="माझ्या भागात पाणी पुरवठा कधी सुरू होईल? मी कोथरूड, पुणे येथे राहतो."
    ),
    Prompt(
        id="jalsetu_042",
        agent="jalsetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How can I apply for a new water connection in my village?",
        expected_data_sources=["ZP Guidelines", "Scheme Documents"],
        tags=["citizen", "connection", "application"],
        marathi_translation="माझ्या गावात नवीन पाणी जोडणीसाठी मी अर्ज कसा करू शकतो?"
    ),
    Prompt(
        id="jalsetu_043",
        agent="jalsetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What water conservation methods are suitable for a small farmer with 2 acres?",
        expected_data_sources=["Agriculture Extension Guides", "Jalyukt Shivar"],
        tags=["citizen", "farmer", "conservation"],
        marathi_translation="२ एकर जमीन असलेल्या लहान शेतकऱ्यासाठी कोणते पाणी संवर्धन उपाय योग्य आहेत?"
    ),
    Prompt(
        id="jalsetu_044",
        agent="jalsetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to file a complaint about water contamination in my area?",
        tags=["citizen", "complaint", "contamination"]
    ),
    Prompt(
        id="jalsetu_045",
        agent="jalsetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="What is the drinking water quality standard and how is it monitored?",
        tags=["citizen", "quality", "standards"]
    ),
    
    # === OFFICER-FACING (Decision Support) - 5 Prompts ===
    Prompt(
        id="jalsetu_046",
        agent="jalsetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a briefing note for the Principal Secretary on Maharashtra's water situation for the upcoming cabinet meeting.",
        expected_data_sources=["All WRD Data", "IMD Forecast", "Policy Documents"],
        tags=["officer", "briefing", "cabinet", "executive"],
        showcase=True,
        notes="High-value executive use case"
    ),
    Prompt(
        id="jalsetu_047",
        agent="jalsetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.ADVANCED,
        query="Which districts should be declared drought-affected based on current parameters?",
        expected_data_sources=["WRD Data", "IMD Data", "Drought Manual Guidelines"],
        tags=["officer", "declaration", "drought", "policy"]
    ),
    Prompt(
        id="jalsetu_048",
        agent="jalsetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Generate a weekly water situation report for the state control room.",
        expected_data_sources=["All WRD Data", "IMD Data"],
        tags=["officer", "report", "weekly"]
    ),
    Prompt(
        id="jalsetu_049",
        agent="jalsetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the cost-benefit of desalination plants for coastal Maharashtra.",
        tags=["policy", "desalination", "coastal", "analysis"]
    ),
    Prompt(
        id="jalsetu_050",
        agent="jalsetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Draft a policy brief on groundwater regulation for the state cabinet.",
        tags=["policy", "groundwater", "regulation", "cabinet"],
        showcase=True
    ),
]

def register_jalsetu_prompts(library):
    """Register all JalSetu prompts in the library."""
    for prompt in JALSETU_PROMPTS:
        library.register(prompt)
