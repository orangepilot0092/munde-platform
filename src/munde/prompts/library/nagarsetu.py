"""
NagarSetu: Urban Intelligence Prompt Library
50 carefully crafted prompts covering all urban governance scenarios in Maharashtra.
"""
from munde.prompts.base import Prompt, PromptCategory, PromptDifficulty

NAGARSETU_PROMPTS = [
    # === SITUATIONAL (Current State) - 10 Prompts ===
    Prompt(
        id="nagarsetu_001",
        agent="nagarsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current waste collection status in Pune Municipal Corporation area?",
        expected_data_sources=["PMC Waste Management Dashboard"],
        tags=["waste", "pune", "collection"],
        marathi_translation="पुणे महानगरपालिका क्षेत्रातील कचरा संकलनाची सध्याची स्थिती काय आहे?",
        showcase=True
    ),
    Prompt(
        id="nagarsetu_002",
        agent="nagarsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me traffic congestion levels at major junctions in Mumbai.",
        expected_data_sources=["Mumbai Traffic Police Data"],
        tags=["traffic", "mumbai", "congestion"],
        marathi_translation="मुंबईतील प्रमुख चौकांमध्ये वाहतुकीची कोंडी किती आहे?"
    ),
    Prompt(
        id="nagarsetu_003",
        agent="nagarsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the air quality index across all major cities in Maharashtra?",
        expected_data_sources=["MPCB Air Quality Data", "CPCB"],
        tags=["air-quality", "cities", "state"],
        showcase=True
    ),
    Prompt(
        id="nagarsetu_004",
        agent="nagarsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many smart city projects are currently active in Maharashtra?",
        expected_data_sources=["Smart City Mission Data"],
        tags=["smart-city", "projects", "status"]
    ),
    Prompt(
        id="nagarsetu_005",
        agent="nagarsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current water supply coverage in Nagpur city?",
        expected_data_sources=["NMC Water Department"],
        tags=["water-supply", "nagpur", "coverage"]
    ),
    Prompt(
        id="nagarsetu_006",
        agent="nagarsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the status of public toilets in Thane municipal area.",
        expected_data_sources=["TMC Public Amenities Data"],
        tags=["toilets", "thane", "amenities"]
    ),
    Prompt(
        id="nagarsetu_007",
        agent="nagarsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current property tax collection status in PMC?",
        expected_data_sources=["PMC Revenue Department"],
        tags=["property-tax", "pune", "collection"]
    ),
    Prompt(
        id="nagarsetu_008",
        agent="nagarsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many building proposals are pending approval in Mumbai?",
        expected_data_sources=["BMC Development Plan Dept"],
        tags=["building", "mumbai", "approvals"]
    ),
    Prompt(
        id="nagarsetu_009",
        agent="nagarsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current status of solid waste processing plants in Maharashtra?",
        expected_data_sources=["SWaCH Data", "Urban Development Dept"],
        tags=["waste-processing", "plants", "state"]
    ),
    Prompt(
        id="nagarsetu_010",
        agent="nagarsetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the list of active AMRUT projects in Nashik.",
        expected_data_sources=["AMRUT Mission Data"],
        tags=["amrut", "nashik", "projects"]
    ),
    
    # === PREDICTIVE (Forecasting & Risk) - 10 Prompts ===
    Prompt(
        id="nagarsetu_011",
        agent="nagarsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict traffic congestion patterns in Mumbai for the next week considering upcoming events.",
        expected_data_sources=["Historical Traffic Data", "Event Calendar", "Weather"],
        tags=["traffic", "mumbai", "prediction"],
        marathi_translation="आगामी कार्यक्रमांनुसार पुढील आठवड्यासाठी मुंबईतील वाहतूक कोंडीचा अंदाज काय आहे?"
    ),
    Prompt(
        id="nagarsetu_012",
        agent="nagarsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast urban flooding risk in low-lying areas of Mumbai during heavy rainfall.",
        expected_data_sources=["Topography Data", "IMD Forecast", "Drainage Maps"],
        tags=["flood", "mumbai", "urban", "risk"],
        showcase=True
    ),
    Prompt(
        id="nagarsetu_013",
        agent="nagarsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict waste generation in Pune for the next month based on seasonal trends.",
        expected_data_sources=["Historical Waste Data", "Population Trends"],
        tags=["waste", "pune", "prediction"]
    ),
    Prompt(
        id="nagarsetu_014",
        agent="nagarsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the impact of new metro lines on traffic patterns in Pune over the next 5 years.",
        expected_data_sources=["Metro Project Data", "Traffic Models"],
        tags=["metro", "pune", "traffic", "impact"]
    ),
    Prompt(
        id="nagarsetu_015",
        agent="nagarsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict air quality deterioration in industrial zones of Nashik during winter.",
        expected_data_sources=["MPCB Data", "Weather Patterns", "Industrial Activity"],
        tags=["air-quality", "nashik", "industrial"]
    ),
    Prompt(
        id="nagarsetu_016",
        agent="nagarsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast property price trends in Mumbai suburbs for the next 2 years.",
        expected_data_sources=["Property Registration Data", "Market Trends"],
        tags=["property", "mumbai", "prices", "prediction"]
    ),
    Prompt(
        id="nagarsetu_017",
        agent="nagarsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict water demand in Nagpur city during summer peak months.",
        expected_data_sources=["Historical Consumption", "Population Data", "Weather"],
        tags=["water-demand", "nagpur", "summer"]
    ),
    Prompt(
        id="nagarsetu_018",
        agent="nagarsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the impact of rapid urbanization on groundwater levels in Pune.",
        expected_data_sources=["CGWB Data", "Urban Expansion Maps"],
        tags=["groundwater", "pune", "urbanization"]
    ),
    Prompt(
        id="nagarsetu_019",
        agent="nagarsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict the need for new public transport routes in Thane based on population growth.",
        expected_data_sources=["Population Data", "Transport Usage"],
        tags=["transport", "thane", "prediction"]
    ),
    Prompt(
        id="nagarsetu_020",
        agent="nagarsetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast the impact of climate change on Mumbai's coastal infrastructure by 2030.",
        expected_data_sources=["Climate Models", "Coastal Zone Maps"],
        tags=["climate", "mumbai", "coastal", "infrastructure"]
    ),
    
    # === PRESCRIPTIVE (Recommendations) - 10 Prompts ===
    Prompt(
        id="nagarsetu_021",
        agent="nagarsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Recommend waste segregation strategies for residential societies in Pune.",
        expected_data_sources=["SWaCH Guidelines", "Best Practices"],
        tags=["waste", "segregation", "pune", "recommendation"],
        marathi_translation="पुण्यातील निवासी सोसायट्यांसाठी कचरा वर्गीकरणाच्या रणनीती सुचवा.",
        showcase=True
    ),
    Prompt(
        id="nagarsetu_022",
        agent="nagarsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="As Municipal Commissioner, what measures should I implement to reduce traffic congestion in Mumbai?",
        expected_data_sources=["Traffic Studies", "International Best Practices"],
        tags=["traffic", "mumbai", "policy", "measures"]
    ),
    Prompt(
        id="nagarsetu_023",
        agent="nagarsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest rainwater harvesting mandates for new buildings in Nashik.",
        expected_data_sources=["Building Bylaws", "Water Conservation Guidelines"],
        tags=["rainwater", "nashik", "buildings"]
    ),
    Prompt(
        id="nagarsetu_024",
        agent="nagarsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a comprehensive urban mobility plan for Nagpur considering metro expansion.",
        expected_data_sources=["Transport Data", "Metro Plans", "Population Projections"],
        tags=["mobility", "nagpur", "metro", "plan"]
    ),
    Prompt(
        id="nagarsetu_025",
        agent="nagarsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What green building standards should be mandatory for commercial complexes in Pune?",
        expected_data_sources=["GRIHA Guidelines", "Energy Conservation Codes"],
        tags=["green-building", "pune", "standards"]
    ),
    Prompt(
        id="nagarsetu_026",
        agent="nagarsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend strategies to improve air quality in Mumbai's industrial zones.",
        expected_data_sources=["MPCB Data", "Industrial Emission Studies"],
        tags=["air-quality", "mumbai", "industrial", "strategy"]
    ),
    Prompt(
        id="nagarsetu_027",
        agent="nagarsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest parking management solutions for congested areas in Thane.",
        expected_data_sources=["Traffic Studies", "Smart City Guidelines"],
        tags=["parking", "thane", "management"]
    ),
    Prompt(
        id="nagarsetu_028",
        agent="nagarsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a flood-resilient urban planning framework for coastal Mumbai.",
        expected_data_sources=["Flood Maps", "Coastal Regulations", "Climate Data"],
        tags=["flood", "mumbai", "planning", "resilient"]
    ),
    Prompt(
        id="nagarsetu_029",
        agent="nagarsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What smart city technologies should be prioritized for Aurangabad?",
        expected_data_sources=["Smart City Guidelines", "City Needs Assessment"],
        tags=["smart-city", "aurangabad", "technology"]
    ),
    Prompt(
        id="nagarsetu_030",
        agent="nagarsetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend a city-wide waste-to-energy plant strategy for Pune.",
        expected_data_sources=["Waste Generation Data", "Technology Options"],
        tags=["waste-to-energy", "pune", "strategy"]
    ),
    
    # === COMPARATIVE (Historical Analysis) - 5 Prompts ===
    Prompt(
        id="nagarsetu_031",
        agent="nagarsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare waste management performance across major municipal corporations in Maharashtra.",
        expected_data_sources=["Municipal Performance Data"],
        tags=["waste", "comparison", "municipal"],
        marathi_translation="महाराष्ट्रातील प्रमुख महानगरपालिकांच्या कचरा व्यवस्थापन कामगिरीची तुलना करा."
    ),
    Prompt(
        id="nagarsetu_032",
        agent="nagarsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.BASIC,
        query="How has Mumbai's air quality changed over the last 5 years?",
        expected_data_sources=["MPCB Historical Data"],
        tags=["air-quality", "mumbai", "trend"]
    ),
    Prompt(
        id="nagarsetu_033",
        agent="nagarsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare property tax rates across major cities in Maharashtra.",
        expected_data_sources=["Municipal Tax Data"],
        tags=["property-tax", "comparison", "cities"]
    ),
    Prompt(
        id="nagarsetu_034",
        agent="nagarsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare public transport usage in Pune before and after metro inauguration.",
        expected_data_sources=["Transport Usage Data"],
        tags=["transport", "pune", "metro", "comparison"]
    ),
    Prompt(
        id="nagarsetu_035",
        agent="nagarsetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Compare Maharashtra's urbanization rate with other major Indian states.",
        expected_data_sources=["Census Data", "Urban Development Reports"],
        tags=["urbanization", "comparison", "states"]
    ),
    
    # === CROSS-DOMAIN (Multi-Agent) - 5 Prompts ===
    Prompt(
        id="nagarsetu_036",
        agent="nagarsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How does urban expansion in Pune affect surrounding agricultural land and water resources?",
        expected_data_sources=["Urban Planning Data", "Land Use Maps", "WRD Data"],
        tags=["cross-domain", "jalsetu", "krishisetu", "pune", "expansion"],
        marathi_translation="पुण्यातील शहरी विस्तार आजूबाजूच्या शेतजमीन आणि पाण्याच्या स्त्रोतांवर कसा परिणाम करतो?"
    ),
    Prompt(
        id="nagarsetu_037",
        agent="nagarsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the health impact of air pollution in Mumbai's industrial zones.",
        expected_data_sources=["MPCB Data", "Health Department Data"],
        tags=["cross-domain", "arogyasetu", "air-quality", "mumbai", "health"]
    ),
    Prompt(
        id="nagarsetu_038",
        agent="nagarsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How can urban waste management support rural composting initiatives?",
        expected_data_sources=["Waste Management Data", "Agriculture Extension"],
        tags=["cross-domain", "krishisetu", "waste", "composting"]
    ),
    Prompt(
        id="nagarsetu_039",
        agent="nagarsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="What disaster preparedness measures should Mumbai implement considering coastal vulnerability?",
        expected_data_sources=["Coastal Data", "Disaster Management Plans"],
        tags=["cross-domain", "aapattisetu", "mumbai", "disaster"]
    ),
    Prompt(
        id="nagarsetu_040",
        agent="nagarsetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How can smart city initiatives improve education infrastructure in urban areas?",
        expected_data_sources=["Smart City Plans", "Education Dept Data"],
        tags=["cross-domain", "shikshansetu", "smart-city", "education"],
        showcase=True
    ),
    
    # === CITIZEN-FACING - 5 Prompts ===
    Prompt(
        id="nagarsetu_041",
        agent="nagarsetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to apply for a building permission in Pune Municipal Corporation?",
        expected_data_sources=["PMC Building Dept Guidelines"],
        tags=["citizen", "building", "permission", "pune"],
        marathi_translation="पुणे महानगरपालिकेत बांधकाम परवानगीसाठी अर्ज कसा करायचा?"
    ),
    Prompt(
        id="nagarsetu_042",
        agent="nagarsetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to pay property tax online in Mumbai?",
        expected_data_sources=["BMC Property Tax Portal"],
        tags=["citizen", "property-tax", "mumbai", "online"],
        marathi_translation="मुंबईत ऑनलाइन मालमत्ता कर कसा भरावा?"
    ),
    Prompt(
        id="nagarsetu_043",
        agent="nagarsetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the procedure to file a complaint about garbage not being collected?",
        expected_data_sources=["Municipal Grievance Portal"],
        tags=["citizen", "complaint", "garbage"],
        marathi_translation="कचरा उचलला जात नसल्याची तक्रार कशी नोंदवावी?"
    ),
    Prompt(
        id="nagarsetu_044",
        agent="nagarsetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to get a birth certificate from the municipal corporation?",
        expected_data_sources=["Municipal Civil Dept"],
        tags=["citizen", "birth-certificate", "municipal"]
    ),
    Prompt(
        id="nagarsetu_045",
        agent="nagarsetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What documents are required for name mutation in property records?",
        expected_data_sources=["Revenue Dept Guidelines"],
        tags=["citizen", "mutation", "property", "documents"],
        marathi_translation="मालमत्ता नोंदणीत नाव बदलण्यासाठी कोणती कागदपत्रे आवश्यक आहेत?"
    ),
    
    # === OFFICER-FACING (Decision Support) - 5 Prompts ===
    Prompt(
        id="nagarsetu_046",
        agent="nagarsetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a comprehensive urban development strategy for tier-2 cities in Maharashtra.",
        expected_data_sources=["Urban Development Data", "Economic Surveys"],
        tags=["officer", "urban-development", "tier-2", "strategy"],
        showcase=True
    ),
    Prompt(
        id="nagarsetu_047",
        agent="nagarsetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the effectiveness of Smart City Mission projects in Maharashtra.",
        expected_data_sources=["Smart City Project Data", "Performance Reports"],
        tags=["officer", "smart-city", "effectiveness", "analysis"]
    ),
    Prompt(
        id="nagarsetu_048",
        agent="nagarsetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.ADVANCED,
        query="Draft a policy framework for sustainable urban mobility in Maharashtra cities.",
        expected_data_sources=["Transport Data", "Sustainability Guidelines"],
        tags=["officer", "mobility", "policy", "sustainable"]
    ),
    Prompt(
        id="nagarsetu_049",
        agent="nagarsetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a report on municipal corporation financial health across Maharashtra.",
        expected_data_sources=["Municipal Finance Data", "CAG Reports"],
        tags=["officer", "municipal", "finance", "report"]
    ),
    Prompt(
        id="nagarsetu_050",
        agent="nagarsetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Design a climate action plan for Maharashtra's urban local bodies.",
        expected_data_sources=["Climate Data", "Urban Planning Guidelines"],
        tags=["officer", "climate", "urban", "action-plan"]
    ),
]

def register_nagarsetu_prompts(library):
    """Register all NagarSetu prompts in the library."""
    for prompt in NAGARSETU_PROMPTS:
        library.register(prompt)
