# Module 21: Allergy-Aware Medication Alert System (Python/MongoDB)
## Project Report

**Course:** Database Management Systems (DBMS) — IIT(ISM) Dhanbad  
**Project:** AI-Based Clinical Decision Support System  
**Module Number:** M21  
**Category:** D — Drug & Prescription Safety Systems  
**Academic Year:** 2025–2026, Winter Semester  

---

## Executive Summary

Module 21 implements a comprehensive Allergy-Aware Medication Alert System using modern Python technologies and MongoDB. The system performs real-time safety checks when prescriptions are submitted using a sophisticated 3-level cascade checking mechanism to identify potential allergic reactions and provides safe alternative medications when alerts are triggered.

## Technology Stack

### Backend Architecture
- **API Framework:** FastAPI with automatic OpenAPI documentation
- **Database:** MongoDB with advanced aggregation pipelines
- **Data Validation:** Pydantic models with type safety
- **Async Processing:** Asynchronous request handling

### Frontend Architecture
- **Framework:** Streamlit for rapid dashboard development
- **Visualization:** Plotly for interactive charts and graphs
- **Data Processing:** Pandas for data manipulation
- **UI Components:** Custom CSS with responsive design

### Database Design
- **9 Collections:** Document-based schema optimized for MongoDB
- **Aggregation Pipelines:** Complex queries using MongoDB's aggregation framework
- **Indexing Strategy:** Optimized indexes for performance
- **Data Validation:** Schema validation at application level

## Core Functionality

### 3-Level Cascade Checking System

1. **Level 1 - Exact Match Check**
   - Direct comparison between medication name and patient allergies
   - Case-insensitive string matching
   - Highest priority alert type

2. **Level 2 - Drug Class Match Check**
   - Checks if medication's drug class matches patient's allergy categories
   - Uses drug_class_allergies collection for mapping
   - Catches broader category allergies (e.g., "NSAIDs", "Penicillins")

3. **Level 3 - Cross-Reactivity Check**
   - Analyzes cross-reactivity patterns with configurable risk scoring
   - Default risk threshold: 0.5 (configurable)
   - Identifies medications that may cause reactions due to chemical similarity

### MongoDB Collections Schema

#### Core Collections
```javascript
// patients
{
  _id: "patient_1",
  name: "Arjun Sharma",
  dob: ISODate("1990-05-10"),
  sex: "M",
  created_at: ISODate()
}

// allergies
{
  _id: "allergy_1",
  allergy_name: "Penicillin",
  allergy_type: "Drug",
  created_at: ISODate()
}

// medications
{
  _id: "med_1",
  med_name: "Amoxicillin",
  drug_class: "Penicillin",
  active_ingredients: "Amoxicillin trihydrate",
  created_at: ISODate()
}
```

#### Relationship Collections
```javascript
// patient_allergies (Many-to-Many)
{
  _id: ObjectId(),
  patient_id: "patient_1",
  allergy_id: "allergy_1",
  date_recorded: ISODate("2023-01-10"),
  notes: "Severe rash observed",
  created_at: ISODate()
}

// cross_reactivity_rules
{
  _id: ObjectId(),
  allergen_id: "allergy_1",
  reactive_med_id: "med_3",
  risk_level: "High",
  risk_score: 0.80,
  created_at: ISODate()
}
```

## Advanced MongoDB Features

### Aggregation Pipelines

**Patient Allergy Profile with Risk Assessment:**
```javascript
[
  { $match: { patient_id: "patient_1" } },
  { $lookup: {
      from: "allergies",
      localField: "allergy_id",
      foreignField: "_id",
      as: "allergy_details"
  }},
  { $lookup: {
      from: "cross_reactivity_rules",
      localField: "allergy_id",
      foreignField: "allergen_id",
      as: "cross_rules"
  }},
  { $unwind: { path: "$cross_rules", preserveNullAndEmptyArrays: true } },
  { $lookup: {
      from: "medications",
      localField: "cross_rules.reactive_med_id",
      foreignField: "_id",
      as: "reactive_med"
  }}
]
```

**Alert Statistics Aggregation:**
```javascript
[
  { $group: {
      _id: "$alert_type",
      total: { $sum: 1 }
  }},
  { $sort: { total: -1 } }
]
```

