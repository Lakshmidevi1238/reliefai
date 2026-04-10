"""
ReliefLink AI — Comprehensive Sample / Mock Data
Used as fallback when News API is unavailable and for donation/help request data.
"""
from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────────────────────────────────────────
# SAMPLE NEWS ARTICLES (fallback when News API key is missing)
# ─────────────────────────────────────────────────────────────────────────────
_SAMPLE_ARTICLES = [
    {
        "title": "Sudan Crisis: 18 Million People Face Catastrophic Food Insecurity as Civil War Enters Second Year",
        "description": "The ongoing conflict between the Sudanese Armed Forces and the Rapid Support Forces has displaced over 8.8 million people internally, creating one of the world's worst displacement crises. Aid organizations warn of imminent famine in Darfur.",
        "source": {"name": "Reuters"},
        "url": "https://www.reuters.com",
        "publishedAt": (datetime.now() - timedelta(hours=2)).isoformat(),
    },
    {
        "title": "Gaza: Critical Shortage of Food, Water and Medicine as Humanitarian Corridors Blocked",
        "description": "Over 2.3 million Palestinians face acute shortages of basic necessities. Hospitals are operating at minimal capacity with critical medical supply shortfalls. UN reports 90% of population experiencing extreme food insecurity.",
        "source": {"name": "BBC News"},
        "url": "https://www.bbc.com",
        "publishedAt": (datetime.now() - timedelta(hours=4)).isoformat(),
    },
    {
        "title": "Ukraine: 14 Million Internally Displaced as Winter Intensifies Humanitarian Needs",
        "description": "Continued strikes on civilian infrastructure have left millions without heating and electricity. UNHCR reports 6.5 million refugees abroad, with millions more displaced internally facing harsh winter conditions.",
        "source": {"name": "AP News"},
        "url": "https://apnews.com",
        "publishedAt": (datetime.now() - timedelta(hours=6)).isoformat(),
    },
    {
        "title": "Haiti: Gang Violence and Political Collapse Leave 5 Million Facing Acute Hunger",
        "description": "Haiti's humanitarian crisis has deepened as gang control over key supply routes has blocked food and medical aid. UNICEF reports 1.8 million children are acutely malnourished. The capital Port-au-Prince is 80% under gang control.",
        "source": {"name": "Al Jazeera"},
        "url": "https://www.aljazeera.com",
        "publishedAt": (datetime.now() - timedelta(hours=8)).isoformat(),
    },
    {
        "title": "Yemen: Decade of War Leaves 21 Million in Need of Humanitarian Assistance",
        "description": "Ten years of conflict have left Yemen with one of the world's worst humanitarian crises. Cholera outbreaks, malnutrition affecting 2.2 million children, and a crumbling health system have pushed millions to the brink.",
        "source": {"name": "Guardian"},
        "url": "https://www.theguardian.com",
        "publishedAt": (datetime.now() - timedelta(hours=10)).isoformat(),
    },
    {
        "title": "Somalia: Climate-Driven Drought and Conflict Force 6.6 Million from Their Homes",
        "description": "Five consecutive failed rainy seasons coupled with Al-Shabaab violence have created catastrophic conditions. Over 3.8 million people are internally displaced with acute food shortages affecting coastal and southern regions.",
        "source": {"name": "OCHA"},
        "url": "https://www.unocha.org",
        "publishedAt": (datetime.now() - timedelta(hours=12)).isoformat(),
    },
    {
        "title": "Ethiopia: Tigray and Amhara Conflict Creates New Displacement Emergency",
        "description": "Renewed fighting in northern Ethiopia has displaced over 2 million people. Aid access remains severely constrained with reports of sexual violence and looting of humanitarian supplies by armed groups.",
        "source": {"name": "MSF"},
        "url": "https://www.msf.org",
        "publishedAt": (datetime.now() - timedelta(hours=14)).isoformat(),
    },
    {
        "title": "Syria: 13 Years of Crisis — 12 Million Displaced, Reconstruction Aid Still Blocked",
        "description": "Syria remains one of the world's largest displacement crises with 6.8 million refugees abroad. A new earthquake in the northwest has destroyed thousands of homes. Sanctions continue to hamper aid delivery.",
        "source": {"name": "UNHCR"},
        "url": "https://www.unhcr.org",
        "publishedAt": (datetime.now() - timedelta(hours=16)).isoformat(),
    },
]


