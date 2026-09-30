import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from database import find_patient, add_note, get_all_patients_summary
from rag_engine import get_rag_engine

logger = logging.getLogger(__name__)

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_patient_info",
            "description": "Retrieve patient demographic information, diagnosis, allergies, code status, isolation status, and room assignment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_identifier": {
                        "type": "string",
                        "description": "Patient ID (e.g., P001), patient name, or MRN.",
                    }
                },
                "required": ["patient_identifier"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_vital_signs",
            "description": "Get recent vital signs for a patient: blood pressure, heart rate, respiratory rate, temperature, SpO2, weight, and pain score.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_identifier": {
                        "type": "string",
                        "description": "Patient ID, name, or MRN.",
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of recent vital sign sets to retrieve (default: 3).",
                        "default": 3,
                    },
                },
                "required": ["patient_identifier"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_medications",
            "description": "Get the full medication list for a patient, including doses, routes, frequency, last administered time, and next due time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_identifier": {
                        "type": "string",
                        "description": "Patient ID, name, or MRN.",
                    }
                },
                "required": ["patient_identifier"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_lab_results",
            "description": "Get recent laboratory results for a patient. Flags critical values automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_identifier": {
                        "type": "string",
                        "description": "Patient ID, name, or MRN.",
                    }
                },
                "required": ["patient_identifier"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_upcoming_medications",
            "description": "Get medications due within the next specified hours for a patient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_identifier": {
                        "type": "string",
                        "description": "Patient ID, name, or MRN.",
                    },
                    "hours": {
                        "type": "integer",
                        "description": "Number of hours to look ahead (default: 2).",
                        "default": 2,
                    },
                },
                "required": ["patient_identifier"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pending_orders",
            "description": "Get pending physician orders for a patient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_identifier": {
                        "type": "string",
                        "description": "Patient ID, name, or MRN.",
                    }
                },
                "required": ["patient_identifier"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_nursing_note",
            "description": "Add a nursing note to a patient's electronic health record.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_identifier": {
                        "type": "string",
                        "description": "Patient ID, name, or MRN.",
                    },
                    "note": {
                        "type": "string",
                        "description": "The nursing note content to add to the chart.",
                    },
                },
                "required": ["patient_identifier", "note"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_clinical_protocols",
            "description": "Search clinical protocols, nursing procedures, and medication guidelines. Use for questions about sepsis protocol, fall prevention, medication administration, wound care, vital signs interpretation, IV care, SBAR, code blue, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Clinical question or topic to search (e.g., 'sepsis treatment', 'fall prevention interventions', 'vancomycin dosing', 'SBAR example').",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_all_patients",
            "description": "List all patients currently on the unit with their room, diagnosis, code status, fall risk, and isolation precautions.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
]


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    logger.info(f"Executing tool: {tool_name} with args: {arguments}")
    try:
        if tool_name == "get_patient_info":
            return _get_patient_info(arguments.get("patient_identifier", ""))
        elif tool_name == "get_vital_signs":
            return _get_vital_signs(
                arguments.get("patient_identifier", ""),
                arguments.get("count", 3),
            )
        elif tool_name == "get_medications":
            return _get_medications(arguments.get("patient_identifier", ""))
        elif tool_name == "get_lab_results":
            return _get_lab_results(arguments.get("patient_identifier", ""))
        elif tool_name == "get_upcoming_medications":
            return _get_upcoming_medications(
                arguments.get("patient_identifier", ""),
                arguments.get("hours", 2),
            )
        elif tool_name == "get_pending_orders":
            return _get_pending_orders(arguments.get("patient_identifier", ""))
        elif tool_name == "add_nursing_note":
            return _add_nursing_note(
                arguments.get("patient_identifier", ""),
                arguments.get("note", ""),
            )
        elif tool_name == "search_clinical_protocols":
            return _search_protocols(arguments.get("query", ""))
        elif tool_name == "list_all_patients":
            return _list_all_patients()
        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})
    except Exception as e:
        logger.error(f"Tool execution error ({tool_name}): {e}")
        return json.dumps({"error": str(e)})


def _get_patient_info(identifier: str) -> str:
    patient = find_patient(identifier)
    if not patient:
        return json.dumps({"error": f"Patient '{identifier}' not found. Please verify the name or ID."})
    return json.dumps({
        "patient_id": patient["id"],
        "name": patient["name"],
        "age": patient["age"],
        "dob": patient["dob"],
        "mrn": patient["mrn"],
        "room": patient["room"],
        "admission_date": patient["admission_date"],
        "diagnosis": patient["diagnosis"],
        "secondary_diagnoses": patient["secondary_diagnoses"],
        "attending": patient["attending"],
        "code_status": patient["code_status"],
        "isolation": patient["isolation"],
        "fall_risk": patient["fall_risk"],
        "allergies": patient["allergies"],
    })


