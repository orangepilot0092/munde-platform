"""
Munde Sahayak: Orchestrator Prompt Library
30 carefully crafted prompts covering multi-agent routing, complex synthesis, and system-level interactions.
"""
from munde.prompts.base import Prompt, PromptCategory, PromptDifficulty

MUNDE_SAHAYAK_PROMPTS = [
    # === SITUATIONAL (System State & Routing) - 6 Prompts ===
    Prompt(
        id="munde_001",
        agent="munde_sahayak",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Which specialized agent should handle my query about reservoir water levels?",
        expected_data_sources=["Agent Registry"],
        tags=["routing", "water", "jalsetu"],
        marathi_translation="धरणाच्या पाणी पातळीबद्दलच्या माझ्या प्रश्नासाठी कोणता विशेषज्ञ एजंट योग्य आहे?",
        showcase=True
    ),
    Prompt(
        id="munde_002",
        agent="munde_sahayak",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Summarize the current status of all active government schemes for farmers.",
        expected_data_sources=["KrishiSetu", "JanSetu"],
        tags=["summary", "schemes", "farmers"]
    ),
    Prompt(
        id="munde_003",
        agent="munde_sahayak",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What are the capabilities of the ArogyaSetu agent?",
        expected_data_sources=["Agent Registry"],
        tags=["capabilities", "arogyasetu", "health"]
    ),
    Prompt(
        id="munde_004",
        agent="munde_sahayak",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Provide a dashboard-style summary of Maharashtra's key development indicators.",
        expected_data_sources=["All Agents"],
        tags=["dashboard", "indicators", "state"]
    ),
    Prompt(
        id="munde_005",
        agent="munde_sahayak",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Translate my previous query about land records into Marathi.",
        expected_data_sources=["Translation Module"],
        tags=["translation", "marathi", "land-records"]
    ),
    Prompt(
        id="munde_006",
        agent="munde_sahayak",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Identify which department is responsible for fixing potholes on state highways.",
        expected_data_sources=["MargSetu", "PWD Guidelines"],
        tags=["responsibility", "potholes", "highways"]
    ),
    
    # === PREDICTIVE (Complex Forecasting Synthesis) - 6 Prompts ===
    Prompt(
        id="munde_007",
        agent="munde_sahayak",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.EXPERT,
        query="Synthesize a comprehensive risk assessment for Marathwada considering drought, agriculture, and health factors.",
        expected_data_sources=["JalSetu", "KrishiSetu", "ArogyaSetu"],
        tags=["synthesis", "marathwada", "multi-domain-risk"],
        marathi_translation="दुष्काळ, कृषी आणि आरोग्य घटकांचा विचार करून मराठवाड्यासाठी संपूर्ण जोखीम मूल्यांकन तयार करा.",
        showcase=True
    ),
    Prompt(
        id="munde_008",
        agent="munde_sahayak",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast the cascading impact of a severe cyclone on Mumbai's transport, power, and citizen services.",
        expected_data_sources=["AapattiSetu", "MargSetu", "UrjaSetu", "JanSetu"],
        tags=["cascading-impact", "cyclone", "mumbai"]
    ),
    Prompt(
        id="munde_009",
        agent="munde_sahayak",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict the long-term socio-economic impact of the new bullet train project on connected districts.",
        expected_data_sources=["MargSetu", "BhoomiSetu", "Economic Data"],
        tags=["bullet-train", "socio-economic", "impact"]
    ),
    Prompt(
        id="munde_010",
        agent="munde_sahayak",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Analyze how changing monsoon patterns will affect both urban flooding and rural agriculture.",
        expected_data_sources=["NagarSetu", "KrishiSetu", "IMD Data"],
        tags=["monsoon", "urban-flood", "rural-agri"]
    ),
    Prompt(
        id="munde_011",
        agent="munde_sahayak",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast the demand for educational infrastructure in newly industrialized zones over the next decade.",
        expected_data_sources=["ShikshanSetu", "Industrial Growth Data"],
        tags=["education-demand", "industrial-zones", "forecast"]
    ),
    Prompt(
        id="munde_012",
        agent="munde_sahayak",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.EXPERT,
        query="Predict the strain on the healthcare system during a concurrent heatwave and disease outbreak.",
        expected_data_sources=["ArogyaSetu", "AapattiSetu"],
        tags=["healthcare-strain", "heatwave", "outbreak"]
    ),
    
    # === PRESCRIPTIVE (Multi-Agent Recommendations) - 6 Prompts ===
    Prompt(
        id="munde_013",
        agent="munde_sahayak",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.EXPERT,
        query="Design a holistic rural development strategy integrating water, agriculture, and education.",
        expected_data_sources=["JalSetu", "KrishiSetu", "ShikshanSetu"],
        tags=["rural-development", "holistic", "strategy"],
        marathi_translation="पाणी, कृषी आणि शिक्षण यांचा समावेश असलेली संपूर्ण ग्रामीण विकास रणनीती तयार करा.",
        showcase=True
    ),
    Prompt(
        id="munde_014",
        agent="munde_sahayak",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend a coordinated response plan for a district facing simultaneous flood and disease outbreak.",
        expected_data_sources=["AapattiSetu", "ArogyaSetu", "MargSetu"],
        tags=["coordinated-response", "flood", "disease"]
    ),
    Prompt(
        id="munde_015",
        agent="munde_sahayak",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Suggest policy interventions to balance urban expansion with agricultural land preservation.",
        expected_data_sources=["NagarSetu", "BhoomiSetu", "KrishiSetu"],
        tags=["policy", "urban-expansion", "agri-preservation"]
    ),
    Prompt(
        id="munde_016",
        agent="munde_sahayak",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Provide a step-by-step guide for a citizen to access all available benefits after a natural disaster.",
        expected_data_sources=["AapattiSetu", "JanSetu"],
        tags=["citizen-guide", "disaster-benefits", "step-by-step"]
    ),
    Prompt(
        id="munde_017",
        agent="munde_sahayak",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design an integrated smart city framework that connects transport, waste, and energy management.",
        expected_data_sources=["NagarSetu", "MargSetu", "UrjaSetu"],
        tags=["smart-city", "integrated", "framework"]
    ),
    Prompt(
        id="munde_018",
        agent="munde_sahayak",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.EXPERT,
        query="Formulate a state-wide strategy to improve the ease of doing business for MSMEs.",
        expected_data_sources=["UdyogSetu", "BhoomiSetu", "JanSetu"],
        tags=["msme", "ease-of-doing-business", "strategy"]
    ),
    
    # === COMPARATIVE (Cross-Domain Analysis) - 4 Prompts ===
    Prompt(
        id="munde_019",
        agent="munde_sahayak",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.EXPERT,
        query="Compare the development trajectory of Pune and Nagpur across infrastructure, education, and health.",
        expected_data_sources=["NagarSetu", "ShikshanSetu", "ArogyaSetu"],
        tags=["comparison", "pune", "nagpur", "trajectory"],
        marathi_translation="पायाभूत सुविधा, शिक्षण आणि आरोग्य या क्षेत्रात पुणे आणि नागपूरच्या विकास वाटचालीची तुलना करा."
    ),
    Prompt(
        id="munde_020",
        agent="munde_sahayak",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the trade-offs between rapid industrialization and environmental conservation in Maharashtra.",
        expected_data_sources=["UdyogSetu", "VanaSetu", "Economic Data"],
        tags=["trade-offs", "industrialization", "environment"]
    ),
    Prompt(
        id="munde_021",
        agent="munde_sahayak",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare the effectiveness of different welfare delivery models across districts.",
        expected_data_sources=["JanSetu", "District Performance Data"],
        tags=["welfare-delivery", "comparison", "districts"]
    ),
    Prompt(
        id="munde_022",
        agent="munde_sahayak",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Evaluate how Maharashtra's digital governance maturity compares to global best practices.",
        expected_data_sources=["E-Governance Metrics", "Global Indices"],
        tags=["digital-governance", "global-comparison", "evaluation"]
    ),
    
    # === CITIZEN-FACING (Conversational & Helpful) - 4 Prompts ===
    Prompt(
        id="munde_023",
        agent="munde_sahayak",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="I am a farmer in drought-affected Beed. What help can the government provide me?",
        expected_data_sources=["KrishiSetu", "JanSetu", "AapattiSetu"],
        tags=["citizen", "farmer", "drought-help"],
        marathi_translation="मी दुष्काळग्रस्त बीडमधील शेतकरी आहे. सरकार मला काय मदत करू शकते?",
        showcase=True
    ),
    Prompt(
        id="munde_024",
        agent="munde_sahayak",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Explain the new education policy in simple Marathi for a parent.",
        expected_data_sources=["ShikshanSetu", "NEP 2020 Simplified"],
        tags=["citizen", "education-policy", "simple-marathi"]
    ),
    Prompt(
        id="munde_025",
        agent="munde_sahayak",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="My ration card application is delayed. Who should I contact and what is the process?",
        expected_data_sources=["JanSetu", "Civil Supplies Guidelines"],
        tags=["citizen", "ration-card", "delay", "contact"]
    ),
    Prompt(
        id="munde_026",
        agent="munde_sahayak",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Summarize the key benefits of the state health insurance scheme for my family.",
        expected_data_sources=["ArogyaSetu", "MJPJAY Guidelines"],
        tags=["citizen", "health-insurance", "benefits"]
    ),
    
    # === OFFICER-FACING (Executive Synthesis) - 4 Prompts ===
    Prompt(
        id="munde_027",
        agent="munde_sahayak",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a comprehensive briefing note for the Chief Minister on the state's preparedness for the upcoming monsoon.",
        expected_data_sources=["AapattiSetu", "JalSetu", "NagarSetu", "MargSetu"],
        tags=["officer", "briefing", "monsoon-preparedness", "cm"],
        showcase=True
    ),
    Prompt(
        id="munde_028",
        agent="munde_sahayak",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Synthesize a cross-departmental action plan to improve the state's ranking in the NITI Aayog SDG Index.",
        expected_data_sources=["All Agents", "SDG Framework"],
        tags=["officer", "sdg", "action-plan", "niti-aayog"]
    ),
    Prompt(
        id="munde_029",
        agent="munde_sahayak",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.ADVANCED,
        query="Identify the top 3 systemic bottlenecks in welfare delivery and propose cross-departmental solutions.",
        expected_data_sources=["JanSetu", "Process Analytics"],
        tags=["officer", "bottlenecks", "welfare", "solutions"]
    ),
    Prompt(
        id="munde_030",
        agent="munde_sahayak",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Draft a vision document for 'Digital Maharashtra 2030' integrating all domain intelligence.",
        expected_data_sources=["All Agents", "IT Policy", "Economic Vision"],
        tags=["officer", "vision", "digital-maharashtra", "2030"]
    ),
]

def register_munde_sahayak_prompts(library):
    """Register all Munde Sahayak prompts in the library."""
    for prompt in MUNDE_SAHAYAK_PROMPTS:
        library.register(prompt)
