"""
JanSetu: Citizen Services Intelligence Prompt Library
30 carefully crafted prompts covering citizen grievances, certificates, and welfare schemes in Maharashtra.
"""
from munde.prompts.base import Prompt, PromptCategory, PromptDifficulty

JANSETU_PROMPTS = [
    # === SITUATIONAL (Current State) - 8 Prompts ===
    Prompt(
        id="jansetu_001",
        agent="jansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current status of my grievance filed on Aaple Sarkar portal?",
        expected_data_sources=["Aaple Sarkar Grievance Portal"],
        tags=["grievance", "aaple-sarkar", "status"],
        marathi_translation="आपले सरकार पोर्टलवर दाखल केलेल्या माझ्या तक्रारीची सध्याची स्थिती काय आहे?",
        showcase=True
    ),
    Prompt(
        id="jansetu_002",
        agent="jansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the list of active welfare schemes I am eligible for based on my profile.",
        expected_data_sources=["MahaDBT Portal", "Citizen Profile Data"],
        tags=["welfare-schemes", "eligibility", "mahadbt"]
    ),
    Prompt(
        id="jansetu_003",
        agent="jansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the average resolution time for civic complaints in Pune Municipal Corporation?",
        expected_data_sources=["PMC Grievance Dashboard"],
        tags=["resolution-time", "civic", "pune"],
        marathi_translation="पुणे महानगरपालिकेत नागरी तक्रारींचा सरासरी निकाल लागण्याचा वेळ किती आहे?"
    ),
    Prompt(
        id="jansetu_004",
        agent="jansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many ration cards were issued in my district last month?",
        expected_data_sources=["Civil Supplies Dept Data"],
        tags=["ration-card", "issued", "district"]
    ),
    Prompt(
        id="jansetu_005",
        agent="jansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current pending count for caste validity certificates in my region?",
        expected_data_sources=["Social Justice Dept Data"],
        tags=["caste-validity", "pending", "region"]
    ),
    Prompt(
        id="jansetu_006",
        agent="jansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the list of documents required for a new birth certificate.",
        expected_data_sources=["Municipal Corp Guidelines"],
        tags=["birth-certificate", "documents", "requirements"]
    ),
    Prompt(
        id="jansetu_007",
        agent="jansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the status of pension disbursement for elderly citizens in my taluka?",
        expected_data_sources=["Social Security Pension Data"],
        tags=["pension", "elderly", "taluka"]
    ),
    Prompt(
        id="jansetu_008",
        agent="jansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many grievances were registered under the 'Women and Child' category this year?",
        expected_data_sources=["Grievance Portal Analytics"],
        tags=["grievances", "women-child", "yearly"]
    ),
    
    # === PREDICTIVE (Forecasting & Risk) - 7 Prompts ===
    Prompt(
        id="jansetu_009",
        agent="jansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict the surge in grievance registrations during the monsoon season in Mumbai.",
        expected_data_sources=["Historical Grievance Data", "Monsoon Impact Reports"],
        tags=["grievance-surge", "monsoon", "mumbai", "prediction"],
        marathi_translation="मुंबईत पावसाळ्यात तक्रारींच्या नोंदणीत होणाऱ्या वाढीचा अंदाज काय आहे?",
        showcase=True
    ),
    Prompt(
        id="jansetu_010",
        agent="jansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Forecast the demand for ration cards in newly developed urban areas.",
        expected_data_sources=["Population Migration Data", "Housing Data"],
        tags=["ration-card", "demand", "urban"]
    ),
    Prompt(
        id="jansetu_011",
        agent="jansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the risk of welfare scheme exclusion errors in tribal districts.",
        expected_data_sources=["MahaDBT Data", "Demographic Surveys"],
        tags=["exclusion-error", "tribal", "welfare"]
    ),
    Prompt(
        id="jansetu_012",
        agent="jansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict the processing time for caste certificates based on current application volume.",
        expected_data_sources=["Application Queue Data", "Staffing Levels"],
        tags=["caste-certificate", "processing-time", "prediction"]
    ),
    Prompt(
        id="jansetu_013",
        agent="jansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast the budget requirement for old age pensions over the next 5 years.",
        expected_data_sources=["Demographic Aging Data", "Current Pension Rolls"],
        tags=["pension", "budget", "forecast"]
    ),
    Prompt(
        id="jansetu_014",
        agent="jansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict the impact of digitization on grievance redressal efficiency.",
        expected_data_sources=["Digital Adoption Rates", "Resolution Time Trends"],
        tags=["digitization", "grievance", "efficiency"]
    ),
    Prompt(
        id="jansetu_015",
        agent="jansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the potential drop in scheme uptake if application procedures are simplified.",
        expected_data_sources=["User Behavior Data", "Scheme Enrollment Trends"],
        tags=["scheme-uptake", "simplification", "impact"]
    ),
    
    # === PRESCRIPTIVE (Recommendations) - 7 Prompts ===
    Prompt(
        id="jansetu_016",
        agent="jansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Recommend strategies to reduce the pendency of caste validity certificates.",
        expected_data_sources=["Process Bottleneck Analysis", "Best Practices"],
        tags=["pendency", "caste-validity", "strategy"],
        marathi_translation="जात वैधता प्रमाणपत्रांची प्रलंबितता कमी करण्यासाठी रणनीती सुचवा.",
        showcase=True
    ),
    Prompt(
        id="jansetu_017",
        agent="jansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="As a policy maker, what measures should I implement to improve MahaDBT penetration?",
        expected_data_sources=["MahaDBT Analytics", "Digital Literacy Data"],
        tags=["mahadbt", "penetration", "policy"]
    ),
    Prompt(
        id="jansetu_018",
        agent="jansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest ways to make grievance redressal more accessible for non-literate citizens.",
        expected_data_sources=["Accessibility Guidelines", "Voice/IVR Solutions"],
        tags=["accessibility", "grievance", "non-literate"]
    ),
    Prompt(
        id="jansetu_019",
        agent="jansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a proactive welfare delivery model that identifies eligible citizens automatically.",
        expected_data_sources=["Integrated Citizen Data", "Eligibility Rules"],
        tags=["proactive-welfare", "automatic", "model"]
    ),
    Prompt(
        id="jansetu_020",
        agent="jansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What process improvements can reduce the time to issue a domicile certificate?",
        expected_data_sources=["Current Process Maps", "Automation Options"],
        tags=["domicile", "process-improvement", "time-reduction"]
    ),
    Prompt(
        id="jansetu_021",
        agent="jansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend a comprehensive citizen feedback mechanism for government services.",
        expected_data_sources=["Feedback System Best Practices", "Citizen Satisfaction Data"],
        tags=["feedback", "citizen", "mechanism"]
    ),
    Prompt(
        id="jansetu_022",
        agent="jansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest measures to prevent fraudulent claims in welfare schemes.",
        expected_data_sources=["Fraud Detection Analytics", "Verification Protocols"],
        tags=["fraud-prevention", "welfare", "measures"]
    ),
    
    # === COMPARATIVE (Historical Analysis) - 4 Prompts ===
    Prompt(
        id="jansetu_023",
        agent="jansetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare grievance redressal performance across all districts in Maharashtra.",
        expected_data_sources=["Aaple Sarkar District Reports"],
        tags=["grievance", "comparison", "districts"],
        marathi_translation="महाराष्ट्रातील सर्व जिल्ह्यांच्या तक्रार निवारण कामगिरीची तुलना करा."
    ),
    Prompt(
        id="jansetu_024",
        agent="jansetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.BASIC,
        query="How has the number of digital welfare transactions changed over the last 3 years?",
        expected_data_sources=["MahaDBT Historical Data"],
        tags=["digital-transactions", "welfare", "trend"]
    ),
    Prompt(
        id="jansetu_025",
        agent="jansetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare the uptake of pension schemes between male and female beneficiaries.",
        expected_data_sources=["Social Security Data"],
        tags=["pension", "gender", "comparison"]
    ),
    Prompt(
        id="jansetu_026",
        agent="jansetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare Maharashtra's e-governance maturity index with other leading states.",
        expected_data_sources=["National e-Governance Division Data"],
        tags=["e-governance", "comparison", "states"]
    ),
    
    # === CROSS-DOMAIN (Multi-Agent) - 2 Prompts ===
    Prompt(
        id="jansetu_027",
        agent="jansetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How do delays in ration card issuance affect food security in drought-affected areas?",
        expected_data_sources=["Ration Card Data", "Food Security Surveys"],
        tags=["cross-domain", "krishisetu", "ration-card", "food-security"],
        showcase=True
    ),
    Prompt(
        id="jansetu_028",
        agent="jansetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the correlation between unresolved civic grievances and citizen trust in local government.",
        expected_data_sources=["Grievance Data", "Citizen Satisfaction Surveys"],
        tags=["cross-domain", "nagarsetu", "grievance", "trust"]
    ),
    
    # === CITIZEN-FACING - 1 Prompt ===
    Prompt(
        id="jansetu_029",
        agent="jansetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="What is the step-by-step process to apply for a domicile certificate online?",
        expected_data_sources=["Aaple Sarkar Domicile Guidelines"],
        tags=["citizen", "domicile", "online-process"],
        marathi_translation="ऑनलाइन रहिवासी दाखल्यासाठी अर्ज करण्याची पायरी-दर-पायरी प्रक्रिया काय आहे?"
    ),
    
    # === OFFICER-FACING (Decision Support) - 1 Prompt ===
    Prompt(
        id="jansetu_030",
        agent="jansetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a comprehensive strategy to achieve 100% saturation of flagship welfare schemes.",
        expected_data_sources=["Scheme Enrollment Data", "Demographic Gaps", "Best Practices"],
        tags=["officer", "saturation", "welfare", "strategy"],
        showcase=True
    ),
]

def register_jansetu_prompts(library):
    """Register all JanSetu prompts in the library."""
    for prompt in JANSETU_PROMPTS:
        library.register(prompt)
