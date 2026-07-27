"""
BhoomiSetu: Land Intelligence Prompt Library
30 carefully crafted prompts covering land records, property, and revenue scenarios in Maharashtra.
"""
from munde.prompts.base import Prompt, PromptCategory, PromptDifficulty

BHOOMISETU_PROMPTS = [
    # === SITUATIONAL (Current State) - 8 Prompts ===
    Prompt(
        id="bhoomisetu_001",
        agent="bhoomisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current status of digitization of land records in Maharashtra?",
        expected_data_sources=["Revenue Dept Dashboard", "Bhulekh Data"],
        tags=["digitization", "land-records", "state"],
        marathi_translation="महाराष्ट्रातील भूमी अभिलेखांच्या डिजिटायझेशनची सध्याची स्थिती काय आहे?",
        showcase=True
    ),
    Prompt(
        id="bhoomisetu_002",
        agent="bhoomisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the total agricultural land area in Pune district.",
        expected_data_sources=["Land Use Statistics", "Agriculture Census"],
        tags=["agricultural-land", "pune", "area"]
    ),
    Prompt(
        id="bhoomisetu_003",
        agent="bhoomisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current pending mutation cases count in my taluka?",
        expected_data_sources=["Revenue Dept Mutation Data"],
        tags=["mutation", "pending", "taluka"],
        marathi_translation="माझ्या तालुक्यातील प्रलंबित फेरफार प्रकरणांची संख्या किती आहे?"
    ),
    Prompt(
        id="bhoomisetu_004",
        agent="bhoomisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many property registrations happened in Mumbai last month?",
        expected_data_sources=["Registration Dept Data"],
        tags=["registration", "mumbai", "property"]
    ),
    Prompt(
        id="bhoomisetu_005",
        agent="bhoomisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the average land price per square foot in different zones of Nagpur?",
        expected_data_sources=["Ready Reckoner Rates", "Market Data"],
        tags=["land-price", "nagpur", "zones"]
    ),
    Prompt(
        id="bhoomisetu_006",
        agent="bhoomisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the list of government land parcels available for lease in my district.",
        expected_data_sources=["Revenue Dept Land Bank"],
        tags=["government-land", "lease", "district"]
    ),
    Prompt(
        id="bhoomisetu_007",
        agent="bhoomisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current status of land acquisition for the Mumbai-Ahmedabad bullet train project?",
        expected_data_sources=["MSRTC Land Acquisition Data"],
        tags=["land-acquisition", "bullet-train", "mumbai"]
    ),
    Prompt(
        id="bhoomisetu_008",
        agent="bhoomisetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many encroachment cases are pending on government land in Maharashtra?",
        expected_data_sources=["Revenue Dept Encroachment Data"],
        tags=["encroachment", "government-land", "cases"]
    ),
    
    # === PREDICTIVE (Forecasting & Risk) - 7 Prompts ===
    Prompt(
        id="bhoomisetu_009",
        agent="bhoomisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict land price trends in Pune's peripheral areas over the next 3 years.",
        expected_data_sources=["Historical Price Data", "Infrastructure Plans", "Demand Trends"],
        tags=["land-price", "pune", "prediction"],
        marathi_translation="पुण्याच्या उपनगरीय भागातील भूमी किमतीचा पुढील ३ वर्षांचा अंदाज काय आहे?",
        showcase=True
    ),
    Prompt(
        id="bhoomisetu_010",
        agent="bhoomisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Forecast the demand for residential plots in Nashik considering industrial growth.",
        expected_data_sources=["Industrial Growth Data", "Population Trends"],
        tags=["residential", "nashik", "demand"]
    ),
    Prompt(
        id="bhoomisetu_011",
        agent="bhoomisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the impact of new metro lines on property values in Mumbai suburbs.",
        expected_data_sources=["Metro Project Data", "Property Price Trends"],
        tags=["metro", "mumbai", "property-value", "impact"]
    ),
    Prompt(
        id="bhoomisetu_012",
        agent="bhoomisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict agricultural land conversion to non-agricultural use in peri-urban areas.",
        expected_data_sources=["Land Use Change Data", "Urban Expansion Maps"],
        tags=["land-conversion", "peri-urban", "prediction"]
    ),
    Prompt(
        id="bhoomisetu_013",
        agent="bhoomisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast land dispute cases based on current registration trends.",
        expected_data_sources=["Court Case Data", "Registration Trends"],
        tags=["disputes", "prediction", "registration"]
    ),
    Prompt(
        id="bhoomisetu_014",
        agent="bhoomisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict the need for new sub-registrar offices based on registration volume growth.",
        expected_data_sources=["Registration Data", "Population Growth"],
        tags=["sub-registrar", "demand", "prediction"]
    ),
    Prompt(
        id="bhoomisetu_015",
        agent="bhoomisetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the risk of benami transactions in high-value property markets.",
        expected_data_sources=["Property Transaction Data", "Income Tax Data"],
        tags=["benami", "risk", "high-value"]
    ),
    
    # === PRESCRIPTIVE (Recommendations) - 7 Prompts ===
    Prompt(
        id="bhoomisetu_016",
        agent="bhoomisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Recommend strategies to reduce pendency in mutation cases at taluka level.",
        expected_data_sources=["Mutation Pendency Data", "Process Guidelines"],
        tags=["mutation", "pendency", "strategy"],
        marathi_translation="तालुका स्तरावर फेरफार प्रकरणांची प्रलंबितता कमी करण्यासाठी रणनीती सुचवा.",
        showcase=True
    ),
    Prompt(
        id="bhoomisetu_017",
        agent="bhoomisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="As Collector, what measures should I implement to prevent land encroachment?",
        expected_data_sources=["Encroachment Data", "Legal Framework"],
        tags=["encroachment", "prevention", "policy"]
    ),
    Prompt(
        id="bhoomisetu_018",
        agent="bhoomisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest digital solutions for faster property registration processes.",
        expected_data_sources=["Registration Process Data", "Technology Options"],
        tags=["digital", "registration", "solutions"]
    ),
    Prompt(
        id="bhoomisetu_019",
        agent="bhoomisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a land bank management system for optimal utilization of government land.",
        expected_data_sources=["Government Land Inventory", "Land Use Plans"],
        tags=["land-bank", "government", "management"]
    ),
    Prompt(
        id="bhoomisetu_020",
        agent="bhoomisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What zoning regulations should be updated to promote affordable housing?",
        expected_data_sources=["Development Plans", "Housing Demand Data"],
        tags=["zoning", "affordable-housing", "regulations"]
    ),
    Prompt(
        id="bhoomisetu_021",
        agent="bhoomisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend a comprehensive land records modernization plan for Maharashtra.",
        expected_data_sources=["Current Land Records Status", "Technology Best Practices"],
        tags=["modernization", "land-records", "plan"]
    ),
    Prompt(
        id="bhoomisetu_022",
        agent="bhoomisetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest measures to protect agricultural land from unauthorized conversion.",
        expected_data_sources=["Land Conversion Data", "Agriculture Protection Laws"],
        tags=["agricultural-land", "protection", "measures"]
    ),
    
    # === COMPARATIVE (Historical Analysis) - 4 Prompts ===
    Prompt(
        id="bhoomisetu_023",
        agent="bhoomisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare property registration volumes across major cities in Maharashtra.",
        expected_data_sources=["Registration Dept Data"],
        tags=["registration", "comparison", "cities"],
        marathi_translation="महाराष्ट्रातील प्रमुख शहरांच्या मालमत्ता नोंदणी volumes ची तुलना करा."
    ),
    Prompt(
        id="bhoomisetu_024",
        agent="bhoomisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.BASIC,
        query="How have ready reckoner rates changed in Mumbai over the last 5 years?",
        expected_data_sources=["Historical Ready Reckoner Data"],
        tags=["ready-reckoner", "mumbai", "trend"]
    ),
    Prompt(
        id="bhoomisetu_025",
        agent="bhoomisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare land dispute resolution time across different districts.",
        expected_data_sources=["Court Case Data", "Revenue Dept Reports"],
        tags=["disputes", "resolution-time", "comparison"]
    ),
    Prompt(
        id="bhoomisetu_026",
        agent="bhoomisetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare Maharashtra's land record digitization progress with other states.",
        expected_data_sources=["National Land Records Data"],
        tags=["digitization", "comparison", "states"]
    ),
    
    # === CROSS-DOMAIN (Multi-Agent) - 2 Prompts ===
    Prompt(
        id="bhoomisetu_027",
        agent="bhoomisetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How does agricultural land fragmentation affect farming productivity in Vidarbha?",
        expected_data_sources=["Land Holdings Data", "Agriculture Productivity Data"],
        tags=["cross-domain", "krishisetu", "fragmentation", "productivity"],
        showcase=True
    ),
    Prompt(
        id="bhoomisetu_028",
        agent="bhoomisetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the impact of urban expansion on surrounding agricultural land in Pune.",
        expected_data_sources=["Urban Planning Data", "Land Use Maps"],
        tags=["cross-domain", "nagarsetu", "urban-expansion", "agriculture"]
    ),
    
    # === CITIZEN-FACING - 1 Prompt ===
    Prompt(
        id="bhoomisetu_029",
        agent="bhoomisetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to download 7/12 extract (Satbara) online for my land?",
        expected_data_sources=["Bhulekh Portal Guidelines"],
        tags=["citizen", "7/12", "satbara", "download"],
        marathi_translation="माझ्या जमिनीसाठी ७/१२ उतारा ऑनलाइन कसा डाउनलोड करायचा?"
    ),
    
    # === OFFICER-FACING (Decision Support) - 1 Prompt ===
    Prompt(
        id="bhoomisetu_030",
        agent="bhoomisetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a comprehensive land administration reform plan for Maharashtra.",
        expected_data_sources=["Land Administration Data", "International Best Practices"],
        tags=["officer", "reform", "land-administration", "plan"],
        showcase=True
    ),
]

def register_bhoomisetu_prompts(library):
    """Register all BhoomiSetu prompts in the library."""
    for prompt in BHOOMISETU_PROMPTS:
        library.register(prompt)