def _get_vital_signs(identifier: str, count: int = 3) -> str:
    patient = find_patient(identifier)
    if not patient:
        return json.dumps({"error": f"Patient '{identifier}' not found."})
    vitals = patient["vitals"][-count:]
    latest = vitals[-1] if vitals else {}
    alerts = []
    if latest:
        hr = latest.get("hr", 0)
        spo2 = latest.get("spo2", 100)
        rr = latest.get("rr", 16)
        if hr < 40 or hr > 150:
            alerts.append(f"CRITICAL HR: {hr} bpm")
        if spo2 < 88:
            alerts.append(f"CRITICAL SpO2: {spo2}%")
        if rr < 8 or rr > 28:
            alerts.append(f"CRITICAL RR: {rr}/min — consider Rapid Response")
    return json.dumps({
        "patient": patient["name"],
        "room": patient["room"],
        "recent_vitals": vitals,
        "critical_alerts": alerts,
    })


def _get_medications(identifier: str) -> str:
    patient = find_patient(identifier)
    if not patient:
        return json.dumps({"error": f"Patient '{identifier}' not found."})
    allergies = [a["drug"] for a in patient.get("allergies", [])]
    return json.dumps({
        "patient": patient["name"],
        "room": patient["room"],
        "allergies": allergies,
        "medications": patient["medications"],
        "count": len(patient["medications"]),
    })


def _get_lab_results(identifier: str) -> str:
    patient = find_patient(identifier)
    if not patient:
        return json.dumps({"error": f"Patient '{identifier}' not found."})
    critical_values = []
    for lab_set in patient["labs"]:
        for test_name, result in lab_set["results"].items():
            if result.get("critical"):
                critical_values.append(
                    f"CRITICAL: {test_name} = {result['value']} {result['unit']} (normal: {result['normal']})"
                )
    return json.dumps({
        "patient": patient["name"],
        "room": patient["room"],
        "labs": patient["labs"],
        "critical_values": critical_values,
    })


def _get_upcoming_medications(identifier: str, hours: int = 2) -> str:
    patient = find_patient(identifier)
    if not patient:
        return json.dumps({"error": f"Patient '{identifier}' not found."})
    now = datetime.now()
    upcoming = []
    for med in patient["medications"]:
        next_due = med.get("next_due", "")
        if next_due == "Continuous":
            upcoming.append({**med, "status": "Currently infusing"})
        elif ":" in next_due:
            try:
                due_time = datetime.strptime(next_due, "%H:%M").replace(
                    year=now.year, month=now.month, day=now.day
                )
                diff_hrs = (due_time - now).total_seconds() / 3600
                if -0.5 <= diff_hrs <= hours:
                    status = "OVERDUE" if diff_hrs < 0 else f"Due in {int(diff_hrs * 60)} min"
                    upcoming.append({**med, "status": status})
            except ValueError:
                pass
    return json.dumps({
        "patient": patient["name"],
        "room": patient["room"],
        "upcoming_medications": upcoming,
        "window_hours": hours,
        "allergies": [a["drug"] for a in patient.get("allergies", [])],
    })


def _get_pending_orders(identifier: str) -> str:
    patient = find_patient(identifier)
    if not patient:
        return json.dumps({"error": f"Patient '{identifier}' not found."})
    pending = [o for o in patient["orders"] if o.get("status") in ("Pending", "Due Now", "Active")]
    return json.dumps({
        "patient": patient["name"],
        "room": patient["room"],
        "pending_orders": pending,
    })


def _add_nursing_note(identifier: str, note: str) -> str:
    patient = find_patient(identifier)
    if not patient:
        return json.dumps({"error": f"Patient '{identifier}' not found."})
    if not note.strip():
        return json.dumps({"error": "Note content cannot be empty."})
    success = add_note(patient["id"], note, author="Nia AI (Voice)")
    if success:
        return json.dumps({
            "success": True,
            "message": f"Nursing note successfully added to {patient['name']}'s chart.",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "patient": patient["name"],
        })
    return json.dumps({"error": "Failed to add note."})


def _search_protocols(query: str) -> str:
    rag = get_rag_engine()
    results = rag.search(query, top_k=3)
    return json.dumps({"query": query, "results": results})


def _list_all_patients() -> str:
    patients = get_all_patients_summary()
    return json.dumps({"patients": patients, "count": len(patients)})