def get_sample_articles(region: str = "global") -> list:
    """Return sample articles, optionally filtered by region."""
    region_lower = region.lower()
    if region_lower == "global":
        return _SAMPLE_ARTICLES
    filtered = [
        a for a in _SAMPLE_ARTICLES
        if region_lower in a["title"].lower() or region_lower in a["description"].lower()
    ]
    return filtered if filtered else _SAMPLE_ARTICLES[:4]


# ─────────────────────────────────────────────────────────────────────────────
# PRE-ANALYZED CRISIS DATA (used when OpenAI API is unavailable)
# ─────────────────────────────────────────────────────────────────────────────
_SAMPLE_CRISES = [
    {
        "title": "Sudan Civil War: Catastrophic Displacement and Famine Risk",
        "region": "Sudan",
        "crisis_type": "Armed Conflict",
        "summary": "Sudan's civil war between the SAF and RSF has created one of the world's worst humanitarian crises. 8.8 million people are internally displaced and 25 million face severe food insecurity, with imminent famine risk in Darfur. Aid access is severely restricted by ongoing fighting.",
        "needs": ["food", "water", "medical", "shelter", "money"],
        "urgency": "High",
        "urgency_color": "#ef4444",
        "people_affected": "25 million",
        "source": "UNHCR / Reuters",
        "url": "https://www.unhcr.org",
        "published_at": datetime.now().strftime("%Y-%m-%d"),
    },
    {
        "title": "Gaza Humanitarian Crisis: 90% Population in Extreme Food Insecurity",
        "region": "Gaza",
        "crisis_type": "Humanitarian Emergency",
        "summary": "2.3 million Palestinians face catastrophic conditions with nearly all experiencing food insecurity at crisis or emergency levels. Hospitals are at minimal capacity, water infrastructure is damaged, and humanitarian aid flows remain critically blocked.",
        "needs": ["food", "medical", "water", "shelter"],
        "urgency": "High",
        "urgency_color": "#ef4444",
        "people_affected": "2.3 million",
        "source": "UNRWA / BBC",
        "url": "https://www.unrwa.org",
        "published_at": datetime.now().strftime("%Y-%m-%d"),
    },
    {
        "title": "Ukraine: Winter Displacement Crisis Deepens for Millions",
        "region": "Ukraine",
        "crisis_type": "Armed Conflict",
        "summary": "Continued shelling of energy infrastructure has left millions without heat and electricity as winter intensifies. 14.6 million people are internally displaced or abroad as refugees. Mental health, child protection, and housing top the humanitarian agenda.",
        "needs": ["shelter", "money", "medical", "clothing"],
        "urgency": "High",
        "urgency_color": "#ef4444",
        "people_affected": "14.6 million",
        "source": "UNHCR / AP",
        "url": "https://www.unhcr.org/ukraine",
        "published_at": datetime.now().strftime("%Y-%m-%d"),
    },
    {
        "title": "Haiti: Gang Takeover Fuels Hunger Crisis for 5 Million",
        "region": "Haiti",
        "crisis_type": "Political Instability",
        "summary": "Gang violence controls over 80% of Port-au-Prince, blocking food aid and medical supplies. 5 million face acute hunger, with 1.8 million children acutely malnourished. The health system has effectively collapsed in many regions.",
        "needs": ["food", "medical", "water", "shelter", "money"],
        "urgency": "High",
        "urgency_color": "#ef4444",
        "people_affected": "5 million",
        "source": "UNICEF / Al Jazeera",
        "url": "https://www.unicef.org/haiti",
        "published_at": datetime.now().strftime("%Y-%m-%d"),
    },
    {
        "title": "Yemen: Decade-Long War Sustains World's Worst Humanitarian Crisis",
        "region": "Yemen",
        "crisis_type": "Armed Conflict + Famine",
        "summary": "Ten years of war have left 21 million Yemenis needing assistance. 2.2 million children are acutely malnourished and cholera outbreaks continue. The economy has collapsed, healthcare infrastructure is devastated, and access for aid workers remains dangerous.",
        "needs": ["food", "medical", "water", "money"],
        "urgency": "High",
        "urgency_color": "#ef4444",
        "people_affected": "21 million",
        "source": "WFP / Guardian",
        "url": "https://www.wfp.org/yemen",
        "published_at": datetime.now().strftime("%Y-%m-%d"),
    },
    {
        "title": "Somalia: Drought and Conflict Drive Millions From Their Homes",
        "region": "Somalia",
        "crisis_type": "Climate Disaster + Conflict",
        "summary": "Five consecutive failed rainy seasons combined with Al-Shabaab insurgency have displaced 3.8 million people. Acute food insecurity affects 6.6 million. Flash floods in southern regions have compounded the crisis, destroying crops and livestock.",
        "needs": ["food", "water", "shelter", "medical"],
        "urgency": "Medium",
        "urgency_color": "#f59e0b",
        "people_affected": "6.6 million",
        "source": "OCHA / MSF",
        "url": "https://www.unocha.org",
        "published_at": datetime.now().strftime("%Y-%m-%d"),
    },
    {
        "title": "Ethiopia: Tigray Ceasefire Fragile as 2 Million Remain Displaced",
        "region": "Ethiopia",
        "crisis_type": "Armed Conflict",
        "summary": "Despite a nominal ceasefire in Tigray, 2 million remain displaced across northern Ethiopia and access for humanitarian aid is restricted. Renewed Amhara conflict has created new displacement flows. Reconstruction aid has barely begun reaching affected communities.",
        "needs": ["food", "shelter", "medical", "money"],
        "urgency": "Medium",
        "urgency_color": "#f59e0b",
        "people_affected": "2 million",
        "source": "UNHCR / MSF",
        "url": "https://www.unhcr.org/ethiopia",
        "published_at": datetime.now().strftime("%Y-%m-%d"),
    },
    {
        "title": "Syria: 13 Years On — Millions Still Displaced, Earthquake Adds to Misery",
        "region": "Syria",
        "crisis_type": "Armed Conflict",
        "summary": "Syria's 13-year crisis has displaced 6.8 million abroad and 6.9 million internally. A devastating earthquake in northwestern Syria destroyed thousands of homes. Sanctions continue to block reconstruction aid, and over 15 million people need humanitarian assistance.",
        "needs": ["shelter", "food", "medical", "water"],
        "urgency": "Medium",
        "urgency_color": "#f59e0b",
        "people_affected": "15 million",
        "source": "UNHCR / Reuters",
        "url": "https://www.unhcr.org/syria",
        "published_at": datetime.now().strftime("%Y-%m-%d"),
    },
]


