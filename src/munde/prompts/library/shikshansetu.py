"""
ShikshanSetu: Education Intelligence Prompt Library
50 carefully crafted prompts covering all education scenarios in Maharashtra.
"""
from munde.prompts.base import Prompt, PromptCategory, PromptDifficulty

SHIKSHANSETU_PROMPTS = [
    # === SITUATIONAL (Current State) - 10 Prompts ===
    Prompt(
        id="shikshansetu_001",
        agent="shikshansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="What is the current student enrollment in government schools across Maharashtra?",
        expected_data_sources=["UDISE+ Data", "Education Dept Dashboard"],
        tags=["enrollment", "schools", "state"],
        marathi_translation="महाराष्ट्रातील सरकारी शाळांतील विद्यार्थ्यांची सध्याची नोंदणी काय आहे?",
        showcase=True
    ),
    Prompt(
        id="shikshansetu_002",
        agent="shikshansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the teacher-student ratio in all districts of Maharashtra.",
        expected_data_sources=["UDISE+ Data"],
        tags=["teacher-student", "ratio", "districts"],
        marathi_translation="महाराष्ट्रातील सर्व जिल्ह्यांतील शिक्षक-विद्यार्थी गुणोत्तर दाखवा."
    ),
    Prompt(
        id="shikshansetu_003",
        agent="shikshansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current literacy rate across different age groups in Maharashtra?",
        expected_data_sources=["Census Data", "NSSO Surveys"],
        tags=["literacy", "age-groups", "state"],
        showcase=True
    ),
    Prompt(
        id="shikshansetu_004",
        agent="shikshansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many schools in Maharashtra have access to computers and internet?",
        expected_data_sources=["UDISE+ Infrastructure Data"],
        tags=["infrastructure", "computers", "internet"]
    ),
    Prompt(
        id="shikshansetu_005",
        agent="shikshansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current dropout rate in secondary schools across districts?",
        expected_data_sources=["UDISE+ Data", "Education Dept Reports"],
        tags=["dropout", "secondary", "districts"]
    ),
    Prompt(
        id="shikshansetu_006",
        agent="shikshansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the number of colleges and universities in Maharashtra.",
        expected_data_sources=["Higher Education Dept Data"],
        tags=["colleges", "universities", "higher-education"]
    ),
    Prompt(
        id="shikshansetu_007",
        agent="shikshansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current status of mid-day meal distribution in government schools?",
        expected_data_sources=["MDM Scheme Data"],
        tags=["mid-day-meal", "schools", "distribution"]
    ),
    Prompt(
        id="shikshansetu_008",
        agent="shikshansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="How many students are enrolled in ITI and polytechnic institutes in Maharashtra?",
        expected_data_sources=["Technical Education Dept Data"],
        tags=["iti", "polytechnic", "enrollment"]
    ),
    Prompt(
        id="shikshansetu_009",
        agent="shikshansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the current pass percentage in SSC and HSC board exams?",
        expected_data_sources=["MSBSHSE Results Data"],
        tags=["board-exams", "ssc", "hsc", "results"]
    ),
    Prompt(
        id="shikshansetu_010",
        agent="shikshansetu",
        category=PromptCategory.SITUATIONAL,
        difficulty=PromptDifficulty.BASIC,
        query="Show me the list of scholarship schemes available for students in Maharashtra.",
        expected_data_sources=["Scholarship Portal Data"],
        tags=["scholarships", "schemes", "students"]
    ),
    
    # === PREDICTIVE (Forecasting & Risk) - 10 Prompts ===
    Prompt(
        id="shikshansetu_011",
        agent="shikshansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Predict school dropout risk in tribal districts based on socio-economic indicators.",
        expected_data_sources=["Socio-Economic Data", "Historical Dropout Data"],
        tags=["dropout", "tribal", "prediction", "risk"],
        marathi_translation="सामाजिक-आर्थिक निर्देशांकांच्या आधारे आदिवासी जिल्ह्यांतील शाळा सोडण्याचा धोका काय आहे?",
        showcase=True
    ),
    Prompt(
        id="shikshansetu_012",
        agent="shikshansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast the demand for engineering seats in Maharashtra over the next 5 years.",
        expected_data_sources=["Historical Admission Data", "Industry Demand"],
        tags=["engineering", "seats", "demand", "forecast"]
    ),
    Prompt(
        id="shikshansetu_013",
        agent="shikshansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict the impact of digital divide on learning outcomes in rural schools.",
        expected_data_sources=["Digital Access Data", "Learning Assessment Data"],
        tags=["digital-divide", "rural", "learning"]
    ),
    Prompt(
        id="shikshansetu_014",
        agent="shikshansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the future need for teacher training programs based on retirement patterns.",
        expected_data_sources=["Teacher Demographics", "Retirement Data"],
        tags=["teachers", "training", "retirement"]
    ),
    Prompt(
        id="shikshansetu_015",
        agent="shikshansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict enrollment trends in private vs government schools over the next decade.",
        expected_data_sources=["Historical Enrollment Data", "Demographic Trends"],
        tags=["enrollment", "private", "government", "trend"]
    ),
    Prompt(
        id="shikshansetu_016",
        agent="shikshansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast the skill gaps in Maharashtra's workforce based on industry requirements.",
        expected_data_sources=["Industry Demand Data", "Education Outcomes"],
        tags=["skills", "workforce", "gap", "forecast"]
    ),
    Prompt(
        id="shikshansetu_017",
        agent="shikshansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict the impact of NEP 2020 implementation on higher education in Maharashtra.",
        expected_data_sources=["NEP Guidelines", "Current Education Data"],
        tags=["nep-2020", "higher-education", "impact"]
    ),
    Prompt(
        id="shikshansetu_018",
        agent="shikshansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Analyze the future demand for vocational education based on industry 4.0 trends.",
        expected_data_sources=["Industry Trends", "Vocational Education Data"],
        tags=["vocational", "industry-4", "demand"]
    ),
    Prompt(
        id="shikshansetu_019",
        agent="shikshansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Predict girl child education enrollment in conservative rural areas.",
        expected_data_sources=["Gender Data", "Social Indicators"],
        tags=["girls", "education", "rural", "prediction"]
    ),
    Prompt(
        id="shikshansetu_020",
        agent="shikshansetu",
        category=PromptCategory.PREDICTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Forecast the need for special education infrastructure for children with disabilities.",
        expected_data_sources=["Disability Data", "Current Infrastructure"],
        tags=["disability", "special-education", "forecast"]
    ),
    
    # === PRESCRIPTIVE (Recommendations) - 10 Prompts ===
    Prompt(
        id="shikshansetu_021",
        agent="shikshansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Recommend strategies to improve learning outcomes in rural government schools.",
        expected_data_sources=["Learning Assessment Data", "Best Practices"],
        tags=["learning", "rural", "strategy"],
        marathi_translation="ग्रामीण सरकारी शाळांतील शिक्षणाचे दर्जा सुधारण्यासाठी रणनीती सुचवा.",
        showcase=True
    ),
    Prompt(
        id="shikshansetu_022",
        agent="shikshansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="As Education Minister, what reforms should I implement to reduce dropout rates?",
        expected_data_sources=["Dropout Analysis", "International Best Practices"],
        tags=["dropout", "reforms", "policy"]
    ),
    Prompt(
        id="shikshansetu_023",
        agent="shikshansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest digital learning tools for tribal schools with limited internet connectivity.",
        expected_data_sources=["Digital Education Guidelines", "Offline Solutions"],
        tags=["digital", "tribal", "offline"]
    ),
    Prompt(
        id="shikshansetu_024",
        agent="shikshansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a teacher training program to implement competency-based education.",
        expected_data_sources=["Teacher Training Guidelines", "CBE Framework"],
        tags=["teacher-training", "competency", "program"]
    ),
    Prompt(
        id="shikshansetu_025",
        agent="shikshansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What interventions are needed to improve girls' education in conservative areas?",
        expected_data_sources=["Gender Studies", "Social Programs"],
        tags=["girls", "education", "interventions"]
    ),
    Prompt(
        id="shikshansetu_026",
        agent="shikshansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend a curriculum reform plan to align with industry skill requirements.",
        expected_data_sources=["Industry Requirements", "Curriculum Framework"],
        tags=["curriculum", "skills", "reform"]
    ),
    Prompt(
        id="shikshansetu_027",
        agent="shikshansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Suggest measures to improve infrastructure in schools lacking basic facilities.",
        expected_data_sources=["Infrastructure Audit Data", "Fund Allocation Guidelines"],
        tags=["infrastructure", "schools", "facilities"]
    ),
    Prompt(
        id="shikshansetu_028",
        agent="shikshansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Design a comprehensive plan for inclusive education for children with special needs.",
        expected_data_sources=["Inclusive Education Guidelines", "Disability Data"],
        tags=["inclusive", "disability", "plan"]
    ),
    Prompt(
        id="shikshansetu_029",
        agent="shikshansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What scholarship schemes should be expanded to support first-generation learners?",
        expected_data_sources=["Scholarship Data", "Student Demographics"],
        tags=["scholarships", "first-generation", "support"]
    ),
    Prompt(
        id="shikshansetu_030",
        agent="shikshansetu",
        category=PromptCategory.PRESCRIPTIVE,
        difficulty=PromptDifficulty.ADVANCED,
        query="Recommend a state-wide strategy for implementing mother tongue-based education.",
        expected_data_sources=["Language Policy", "Learning Research"],
        tags=["mother-tongue", "language", "strategy"]
    ),
    
    # === COMPARATIVE (Historical Analysis) - 5 Prompts ===
    Prompt(
        id="shikshansetu_031",
        agent="shikshansetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare education indicators across all districts in Maharashtra.",
        expected_data_sources=["UDISE+ Data", "District Reports"],
        tags=["indicators", "comparison", "districts"],
        marathi_translation="महाराष्ट्रातील सर्व जिल्ह्यांच्या शिक्षण निर्देशांकांची तुलना करा."
    ),
    Prompt(
        id="shikshansetu_032",
        agent="shikshansetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.BASIC,
        query="How has literacy rate in Maharashtra changed over the last 20 years?",
        expected_data_sources=["Census Historical Data"],
        tags=["literacy", "trend", "historical"]
    ),
    Prompt(
        id="shikshansetu_033",
        agent="shikshansetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare Maharashtra's education performance with other major Indian states.",
        expected_data_sources=["National Education Data"],
        tags=["comparison", "states", "performance"]
    ),
    Prompt(
        id="shikshansetu_034",
        agent="shikshansetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="Compare learning outcomes between government and private schools.",
        expected_data_sources=["ASER Data", "Learning Assessments"],
        tags=["learning", "government", "private", "comparison"]
    ),
    Prompt(
        id="shikshansetu_035",
        agent="shikshansetu",
        category=PromptCategory.COMPARATIVE,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="How has gender parity in education evolved in Maharashtra over the last decade?",
        expected_data_sources=["Gender Education Data"],
        tags=["gender", "parity", "trend"]
    ),
    
    # === CROSS-DOMAIN (Multi-Agent) - 5 Prompts ===
    Prompt(
        id="shikshansetu_036",
        agent="shikshansetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How does malnutrition affect school attendance and learning outcomes in tribal areas?",
        expected_data_sources=["Nutrition Data", "Education Data"],
        tags=["cross-domain", "arogyasetu", "nutrition", "education"],
        showcase=True
    ),
    Prompt(
        id="shikshansetu_037",
        agent="shikshansetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the impact of rural road connectivity on school enrollment in remote areas.",
        expected_data_sources=["Road Infrastructure Data", "Education Data"],
        tags=["cross-domain", "margsetu", "roads", "education"]
    ),
    Prompt(
        id="shikshansetu_038",
        agent="shikshansetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How can agricultural education programs support farmer livelihoods in Vidarbha?",
        expected_data_sources=["Agriculture Education Data", "Farmer Surveys"],
        tags=["cross-domain", "krishisetu", "agriculture", "education"]
    ),
    Prompt(
        id="shikshansetu_039",
        agent="shikshansetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="What disaster preparedness education should be included in school curriculum?",
        expected_data_sources=["Disaster Management Guidelines", "Education Framework"],
        tags=["cross-domain", "aapattisetu", "disaster", "education"]
    ),
    Prompt(
        id="shikshansetu_040",
        agent="shikshansetu",
        category=PromptCategory.CROSS_DOMAIN,
        difficulty=PromptDifficulty.EXPERT,
        query="How can urban planning ensure adequate school infrastructure in growing cities?",
        expected_data_sources=["Urban Planning Data", "Education Infrastructure"],
        tags=["cross-domain", "nagarsetu", "urban", "schools"]
    ),
    
    # === CITIZEN-FACING - 5 Prompts ===
    Prompt(
        id="shikshansetu_041",
        agent="shikshansetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="How to apply for admission in government schools for my child?",
        expected_data_sources=["School Admission Guidelines"],
        tags=["citizen", "admission", "schools"],
        marathi_translation="माझ्या मुलासाठी सरकारी शाळेत प्रवेशासाठी अर्ज कसा करायचा?"
    ),
    Prompt(
        id="shikshansetu_042",
        agent="shikshansetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="What scholarships are available for SC/ST students in Maharashtra?",
        expected_data_sources=["Scholarship Schemes"],
        tags=["citizen", "scholarships", "sc-st"],
        marathi_translation="महाराष्ट्रातील SC/ST विद्यार्थ्यांसाठी कोणत्या शिष्यवृत्ती उपलब्ध आहेत?"
    ),
    Prompt(
        id="shikshansetu_043",
        agent="shikshansetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="How to get a transfer certificate when moving to another district?",
        expected_data_sources=["School Administration Guidelines"],
        tags=["citizen", "transfer-certificate", "migration"]
    ),
    Prompt(
        id="shikshansetu_044",
        agent="shikshansetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.BASIC,
        query="Where can I find information about ITI courses and admission?",
        expected_data_sources=["Technical Education Portal"],
        tags=["citizen", "iti", "courses"]
    ),
    Prompt(
        id="shikshansetu_045",
        agent="shikshansetu",
        category=PromptCategory.CITIZEN_FACING,
        difficulty=PromptDifficulty.INTERMEDIATE,
        query="What is the procedure to apply for equivalence certificate for foreign education?",
        expected_data_sources=["Equivalence Guidelines"],
        tags=["citizen", "equivalence", "foreign"]
    ),
    
    # === OFFICER-FACING (Decision Support) - 5 Prompts ===
    Prompt(
        id="shikshansetu_046",
        agent="shikshansetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a comprehensive education sector analysis for Maharashtra.",
        expected_data_sources=["All Education Data", "Economic Survey"],
        tags=["officer", "sector-analysis", "comprehensive"],
        showcase=True
    ),
    Prompt(
        id="shikshansetu_047",
        agent="shikshansetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Analyze the effectiveness of Sarva Shiksha Abhiyan in Maharashtra.",
        expected_data_sources=["SSA Implementation Data", "Outcome Reports"],
        tags=["officer", "ssa", "effectiveness", "analysis"]
    ),
    Prompt(
        id="shikshansetu_048",
        agent="shikshansetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.ADVANCED,
        query="Draft a state education policy framework aligned with NEP 2020.",
        expected_data_sources=["NEP 2020", "State Education Data"],
        tags=["officer", "policy", "nep-2020", "framework"]
    ),
    Prompt(
        id="shikshansetu_049",
        agent="shikshansetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Prepare a resource allocation plan for schools based on learning outcomes.",
        expected_data_sources=["Learning Data", "School Infrastructure"],
        tags=["officer", "resource-allocation", "schools"]
    ),
    Prompt(
        id="shikshansetu_050",
        agent="shikshansetu",
        category=PromptCategory.OFFICER_FACING,
        difficulty=PromptDifficulty.EXPERT,
        query="Design a teacher recruitment and deployment strategy for equitable distribution.",
        expected_data_sources=["Teacher Data", "School Requirements"],
        tags=["officer", "teachers", "recruitment", "strategy"]
    ),
]

def register_shikshansetu_prompts(library):
    """Register all ShikshanSetu prompts in the library."""
    for prompt in SHIKSHANSETU_PROMPTS:
        library.register(prompt)
