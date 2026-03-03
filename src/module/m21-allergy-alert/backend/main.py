"""
FastAPI backend for M21 Allergy Alert System
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import sys
import os
from bson import ObjectId

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import *
from shared.database import db_manager, allergy_service

# Initialize FastAPI app
app = FastAPI(
    title="M21 Allergy Alert System API",
    description="Backend API for Allergy-Aware Medication Alert System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    if not db_manager.connect():
        raise Exception("Failed to connect to MongoDB")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    db_manager.disconnect()


@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        "service": "Module 21: Allergy-Aware Medication Alert System",
        "version": "1.0.0",
        "description": "Python/MongoDB backend API for checking medication allergies and cross-reactivities",
        "technology_stack": {
            "backend": "FastAPI + Python",
            "database": "MongoDB",
            "frontend": "Streamlit"
        },
        "endpoints": {
            "validation": {
                "POST /api/v1/validate": "Run full allergy check for a prescription",
                "POST /api/v1/check-exact": "Test exact drug match",
                "POST /api/v1/check-class": "Test drug class match",
                "POST /api/v1/check-cross-reactivity": "Test cross-reactivity"
            },
            "patients": {
                "GET /api/v1/patients": "List all patients",
                "GET /api/v1/patient/{id}/allergies": "Get patient allergy profile",
                "GET /api/v1/patient/{id}/alerts": "Get patient alert history"
            },
            "medications": {
                "GET /api/v1/medications": "List all medications",
                "GET /api/v1/medication/{id}": "Get medication details",
                "GET /api/v1/medication/{id}/alternatives": "Get safe alternatives"
            },
            "analytics": {
                "GET /api/v1/stats": "Get system statistics",
                "GET /api/v1/alerts/recent": "Get recent alerts"
            }
        },
        "database_features": {
            "collections": 9,
            "indexes": "Optimized for performance",
            "aggregation_pipelines": "Advanced MongoDB queries",
            "validation": "3-level cascade checking"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db_manager.client.admin.command('ping')
        return {
            "status": "OK",
            "service": "M21 Allergy Alert System",
            "timestamp": datetime.now().isoformat(),
            "database": "Connected"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")


# Validation Endpoints
@app.post("/api/v1/validate", response_model=ValidationResponse)
async def validate_prescription(request: PrescriptionRequest):
    """Main prescription validation endpoint"""
    try:
        # Create prescription record
        prescription_data = {
            "_id": str(ObjectId()),
            "patient_id": request.patient_id,
            "med_id": request.med_id,
            "dose": request.dose,
            "frequency": request.frequency,
            "start_date": request.start_date,
            "status": "Pending",
            "created_at": datetime.now()
        }
        
        db_manager.get_collection("prescriptions").insert_one(prescription_data)
        prescription_id = prescription_data["_id"]
        
        # Perform allergy check
        check_result = allergy_service.perform_full_check(
            request.patient_id, request.med_id, prescription_id
        )
        
        # Prepare response
        response_data = {
            "status": check_result["status"],
            "alert_type": check_result.get("alert_type"),
            "message": check_result["message"],
            "prescription_id": prescription_id,
            "alternatives": check_result.get("alternatives", []),
            "logged_at": datetime.now()
        }
        
        # Add approval token for safe prescriptions
        if check_result["status"] == "SAFE":
            response_data["approval_token"] = generate_approval_token(
                request.patient_id, request.med_id
            )
        
        return ValidationResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@app.post("/api/v1/check-exact")
async def check_exact_match(patient_id: str, med_id: str):
    """Debug endpoint for exact match checking"""
    try:
        result = allergy_service.check_exact_match(patient_id, med_id)
        return {
            "check_type": "EXACT_MATCH",
            "match_found": result,
            "patient_id": patient_id,
            "med_id": med_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/check-class")
async def check_class_match(patient_id: str, med_id: str):
    """Debug endpoint for class match checking"""
    try:
        result = allergy_service.check_class_match(patient_id, med_id)
        return {
            "check_type": "CLASS_MATCH",
            "match_found": result,
            "patient_id": patient_id,
            "med_id": med_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/check-cross-reactivity")
async def check_cross_reactivity(patient_id: str, med_id: str, threshold: float = 0.5):
    """Debug endpoint for cross-reactivity checking"""
    try:
        result = allergy_service.check_cross_reactivity(patient_id, med_id, threshold)
        return {
            "check_type": "CROSS_REACTIVITY",
            "match_found": result,
            "patient_id": patient_id,
            "med_id": med_id,
            "threshold": threshold
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Patient Endpoints
@app.get("/api/v1/patients")
async def get_patients():
    """Get all patients with calculated age"""
    try:
        patients = list(db_manager.get_collection("patients").find())
        
        # Add calculated age
        for patient in patients:
            patient["age"] = get_age(patient["dob"])
            patient["patient_id"] = patient["_id"]
        
        return {"success": True, "patients": patients}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/patient/{patient_id}/allergies")
async def get_patient_allergies(patient_id: str):
    """Get patient's allergy profile"""
    try:
        # Get patient info
        patient = db_manager.get_collection("patients").find_one({"_id": patient_id})
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Get patient allergies with details
        pipeline = [
            {"$match": {"patient_id": patient_id}},
            {"$lookup": {
                "from": "allergies",
                "localField": "allergy_id",
                "foreignField": "_id",
                "as": "allergy_details"
            }},
            {"$unwind": "$allergy_details"},
            {"$project": {
                "allergy_id": "$allergy_id",
                "allergy_name": "$allergy_details.allergy_name",
                "allergy_type": "$allergy_details.allergy_type",
                "date_recorded": "$date_recorded",
                "notes": "$notes"
            }}
        ]
        
        allergies = list(db_manager.get_collection("patient_allergies").aggregate(pipeline))
        
        # Get risk profile
        risk_pipeline = [
            {"$match": {"patient_id": patient_id}},
            {"$lookup": {
                "from": "cross_reactivity_rules",
                "localField": "allergy_id",
                "foreignField": "allergen_id",
                "as": "cross_rules"
            }},
            {"$unwind": {"path": "$cross_rules", "preserveNullAndEmptyArrays": True}},
            {"$lookup": {
                "from": "allergies",
                "localField": "allergy_id",
                "foreignField": "_id",
                "as": "allergy_details"
            }},
            {"$unwind": "$allergy_details"},
            {"$lookup": {
                "from": "medications",
                "localField": "cross_rules.reactive_med_id",
                "foreignField": "_id",
                "as": "reactive_med"
            }},
            {"$unwind": {"path": "$reactive_med", "preserveNullAndEmptyArrays": True}},
            {"$project": {
                "allergy_name": "$allergy_details.allergy_name",
                "allergy_type": "$allergy_details.allergy_type",
                "risk_level": "$cross_rules.risk_level",
                "risk_score": "$cross_rules.risk_score",
                "reactive_drug": "$reactive_med.med_name"
            }}
        ]
        
        risk_profile = list(db_manager.get_collection("patient_allergies").aggregate(risk_pipeline))
        
        patient["age"] = get_age(patient["dob"])
        
        return {
            "success": True,
            "patient": patient,
            "allergies": allergies,
            "risk_profile": risk_profile
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/patient/{patient_id}/alerts")
async def get_patient_alerts(patient_id: str):
    """Get patient's alert history"""
    try:
        # Get alerts with medication details
        pipeline = [
            {"$match": {"patient_id": patient_id}},
            {"$lookup": {
                "from": "medications",
                "localField": "med_id",
                "foreignField": "_id",
                "as": "medication"
            }},
            {"$unwind": "$medication"},
            {"$lookup": {
                "from": "prescriptions",
                "localField": "prescription_id",
                "foreignField": "_id",
                "as": "prescription"
            }},
            {"$unwind": {"path": "$prescription", "preserveNullAndEmptyArrays": True}},
            {"$project": {
                "log_id": "$_id",
                "alert_type": "$alert_type",
                "med_name": "$medication.med_name",
                "alert_message": "$alert_message",
                "logged_at": "$logged_at",
                "prescription_status": "$prescription.status",
                "dose": "$prescription.dose",
                "frequency": "$prescription.frequency"
            }},
            {"$sort": {"logged_at": -1}}
        ]
        
        alerts = list(db_manager.get_collection("alert_log").aggregate(pipeline))
        
        return {
            "success": True,
            "patient_id": patient_id,
            "alerts": alerts
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Medication Endpoints
@app.get("/api/v1/medications")
async def get_medications():
    """Get all medications"""
    try:
        medications = list(db_manager.get_collection("medications").find())
        
        for med in medications:
            med["med_id"] = med["_id"]
        
        return {"success": True, "medications": medications}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/medication/{med_id}")
async def get_medication_details(med_id: str):
    """Get detailed medication information"""
    try:
        medication = db_manager.get_collection("medications").find_one({"_id": med_id})
        if not medication:
            raise HTTPException(status_code=404, detail="Medication not found")
        
        # Get alternatives
        alternatives = allergy_service.get_alternatives(med_id)
        
        # Get cross-reactivity info
        cross_reactivity = list(db_manager.get_collection("cross_reactivity_rules").aggregate([
            {"$match": {"reactive_med_id": med_id}},
            {"$lookup": {
                "from": "allergies",
                "localField": "allergen_id",
                "foreignField": "_id",
                "as": "allergy"
            }},
            {"$unwind": "$allergy"},
            {"$project": {
                "allergy_name": "$allergy.allergy_name",
                "risk_level": "$risk_level",
                "risk_score": "$risk_score"
            }}
        ]))
        
        return {
            "success": True,
            "medication": medication,
            "alternatives": alternatives,
            "cross_reactivity": cross_reactivity
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/medication/{med_id}/alternatives")
async def get_medication_alternatives(med_id: str):
    """Get safe alternatives for a medication"""
    try:
        alternatives = allergy_service.get_alternatives(med_id)
        
        return {
            "success": True,
            "med_id": med_id,
            "alternatives": alternatives
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/drug-classes")
async def get_drug_classes():
    """Get all drug classes with medication counts"""
    try:
        pipeline = [
            {"$group": {
                "_id": "$drug_class",
                "medication_count": {"$sum": 1},
                "medications": {"$push": "$med_name"}
            }},
            {"$project": {
                "drug_class": "$_id",
                "medication_count": "$medication_count",
                "medications": {"$slice": ["$medications", 3]}  # First 3 examples
            }},
            {"$sort": {"drug_class": 1}}
        ]
        
        drug_classes = list(db_manager.get_collection("medications").aggregate(pipeline))
        
        return {"success": True, "drug_classes": drug_classes}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Analytics Endpoints
@app.get("/api/v1/stats")
async def get_system_stats():
    """Get system statistics"""
    try:
        # Alert type statistics
        alert_stats_pipeline = [
            {"$group": {
                "_id": "$alert_type",
                "total": {"$sum": 1}
            }},
            {"$project": {
                "alert_type": "$_id",
                "total": "$total"
            }},
            {"$sort": {"total": -1}}
        ]
        
        alert_statistics = list(db_manager.get_collection("alert_log").aggregate(alert_stats_pipeline))
        
        # Additional statistics
        total_patients = db_manager.get_collection("patients").count_documents({})
        total_medications = db_manager.get_collection("medications").count_documents({})
        total_prescriptions = db_manager.get_collection("prescriptions").count_documents({})
        
        patients_with_allergies = len(list(db_manager.get_collection("patient_allergies").distinct("patient_id")))
        
        high_risk_rules = db_manager.get_collection("cross_reactivity_rules").count_documents(
            {"risk_score": {"$gt": 0.7}}
        )
        
        # Prescription status breakdown
        prescription_stats_pipeline = [
            {"$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }}
        ]
        
        prescription_breakdown = list(db_manager.get_collection("prescriptions").aggregate(prescription_stats_pipeline))
        prescription_stats = {item["_id"]: item["count"] for item in prescription_breakdown}
        
        return {
            "success": True,
            "alert_statistics": alert_statistics,
            "additional_stats": {
                "total_patients": total_patients,
                "patients_with_allergies": patients_with_allergies,
                "total_medications": total_medications,
                "total_prescriptions": total_prescriptions,
                "high_risk_rules": high_risk_rules,
                "prescription_stats": prescription_stats
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/alerts/recent")
async def get_recent_alerts(limit: int = 20):
    """Get recent alerts across all patients"""
    try:
        pipeline = [
            {"$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient"
            }},
            {"$unwind": "$patient"},
            {"$lookup": {
                "from": "medications",
                "localField": "med_id",
                "foreignField": "_id",
                "as": "medication"
            }},
            {"$unwind": "$medication"},
            {"$lookup": {
                "from": "prescriptions",
                "localField": "prescription_id",
                "foreignField": "_id",
                "as": "prescription"
            }},
            {"$unwind": {"path": "$prescription", "preserveNullAndEmptyArrays": True}},
            {"$project": {
                "log_id": "$_id",
                "alert_type": "$alert_type",
                "patient_name": "$patient.name",
                "med_name": "$medication.med_name",
                "alert_message": "$alert_message",
                "logged_at": "$logged_at",
                "prescription_status": "$prescription.status"
            }},
            {"$sort": {"logged_at": -1}},
            {"$limit": limit}
        ]
        
        recent_alerts = list(db_manager.get_collection("alert_log").aggregate(pipeline))
        
        return {
            "success": True,
            "recent_alerts": recent_alerts
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/prescriptions")
async def get_prescriptions():
    """Get all prescriptions with patient and medication details"""
    try:
        pipeline = [
            {"$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient"
            }},
            {"$unwind": "$patient"},
            {"$lookup": {
                "from": "medications",
                "localField": "med_id",
                "foreignField": "_id",
                "as": "medication"
            }},
            {"$unwind": "$medication"},
            {"$project": {
                "prescription_id": "$_id",
                "patient_name": "$patient.name",
                "med_name": "$medication.med_name",
                "drug_class": "$medication.drug_class",
                "dose": "$dose",
                "frequency": "$frequency",
                "start_date": "$start_date",
                "status": "$status",
                "created_at": "$created_at"
            }},
            {"$sort": {"created_at": -1}}
        ]
        
        prescriptions = list(db_manager.get_collection("prescriptions").aggregate(pipeline))
        
        return {
            "success": True,
            "prescriptions": prescriptions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)