def get_sample_crises(region: str = "global") -> list:
    """Return pre-analyzed crisis data, optionally filtered."""
    if region.lower() == "global":
        return _SAMPLE_CRISES
    filtered = [c for c in _SAMPLE_CRISES if region.lower() in c["region"].lower()]
    return filtered if filtered else _SAMPLE_CRISES


# ─────────────────────────────────────────────────────────────────────────────
# DONATION ORGANIZATIONS (by region)
# ─────────────────────────────────────────────────────────────────────────────
_DONATION_ORGS = {
    "Global": [
        {"name": "UNHCR — UN Refugee Agency", "type": "UN Agency", "trust": "✅ UN Verified", "url": "https://donate.unhcr.org", "rating": "4.9/5"},
        {"name": "UNICEF", "type": "Children's Aid", "trust": "✅ UN Verified", "url": "https://www.unicef.org/donate", "rating": "4.9/5"},
        {"name": "World Food Programme", "type": "Food Aid", "trust": "✅ UN Verified", "url": "https://donate.wfp.org", "rating": "4.8/5"},
        {"name": "Red Cross / Red Crescent", "type": "Emergency Response", "trust": "✅ ICRC Verified", "url": "https://www.redcross.org/donate", "rating": "4.8/5"},
        {"name": "Médecins Sans Frontières (MSF)", "type": "Medical Aid", "trust": "✅ ISO Certified", "url": "https://www.msf.org/donate", "rating": "4.7/5"},
    ],
    "Sudan": [
        {"name": "UNHCR Sudan Emergency", "type": "Refugee Aid", "trust": "✅ UN Verified", "url": "https://donate.unhcr.org/sudan", "rating": "4.9/5"},
        {"name": "International Rescue Committee", "type": "Humanitarian Aid", "trust": "✅ Charity Navigator 4-Star", "url": "https://help.rescue.org/donate", "rating": "4.8/5"},
        {"name": "Save the Children Sudan", "type": "Child Protection", "trust": "✅ GuideStar Platinum", "url": "https://www.savethechildren.org/donate", "rating": "4.7/5"},
        {"name": "Care International", "type": "Women & Families", "trust": "✅ Charity Navigator 4-Star", "url": "https://www.care.org/donate", "rating": "4.7/5"},
    ],
    "Gaza": [
        {"name": "UNRWA Palestinian Relief", "type": "UN Relief Agency", "trust": "✅ UN Verified", "url": "https://www.unrwa.org/donate", "rating": "4.8/5"},
        {"name": "Medical Aid for Palestinians", "type": "Medical Aid", "trust": "✅ UK Charity Commission", "url": "https://www.map.org.uk/donate", "rating": "4.7/5"},
        {"name": "Norwegian Refugee Council", "type": "Shelter & Legal Aid", "trust": "✅ Charity Navigator", "url": "https://www.nrc.no/donate", "rating": "4.7/5"},
        {"name": "Oxfam Gaza Emergency", "type": "Food & Water", "trust": "✅ GuideStar Platinum", "url": "https://www.oxfam.org/donate", "rating": "4.6/5"},
    ],
    "Ukraine": [
        {"name": "UNICEF Ukraine Emergency", "type": "Child Aid", "trust": "✅ UN Verified", "url": "https://www.unicef.org/emergencies/ukraine", "rating": "4.9/5"},
        {"name": "United24 — Official Ukraine Fund", "type": "Government Aid", "trust": "✅ Ukrainian Gov Verified", "url": "https://u24.gov.ua/donate", "rating": "4.8/5"},
        {"name": "UNHCR Ukraine", "type": "Refugee Aid", "trust": "✅ UN Verified", "url": "https://www.unhcr.org/ukraine-emergency", "rating": "4.9/5"},
        {"name": "Direct Relief Ukraine", "type": "Medical Aid", "trust": "✅ Charity Navigator 4-Star", "url": "https://www.directrelief.org/ukraine", "rating": "4.8/5"},
    ],
    "Haiti": [
        {"name": "UNICEF Haiti", "type": "Child Protection", "trust": "✅ UN Verified", "url": "https://www.unicef.org/haiti", "rating": "4.9/5"},
        {"name": "World Food Programme Haiti", "type": "Food Aid", "trust": "✅ UN Verified", "url": "https://www.wfp.org/countries/haiti", "rating": "4.8/5"},
        {"name": "Action Against Hunger Haiti", "type": "Nutrition Aid", "trust": "✅ Charity Navigator 4-Star", "url": "https://www.actionagainsthunger.org/donate", "rating": "4.7/5"},
    ],
    "Yemen": [
        {"name": "WFP Yemen Emergency", "type": "Food & Nutrition", "trust": "✅ UN Verified", "url": "https://www.wfp.org/yemen", "rating": "4.9/5"},
        {"name": "UNICEF Yemen", "type": "Child Aid", "trust": "✅ UN Verified", "url": "https://www.unicef.org/yemen", "rating": "4.8/5"},
        {"name": "MSF Yemen", "type": "Medical Aid", "trust": "✅ ISO Certified", "url": "https://www.msf.org/yemen", "rating": "4.7/5"},
    ],
    "Somalia": [
        {"name": "UNHCR Somalia", "type": "Refugee Aid", "trust": "✅ UN Verified", "url": "https://donate.unhcr.org", "rating": "4.9/5"},
        {"name": "WFP Somalia", "type": "Food Aid", "trust": "✅ UN Verified", "url": "https://donate.wfp.org", "rating": "4.8/5"},
        {"name": "Oxfam Somalia", "type": "Water & Food", "trust": "✅ Charity Rating A", "url": "https://www.oxfam.org/donate", "rating": "4.6/5"},
    ],
    "Ethiopia": [
        {"name": "UNHCR Ethiopia", "type": "Refugee Aid", "trust": "✅ UN Verified", "url": "https://donate.unhcr.org", "rating": "4.9/5"},
        {"name": "MSF Ethiopia", "type": "Medical Aid", "trust": "✅ ISO Certified", "url": "https://www.msf.org/donate", "rating": "4.7/5"},
        {"name": "Save the Children Ethiopia", "type": "Child Protection", "trust": "✅ GuideStar Platinum", "url": "https://www.savethechildren.org/donate", "rating": "4.7/5"},
    ],
    "Syria": [
        {"name": "UNHCR Syria", "type": "Refugee Aid", "trust": "✅ UN Verified", "url": "https://donate.unhcr.org", "rating": "4.9/5"},
        {"name": "MSF Syria", "type": "Medical Aid", "trust": "✅ ISO Certified", "url": "https://www.msf.org/donate", "rating": "4.7/5"},
        {"name": "Syria Relief UK", "type": "Humanitarian Aid", "trust": "✅ UK Charity Commission", "url": "https://syriarelief.org.uk/donate", "rating": "4.6/5"},
    ],
    "Pakistan": [
        {"name": "UNICEF Pakistan Floods", "type": "Child Aid", "trust": "✅ UN Verified", "url": "https://www.unicef.org/pakistan", "rating": "4.9/5"},
        {"name": "Edhi Foundation", "type": "Local Aid Org", "trust": "✅ Gov Registered", "url": "https://www.edhi.org", "rating": "4.7/5"},
    ],
    "Afghanistan": [
        {"name": "WFP Afghanistan", "type": "Food Aid", "trust": "✅ UN Verified", "url": "https://donate.wfp.org", "rating": "4.9/5"},
        {"name": "UNICEF Afghanistan", "type": "Child Aid", "trust": "✅ UN Verified", "url": "https://www.unicef.org/afghanistan", "rating": "4.8/5"},
    ],
}

