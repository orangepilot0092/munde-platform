"""
AapattiSetu: Disaster Intelligence Prompt Library
30 carefully crafted prompts covering disaster management, response, and mitigation scenarios in Maharashtra.
"""
from munde.prompts.base import Prompt, PromptCategory, PromptDifficulty

AAPATTISETU_PROMPTS = [
    # === SITUATIONAL (Current State) - 8 Prompts ===
    Prompt(
        id="aapattisetu_001",
        agent="aapattisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current flood warning status for rivers in Konkan?",
        expected_data_sources=["CWC Flood Forecast", "WRD Data"],
        tags=["flood", "konkan", "warning"],
        marathi_translation="कोकणातील नद्यांसाठी सध्याचा पूर इशारा स्थिती काय आहे?",
        showcase=True
    ),
    Prompt(
        id="aapattisetu_002",
        agent="aapattisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the number of active drought-affected talukas in Maharashtra.",
        expected_data_sources=["Revenue Dept Drought Data", "IMD Data"],
        tags=["drought", "talukas", "state"]
    ),
    Prompt(
        id="aapattisetu_003",
        agent="aapattisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current capacity and occupancy of relief camps in Kolhapur district?",
        expected_data_sources=["District Disaster Management Authority Data"],
        tags=["relief-camps", "kolhapur", "occupancy"],
        marathi_translation="कोल्हापूर जिल्ह्यातील मदत छावण्यांची सध्याची क्षमता आणि ocupancy किती आहे?"
    ),
    Prompt(
        id="aapattisetu_004",
        agent="aapattisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many villages are currently under 'No Touch' policy due to extreme drought?",
        expected_data_sources=["Revenue Dept Data"],
        tags=["no-touch", "drought", "villages"]
    ),
    Prompt(
        id="aapattisetu_005",
        agent="aapattisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current status of cyclone preparedness in coastal Maharashtra?",
        expected_data_sources=["SDMA Preparedness Reports", "IMD Cyclone Bulletins"],
        tags=["cyclone", "coastal", "preparedness"]
    ),
    Prompt(
        id="aapattisetu_006",
        agent="aapattisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the list of emergency response teams deployed in flood-affected areas.",
        expected_data_sources=["NDRF/SDRF Deployment Data"],
        tags=["ndrf", "sdrf", "deployment"]
    ),
    Prompt(
        id="aapattisetu_007",
        agent="aapattisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current availability of essential medicines in disaster-affected PHCs?",
        expected_data_sources=["Health Dept Emergency Stock Data"],
        tags=["medicines", "phc", "disaster"]
    ),
    Prompt(
        id="aapattisetu_008",
        agent="aapattisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many hectares of crop area were damaged in the recent unseasonal rainfall?",
        expected_data_sources=["Agriculture Dept Damage Assessment"],
        tags=["crop-damage", "unseasonal-rain", "hectares"]
    ),
    
    # === PREDICTIVE (Forecasting & Risk) - 7 Prompts ===
    Prompt(
        id="aapattisetu_009",
        agent="aapattisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict flood inundation zones in Mumbai for the next 48 hours based on rainfall forecasts.",
        expected_data_sources=["IMD Rainfall Forecast", "BMC Flood Maps", "Topography Data"],
        tags=["flood", "mumbai", "inundation", "prediction"],
        marathi_translation="पावसाच्या अंदाजानुसार पुढील ४८ तासांत मुंबईतील पूरग्रस्त झोनचा अंदाज काय आहे?",
        showcase=True
    ),
    Prompt(
        id="aapattisetu_010",
        agent="aapattisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Forecast the risk of landslides in Western Ghats during heavy monsoon.",
        expected_data_sources=["Geological Survey Data", "Rainfall Intensity"],
        tags=["landslide", "western-ghats", "risk"]
    ),
    Prompt(
        id="aapattisetu_011",
        agent="aapattisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the probability of drought declaration in Marathwada this year.",
        expected_data_sources=["Rainfall Deficit Data", "Soil Moisture", "Historical Patterns"],
        tags=["drought", "marathwada", "probability"]
    ),
    Prompt(
        id="aapattisetu_012",
        agent="aapattisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict the demand for drinking water tankers in drought-prone villages next month.",
        expected_data_sources=["Groundwater Data", "Historical Tanker Deployment"],
        tags=["water-tankers", "drought", "demand"]
    ),
    Prompt(
        id="aapattisetu_013",
        agent="aapattisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast the economic impact of cyclones on coastal infrastructure over the next decade.",
        expected_data_sources=["Climate Models", "Infrastructure Valuation"],
        tags=["cyclone", "economic-impact", "coastal"]
    ),
    Prompt(
        id="aapattisetu_014",
        agent="aapattisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict heatwave vulnerability in urban areas of Maharashtra for the upcoming summer.",
        expected_data_sources=["IMD Heatwave Forecast", "Urban Heat Island Data"],
        tags=["heatwave", "urban", "vulnerability"]
    ),
    Prompt(
        id="aapattisetu_015",
        agent="aapattisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the cascading effects of a major earthquake on Mumbai's critical infrastructure.",
        expected_data_sources=["Seismic Hazard Maps", "Infrastructure Resilience Data"],
        tags=["earthquake", "mumbai", "cascading-effects"]
    ),
    
    # === PRESCRIPTIVE (Recommendations) - 7 Prompts ===
    Prompt(
        id="aapattisetu_016",
        agent="aapattisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Recommend immediate evacuation strategies for low-lying areas in Konkan during heavy rainfall.",
        expected_data_sources=["Evacuation Plans", "Topography Data"],
        tags=["evacuation", "konkan", "strategy"],
        marathi_translation="कोकणातील सखल भागात मुसळधार पावसाच्या वेळी तात्काळ स्थलांतराच्या रणनीती सुचवा.",
        showcase=True
    ),
    Prompt(
        id="aapattisetu_017",
        agent="aapattisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="As District Collector, what protocol should I follow for declaring a drought-affected taluka?",
        expected_data_sources=["Drought Manual", "Revenue Guidelines"],
        tags=["drought-declaration", "protocol", "collector"]
    ),
    Prompt(
        id="aapattisetu_018",
        agent="aapattisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest measures to improve early warning dissemination in remote tribal villages.",
        expected_data_sources=["Communication Infrastructure Data", "Best Practices"],
        tags=["early-warning", "tribal", "measures"]
    ),
    Prompt(
        id="aapattisetu_019",
        agent="aapattisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a comprehensive flood mitigation plan for the Mula-Mutha river basin.",
        expected_data_sources=["River Basin Data", "Flood Modeling"],
        tags=["flood-mitigation", "mula-mutha", "plan"]
    ),
    Prompt(
        id="aapattisetu_020",
        agent="aapattisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What are the standard operating procedures for setting up temporary relief camps?",
        expected_data_sources=["SDMA SOPs", "Disaster Management Guidelines"],
        tags=["relief-camps", "sop", "setup"]
    ),
    Prompt(
        id="aapattisetu_021",
        agent="aapattisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend a post-disaster livelihood restoration program for affected farmers.",
        expected_data_sources=["Agriculture Damage Data", "Livelihood Guidelines"],
        tags=["livelihood", "post-disaster", "farmers"]
    ),
    Prompt(
        id="aapattisetu_022",
        agent="aapattisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest strategies to prevent waterborne disease outbreaks in flood-affected areas.",
        expected_data_sources=["Health Dept Guidelines", "Water Quality Data"],
        tags=["waterborne-disease", "flood", "prevention"]
    ),
    
    # === COMPARATIVE (Historical Analysis) - 4 Prompts ===
    Prompt(
        id="aapattisetu_023",
        agent="aapattisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare the response time of disaster management authorities across different districts.",
        expected_data_sources=["SDMA Response Reports"],
        tags=["response-time", "comparison", "districts"],
        marathi_translation="वेगवेगळ्या जिल्ह्यांतील आपत्ती व्यवस्थापन प्राधिकाऱ्यांच्या प्रतिसाद वेळेची तुलना करा."
    ),
    Prompt(
        id="aapattisetu_024",
        agent="aapattisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.BASIC,
        query="How has the frequency of extreme weather events changed in Maharashtra over the last 20 years?",
        expected_data_sources=["IMD Historical Data"],
        tags=["extreme-weather", "frequency", "trend"]
    ),
    Prompt(
        id="aapattisetu_025",
        agent="aapattisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare the effectiveness of drought relief measures in 2016 vs 2 сновида.",
        expected_data_sources=["Drought Relief Reports"],
        tags=["drought-relief", "2016", "comparison"]
    ),
    Prompt(
        id="aapattisetu_026",
        agent="aapattisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare Maharashtra's disaster preparedness index with other coastal states.",
        expected_data_sources=["National Disaster Management Authority Data"],
        tags=["preparedness-index", "comparison", "coastal-states"]
    ),
    
    # === CROSS-DOMAIN (Multi-Agent) - 2 Prompts ===
    Prompt(
        id="aapattisetu_027",
        agent="aapattisetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How does flood damage to rural roads affect emergency medical response times?",
        expected_data_sources=["Road Damage Data", "Health Emergency Response Data"],
        tags=["cross-domain", "margsetu", "arogyasetu", "flood"],
        showcase=True
    ),
    Prompt(
        id="aapattisetu_028",
        agent="aapattisetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the impact of drought on school dropout rates in affected districts.",
        expected_data_sources=["Drought Data", "Education Enrollment Data"],
        tags=["cross-domain", "shikshansetu", "drought", "dropout"]
    ),
    
    # === CITIZEN-FACING - 1 Prompt ===
    Prompt(
        id="aapattisetu_029",
        agent="aapattisetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to apply for ex-gratia compensation for house damage due to floods?",
        expected_data_sources=["Revenue Dept Compensation Guidelines"],
        tags=["citizen", "compensation", "flood-damage"],
        marathi_translation="पुरामुळे घराला झालेल्या नुकसानीसाठी मोबदला मिळवण्यासाठी अर्ज कसा करायचा?"
    ),
    
    # === OFFICER-FACING (Decision Support) - 1 Prompt ===
    Prompt(
        id="aapattisetu_030",
        agent="aapattisetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a comprehensive state disaster management plan update incorporating climate change projections.",
        expected_data_sources=["Climate Projections", "SDMA Framework", "Infrastructure Data"],
        tags=["officer", "disaster-plan", "climate-change", "update"],
        showcase=True
    ),
]

def register_aapattisetu_prompts(library):
    """Register all AapattiSetu prompts in the library."""
    for prompt in AAPATTISETU_PROMPTS:
        library.register(prompt)
