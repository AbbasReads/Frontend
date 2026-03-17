"""
Shared data models for M21 Allergy Alert System
"""
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class Sex(str, Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "Other"


class AllergyType(str, Enum):
    DRUG = "Drug"
    FOOD = "Food"
    ENVIRONMENTAL = "Environmental"
    LATEX = "Latex"


class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class AlertType(str, Enum):
    EXACT_MATCH = "EXACT_MATCH"
    CLASS_MATCH = "CLASS_MATCH"
    CROSS_REACTIVITY = "CROSS_REACTIVITY"
    SAFE = "SAFE"


class PrescriptionStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


# Database Models
class Patient(BaseModel):
    patient_id: Optional[str] = Field(None, alias="_id")
    name: str
    dob: date
    sex: Sex
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class Allergy(BaseModel):
    allergy_id: Optional[str] = Field(None, alias="_id")
    allergy_name: str
    allergy_type: AllergyType
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class Medication(BaseModel):
    med_id: Optional[str] = Field(None, alias="_id")
    med_name: str
    drug_class: str
    active_ingredients: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class PatientAllergy(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    patient_id: str
    allergy_id: str
    date_recorded: date
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class CrossReactivityRule(BaseModel):
    rule_id: Optional[str] = Field(None, alias="_id")
    allergen_id: str
    reactive_med_id: str
    risk_level: RiskLevel
    risk_score: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class DrugClassAllergy(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    drug_class: str
    allergy_id: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class Alternative(BaseModel):
    alt_id: Optional[str] = Field(None, alias="_id")
    original_med_id: str
    alternative_med_id: str
    reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class Prescription(BaseModel):
    prescription_id: Optional[str] = Field(None, alias="_id")
    patient_id: str
    med_id: str
    dose: str
    frequency: str
    start_date: date
    status: PrescriptionStatus = PrescriptionStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class AlertLog(BaseModel):
    log_id: Optional[str] = Field(None, alias="_id")
    prescription_id: Optional[str] = None
    patient_id: str
    med_id: str
    alert_type: AlertType
    alert_message: str
    logged_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


# API Request/Response Models
class PrescriptionRequest(BaseModel):
    patient_id: str
    med_id: str
    dose: str
    frequency: str
    start_date: date


class ValidationResponse(BaseModel):
    status: str  # "ALERT" or "SAFE"
    alert_type: Optional[AlertType] = None
    message: str
    prescription_id: str
    alternatives: List[Dict[str, Any]] = []
    approval_token: Optional[str] = None
    logged_at: datetime


class PatientAllergyProfile(BaseModel):
    patient: Patient
    allergies: List[Dict[str, Any]]
    risk_profile: List[Dict[str, Any]]


class SystemStats(BaseModel):
    alert_statistics: List[Dict[str, Any]]
    total_patients: int
    total_medications: int
    total_prescriptions: int
    high_risk_rules: int


# Utility Functions
def get_age(dob: date) -> int:
    """Calculate age from date of birth"""
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def generate_approval_token(patient_id: str, med_id: str) -> str:
    """Generate approval token for safe prescriptions"""
    today = datetime.now().strftime("%Y%m%d")
    return f"SAFE-{today}-PT{patient_id}-MD{med_id}"