_URGENT_NEEDS_BY_REGION = {
    "Sudan": ["Emergency food packages for 25M people", "Emergency medical supplies to conflict zones", "Safe water and sanitation for displaced camps", "Temporary shelter for 8.8M displaced persons", "Child nutrition supplements (severe acute malnutrition)"],
    "Gaza": ["Food and clean water for 2.3M residents", "Emergency surgical supplies and medicines", "Fuel for hospital generators", "Hygiene kits for families", "Baby food and infant formula"],
    "Ukraine": ["Heating equipment and winter clothing", "Housing/shelter for displaced families", "Mental health support services", "Emergency food parcels", "Medical prosthetics for war wounded"],
    "Haiti": ["Emergency food for 5M in acute hunger", "Medical supplies for collapsed health system", "Clean water for Port-au-Prince", "Child nutrition programs", "Safe shelter from gang violence"],
    "Yemen": ["Food aid for 21M in need", "Cholera treatment kits", "Therapeutic food for 2.2M malnourished children", "Fuel for hospitals", "Safe drinking water"],
    "Somalia": ["Emergency food for drought victims", "Potable water for drought-hit communities", "Livestock support for herder families", "Medical care for malnourished children", "Shelter for flooding victims"],
    "Ethiopia": ["Food assistance for Tigray IDPs", "Medical care in conflict-affected areas", "Shelter reconstruction aid", "Child protection services", "Livelihood support for returned families"],
    "Syria": ["Shelter reconstruction in earthquake zones", "Food for 15M people in need", "Medical equipment for hospitals", "Water infrastructure repair", "Education for displaced children"],
    "Global": ["Emergency food aid worldwide", "Medical supplies for conflict zones", "Clean water and sanitation", "Temporary shelter", "Financial support for humanitarian organizations"],
}


