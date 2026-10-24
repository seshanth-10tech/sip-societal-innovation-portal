import re


# ============================================================
# PROBLEM KNOWLEDGE BASE
# ============================================================

PROBLEM_DOMAINS = {

    "Water Management": {

        "keywords": [
            "water",
            "drinking water",
            "water shortage",
            "water supply",
            "water contamination",
            "dirty water",
            "water pollution",
            "drainage",
            "drain",
            "drains",
            "sewage",
            "sewer",
            "wastewater",
            "rainwater",
            "flooding",
            "flood",
            "waterlogging",
            "water logging",
            "irrigation",
            "canal",
            "pond",
            "river",
            "well",
            "borewell",
            "pipeline"
        ],

        "expertise": [
            "Civil Engineering",
            "Environmental Engineering",
            "Water Resources",
            "IoT"
        ],

        "team": "Water & Environmental Infrastructure Team",
        "solution": "Start with a community-level assessment of the water source and distribution route, test water quality, then prioritize a repair or treatment plan with local maintenance ownership."
    },


    "Agriculture": {

        "keywords": [
            "farmer",
            "farmers",
            "farm",
            "agriculture",
            "crop",
            "crops",
            "farming",
            "cultivation",
            "fertilizer",
            "fertiliser",
            "pesticide",
            "soil",
            "harvest",
            "seed",
            "seeds",
            "irrigation",
            "pest",
            "plant disease",
            "livestock",
            "cattle",
            "tractor"
        ],

        "expertise": [
            "Agricultural Engineering",
            "Soil Science",
            "IoT",
            "Artificial Intelligence"
        ],

        "team": "Smart Agriculture & Rural Technology Team",
        "solution": "Begin with a field assessment of soil, crop health, and water access; then pilot an affordable, locally maintainable farming intervention with nearby growers."
    },


    "Healthcare": {

        "keywords": [
            "hospital",
            "doctor",
            "doctors",
            "patient",
            "patients",
            "medicine",
            "medical",
            "health",
            "healthcare",
            "clinic",
            "ambulance",
            "disease",
            "treatment",
            "diagnosis",
            "pharmacy",
            "emergency",
            "blood",
            "health centre",
            "health center"
        ],

        "expertise": [
            "Healthcare Technology",
            "Public Health",
            "Medical Technology",
            "Artificial Intelligence"
        ],

        "team": "Healthcare Technology & Public Health Team",
        "solution": "Map the access gap with local health workers, identify the most affected groups, and pilot a practical referral, outreach, or service-delivery improvement."
    },


    "Education": {

        "keywords": [
            "school",
            "schools",
            "student",
            "students",
            "teacher",
            "teachers",
            "education",
            "college",
            "classroom",
            "learning",
            "library",
            "computer lab",
            "laboratory",
            "exam",
            "digital learning",
            "online class"
        ],

        "expertise": [
            "Computer Science",
            "Artificial Intelligence",
            "Education Technology",
            "Information Technology"
        ],

        "team": "Digital Education & Learning Technology Team",
        "solution": "Work with learners and teachers to identify the main barrier, then pilot an accessible learning resource or classroom improvement and measure participation."
    },


    "Environment": {

        "keywords": [
            "pollution",
            "air pollution",
            "garbage",
            "waste",
            "plastic",
            "plastic waste",
            "solid waste",
            "recycling",
            "recycle",
            "forest",
            "deforestation",
            "environment",
            "smoke",
            "dust",
            "land pollution",
            "waste management"
        ],

        "expertise": [
            "Environmental Engineering",
            "Waste Management",
            "Civil Engineering",
            "Sustainable Technology"
        ],

        "team": "Environmental Sustainability Team",
        "solution": "Trace where the pollution or waste originates, organize a small local audit, and test a prevention, collection, or reuse approach with residents."
    },


    "Energy": {

        "keywords": [
            "electricity",
            "power",
            "solar",
            "solar energy",
            "energy",
            "street light",
            "streetlight",
            "lights",
            "power cut",
            "transformer",
            "electric",
            "renewable energy"
        ],

        "expertise": [
            "Electrical Engineering",
            "Renewable Energy",
            "IoT",
            "Power Systems"
        ],

        "team": "Smart Energy & Renewable Technology Team",
        "solution": "Assess the reliability and demand pattern first, then evaluate a safe, maintainable efficiency or renewable-energy pilot suited to the location."
    },


    "Accessibility": {

        "keywords": [
            "disabled",
            "disability",
            "wheelchair",
            "blind",
            "visually impaired",
            "accessibility",
            "accessible",
            "ramp",
            "ramps",
            "elderly",
            "special needs"
        ],

        "expertise": [
            "Assistive Technology",
            "Mechanical Engineering",
            "Computer Science",
            "Human-Centered Design"
        ],

        "team": "Accessibility & Assistive Technology Team",
        "solution": "Walk through the affected route or service with people who face the barrier, agree on the highest-impact change, and prototype an accessible improvement."
    },


    "Urban Infrastructure": {

        "keywords": [
            "road",
            "roads",
            "pothole",
            "potholes",
            "traffic",
            "bridge",
            "bridges",
            "parking",
            "transport",
            "bus",
            "footpath",
            "sidewalk",
            "street",
            "infrastructure"
        ],

        "expertise": [
            "Civil Engineering",
            "Transportation Engineering",
            "Smart City Technology",
            "IoT"
        ],

        "team": "Smart Infrastructure & Mobility Team",
        "solution": "Document the affected locations and users, prioritize safety-critical points, and develop a phased repair or mobility plan with local authorities."
    },


    "Rural Livelihood": {

        "keywords": [
            "job",
            "jobs",
            "employment",
            "unemployment",
            "livelihood",
            "income",
            "rural",
            "village development",
            "self employment",
            "small business",
            "skill development"
        ],

        "expertise": [
            "Rural Development",
            "Entrepreneurship",
            "Economics",
            "Information Technology"
        ],

        "team": "Rural Development & Livelihood Team",
        "solution": "Talk with local residents and enterprises to identify the livelihood bottleneck, then pilot a skills, market-access, or small-business support pathway."
    }
}