### Indexing Strategy
```javascript
// Performance-optimized indexes
db.patient_allergies.createIndex({ patient_id: 1, allergy_id: 1 }, { unique: true })
db.cross_reactivity_rules.createIndex({ allergen_id: 1, reactive_med_id: 1 })
db.cross_reactivity_rules.createIndex({ risk_score: 1 })
db.alert_log.createIndex({ patient_id: 1, logged_at: -1 })
db.medications.createIndex({ med_name: 1 }, { unique: true })
```

## API Architecture

### FastAPI Endpoints

#### Validation Endpoints
- `POST /api/v1/validate` - Complete prescription validation
- `POST /api/v1/check-exact` - Debug exact match checking
- `POST /api/v1/check-class` - Debug class match checking
- `POST /api/v1/check-cross-reactivity` - Debug cross-reactivity checking

#### Data Access Endpoints
- `GET /api/v1/patients` - Patient listing with calculated ages
- `GET /api/v1/patient/{id}/allergies` - Comprehensive allergy profile
- `GET /api/v1/patient/{id}/alerts` - Patient alert history
- `GET /api/v1/medications` - Medication database
- `GET /api/v1/medication/{id}` - Detailed medication information
- `GET /api/v1/stats` - System analytics and statistics

### Request/Response Models

**Prescription Validation Request:**
```python
class PrescriptionRequest(BaseModel):
    patient_id: str
    med_id: str
    dose: str
    frequency: str
    start_date: date
```

**Validation Response:**
```python
class ValidationResponse(BaseModel):
    status: str  # "ALERT" or "SAFE"
    alert_type: Optional[AlertType]
    message: str
    prescription_id: str
    alternatives: List[Dict[str, Any]]
    approval_token: Optional[str]
    logged_at: datetime
```

## Streamlit Dashboard Features

### 1. Prescription Validator
- **Interactive Form:** Real-time patient and medication selection
- **Immediate Feedback:** Instant alert/safe response display
- **Alternative Suggestions:** Safe medication recommendations
- **Approval Tokens:** Unique tokens for approved prescriptions

### 2. Patient Allergy Profile Viewer
- **Comprehensive Display:** Complete allergy history with notes
- **Risk Assessment:** Cross-reactivity analysis with risk scores
- **Visual Indicators:** Color-coded risk levels and allergy types
- **Data Transparency:** Clear presentation of underlying data

### 3. Alert Log & Audit Trail
- **Complete History:** All allergy checks with timestamps
- **Advanced Filtering:** By patient, alert type, and date ranges
- **Status Tracking:** Prescription approval/rejection status
- **Audit Compliance:** Complete transaction logging

### 4. Statistics Dashboard
- **Interactive Charts:** Plotly-powered visualizations
- **Key Metrics:** Safety rates, alert distributions, system performance
- **Real-time Data:** Live statistics from MongoDB aggregations
- **Performance Indicators:** System health and usage metrics

### 5. Medication Browser
- **Searchable Database:** Filter by drug class and name
- **Detailed Information:** Complete medication profiles
- **Alternative Mapping:** Safe substitution recommendations
- **Cross-reactivity Warnings:** Risk assessment for each medication

## Data Seeding & Test Scenarios

### Comprehensive Test Data
- **5 Patients:** Diverse demographics and allergy profiles
- **12 Allergies:** Covering drugs, foods, environmental factors
- **16 Medications:** Across 6 major drug classes
- **13 Cross-reactivity Rules:** Varied risk scores (0.25-0.95)
- **8 Drug Class Mappings:** Broad allergy category coverage
- **15 Alternative Medications:** Safe substitution options

### Test Case Coverage
```python
# Exact Match Scenarios
patient_1 + amoxicillin → EXACT_MATCH (Penicillin allergy)

# Class Match Scenarios  
patient_2 + ibuprofen → CLASS_MATCH (NSAID allergy)

# Cross-Reactivity Scenarios
patient_1 + cephalexin → CROSS_REACTIVITY (Penicillin→Cephalosporin, risk: 0.80)

# Safe Scenarios
patient_1 + azithromycin → SAFE (No conflicts detected)
```

## Performance Optimizations

### Database Performance
- **Connection Pooling:** Efficient MongoDB connection management
- **Strategic Indexing:** Optimized for frequent query patterns
- **Aggregation Optimization:** Efficient pipeline operations
- **Document Structure:** Denormalized where appropriate for read performance

### Application Performance
- **Async Processing:** Non-blocking API operations
- **Caching Strategy:** Session state management in Streamlit
- **Lazy Loading:** On-demand data fetching
- **Error Handling:** Graceful degradation and user feedback