def get_donation_info(region: str) -> dict:
    """Return donation organizations and urgent needs for a region."""
    orgs = _DONATION_ORGS.get(region, _DONATION_ORGS["Global"])
    needs = _URGENT_NEEDS_BY_REGION.get(region, _URGENT_NEEDS_BY_REGION["Global"])
    return {"organizations": orgs, "needs": needs, "region": region}


# ─────────────────────────────────────────────────────────────────────────────
# DONATION CENTERS (Physical locations, by country)
# ─────────────────────────────────────────────────────────────────────────────
_DONATION_CENTERS = {
    "United States": [
        {
            "name": "American Red Cross — Washington DC Collection Hub",
            "address": "430 17th Street NW, Washington, DC 20006",
            "phone": "+1 (800) 733-2767",
            "hours": "Mon–Fri: 9 AM – 5 PM | Sat: 10 AM – 3 PM",
            "accepts": ["Non-perishable Food", "Clothing", "Hygiene Kits", "Cash"],
            "distance": "2.3 mi",
        },
        {
            "name": "UNICEF USA Drop-off — New York",
            "address": "125 Maiden Lane, 11th Floor, New York, NY 10038",
            "phone": "+1 (800) 367-5437",
            "hours": "Mon–Fri: 9 AM – 6 PM",
            "accepts": ["Medical Supplies", "Baby Food", "Hygiene Kits", "Cash"],
            "distance": "4.1 mi",
        },
        {
            "name": "World Vision Collection Hub — Federal Way, WA",
            "address": "34834 Weyerhaeuser Way S, Federal Way, WA 98001",
            "phone": "+1 (888) 511-6548",
            "hours": "Mon–Fri: 8 AM – 5 PM",
            "accepts": ["Clothing", "Food", "School Supplies", "Cash"],
            "distance": "7.8 mi",
        },
    ],
    "United Kingdom": [
        {
            "name": "British Red Cross — London Headquarters",
            "address": "44 Moorfields, London EC2Y 9AL",
            "phone": "+44 344 871 1111",
            "hours": "Mon–Fri: 9 AM – 5 PM",
            "accepts": ["Clothing", "Medical Supplies", "Cash"],
            "distance": "1.2 mi",
        },
        {
            "name": "Oxfam Drop & Shop — Notting Hill",
            "address": "17 Notting Hill Gate, London W11 3JQ",
            "phone": "+44 1865 472 602",
            "hours": "Mon–Sat: 10 AM – 6 PM | Sun: 11 AM – 5 PM",
            "accepts": ["Clothing", "Books", "Food", "Household Items"],
            "distance": "3.5 mi",
        },
        {
            "name": "Save the Children UK — Edinburgh",
            "address": "1 St Colme Street, Edinburgh EH3 6AA",
            "phone": "+44 20 7012 6400",
            "hours": "Mon–Fri: 9 AM – 5:30 PM",
            "accepts": ["Children's Clothing", "Toys", "Books", "Cash"],
            "distance": "5.2 mi",
        },
    ],
    "Canada": [
        {
            "name": "Canadian Red Cross — Ottawa",
            "address": "170 Metcalfe Street, Ottawa, ON K2P 2P2",
            "phone": "+1 (613) 740-1900",
            "hours": "Mon–Fri: 9 AM – 5 PM",
            "accepts": ["Clothing", "Food", "Medical Supplies", "Cash"],
            "distance": "3.7 mi",
        },
        {
            "name": "UNICEF Canada — Toronto",
            "address": "2200 Yonge Street, Suite 1100, Toronto, ON M4S 2C6",
            "phone": "+1 (416) 482-4444",
            "hours": "Mon–Fri: 9 AM – 5 PM",
            "accepts": ["Baby Supplies", "Medical Kits", "Cash"],
            "distance": "6.1 mi",
        },
    ],
    "Australia": [
        {
            "name": "Australian Red Cross — Sydney",
            "address": "159 Clarence Street, Sydney NSW 2000",
            "phone": "+61 1800 733 276",
            "hours": "Mon–Fri: 9 AM – 5 PM | Sat: 9 AM – 1 PM",
            "accepts": ["Clothing", "Food", "Hygiene Kits", "Cash"],
            "distance": "2.1 mi",
        },
        {
            "name": "CARE Australia — Canberra",
            "address": "Level 9, 141 Northbourne Ave, Canberra ACT 2601",
            "phone": "+61 2 6279 0200",
            "hours": "Mon–Fri: 9 AM – 5 PM",
            "accepts": ["Cash", "Medical Supplies", "Educational Materials"],
            "distance": "4.4 mi",
        },
    ],
    "Germany": [
        {
            "name": "Deutsches Rotes Kreuz — Berlin",
            "address": "Carstennstraße 58, 12205 Berlin",
            "phone": "+49 30 85404-0",
            "hours": "Mon–Fri: 8 AM – 4 PM",
            "accepts": ["Clothing", "Food", "Medical Supplies", "Cash"],
            "distance": "3.8 mi",
        },
    ],
    "France": [
        {
            "name": "Croix-Rouge Française — Paris",
            "address": "98 rue Didot, 75014 Paris",
            "phone": "+33 1 44 43 11 00",
            "hours": "Mon–Sat: 9 AM – 6 PM",
            "accepts": ["Clothing", "Food", "Hygiene Items", "Cash"],
            "distance": "2.9 mi",
        },
    ],
    "India": [
        {
            "name": "Indian Red Cross Society — New Delhi",
            "address": "1 Red Cross Road, New Delhi 110001",
            "phone": "+91 11 2371 6441",
            "hours": "Mon–Sat: 9 AM – 5 PM",
            "accepts": ["Medical Supplies", "Clothing", "Food", "Cash"],
            "distance": "5.0 mi",
        },
    ],
}