# ============================================================
# DEMO UNIVERSITY DATABASE
# ============================================================

UNIVERSITIES = [

    {
        "name": "Birsa Institute of Technology",
        "location": "Ranchi",
        "domains": [
            "Water Management",
            "Environment",
            "Urban Infrastructure",
            "Energy"
        ],
        "keywords": [
            "water",
            "drainage",
            "sewage",
            "civil",
            "environment",
            "infrastructure",
            "iot",
            "energy"
        ]
    },

    {
        "name": "National Institute of Technology Jharkhand",
        "location": "Jamshedpur",
        "domains": [
            "Education",
            "Energy",
            "Urban Infrastructure",
            "Accessibility"
        ],
        "keywords": [
            "computer",
            "ai",
            "machine learning",
            "iot",
            "electronics",
            "robotics",
            "smart city",
            "energy",
            "infrastructure"
        ]
    },

    {
        "name": "Birsa Agricultural University",
        "location": "Ranchi",
        "domains": [
            "Agriculture",
            "Water Management",
            "Rural Livelihood"
        ],
        "keywords": [
            "agriculture",
            "farmer",
            "crop",
            "soil",
            "irrigation",
            "farming",
            "rural",
            "livelihood"
        ]
    },

    {
        "name": "Jharkhand Health Technology Institute",
        "location": "Ranchi",
        "domains": [
            "Healthcare"
        ],
        "keywords": [
            "health",
            "hospital",
            "medicine",
            "patient",
            "medical",
            "healthcare",
            "doctor"
        ]
    }
]


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# FIND DOMAIN
# ============================================================

def detect_domain(problem):

    text = clean_text(problem)

    scores = {}

    for domain, data in PROBLEM_DOMAINS.items():

        score = 0

        for keyword in data["keywords"]:

            if keyword in text:

                # Give more weight to longer/more specific phrases
                if " " in keyword:
                    score += 3
                else:
                    score += 1

        scores[domain] = score


    best_domain = max(
        scores,
        key=scores.get
    )


    best_score = scores[best_domain]


    # No meaningful match
    if best_score == 0:

        return {
            "domain": "General Societal Issue",
            "confidence": 0,
            "expertise": [
                "Multidisciplinary Research"
            ],
            "team": "Multidisciplinary Innovation Team",
            "solution": "Start by speaking with the people affected, document when and where the issue occurs, then co-design a small, measurable pilot with a local institution."
        }


    # Convert score into a simple confidence percentage
    confidence = min(
        98,
        60 + best_score * 8
    )


    domain_data = PROBLEM_DOMAINS[best_domain]


    return {

        "domain": best_domain,

        "confidence": confidence,

        "expertise":
            domain_data["expertise"],

        "team":
            domain_data["team"],

        "solution":
            domain_data["solution"]
    }


# ============================================================
# PRIORITY
# ============================================================

def detect_priority(problem):

    text = clean_text(problem)


    critical_words = [

        "death",
        "dying",
        "emergency",
        "critical",
        "danger",
        "dangerous",
        "severe",
        "contamination",
        "toxic",
        "flood",
        "flooding",
        "hospital emergency",
        "no drinking water"

    ]


    high_words = [

        "shortage",
        "lack",
        "unsafe",
        "serious",
        "urgent",
        "broken",
        "overflow",
        "disease",
        "pollution",
        "waterlogging"

    ]


    if any(
        word in text
        for word in critical_words
    ):

        return "Critical"


    if any(
        word in text
        for word in high_words
    ):

        return "High"


    return "Medium"


# ============================================================
# UNIVERSITY MATCHING
# ============================================================

def match_university(problem, domain):

    text = clean_text(problem)

    best_university = None

    best_score = -1


    for university in UNIVERSITIES:

        score = 0


        # Domain match
        if domain in university["domains"]:

            score += 10


        # Keyword match
        for keyword in university["keywords"]:

            if keyword in text:

                score += 2


        if score > best_score:

            best_score = score

            best_university = university


    if best_university is None:

        return {

            "name":
                "University Matching Pending",

            "location":
                "Jharkhand",

            "score":
                0

        }


    match_percentage = min(
        98,
        65 + best_score * 3
    )


    return {

        "name":
            best_university["name"],

        "location":
            best_university["location"],

        "score":
            match_percentage,

        "domains":
            best_university["domains"]
    }


# ============================================================
# COMPLETE ANALYSIS
# ============================================================

def analyze_problem(problem):

    domain_result = detect_domain(problem)

    priority = detect_priority(problem)


    university = match_university(
        problem,
        domain_result["domain"]
    )


    return {

        "domain":
            domain_result["domain"],

        "confidence":
            domain_result["confidence"],

        "priority":
            priority,

        "expertise":
            domain_result["expertise"],

        "team":
            domain_result["team"],

        "solution":
            domain_result["solution"],

        "university":
            university
    }