## Security & Validation

### Data Validation
- **Pydantic Models:** Type-safe data validation
- **Input Sanitization:** Protection against injection attacks
- **Schema Validation:** Consistent data structure enforcement
- **Error Handling:** Comprehensive exception management

### API Security
- **CORS Configuration:** Controlled cross-origin access
- **Request Validation:** Automatic request/response validation
- **Error Sanitization:** Safe error message exposure
- **Health Monitoring:** System status endpoints

## MongoDB vs SQL Comparison

### Advantages of MongoDB Approach
1. **Flexible Schema:** Easy to add new allergy types or medication properties
2. **Aggregation Power:** Complex analytical queries with aggregation pipelines
3. **Horizontal Scaling:** Better scalability for large healthcare systems
4. **JSON-Native:** Direct mapping to API responses without ORM overhead
5. **Embedded Documents:** Natural representation of nested data structures

### Query Complexity Comparison
```python
# MongoDB Aggregation (Patient Risk Profile)
pipeline = [
    {"$match": {"patient_id": patient_id}},
    {"$lookup": {"from": "allergies", "localField": "allergy_id", "foreignField": "_id", "as": "allergy"}},
    {"$lookup": {"from": "cross_reactivity_rules", "localField": "allergy_id", "foreignField": "allergen_id", "as": "risks"}},
    {"$unwind": {"path": "$risks", "preserveNullAndEmptyArrays": True}},
    {"$sort": {"risks.risk_score": -1}}
]

# Equivalent SQL would require multiple JOINs and subqueries
```

## Integration Capabilities

### Microservices Architecture
- **API-First Design:** RESTful endpoints for easy integration
- **Standardized Responses:** Consistent JSON response format
- **Health Endpoints:** Service monitoring and status checking
- **Documentation:** Auto-generated OpenAPI/Swagger documentation

### Healthcare System Integration
- **HL7 FHIR Compatibility:** Extensible for healthcare standards
- **Audit Trail:** Complete logging for regulatory compliance
- **Real-time Alerts:** Immediate notification system
- **Scalable Architecture:** Supports high-volume healthcare environments

## Future Enhancements

### Machine Learning Integration
1. **Predictive Modeling:** Risk prediction based on patient history
2. **Pattern Recognition:** Automated detection of new cross-reactivities
3. **Personalized Medicine:** Individual risk assessment algorithms
4. **Population Health:** Trend analysis across patient populations

### Advanced Features
1. **Real-time Notifications:** WebSocket-based instant alerts
2. **Mobile Application:** React Native or Flutter mobile app
3. **Voice Interface:** Integration with healthcare voice assistants
4. **Blockchain Integration:** Immutable audit trail for compliance

### Scalability Improvements
1. **Microservices Migration:** Service decomposition for better scalability
2. **Container Deployment:** Docker and Kubernetes orchestration
3. **Cloud Integration:** AWS/Azure/GCP deployment strategies
4. **Performance Monitoring:** Advanced APM and logging solutions

## Conclusion

The Python/MongoDB implementation of Module 21 demonstrates modern database management principles while providing a production-ready healthcare safety solution. The combination of FastAPI's performance, MongoDB's flexibility, and Streamlit's rapid development capabilities creates a powerful, scalable system suitable for real-world clinical decision support.

### Key Achievements
- **Modern Tech Stack:** Leveraging cutting-edge Python ecosystem
- **NoSQL Mastery:** Advanced MongoDB aggregation and indexing
- **Interactive Dashboard:** User-friendly Streamlit interface
- **Production Ready:** Comprehensive error handling and validation
- **Healthcare Focus:** Real-world clinical decision support functionality

### Learning Outcomes
- Advanced NoSQL database design and optimization
- Modern Python web development with FastAPI
- Interactive dashboard development with Streamlit
- Healthcare data management and safety systems
- API design and microservices architecture

---

**Team Members:** [To be filled by team]  
**GitHub Repository:** [To be filled with actual repository URL]  
**Submission Date:** [To be filled]  
**Project Status:** Complete and Ready for Demonstration

**Technology Demonstration:**
- MongoDB aggregation pipelines equivalent to complex SQL queries
- Real-time data visualization with Plotly
- Type-safe API development with Pydantic
- Modern Python async/await patterns
- Healthcare-grade audit and compliance features