def get_donation_centers(country: str, crisis: str = "") -> list:
    """Return donation centers for a country."""
    return _DONATION_CENTERS.get(country, _DONATION_CENTERS["United States"])


# ─────────────────────────────────────────────────────────────────────────────
# SAMPLE HELP REQUESTS (mock public feed)
# ─────────────────────────────────────────────────────────────────────────────
_SAMPLE_HELP_REQUESTS = [
    {
        "id": "SR001",
        "name": "Fatima Hassan & Family",
        "region": "Sudan",
        "description": "We are a family of 6 including 4 children aged 2–12. We fled from El Fasher, Darfur when our neighbourhood was attacked. We have been living in a displacement camp for 3 months with no adequate food or clean water. Our youngest child is showing signs of malnutrition. We urgently need food packages, clean water, and medical assistance for the children.",
        "needs": ["Food", "Water", "Medical Aid", "Shelter"],
        "contact_email": "fatima.help@example.com",
        "donation_link": "https://gofundme.com/example-sudan",
        "bank_details": None,
        "has_documents": True,
        "trust_score": {"score": 92, "level": "High", "badge": "✅ AI Verified", "color": "#22c55e", "confidence": "92%"},
        "status": "Active",
        "created_at": (datetime.now() - timedelta(days=2)).isoformat(),
        "upvotes": 247,
    },
    {
        "id": "SR002",
        "name": "Ahmad Al-Rashid",
        "region": "Gaza",
        "description": "I am a father of three children. My 7-year-old son was injured during shelling and needs urgent surgery that is not available locally due to collapsed hospitals. We have been forced to move 4 times in the past 3 months. We desperately need: safe evacuation for my son to receive medical care, food for the family, and basic hygiene items.",
        "needs": ["Medical Aid", "Food", "Financial Support"],
        "contact_email": "ahmad.rashid.help@example.com",
        "donation_link": "https://paypal.me/example-gaza",
        "bank_details": None,
        "has_documents": True,
        "trust_score": {"score": 88, "level": "High", "badge": "✅ AI Verified", "color": "#22c55e", "confidence": "88%"},
        "status": "Active",
        "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
        "upvotes": 413,
    },
    {
        "id": "SR003",
        "name": "Olena Kovalenko",
        "region": "Ukraine",
        "description": "I am a mother of two teenage daughters from Kharkiv. Our apartment building was badly damaged by shelling and we are now staying in a temporary shelter, but the shelter will close next month. The temperatures are dropping below freezing. We need help with finding housing, warm clothing for the children, and financial support to rebuild our lives.",
        "needs": ["Shelter", "Clothing", "Financial Support"],
        "contact_email": "olena.k.help@example.com",
        "donation_link": "https://bank.example.com/ukraine-help",
        "bank_details": "IBAN: UA123456789 — Olena Kovalenko",
        "has_documents": True,
        "trust_score": {"score": 95, "level": "High", "badge": "✅ AI Verified", "color": "#22c55e", "confidence": "95%"},
        "status": "Active",
        "created_at": (datetime.now() - timedelta(days=3)).isoformat(),
        "upvotes": 189,
    },
    {
        "id": "SR004",
        "name": "Jean-Pierre Morel",
        "region": "Haiti",
        "description": "Our community of 200 people in Cité Soleil has been cut off from food supplies for 2 weeks due to gang roadblocks. We have elderly people and infants who are in critical condition. We don't have clean water and the last medical supply delivery was 3 weeks ago. Any help — food packages, water purification tablets, medicines — would save lives.",
        "needs": ["Food", "Water", "Medical Aid"],
        "contact_email": None,
        "donation_link": None,
        "bank_details": None,
        "has_documents": False,
        "trust_score": {"score": 58, "level": "Medium", "badge": "⚠️ Partially Verified", "color": "#f59e0b", "confidence": "58%"},
        "status": "Active",
        "created_at": (datetime.now() - timedelta(days=5)).isoformat(),
        "upvotes": 72,
    },
    {
        "id": "SR005",
        "name": "Amara Diallo",
        "region": "Somalia",
        "description": "I am a herder from Baidoa. Five years of drought have killed all of our 120 cattle — our entire livelihood. My family of 8 has no food or income. We walked for 4 days to reach Baidoa town. We need emergency food, clean water, and any financial support to help us start over. Our children have not eaten properly in weeks.",
        "needs": ["Food", "Water", "Financial Support"],
        "contact_email": "amara.d.help@example.com",
        "donation_link": "https://gofundme.com/example-somalia",
        "bank_details": None,
        "has_documents": False,
        "trust_score": {"score": 65, "level": "Medium", "badge": "⚠️ Partially Verified", "color": "#f59e0b", "confidence": "65%"},
        "status": "Active",
        "created_at": (datetime.now() - timedelta(days=4)).isoformat(),
        "upvotes": 103,
    },
]


def get_sample_help_requests() -> list:
    """Return sample help requests."""
    return _SAMPLE_HELP_REQUESTS
