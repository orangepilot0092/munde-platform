"""
MargSetu: Transport Intelligence Prompt Library
30 carefully crafted prompts covering transport, mobility, and logistics scenarios in Maharashtra.
"""
from munde.prompts.base import Prompt, PromptCategory, PromptDifficulty

MARGSETU_PROMPTS = [
    # === SITUATIONAL (Current State) - 8 Prompts ===
    Prompt(
        id="margsetu_001",
        agent="margsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current operational status of MSRTC buses on the Pune-Mumbai route?",
        expected_data_sources=["MSRTC Real-time Tracking", "Transport Dept Dashboard"],
        tags=["msrtc", "pune-mumbai", "status"],
        marathi_translation="पुणे-मुंबई मार्गावर एमएसआरटीसी बसची सध्याची कार्यरत स्थिती काय आहे?",
        showcase=True
    ),
    Prompt(
        id="margsetu_002",
        agent="margsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the current traffic congestion levels at major junctions in Nagpur.",
        expected_data_sources=["Nagpur Traffic Police Data", "Smart City Sensors"],
        tags=["traffic", "nagpur", "congestion"]
    ),
    Prompt(
        id="margsetu_003",
        agent="margsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current ridership data for Mumbai Metro Line 3?",
        expected_data_sources=["Mumbai Metro Rail Corp Data"],
        tags=["metro", "mumbai", "ridership"],
        marathi_translation="मुंबई मेट्रो लाईन ३ ची सध्याची प्रवासी संख्या किती आहे?"
    ),
    Prompt(
        id="margsetu_004",
        agent="margsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many kilometers of new highways were constructed in Maharashtra last year?",
        expected_data_sources=["MSRDC Annual Report", "PWD Data"],
        tags=["highways", "construction", "state"]
    ),
    Prompt(
        id="margsetu_005",
        agent="margsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current status of pending road repair works in my district?",
        expected_data_sources=["PWD Grievance Portal", "Road Maintenance Data"],
        tags=["road-repair", "pending", "district"]
    ),
    Prompt(
        id="margsetu_006",
        agent="margsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the list of active toll plazas on the Mumbai-Pune Expressway.",
        expected_data_sources=["MSRDC Toll Data"],
        tags=["toll", "mumbai-pune", "expressway"]
    ),
    Prompt(
        id="margsetu_007",
        agent="margsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current freight movement volume through JNPT port?",
        expected_data_sources=["JNPT Traffic Data", "Logistics Dept"],
        tags=["freight", "jnpt", "volume"]
    ),
    Prompt(
        id="margsetu_008",
        agent="margsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many electric buses are currently operational in Pune PMPML?",
        expected_data_sources=["PMPML Fleet Data", "FAME India Scheme"],
        tags=["electric-buses", "pmpml", "pune"]
    ),
    
    # === PREDICTIVE (Forecasting & Risk) - 7 Prompts ===
    Prompt(
        id="margsetu_009",
        agent="margsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict traffic congestion patterns in Mumbai during the upcoming Ganpati festival.",
        expected_data_sources=["Historical Festival Traffic Data", "Event Calendar"],
        tags=["traffic", "mumbai", "festival", "prediction"],
        marathi_translation="आगामी गणपती उत्सवात मुंबईतील वाहतुकीची कोंडी कशी असेल याचा अंदाज काय आहे?",
        showcase=True
    ),
    Prompt(
        id="margsetu_010",
        agent="margsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Forecast MSRTC bus demand for the Diwali holiday season.",
        expected_data_sources=["Historical Holiday Booking Data", "Demographic Trends"],
        tags=["msrtc", "diwali", "demand", "forecast"]
    ),
    Prompt(
        id="margsetu_011",
        agent="margsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the impact of the new coastal road on traffic distribution in South Mumbai.",
        expected_data_sources=["Traffic Simulation Models", "Coastal Road Project Data"],
        tags=["coastal-road", "mumbai", "traffic-impact"]
    ),
    Prompt(
        id="margsetu_012",
        agent="margsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict the maintenance needs of state highways based on current monsoon damage.",
        expected_data_sources=["Monsoon Damage Reports", "Historical Maintenance Data"],
        tags=["maintenance", "highways", "monsoon"]
    ),
    Prompt(
        id="margsetu_013",
        agent="margsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast the adoption rate of EV charging infrastructure in tier-2 cities of Maharashtra.",
        expected_data_sources=["EV Sales Data", "Infrastructure Plans"],
        tags=["ev-charging", "tier-2", "adoption"]
    ),
    Prompt(
        id="margsetu_014",
        agent="margsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict accident hotspots on the Mumbai-Nashik highway based on historical data.",
        expected_data_sources=["Traffic Police Accident Data", "Road Geometry Data"],
        tags=["accidents", "mumbai-nashik", "hotspots"]
    ),
    Prompt(
        id="margsetu_015",
        agent="margsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the long-term impact of remote work on daily commuter traffic in Pune.",
        expected_data_sources=["IT Park Occupancy Data", "Traffic Volume Trends"],
        tags=["remote-work", "commuter", "pune", "impact"]
    ),
    
    # === PRESCRIPTIVE (Recommendations) - 7 Prompts ===
    Prompt(
        id="margsetu_016",
        agent="margsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Recommend strategies to reduce last-mile connectivity issues in suburban Mumbai.",
        expected_data_sources=["Suburban Transport Data", "Best Practices"],
        tags=["last-mile", "mumbai", "strategy"],
        marathi_translation="मुंबईच्या उपनगरांमध्ये अंतिम मैल कनेक्टिव्हिटीच्या समस्या कमी करण्यासाठी रणनीती सुचवा.",
        showcase=True
    ),
    Prompt(
        id="margsetu_017",
        agent="margsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="As Transport Commissioner, what measures should I implement to improve road safety?",
        expected_data_sources=["Accident Data", "Road Safety Guidelines"],
        tags=["road-safety", "policy", "measures"]
    ),
    Prompt(
        id="margsetu_018",
        agent="margsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest optimal bus routing for newly developed areas in Nagpur.",
        expected_data_sources=["Population Density Data", "Existing Route Maps"],
        tags=["bus-routing", "nagpur", "optimization"]
    ),
    Prompt(
        id="margsetu_019",
        agent="margsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a comprehensive freight corridor plan to decongest Mumbai ports.",
        expected_data_sources=["Logistics Data", "Freight Movement Patterns"],
        tags=["freight-corridor", "mumbai", "decongestion"]
    ),
    Prompt(
        id="margsetu_020",
        agent="margsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What intelligent traffic management systems should be deployed in Pune?",
        expected_data_sources=["Smart City Guidelines", "Traffic Flow Data"],
        tags=["intelligent-traffic", "pune", "systems"]
    ),
    Prompt(
        id="margsetu_021",
        agent="margsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend a state-wide policy for promoting non-motorized transport (NMT).",
        expected_data_sources=["NMT Guidelines", "Urban Planning Data"],
        tags=["nmt", "policy", "state-wide"]
    ),
    Prompt(
        id="margsetu_022",
        agent="margsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest measures to improve accessibility for disabled persons in public transport.",
        expected_data_sources=["Accessibility Guidelines", "Transport Infrastructure Data"],
        tags=["accessibility", "disabled", "public-transport"]
    ),
    
    # === COMPARATIVE (Historical Analysis) - 4 Prompts ===
    Prompt(
        id="margsetu_023",
        agent="margsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare public transport ridership across major cities in Maharashtra.",
        expected_data_sources=["City Transport Data"],
        tags=["ridership", "comparison", "cities"],
        marathi_translation="महाराष्ट्रातील प्रमुख शहरांमधील सार्वजनिक वाहतुकीच्या प्रवासी संख्येची तुलना करा."
    ),
    Prompt(
        id="margsetu_024",
        agent="margsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.BASIC,
        query="How has the length of state highways in Maharashtra changed over the last decade?",
        expected_data_sources=["PWD Historical Data"],
        tags=["highways", "length", "trend"]
    ),
    Prompt(
        id="margsetu_025",
        agent="margsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare road accident rates between rural and urban districts in Maharashtra.",
        expected_data_sources=["Traffic Police Accident Data"],
        tags=["accidents", "rural-urban", "comparison"]
    ),
    Prompt(
        id="margsetu_026",
        agent="margsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare Maharashtra's EV adoption rate with other leading Indian states.",
        expected_data_sources=["National EV Data", "State Transport Reports"],
        tags=["ev-adoption", "comparison", "states"]
    ),
    
    # === CROSS-DOMAIN (Multi-Agent) - 2 Prompts ===
    Prompt(
        id="margsetu_027",
        agent="margsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How do poor rural roads affect agricultural market access and farmer income in Vidarbha?",
        expected_data_sources=["Road Infrastructure Data", "Agriculture Market Data"],
        tags=["cross-domain", "krishisetu", "rural-roads", "farmer-income"],
        showcase=True
    ),
    Prompt(
        id="margsetu_028",
        agent="margsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the impact of transport emissions on urban air quality in Mumbai.",
        expected_data_sources=["Traffic Data", "MPCB Air Quality Data"],
        tags=["cross-domain", "nagarsetu", "emissions", "air-quality"]
    ),
    
    # === CITIZEN-FACING - 1 Prompt ===
    Prompt(
        id="margsetu_029",
        agent="margsetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to apply for a duplicate driving license online in Maharashtra?",
        expected_data_sources=["Parivahan Sewa Guidelines"],
        tags=["citizen", "driving-license", "duplicate"],
        marathi_translation="महाराष्ट्रात ऑनलाइन डुप्लिकेट ड्रायव्हिंग लायसन्ससाठी अर्ज कसा करायचा?"
    ),
    
    # === OFFICER-FACING (Decision Support) - 1 Prompt ===
    Prompt(
        id="margsetu_030",
        agent="margsetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a comprehensive state transport policy framework for 2030.",
        expected_data_sources=["Transport Data", "National Transport Policy", "Economic Survey"],
        tags=["officer", "transport-policy", "2030", "framework"],
        showcase=True
    ),
]

def register_margsetu_prompts(library):
    """Register all MargSetu prompts in the library."""
    for prompt in MARGSETU_PROMPTS:
        library.register(prompt)
