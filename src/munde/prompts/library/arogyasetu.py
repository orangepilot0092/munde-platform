"""
ArogyaSetu: Health Intelligence Prompt Library
50 carefully crafted prompts covering all public health scenarios in Maharashtra.
"""
from munde.prompts.base import Prompt, PromptCategory, PromptDifficulty

AROGYASETU_PROMPTS = [
    # === SITUATIONAL (Current State) - 10 Prompts ===
    Prompt(
        id="arogyasetu_001",
        agent="arogyasetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current bed occupancy rate in Pune district hospitals?",
        expected_data_sources=["Health Department Dashboard", "Hospital MIS"],
        tags=["beds", "pune", "occupancy"],
        marathi_translation="पुणे जिल्ह्यातील रुग्णालयांतील बेड व्यापण्याचे प्रमाण काय आहे?",
        showcase=True
    ),
    Prompt(
        id="arogyasetu_002",
        agent="arogyasetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the current dengue case count across all districts in Maharashtra.",
        expected_data_sources=["IDSP Disease Surveillance Data"],
        tags=["dengue", "cases", "districts"],
        marathi_translation="महाराष्ट्रातील सर्व जिल्ह्यांतील डेंग्यू रुग्णांची सध्याची संख्या दाखवा."
    ),
    Prompt(
        id="arogyasetu_003",
        agent="arogyasetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the vaccination coverage for children under 5 in Nagpur district?",
        expected_data_sources=["CoWIN Data", "Health Dept Immunization Records"],
        tags=["vaccination", "children", "nagpur"],
        showcase=True
    ),
    Prompt(
        id="arogyasetu_004",
        agent="arogyasetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many primary health centers are operational in Maharashtra?",
        expected_data_sources=["Health Infrastructure Data"],
        tags=["phc", "infrastructure", "state"]
    ),
    Prompt(
        id="arogyasetu_005",
        agent="arogyasetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current availability of ICU beds in Mumbai hospitals?",
        expected_data_sources=["Mumbai Health Dept", "Hospital Dashboard"],
        tags=["icu", "mumbai", "beds"]
    ),
    Prompt(
        id="arogyasetu_006",
        agent="arogyasetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the maternal mortality rate across all districts in Maharashtra.",
        expected_data_sources=["Health Dept Vital Statistics"],
        tags=["mmr", "maternal", "districts"]
    ),
    Prompt(
        id="arogyasetu_007",
        agent="arogyasetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current status of Ayushman Bharat card enrollment in my district?",
        expected_data_sources=["PM-JAY Portal Data"],
        tags=["ayushman", "enrollment", "district"]
    ),
    Prompt(
        id="arogyasetu_008",
        agent="arogyasetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many community health workers (ASHA) are active in rural Maharashtra?",
        expected_data_sources=["NHM Data"],
        tags=["asha", "workers", "rural"]
    ),
    Prompt(
        id="arogyasetu_009",
        agent="arogyasetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current tuberculosis treatment success rate in Maharashtra?",
        expected_data_sources=["NTEP Data"],
        tags=["tuberculosis", "treatment", "state"]
    ),
    Prompt(
        id="arogyasetu_010",
        agent="arogyasetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the list of empaneled hospitals under Mahatma Jyotiba Phule Jan Arogya Yojana.",
        expected_data_sources=["MJPJAY Portal"],
        tags=["hospitals", "empaneled", "scheme"]
    ),
    
    # === PREDICTIVE (Forecasting & Risk) - 10 Prompts ===
    Prompt(
        id="arogyasetu_011",
        agent="arogyasetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict dengue outbreak risk in Mumbai for the next month based on monsoon patterns.",
        expected_data_sources=["Historical Disease Data", "IMD Rainfall", "Vector Surveillance"],
        tags=["dengue", "mumbai", "outbreak", "prediction"],
        marathi_translation="पावसाच्या पॅटर्ननुसार पुढील महिन्यासाठी मुंबईतील डेंग्यू साथीचा धोका काय आहे?",
        showcase=True
    ),
    Prompt(
        id="arogyasetu_012",
        agent="arogyasetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast hospital bed demand in Pune during the upcoming festival season.",
        expected_data_sources=["Historical Admission Data", "Festival Calendar"],
        tags=["beds", "pune", "demand", "festival"]
    ),
    Prompt(
        id="arogyasetu_013",
        agent="arogyasetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict the spread of waterborne diseases in flood-affected areas of Kolhapur.",
        expected_data_sources=["Flood Data", "Historical Disease Patterns"],
        tags=["waterborne", "kolhapur", "flood", "prediction"]
    ),
    Prompt(
        id="arogyasetu_014",
        agent="arogyasetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the impact of air pollution on respiratory diseases in Mumbai over the next 5 years.",
        expected_data_sources=["MPCB Air Quality Data", "Health Statistics"],
        tags=["air-pollution", "respiratory", "mumbai", "impact"]
    ),
    Prompt(
        id="arogyasetu_015",
        agent="arogyasetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict malnutrition rates in tribal districts based on current PDS distribution.",
        expected_data_sources=["PDS Data", "Nutrition Surveys"],
        tags=["malnutrition", "tribal", "prediction"]
    ),
    Prompt(
        id="arogyasetu_016",
        agent="arogyasetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast the need for dialysis centers in rural Maharashtra over the next decade.",
        expected_data_sources=["CKD Prevalence Data", "Demographic Trends"],
        tags=["dialysis", "rural", "forecast"]
    ),
    Prompt(
        id="arogyasetu_017",
        agent="arogyasetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict malaria risk in coastal districts during post-monsoon period.",
        expected_data_sources=["Historical Malaria Data", "Weather Patterns"],
        tags=["malaria", "coastal", "risk"]
    ),
    Prompt(
        id="arogyasetu_018",
        agent="arogyasetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the impact of climate change on vector-borne diseases in Maharashtra.",
        expected_data_sources=["Climate Models", "Disease Surveillance"],
        tags=["climate", "vector-borne", "impact"]
    ),
    Prompt(
        id="arogyasetu_019",
        agent="arogyasetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict the burden of non-communicable diseases in urban Maharashtra by 2030.",
        expected_data_sources=["NCD Surveys", "Demographic Data"],
        tags=["ncd", "urban", "burden", "prediction"]
    ),
    Prompt(
        id="arogyasetu_020",
        agent="arogyasetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast mental health service requirements in post-pandemic Maharashtra.",
        expected_data_sources=["Mental Health Surveys", "Service Utilization Data"],
        tags=["mental-health", "post-pandemic", "forecast"]
    ),
    
    # === PRESCRIPTIVE (Recommendations) - 10 Prompts ===
    Prompt(
        id="arogyasetu_021",
        agent="arogyasetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Recommend strategies to improve vaccination coverage in remote tribal areas.",
        expected_data_sources=["Vaccination Data", "Tribal Health Guidelines"],
        tags=["vaccination", "tribal", "strategy"],
        marathi_translation="दूरस्थ आदिवासी भागात लसीकरण覆盖率 सुधारण्यासाठी रणनीती सुचवा.",
        showcase=True
    ),
    Prompt(
        id="arogyasetu_022",
        agent="arogyasetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="As District Health Officer, what immediate actions should I take to control a cholera outbreak in Latur?",
        expected_data_sources=["Disease Control Guidelines", "Water Quality Data"],
        tags=["cholera", "outbreak", "latur", "action"]
    ),
    Prompt(
        id="arogyasetu_023",
        agent="arogyasetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest measures to reduce infant mortality in high-MMR districts.",
        expected_data_sources=["Health Indicators", "Best Practices"],
        tags=["infant-mortality", "mmr", "measures"]
    ),
    Prompt(
        id="arogyasetu_024",
        agent="arogyasetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a telemedicine expansion plan for rural Maharashtra considering infrastructure constraints.",
        expected_data_sources=["Infrastructure Data", "Telemedicine Guidelines"],
        tags=["telemedicine", "rural", "plan"]
    ),
    Prompt(
        id="arogyasetu_025",
        agent="arogyasetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What nutrition interventions are most effective for addressing anemia in women?",
        expected_data_sources=["Nutrition Studies", "NFHS Data"],
        tags=["anemia", "women", "nutrition"]
    ),
    Prompt(
        id="arogyasetu_026",
        agent="arogyasetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend a comprehensive mental health program for adolescents in urban schools.",
        expected_data_sources=["Mental Health Guidelines", "School Health Data"],
        tags=["mental-health", "adolescents", "schools"]
    ),
    Prompt(
        id="arogyasetu_027",
        agent="arogyasetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest strategies to reduce out-of-pocket healthcare expenditure for rural families.",
        expected_data_sources=["Health Economics Data", "Insurance Schemes"],
        tags=["out-of-pocket", "rural", "expenditure"]
    ),
    Prompt(
        id="arogyasetu_028",
        agent="arogyasetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a disaster-resilient health infrastructure plan for coastal Maharashtra.",
        expected_data_sources=["Disaster Management Plans", "Health Infrastructure Data"],
        tags=["disaster", "coastal", "infrastructure"]
    ),
    Prompt(
        id="arogyasetu_029",
        agent="arogyasetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What quality improvement measures should be implemented in district hospitals?",
        expected_data_sources=["Quality Standards", "Hospital Performance Data"],
        tags=["quality", "hospitals", "measures"]
    ),
    Prompt(
        id="arogyasetu_030",
        agent="arogyasetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend a public health campaign strategy for diabetes prevention in urban Maharashtra.",
        expected_data_sources=["NCD Prevalence Data", "Health Communication Guidelines"],
        tags=["diabetes", "prevention", "campaign"]
    ),
    
    # === COMPARATIVE (Historical Analysis) - 5 Prompts ===
    Prompt(
        id="arogyasetu_031",
        agent="arogyasetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare health indicators across all districts in Maharashtra.",
        expected_data_sources=["Health Statistics", "NFHS Data"],
        tags=["health-indicators", "comparison", "districts"],
        marathi_translation="महाराष्ट्रातील सर्व जिल्ह्यांच्या आरोग्य निर्देशांकांची तुलना करा."
    ),
    Prompt(
        id="arogyasetu_032",
        agent="arogyasetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.BASIC,
        query="How has maternal mortality rate in Maharashtra changed over the last 10 years?",
        expected_data_sources=["Historical Health Data"],
        tags=["mmr", "trend", "historical"]
    ),
    Prompt(
        id="arogyasetu_033",
        agent="arogyasetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare Maharashtra's health infrastructure with other major Indian states.",
        expected_data_sources=["National Health Data"],
        tags=["infrastructure", "comparison", "states"]
    ),
    Prompt(
        id="arogyasetu_034",
        agent="arogyasetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare disease burden between urban and rural areas in Maharashtra.",
        expected_data_sources=["Disease Surveillance Data"],
        tags=["disease", "urban-rural", "comparison"]
    ),
    Prompt(
        id="arogyasetu_035",
        agent="arogyasetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="How has COVID-19 impacted routine immunization coverage in Maharashtra?",
        expected_data_sources=["Pre and Post COVID Vaccination Data"],
        tags=["covid", "immunization", "impact"]
    ),
    
    # === CROSS-DOMAIN (Multi-Agent) - 5 Prompts ===
    Prompt(
        id="arogyasetu_036",
        agent="arogyasetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How does air pollution in Mumbai affect respiratory health and what interventions are needed?",
        expected_data_sources=["MPCB Air Quality Data", "Health Statistics"],
        tags=["cross-domain", "nagarsetu", "air-pollution", "health"],
        showcase=True
    ),
    Prompt(
        id="arogyasetu_037",
        agent="arogyasetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the impact of water contamination on public health in rural Maharashtra.",
        expected_data_sources=["Water Quality Data", "Disease Surveillance"],
        tags=["cross-domain", "jalsetu", "water", "health"]
    ),
    Prompt(
        id="arogyasetu_038",
        agent="arogyasetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How can agricultural pesticide use affect farmer health in Vidarbha?",
        expected_data_sources=["Pesticide Usage Data", "Health Surveys"],
        tags=["cross-domain", "krishisetu", "pesticide", "health"]
    ),
    Prompt(
        id="arogyasetu_039",
        agent="arogyasetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="What health preparedness measures should be implemented for flood-prone districts?",
        expected_data_sources=["Flood Risk Maps", "Health Infrastructure Data"],
        tags=["cross-domain", "aapattisetu", "flood", "health"]
    ),
    Prompt(
        id="arogyasetu_040",
        agent="arogyasetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How can school health programs improve child nutrition outcomes in tribal areas?",
        expected_data_sources=["School Health Data", "Nutrition Surveys"],
        tags=["cross-domain", "shikshansetu", "schools", "nutrition"]
    ),
    
    # === CITIZEN-FACING - 5 Prompts ===
    Prompt(
        id="arogyasetu_041",
        agent="arogyasetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to apply for Mahatma Jyotiba Phule Jan Arogya Yojana card?",
        expected_data_sources=["MJPJAY Guidelines"],
        tags=["citizen", "scheme", "application"],
        marathi_translation="महात्मा ज्योतिबा फुले जनआरोग्य योजना कार्डसाठी अर्ज कसा करायचा?"
    ),
    Prompt(
        id="arogyasetu_042",
        agent="arogyasetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="Where is the nearest government hospital to my location?",
        expected_data_sources=["Health Facility Directory"],
        tags=["citizen", "hospital", "location"],
        marathi_translation="माझ्या ठिकाणाजवळचे सर्वात जवळचे सरकारी रुग्णालय कुठे आहे?"
    ),
    Prompt(
        id="arogyasetu_043",
        agent="arogyasetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What documents are required for availing cashless treatment under the scheme?",
        expected_data_sources=["Scheme Guidelines"],
        tags=["citizen", "documents", "cashless"],
        marathi_translation="योजनेंतर्गत रोख रहित उपचार घेण्यासाठी कोणती कागदपत्रे आवश्यक आहेत?"
    ),
    Prompt(
        id="arogyasetu_044",
        agent="arogyasetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to book an appointment at a district hospital?",
        expected_data_sources=["Hospital Appointment Portal"],
        tags=["citizen", "appointment", "hospital"]
    ),
    Prompt(
        id="arogyasetu_045",
        agent="arogyasetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the procedure to file a complaint about poor quality of care?",
        expected_data_sources=["Grievance Redressal Guidelines"],
        tags=["citizen", "complaint", "quality"]
    ),
    
    # === OFFICER-FACING (Decision Support) - 5 Prompts ===
    Prompt(
        id="arogyasetu_046",
        agent="arogyasetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a comprehensive health infrastructure gap analysis for Maharashtra.",
        expected_data_sources=["Health Infrastructure Data", "Population Data"],
        tags=["officer", "infrastructure", "gap-analysis"],
        showcase=True
    ),
    Prompt(
        id="arogyasetu_047",
        agent="arogyasetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the effectiveness of National Health Mission programs in Maharashtra.",
        expected_data_sources=["NHM Implementation Data", "Outcome Reports"],
        tags=["officer", "nhm", "effectiveness", "analysis"]
    ),
    Prompt(
        id="arogyasetu_048",
        agent="arogyasetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.ADVANCED,
        query="Draft a state health policy framework for addressing non-communicable diseases.",
        expected_data_sources=["NCD Data", "Policy Guidelines"],
        tags=["officer", "policy", "ncd", "framework"]
    ),
    Prompt(
        id="arogyasetu_049",
        agent="arogyasetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a resource allocation plan for district hospitals based on disease burden.",
        expected_data_sources=["Disease Burden Data", "Hospital Capacity"],
        tags=["officer", "resource-allocation", "hospitals"]
    ),
    Prompt(
        id="arogyasetu_050",
        agent="arogyasetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Design a pandemic preparedness plan for Maharashtra considering lessons from COVID-19.",
        expected_data_sources=["COVID Response Data", "Pandemic Guidelines"],
        tags=["officer", "pandemic", "preparedness", "plan"]
    ),
]

def register_arogyasetu_prompts(library):
    """Register all ArogyaSetu prompts in the library."""
    for prompt in AROGYASETU_PROMPTS:
        library.register(prompt)
