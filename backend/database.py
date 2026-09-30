from datetime import datetime, timedelta
from typing import Optional

_now = datetime.now()

def _t(hours_ago: float) -> str:
    return (_now - timedelta(hours=hours_ago)).strftime("%Y-%m-%d %H:%M")

PATIENTS = {
    "P001": {
        "id": "P001",
        "name": "John Smith",
        "age": 67,
        "dob": "1957-03-15",
        "mrn": "10023456",
        "room": "204A",
        "bed": "A",
        "admission_date": (_now - timedelta(days=3)).strftime("%Y-%m-%d"),
        "diagnosis": "Acute exacerbation of congestive heart failure (CHF)",
        "secondary_diagnoses": ["Type 2 Diabetes Mellitus", "Hypertension", "CKD Stage 3"],
        "attending": "Dr. Sarah Johnson",
        "code_status": "Full Code",
        "isolation": "None",
        "fall_risk": "High",
        "allergies": [
            {"drug": "Penicillin", "reaction": "Anaphylaxis"},
            {"drug": "Aspirin", "reaction": "GI bleed"},
        ],
        "vitals": [
            {"timestamp": _t(8), "bp": "158/92", "hr": 94, "rr": 22, "temp": 37.2, "spo2": 93, "weight_kg": 88.5, "pain": 3},
            {"timestamp": _t(6), "bp": "152/88", "hr": 90, "rr": 20, "temp": 37.1, "spo2": 94, "weight_kg": 88.5, "pain": 2},
            {"timestamp": _t(4), "bp": "148/86", "hr": 86, "rr": 18, "temp": 37.0, "spo2": 95, "weight_kg": 88.2, "pain": 2},
            {"timestamp": _t(2), "bp": "144/84", "hr": 82, "rr": 18, "temp": 37.0, "spo2": 96, "weight_kg": 88.2, "pain": 1},
            {"timestamp": _t(0.5), "bp": "140/82", "hr": 80, "rr": 16, "temp": 36.9, "spo2": 97, "weight_kg": 88.0, "pain": 1},
        ],
        "medications": [
            {"name": "Furosemide (Lasix)", "dose": "80mg", "route": "IV", "frequency": "BID", "next_due": (_now + timedelta(hours=2)).strftime("%H:%M"), "last_given": _t(4), "indication": "CHF - diuresis"},
            {"name": "Carvedilol", "dose": "12.5mg", "route": "PO", "frequency": "BID", "next_due": (_now + timedelta(hours=5)).strftime("%H:%M"), "last_given": _t(7), "indication": "Heart failure / HTN"},
            {"name": "Lisinopril", "dose": "10mg", "route": "PO", "frequency": "Daily", "next_due": (_now + timedelta(hours=14)).strftime("%H:%M"), "last_given": _t(10), "indication": "CHF / HTN"},
            {"name": "Spironolactone", "dose": "25mg", "route": "PO", "frequency": "Daily", "next_due": (_now + timedelta(hours=14)).strftime("%H:%M"), "last_given": _t(10), "indication": "CHF - aldosterone antagonist"},
            {"name": "Metformin", "dose": "500mg", "route": "PO", "frequency": "BID with meals", "next_due": (_now + timedelta(hours=3)).strftime("%H:%M"), "last_given": _t(9), "indication": "Type 2 DM - HELD during contrast"},
            {"name": "Heparin", "dose": "5000 units", "route": "SubQ", "frequency": "Q8H", "next_due": (_now + timedelta(hours=1)).strftime("%H:%M"), "last_given": _t(7), "indication": "DVT prophylaxis"},
        ],
        "labs": [
            {"name": "BMP", "timestamp": _t(6), "results": {
                "Na": {"value": 138, "unit": "mEq/L", "normal": "135-145", "critical": False},
                "K": {"value": 3.4, "unit": "mEq/L", "normal": "3.5-5.0", "critical": False, "flag": "LOW"},
                "Cl": {"value": 98, "unit": "mEq/L", "normal": "96-106", "critical": False},
                "CO2": {"value": 22, "unit": "mEq/L", "normal": "22-29", "critical": False},
                "BUN": {"value": 28, "unit": "mg/dL", "normal": "7-25", "critical": False, "flag": "HIGH"},
                "Creatinine": {"value": 1.8, "unit": "mg/dL", "normal": "0.6-1.2", "critical": False, "flag": "HIGH"},
                "Glucose": {"value": 142, "unit": "mg/dL", "normal": "70-110", "critical": False, "flag": "HIGH"},
            }},
            {"name": "BNP", "timestamp": _t(24), "results": {
                "BNP": {"value": 1240, "unit": "pg/mL", "normal": "<100", "critical": False, "flag": "HIGH"},
            }},
            {"name": "CBC", "timestamp": _t(6), "results": {
                "WBC": {"value": 8.2, "unit": "K/uL", "normal": "4.5-11.0", "critical": False},
                "Hgb": {"value": 10.8, "unit": "g/dL", "normal": "13.5-17.5", "critical": False, "flag": "LOW"},
                "Hct": {"value": 32.4, "unit": "%", "normal": "41-53", "critical": False, "flag": "LOW"},
                "Plt": {"value": 198, "unit": "K/uL", "normal": "150-400", "critical": False},
            }},
        ],
        "notes": [
            {"timestamp": _t(2), "author": "RN Taylor", "note": "Patient reports improved breathing. 2L O2 via NC. UO 480mL last 4 hrs. Lower extremity edema 2+. Tolerating low-sodium diet."},
            {"timestamp": _t(8), "author": "Dr. Johnson", "note": "Patient improving. Continue aggressive diuresis. Goal net negative 1-2L/day. Check BMP Q8H. Renal function trending up."},
        ],
        "orders": [
            {"type": "Lab", "order": "BMP STAT", "ordered_by": "Dr. Johnson", "due": (_now + timedelta(hours=2)).strftime("%H:%M"), "status": "Pending"},
            {"type": "Diet", "order": "2g Na+ restriction, 1.5L fluid restriction", "ordered_by": "Dr. Johnson", "status": "Active"},
            {"type": "Activity", "order": "Bed rest with BRP, fall precautions", "ordered_by": "Dr. Johnson", "status": "Active"},
            {"type": "Monitoring", "order": "Strict I&O, daily weight, telemetry", "ordered_by": "Dr. Johnson", "status": "Active"},
        ],
    },

    "P002": {
        "id": "P002",
        "name": "Maria Garcia",
        "age": 54,
        "dob": "1970-07-22",
        "mrn": "10034567",
        "room": "312B",
        "bed": "B",
        "admission_date": (_now - timedelta(days=1)).strftime("%Y-%m-%d"),
        "diagnosis": "Sepsis secondary to urinary tract infection",
        "secondary_diagnoses": ["Type 2 Diabetes Mellitus", "Obesity"],
        "attending": "Dr. Michael Chen",
        "code_status": "Full Code",
        "isolation": "Contact Precautions - ESBL",
        "fall_risk": "Medium",
        "allergies": [
            {"drug": "Sulfonamides", "reaction": "Rash"},
            {"drug": "Latex", "reaction": "Urticaria"},
        ],
        "vitals": [
            {"timestamp": _t(6), "bp": "88/52", "hr": 118, "rr": 24, "temp": 39.4, "spo2": 94, "weight_kg": 92.0, "pain": 6},
            {"timestamp": _t(4), "bp": "96/60", "hr": 108, "rr": 22, "temp": 38.8, "spo2": 95, "weight_kg": 92.0, "pain": 5},
            {"timestamp": _t(2), "bp": "104/68", "hr": 98, "rr": 20, "temp": 38.2, "spo2": 96, "weight_kg": 92.0, "pain": 4},
            {"timestamp": _t(1), "bp": "108/70", "hr": 94, "rr": 18, "temp": 37.9, "spo2": 97, "weight_kg": 92.0, "pain": 3},
            {"timestamp": _t(0.25), "bp": "112/72", "hr": 90, "rr": 18, "temp": 37.6, "spo2": 97, "weight_kg": 92.0, "pain": 3},
        ],
        "medications": [
            {"name": "Meropenem", "dose": "1g", "route": "IV", "frequency": "Q8H", "next_due": (_now + timedelta(hours=3)).strftime("%H:%M"), "last_given": _t(5), "indication": "ESBL UTI / Sepsis"},
            {"name": "Vancomycin", "dose": "1.5g", "route": "IV", "frequency": "Q12H (renally dosed)", "next_due": (_now + timedelta(hours=4)).strftime("%H:%M"), "last_given": _t(8), "indication": "Broad spectrum coverage"},
            {"name": "Norepinephrine", "dose": "0.08 mcg/kg/min", "route": "IV infusion", "frequency": "Continuous - titrate to MAP >65", "next_due": "Continuous", "last_given": "Infusing", "indication": "Septic shock - vasopressor"},
            {"name": "Normal Saline", "dose": "125mL/hr", "route": "IV", "frequency": "Continuous", "next_due": "Continuous", "last_given": "Infusing", "indication": "Fluid resuscitation"},
            {"name": "Insulin Regular", "dose": "Per sliding scale", "route": "SubQ", "frequency": "AC and bedtime", "next_due": (_now + timedelta(hours=1)).strftime("%H:%M"), "last_given": _t(5), "indication": "Hyperglycemia management"},
        ],
        "labs": [
            {"name": "Sepsis Panel", "timestamp": _t(4), "results": {
                "WBC": {"value": 18.4, "unit": "K/uL", "normal": "4.5-11.0", "critical": True, "flag": "CRITICAL HIGH"},
                "Lactate": {"value": 3.2, "unit": "mmol/L", "normal": "<2.0", "critical": True, "flag": "CRITICAL HIGH"},
                "Procalcitonin": {"value": 22.4, "unit": "ng/mL", "normal": "<0.5", "critical": False, "flag": "HIGH"},
                "CRP": {"value": 286, "unit": "mg/L", "normal": "<10", "critical": False, "flag": "HIGH"},
            }},
            {"name": "BMP", "timestamp": _t(4), "results": {
                "Na": {"value": 132, "unit": "mEq/L", "normal": "135-145", "critical": False, "flag": "LOW"},
                "K": {"value": 4.2, "unit": "mEq/L", "normal": "3.5-5.0", "critical": False},
                "Creatinine": {"value": 2.1, "unit": "mg/dL", "normal": "0.5-1.1", "critical": False, "flag": "HIGH"},
                "Glucose": {"value": 312, "unit": "mg/dL", "normal": "70-110", "critical": True, "flag": "CRITICAL HIGH"},
            }},
        ],
        "notes": [
            {"timestamp": _t(1), "author": "RN Davis", "note": "Blood cultures x2 drawn. Urine culture sent. Foley inserted — urine cloudy, amber. Norepinephrine started per sepsis protocol. MAP maintaining >65. ICU transfer pending bed availability."},
        ],
        "orders": [
            {"type": "Transfer", "order": "ICU transfer — awaiting bed", "ordered_by": "Dr. Chen", "status": "Pending"},
            {"type": "Lab", "order": "Repeat lactate in 2hrs", "ordered_by": "Dr. Chen", "due": (_now + timedelta(hours=1)).strftime("%H:%M"), "status": "Pending"},
            {"type": "Monitoring", "order": "Continuous cardiac monitor, arterial line placement", "ordered_by": "Dr. Chen", "status": "Active"},
            {"type": "IV", "order": "30mL/kg IV fluid bolus — COMPLETED", "ordered_by": "Dr. Chen", "status": "Completed"},
        ],
    },

    "P003": {
        "id": "P003",
        "name": "Robert Johnson",
        "age": 72,
        "dob": "1952-11-08",
        "mrn": "10045678",
        "room": "108C",
        "bed": "C",
        "admission_date": (_now - timedelta(days=2)).strftime("%Y-%m-%d"),
        "diagnosis": "Left hip arthroplasty (post-operative day 2)",
        "secondary_diagnoses": ["Osteoarthritis", "Hypertension", "GERD"],
        "attending": "Dr. Amanda Patel",
        "code_status": "Full Code",
        "isolation": "None",
        "fall_risk": "High",
        "allergies": [
            {"drug": "Codeine", "reaction": "Nausea/vomiting"},
            {"drug": "NSAIDs", "reaction": "GI irritation"},
        ],
        "vitals": [
            {"timestamp": _t(4), "bp": "128/76", "hr": 72, "rr": 16, "temp": 37.4, "spo2": 98, "weight_kg": 79.0, "pain": 4},
            {"timestamp": _t(2), "bp": "124/74", "hr": 70, "rr": 16, "temp": 37.3, "spo2": 99, "weight_kg": 79.0, "pain": 3},
            {"timestamp": _t(0.5), "bp": "122/72", "hr": 68, "rr": 14, "temp": 37.1, "spo2": 99, "weight_kg": 79.0, "pain": 2},
        ],
        "medications": [
            {"name": "Oxycodone/Acetaminophen (Percocet)", "dose": "5/325mg", "route": "PO", "frequency": "Q4H PRN pain (1-3)", "next_due": (_now + timedelta(hours=2)).strftime("%H:%M"), "last_given": _t(2), "indication": "Post-op pain"},
            {"name": "Celecoxib", "dose": "200mg", "route": "PO", "frequency": "BID", "next_due": (_now + timedelta(hours=6)).strftime("%H:%M"), "last_given": _t(6), "indication": "Post-op anti-inflammatory"},
            {"name": "Enoxaparin (Lovenox)", "dose": "40mg", "route": "SubQ", "frequency": "Daily", "next_due": (_now + timedelta(hours=18)).strftime("%H:%M"), "last_given": _t(6), "indication": "DVT prophylaxis post-ortho"},
            {"name": "Omeprazole", "dose": "20mg", "route": "PO", "frequency": "Daily", "next_due": (_now + timedelta(hours=14)).strftime("%H:%M"), "last_given": _t(10), "indication": "GERD / GI protection"},
            {"name": "Amlodipine", "dose": "5mg", "route": "PO", "frequency": "Daily", "next_due": (_now + timedelta(hours=14)).strftime("%H:%M"), "last_given": _t(10), "indication": "Hypertension"},
        ],
        "labs": [
            {"name": "CBC", "timestamp": _t(12), "results": {
                "WBC": {"value": 9.8, "unit": "K/uL", "normal": "4.5-11.0", "critical": False},
                "Hgb": {"value": 9.2, "unit": "g/dL", "normal": "13.5-17.5", "critical": False, "flag": "LOW"},
                "Hct": {"value": 27.6, "unit": "%", "normal": "41-53", "critical": False, "flag": "LOW"},
                "Plt": {"value": 156, "unit": "K/uL", "normal": "150-400", "critical": False},
            }},
        ],
        "notes": [
            {"timestamp": _t(2), "author": "PT Williams", "note": "Patient ambulated 30 feet with walker and assist x2. Weight-bearing as tolerated. Hip precautions maintained. Patient motivated for recovery."},
            {"timestamp": _t(4), "author": "RN Martinez", "note": "Wound dressing changed. Incision clean and dry, well-approximated, no signs of infection. Staples intact. Drains removed per surgeon."},
        ],
        "orders": [
            {"type": "Activity", "order": "PT/OT QD, ambulate BID, hip precautions", "ordered_by": "Dr. Patel", "status": "Active"},
            {"type": "Diet", "order": "Regular diet, advance as tolerated", "ordered_by": "Dr. Patel", "status": "Active"},
            {"type": "Lab", "order": "CBC in morning", "ordered_by": "Dr. Patel", "due": "Tomorrow 06:00", "status": "Pending"},
            {"type": "Wound", "order": "Change hip wound dressing daily", "ordered_by": "Dr. Patel", "status": "Active"},
        ],
    },

    "P004": {
        "id": "P004",
        "name": "Dorothy Williams",
        "age": 78,
        "dob": "1946-05-30",
        "mrn": "10056789",
        "room": "515A",
        "bed": "A",
        "admission_date": (_now - timedelta(days=5)).strftime("%Y-%m-%d"),
        "diagnosis": "Ischemic stroke - right MCA territory",
        "secondary_diagnoses": ["Atrial Fibrillation", "Hypertension", "Hyperlipidemia"],
        "attending": "Dr. James Lee",
        "code_status": "DNR/DNI",
        "isolation": "None",
        "fall_risk": "High",
        "allergies": [
            {"drug": "Warfarin", "reaction": "Prior intracranial bleed"},
            {"drug": "Iodine contrast", "reaction": "Anaphylaxis"},
        ],
        "vitals": [
            {"timestamp": _t(4), "bp": "162/94", "hr": 88, "rr": 18, "temp": 37.2, "spo2": 96, "weight_kg": 63.0, "pain": 0},
            {"timestamp": _t(2), "bp": "158/92", "hr": 86, "rr": 16, "temp": 37.1, "spo2": 97, "weight_kg": 63.0, "pain": 0},
            {"timestamp": _t(0.5), "bp": "156/90", "hr": 84, "rr": 16, "temp": 37.0, "spo2": 97, "weight_kg": 63.0, "pain": 0},
        ],
        "medications": [
            {"name": "Apixaban (Eliquis)", "dose": "5mg", "route": "PO", "frequency": "BID", "next_due": (_now + timedelta(hours=4)).strftime("%H:%M"), "last_given": _t(8), "indication": "Afib anticoagulation (stroke prevention)"},
            {"name": "Amlodipine", "dose": "10mg", "route": "PO", "frequency": "Daily", "next_due": (_now + timedelta(hours=14)).strftime("%H:%M"), "last_given": _t(10), "indication": "Hypertension"},
            {"name": "Atorvastatin", "dose": "80mg", "route": "PO", "frequency": "QHS", "next_due": (_now + timedelta(hours=8)).strftime("%H:%M"), "last_given": _t(16), "indication": "Post-stroke high-intensity statin"},
            {"name": "Aspirin", "dose": "81mg", "route": "PO", "frequency": "Daily", "next_due": (_now + timedelta(hours=14)).strftime("%H:%M"), "last_given": _t(10), "indication": "Antiplatelet - stroke secondary prevention"},
            {"name": "Metoprolol Succinate", "dose": "50mg", "route": "PO", "frequency": "Daily", "next_due": (_now + timedelta(hours=14)).strftime("%H:%M"), "last_given": _t(10), "indication": "Rate control for Afib"},
        ],
        "labs": [
            {"name": "Coagulation", "timestamp": _t(8), "results": {
                "PT": {"value": 13.2, "unit": "seconds", "normal": "11-13", "critical": False, "flag": "HIGH"},
                "INR": {"value": 1.2, "unit": "", "normal": "0.9-1.1", "critical": False, "flag": "HIGH"},
                "aPTT": {"value": 32, "unit": "seconds", "normal": "25-35", "critical": False},
            }},
            {"name": "Lipid Panel", "timestamp": _t(24), "results": {
                "Total Cholesterol": {"value": 224, "unit": "mg/dL", "normal": "<200", "critical": False, "flag": "HIGH"},
                "LDL": {"value": 148, "unit": "mg/dL", "normal": "<100", "critical": False, "flag": "HIGH"},
                "HDL": {"value": 42, "unit": "mg/dL", "normal": ">40", "critical": False},
                "Triglycerides": {"value": 182, "unit": "mg/dL", "normal": "<150", "critical": False, "flag": "HIGH"},
            }},
        ],
        "notes": [
            {"timestamp": _t(2), "author": "RN Thompson", "note": "Patient alert and oriented x2 (person, place). Left-sided weakness persists - 3/5 grip strength. Speech slurred but intelligible. Swallow eval done - regular diet cleared with thin liquids. Fall precautions in place. Family at bedside."},
        ],
        "orders": [
            {"type": "Consult", "order": "Speech therapy - swallowing evaluation", "ordered_by": "Dr. Lee", "status": "Completed"},
            {"type": "Consult", "order": "Physical therapy, occupational therapy, speech therapy ongoing", "ordered_by": "Dr. Lee", "status": "Active"},
            {"type": "Imaging", "order": "MRI brain with DWI sequence", "ordered_by": "Dr. Lee", "due": "Tomorrow", "status": "Pending"},
            {"type": "Monitoring", "order": "BP q4h, cardiac telemetry, neuro checks q4h", "ordered_by": "Dr. Lee", "status": "Active"},
        ],
    },

    "P005": {
        "id": "P005",
        "name": "Thomas Brown",
        "age": 61,
        "dob": "1963-09-12",
        "mrn": "10067890",
        "room": "220B",
        "bed": "B",
        "admission_date": (_now - timedelta(days=4)).strftime("%Y-%m-%d"),
        "diagnosis": "COPD exacerbation with acute hypercapnic respiratory failure",
        "secondary_diagnoses": ["COPD Gold Stage III", "Pulmonary Hypertension", "Former smoker (40 pack-years)"],
        "attending": "Dr. Rebecca Wong",
        "code_status": "Full Code",
        "isolation": "None",
        "fall_risk": "Medium",
        "allergies": [
            {"drug": "No known drug allergies (NKDA)", "reaction": "None"},
        ],
        "vitals": [
            {"timestamp": _t(4), "bp": "138/84", "hr": 96, "rr": 26, "temp": 37.6, "spo2": 88, "weight_kg": 74.0, "pain": 2},
            {"timestamp": _t(2), "bp": "134/82", "hr": 92, "rr": 24, "temp": 37.4, "spo2": 90, "weight_kg": 74.0, "pain": 1},
            {"timestamp": _t(1), "bp": "132/80", "hr": 88, "rr": 22, "temp": 37.2, "spo2": 91, "weight_kg": 74.0, "pain": 1},
            {"timestamp": _t(0.5), "bp": "130/78", "hr": 86, "rr": 20, "temp": 37.0, "spo2": 92, "weight_kg": 74.0, "pain": 1},
        ],
        "medications": [
            {"name": "Albuterol (Ventolin) nebulizer", "dose": "2.5mg in 3mL NS", "route": "Inhaled", "frequency": "Q4H and PRN wheeze/dyspnea", "next_due": (_now + timedelta(hours=2)).strftime("%H:%M"), "last_given": _t(2), "indication": "COPD exacerbation - bronchodilator"},
            {"name": "Ipratropium (Atrovent) nebulizer", "dose": "0.5mg", "route": "Inhaled", "frequency": "Q6H", "next_due": (_now + timedelta(hours=4)).strftime("%H:%M"), "last_given": _t(2), "indication": "COPD - anticholinergic bronchodilator"},
            {"name": "Methylprednisolone (Solu-Medrol)", "dose": "40mg", "route": "IV", "frequency": "Q12H x 5 days", "next_due": (_now + timedelta(hours=6)).strftime("%H:%M"), "last_given": _t(6), "indication": "COPD exacerbation - systemic steroid"},
            {"name": "Azithromycin", "dose": "500mg", "route": "PO", "frequency": "Daily x 5 days (Day 4)", "next_due": (_now + timedelta(hours=14)).strftime("%H:%M"), "last_given": _t(10), "indication": "Antimicrobial for exacerbation"},
            {"name": "Tiotropium (Spiriva)", "dose": "18mcg", "route": "Inhaled (HandiHaler)", "frequency": "Once daily", "next_due": (_now + timedelta(hours=14)).strftime("%H:%M"), "last_given": _t(10), "indication": "COPD maintenance"},
            {"name": "Enoxaparin (Lovenox)", "dose": "40mg", "route": "SubQ", "frequency": "Daily", "next_due": (_now + timedelta(hours=18)).strftime("%H:%M"), "last_given": _t(6), "indication": "DVT prophylaxis"},
        ],
        "labs": [
            {"name": "ABG", "timestamp": _t(4), "results": {
                "pH": {"value": 7.32, "unit": "", "normal": "7.35-7.45", "critical": False, "flag": "LOW"},
                "PaCO2": {"value": 58, "unit": "mmHg", "normal": "35-45", "critical": True, "flag": "CRITICAL HIGH"},
                "PaO2": {"value": 62, "unit": "mmHg", "normal": "80-100", "critical": False, "flag": "LOW"},
                "HCO3": {"value": 30, "unit": "mEq/L", "normal": "22-26", "critical": False, "flag": "HIGH"},
                "SaO2": {"value": 92, "unit": "%", "normal": ">95", "critical": False, "flag": "LOW"},
            }},
            {"name": "BMP", "timestamp": _t(4), "results": {
                "Na": {"value": 140, "unit": "mEq/L", "normal": "135-145", "critical": False},
                "K": {"value": 3.8, "unit": "mEq/L", "normal": "3.5-5.0", "critical": False},
                "Glucose": {"value": 182, "unit": "mg/dL", "normal": "70-110", "critical": False, "flag": "HIGH"},
            }},
        ],
        "notes": [
            {"timestamp": _t(1), "author": "RN Adams", "note": "Patient on 2L O2 via NC, maintaining SpO2 91-93%. Breath sounds with diffuse expiratory wheeze. Using accessory muscles minimally. Cough productive of yellow-green sputum. Sputum culture pending. BiPAP not required at this time but on standby."},
        ],
        "orders": [
            {"type": "Respiratory", "order": "Continuous O2 saturation monitoring. Target SpO2 88-92% (COPD patient)", "ordered_by": "Dr. Wong", "status": "Active"},
            {"type": "Lab", "order": "Repeat ABG in 4 hours", "ordered_by": "Dr. Wong", "due": (_now + timedelta(hours=0)).strftime("%H:%M"), "status": "Due Now"},
            {"type": "Respiratory", "order": "BiPAP standby if SpO2 <88% or RR >30", "ordered_by": "Dr. Wong", "status": "Active"},
            {"type": "Microbiology", "order": "Sputum culture and sensitivity", "ordered_by": "Dr. Wong", "status": "Pending result"},
        ],
    },
}

def find_patient(identifier: str) -> Optional[dict]:
    identifier = identifier.strip().lower()
    for pid, patient in PATIENTS.items():
        if (pid.lower() == identifier or
                patient["name"].lower() == identifier or
                patient["name"].lower().startswith(identifier) or
                identifier in patient["name"].lower() or
                patient["mrn"] == identifier):
            return patient
    return None

def get_all_patients_summary() -> list:
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "room": p["room"],
            "diagnosis": p["diagnosis"],
            "code_status": p["code_status"],
            "fall_risk": p["fall_risk"],
            "isolation": p["isolation"],
        }
        for p in PATIENTS.values()
    ]

def add_note(patient_id: str, note: str, author: str = "Nia AI") -> bool:
    if patient_id in PATIENTS:
        PATIENTS[patient_id]["notes"].insert(0, {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "author": author,
            "note": note,
        })
        return True
    return False
