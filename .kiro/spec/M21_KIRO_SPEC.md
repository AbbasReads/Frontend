# Module 21: Allergy-Aware Medication Alert System
## Kiro Project Specification

**Course:** Database Management Systems (DBMS) — IIT(ISM) Dhanbad  
**Project:** AI-Based Clinical Decision Support System  
**Module Number:** M21  
**Category:** D — Drug & Prescription Safety Systems  
**Academic Year:** 2025–2026, Winter Semester  

---

## 1. Project Overview

Module 21 is a **standalone self-contained module** that implements an Allergy-Aware Medication Alert System. It checks whether a prescribed drug is safe for a patient based on their allergy profile, using a three-level cascade check (Exact Match → Drug Class Match → Cross-Reactivity). The system outputs either an **ALERT** (with safe alternative suggestions) or a **SAFE** token.

> **Dependency Note:** Modules M5 (Allergy Tracking) and M20 (Prescription Validation) are listed as upstream dependencies in the architecture, but since those modules are not available, M21 must be **fully self-contained**. All data for patients, allergies, medications, and prescriptions must be seeded internally within M21's own database. No external API calls to other modules are required — M21 simulates the data it would normally receive.

---

## 2. Core Functional Requirements

### 2.1 What the System Does

When a new prescription is submitted for a patient:

1. **Parse** the drug name and patient ID from the request.
2. **Fetch** the patient's allergy profile from the local database.
3. **Check 1 — Exact Match:** Is the prescribed drug exactly in the patient's allergy list?
4. **Check 2 — Drug Class Match:** Does the prescribed drug belong to a drug class the patient is allergic to?
5. **Check 3 — Cross-Reactivity:** Does the prescribed drug have known cross-reactivity with any allergen in the patient's profile, above a risk threshold?
6. If any check triggers → Generate **ALERT**, log the incident, find safe alternatives.
7. If all checks pass → Generate **SAFE** token, log the validation, return approval JSON.
8. Output flows downstream to M22 (Polypharmacy Risk), M23 (High-Risk Drug Monitor), and the Frontend Dashboard.

### 2.2 Downstream Outputs (simulate these as API response payloads)
- `POST /api/m21/validate` → returns Warning JSON or Approval JSON
- Data fields needed by M22/M23: `patient_id`, `drug_id`, `alert_type`, `risk_level`, `alternatives[]`

---

## 3. Database Schema (M21 owns all these tables)

### 3.1 Tables to Create

#### `patients`
| Column | Type | Constraints |
|--------|------|-------------|
| patient_id | INT | PRIMARY KEY, AUTO_INCREMENT |
| name | VARCHAR(100) | NOT NULL |
| dob | DATE | NOT NULL |
| sex | ENUM('M','F','Other') | NOT NULL |

#### `allergies`
| Column | Type | Constraints |
|--------|------|-------------|
| allergy_id | INT | PRIMARY KEY, AUTO_INCREMENT |
| allergy_name | VARCHAR(100) | NOT NULL UNIQUE |
| allergy_type | ENUM('Drug','Food','Environmental','Latex') | NOT NULL |

#### `patient_allergies` *(junction table — simulates M5 data)*
| Column | Type | Constraints |
|--------|------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| patient_id | INT | FK → patients |
| allergy_id | INT | FK → allergies |
| date_recorded | DATE | NOT NULL |
| notes | TEXT | |

#### `medications`
| Column | Type | Constraints |
|--------|------|-------------|
| med_id | INT | PRIMARY KEY, AUTO_INCREMENT |
| med_name | VARCHAR(100) | NOT NULL UNIQUE |
| drug_class | VARCHAR(100) | NOT NULL |
| active_ingredients | TEXT | NOT NULL |

#### `cross_reactivity_rules`
| Column | Type | Constraints |
|--------|------|-------------|
| rule_id | INT | PRIMARY KEY, AUTO_INCREMENT |
| allergen_id | INT | FK → allergies |
| reactive_med_id | INT | FK → medications |
| risk_level | ENUM('Low','Medium','High','Critical') | NOT NULL |
| risk_score | DECIMAL(3,2) | NOT NULL (0.00–1.00) |

#### `drug_class_allergies` *(maps drug class names to allergy entries)*
| Column | Type | Constraints |
|--------|------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| drug_class | VARCHAR(100) | NOT NULL |
| allergy_id | INT | FK → allergies |

#### `alternatives`
| Column | Type | Constraints |
|--------|------|-------------|
| alt_id | INT | PRIMARY KEY, AUTO_INCREMENT |
| original_med_id | INT | FK → medications |
| alternative_med_id | INT | FK → medications |
| reason | TEXT | |

#### `prescriptions` *(simulates M20 data)*
| Column | Type | Constraints |
|--------|------|-------------|
| prescription_id | INT | PRIMARY KEY, AUTO_INCREMENT |
| patient_id | INT | FK → patients |
| med_id | INT | FK → medications |
| dose | VARCHAR(50) | NOT NULL |
| frequency | VARCHAR(50) | NOT NULL |
| start_date | DATE | NOT NULL |
| status | ENUM('Pending','Approved','Rejected') | DEFAULT 'Pending' |

#### `alert_log`
| Column | Type | Constraints |
|--------|------|-------------|
| log_id | INT | PRIMARY KEY, AUTO_INCREMENT |
| prescription_id | INT | FK → prescriptions |
| patient_id | INT | NOT NULL |
| med_id | INT | NOT NULL |
| alert_type | ENUM('EXACT_MATCH','CLASS_MATCH','CROSS_REACTIVITY','SAFE') | NOT NULL |
| alert_message | TEXT | |
| logged_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

---

## 4. SQL Requirements

### 4.1 Core Queries (must implement all)

**Q1 — Fetch patient allergy profile:**
```sql
SELECT a.allergy_id, a.allergy_name, a.allergy_type, pa.notes
FROM patient_allergies pa
JOIN allergies a ON pa.allergy_id = a.allergy_id
WHERE pa.patient_id = ?;
```

**Q2 — Check 1: Exact drug-to-allergy match:**
```sql
SELECT COUNT(*) AS exact_match
FROM patient_allergies pa
JOIN allergies a ON pa.allergy_id = a.allergy_id
JOIN medications m ON LOWER(m.med_name) = LOWER(a.allergy_name)
WHERE pa.patient_id = ? AND m.med_id = ?;
```

**Q3 — Check 2: Drug class match:**
```sql
SELECT COUNT(*) AS class_match
FROM patient_allergies pa
JOIN drug_class_allergies dca ON pa.allergy_id = dca.allergy_id
JOIN medications m ON LOWER(m.drug_class) = LOWER(dca.drug_class)
WHERE pa.patient_id = ? AND m.med_id = ?;
```

**Q4 — Check 3: Cross-reactivity above threshold (threshold = 0.5):**
```sql
SELECT cr.risk_level, cr.risk_score, m.med_name
FROM cross_reactivity_rules cr
JOIN patient_allergies pa ON cr.allergen_id = pa.allergy_id
JOIN medications m ON cr.reactive_med_id = m.med_id
WHERE pa.patient_id = ? AND cr.reactive_med_id = ? AND cr.risk_score > 0.5;
```

**Q5 — Fetch safe alternatives:**
```sql
SELECT alt.med_name, alt.drug_class, a.reason
FROM alternatives a
JOIN medications alt ON a.alternative_med_id = alt.med_id
WHERE a.original_med_id = ?;
```

**Q6 — All alerts for a patient (audit view):**
```sql
SELECT al.log_id, al.alert_type, m.med_name, al.alert_message, al.logged_at
FROM alert_log al
JOIN medications m ON al.med_id = m.med_id
WHERE al.patient_id = ?
ORDER BY al.logged_at DESC;
```

**Q7 — Allergy-risk summary view (SQL VIEW):**
```sql
CREATE VIEW v_patient_allergy_risk AS
SELECT 
    p.patient_id,
    p.name AS patient_name,
    a.allergy_name,
    a.allergy_type,
    cr.risk_level,
    m.med_name AS reactive_drug
FROM patients p
JOIN patient_allergies pa ON p.patient_id = pa.patient_id
JOIN allergies a ON pa.allergy_id = a.allergy_id
LEFT JOIN cross_reactivity_rules cr ON cr.allergen_id = a.allergy_id
LEFT JOIN medications m ON cr.reactive_med_id = m.med_id;
```

**Q8 — Count of alerts by type (statistics query):**
```sql
SELECT alert_type, COUNT(*) AS total
FROM alert_log
GROUP BY alert_type;
```

### 4.2 Trigger (mandatory)

**Trigger: Auto-update prescription status after alert log insert**
```sql
DELIMITER //
CREATE TRIGGER trg_update_prescription_status
AFTER INSERT ON alert_log
FOR EACH ROW
BEGIN
    IF NEW.alert_type IN ('EXACT_MATCH', 'CLASS_MATCH', 'CROSS_REACTIVITY') THEN
        UPDATE prescriptions
        SET status = 'Rejected'
        WHERE prescription_id = NEW.prescription_id;
    ELSEIF NEW.alert_type = 'SAFE' THEN
        UPDATE prescriptions
        SET status = 'Approved'
        WHERE prescription_id = NEW.prescription_id;
    END IF;
END //
DELIMITER ;
```

### 4.3 Stored Procedure (mandatory)

**Procedure: Full allergy check — runs all 3 checks, logs result, returns decision**
```sql
DELIMITER //
CREATE PROCEDURE sp_check_allergy_alert(
    IN p_patient_id INT,
    IN p_med_id INT,
    IN p_prescription_id INT,
    OUT p_result VARCHAR(20),
    OUT p_message TEXT
)
BEGIN
    DECLARE v_exact INT DEFAULT 0;
    DECLARE v_class INT DEFAULT 0;
    DECLARE v_cross INT DEFAULT 0;

    -- Check 1: Exact match
    SELECT COUNT(*) INTO v_exact
    FROM patient_allergies pa
    JOIN allergies a ON pa.allergy_id = a.allergy_id
    JOIN medications m ON LOWER(m.med_name) = LOWER(a.allergy_name)
    WHERE pa.patient_id = p_patient_id AND m.med_id = p_med_id;

    IF v_exact > 0 THEN
        SET p_result = 'ALERT';
        SET p_message = 'EXACT MATCH: Patient is directly allergic to this drug.';
        INSERT INTO alert_log(prescription_id, patient_id, med_id, alert_type, alert_message)
        VALUES(p_prescription_id, p_patient_id, p_med_id, 'EXACT_MATCH', p_message);
        LEAVE sp_check_allergy_alert;
    END IF;

    -- Check 2: Class match
    SELECT COUNT(*) INTO v_class
    FROM patient_allergies pa
    JOIN drug_class_allergies dca ON pa.allergy_id = dca.allergy_id
    JOIN medications m ON LOWER(m.drug_class) = LOWER(dca.drug_class)
    WHERE pa.patient_id = p_patient_id AND m.med_id = p_med_id;

    IF v_class > 0 THEN
        SET p_result = 'ALERT';
        SET p_message = 'CLASS MATCH: Drug belongs to an allergenic drug class for this patient.';
        INSERT INTO alert_log(prescription_id, patient_id, med_id, alert_type, alert_message)
        VALUES(p_prescription_id, p_patient_id, p_med_id, 'CLASS_MATCH', p_message);
        LEAVE sp_check_allergy_alert;
    END IF;

    -- Check 3: Cross-reactivity (threshold 0.5)
    SELECT COUNT(*) INTO v_cross
    FROM cross_reactivity_rules cr
    JOIN patient_allergies pa ON cr.allergen_id = pa.allergy_id
    WHERE pa.patient_id = p_patient_id AND cr.reactive_med_id = p_med_id AND cr.risk_score > 0.5;

    IF v_cross > 0 THEN
        SET p_result = 'ALERT';
        SET p_message = 'CROSS-REACTIVITY: High cross-reactivity risk detected.';
        INSERT INTO alert_log(prescription_id, patient_id, med_id, alert_type, alert_message)
        VALUES(p_prescription_id, p_patient_id, p_med_id, 'CROSS_REACTIVITY', p_message);
        LEAVE sp_check_allergy_alert;
    END IF;

    -- All checks passed
    SET p_result = 'SAFE';
    SET p_message = 'No allergy conflicts detected. Drug is safe for this patient.';
    INSERT INTO alert_log(prescription_id, patient_id, med_id, alert_type, alert_message)
    VALUES(p_prescription_id, p_patient_id, p_med_id, 'SAFE', p_message);

END //
DELIMITER ;
```

---

## 5. Backend API Specification

**Technology:** Node.js (Express) or Python (Flask) — team's choice.  
**Database:** MySQL or PostgreSQL.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/m21/validate` | Run full allergy check for a prescription |
| GET | `/api/m21/patient/:id/allergies` | Get patient's allergy profile |
| GET | `/api/m21/patient/:id/alerts` | Get all past alerts for a patient |
| GET | `/api/m21/drug/:id/alternatives` | Get safe alternatives for a drug |
| GET | `/api/m21/stats` | Get alert type statistics |
| GET | `/api/m21/patients` | List all patients |
| GET | `/api/m21/medications` | List all medications |

### POST `/api/m21/validate` — Request & Response

**Request Body:**
```json
{
  "patient_id": 3,
  "med_id": 7,
  "dose": "500mg",
  "frequency": "Twice daily",
  "start_date": "2026-03-20"
}
```

**Response (ALERT):**
```json
{
  "status": "ALERT",
  "alert_type": "EXACT_MATCH",
  "message": "EXACT MATCH: Patient is directly allergic to this drug.",
  "alternatives": [
    { "med_name": "Azithromycin", "drug_class": "Macrolide" }
  ],
  "prescription_id": 12,
  "logged_at": "2026-03-20T10:32:00Z"
}
```

**Response (SAFE):**
```json
{
  "status": "SAFE",
  "message": "No allergy conflicts detected. Drug is safe for this patient.",
  "prescription_id": 13,
  "approval_token": "SAFE-20260320-PT3-MD7",
  "logged_at": "2026-03-20T10:35:00Z"
}
```

---

## 6. Frontend Dashboard

**Technology:** React.js (preferred) or plain HTML/CSS/JS.

### Pages / Sections Required

1. **Prescription Validator Form**  
   - Dropdowns: Select Patient, Select Drug  
   - Fields: Dose, Frequency, Start Date  
   - Button: "Check & Submit"  
   - Result panel: Shows ALERT (red) or SAFE (green) with message and alternatives

2. **Patient Allergy Profile Viewer**  
   - Select a patient → see allergy table (allergy name, type, notes)

3. **Alert Log Table**  
   - Columns: Log ID, Patient, Drug, Alert Type, Message, Timestamp  
   - Filter by alert type

4. **Statistics Panel**  
   - Bar/pie chart showing count of EXACT_MATCH / CLASS_MATCH / CROSS_REACTIVITY / SAFE

5. **Medication & Alternatives Browser**  
   - Select drug → see its drug class, active ingredients, list of safe alternatives

### UI Requirements per Project Spec
The Module Dashboard must visually show:
- Database **tables** (rendered in the UI)
- **SQL queries** used (display raw SQL alongside results)
- **Trigger/Procedure** demonstration (show before/after trigger fire)
- **Output results** clearly labeled

---

## 7. Seed Data

Provide at minimum:
- **5 patients** with varied demographics
- **10 allergies** (mix of drug and food types)
- **15 medications** across at least 5 drug classes (e.g., Penicillins, Cephalosporins, NSAIDs, Macrolides, Sulfonamides)
- **8+ cross-reactivity rules** with varied risk scores
- **6+ drug class allergy mappings**
- **10+ alternative medication mappings**
- **Prescriptions** that trigger all three alert types plus safe cases

### Sample Seed (illustrative)

```sql
-- Patients
INSERT INTO patients VALUES (1,'Arjun Sharma','1990-05-10','M');
INSERT INTO patients VALUES (2,'Priya Singh','1985-11-22','F');
INSERT INTO patients VALUES (3,'Rahul Verma','2001-03-15','M');

-- Allergies  
INSERT INTO allergies VALUES (1,'Penicillin','Drug');
INSERT INTO allergies VALUES (2,'Amoxicillin','Drug');
INSERT INTO allergies VALUES (3,'Aspirin','Drug');
INSERT INTO allergies VALUES (4,'Sulfonamides','Drug');
INSERT INTO allergies VALUES (5,'Peanuts','Food');

-- Medications
INSERT INTO medications VALUES (1,'Amoxicillin','Penicillin','Amoxicillin trihydrate');
INSERT INTO medications VALUES (2,'Cephalexin','Cephalosporin','Cephalexin monohydrate');
INSERT INTO medications VALUES (3,'Ibuprofen','NSAID','Ibuprofen');
INSERT INTO medications VALUES (4,'Azithromycin','Macrolide','Azithromycin dihydrate');
INSERT INTO medications VALUES (5,'Trimethoprim-Sulfamethoxazole','Sulfonamide','Sulfamethoxazole, Trimethoprim');

-- Cross-reactivity rules
INSERT INTO cross_reactivity_rules VALUES (1,1,2,'High',0.80);   -- Penicillin allergy → Cephalexin risky
INSERT INTO cross_reactivity_rules VALUES (2,3,3,'Medium',0.60); -- Aspirin allergy → Ibuprofen risky

-- Patient allergies
INSERT INTO patient_allergies VALUES (1,1,1,'2023-01-10','Rash observed');
INSERT INTO patient_allergies VALUES (2,2,3,'2022-06-05','GI distress');
INSERT INTO patient_allergies VALUES (3,3,4,'2024-02-20','Anaphylaxis history');
```

---

## 8. File/Folder Structure

```
m21-allergy-alert/
│
├── backend/
│   ├── db/
│   │   ├── schema.sql          # DDL: CREATE TABLE statements
│   │   ├── seed.sql            # DML: INSERT seed data
│   │   ├── views.sql           # SQL VIEWs
│   │   ├── triggers.sql        # Triggers
│   │   └── procedures.sql      # Stored procedures
│   ├── routes/
│   │   ├── validate.js         # POST /api/m21/validate
│   │   ├── patients.js
│   │   ├── medications.js
│   │   └── alerts.js
│   ├── db.js                   # DB connection config
│   ├── app.js                  # Express app entry
│   └── package.json
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ValidatorForm.jsx
│   │   │   ├── AllergyProfile.jsx
│   │   │   ├── AlertLog.jsx
│   │   │   ├── StatsPanel.jsx
│   │   │   └── MedicationBrowser.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
├── docs/
│   ├── ER_DIAGRAM.png          # Your hand-drawn ER (already done)
│   └── REPORT.md
│
└── README.md
```

---

## 9. GitHub / Submission Checklist

Per Prof. ACS Rao's submission requirements:

- [ ] ER Diagram included (you already have the hand-drawn one; digitize it)
- [ ] Normalized Database Schema (DDL in `schema.sql`)
- [ ] SQL Scripts: DDL + DML + Constraints
- [ ] At least 8 meaningful SQL queries with outputs shown in UI
- [ ] At least 1 Trigger implemented and demonstrated
- [ ] At least 1 Stored Procedure implemented and demonstrated
- [ ] 1 SQL View created
- [ ] All 3 team members have meaningful commits
- [ ] Branch named `module/allergy-aware-medication-alert`
- [ ] PR description includes: module name, team member names + GitHub IDs, features list, individual contribution summary

---

## 10. Integration Contract (for M22 and M23)

Even though M22/M23 may call M21's API, expose the following on your backend so they can consume it:

```
GET /api/m21/patient/:id/latest-alert
```

**Response:**
```json
{
  "patient_id": 3,
  "last_checked_drug": "Amoxicillin",
  "alert_type": "EXACT_MATCH",
  "risk_level": "High",
  "alternatives": ["Azithromycin", "Clarithromycin"],
  "checked_at": "2026-03-20T10:32:00Z"
}
```

---

## 11. Normalization Notes

The schema is designed to be in **Third Normal Form (3NF)**:

- `patients` — no transitive dependencies; all attributes depend only on `patient_id`
- `patient_allergies` — junction table resolving the M:N between patients and allergies
- `cross_reactivity_rules` — risk data depends on (allergen_id, reactive_med_id) composite, not on individual keys alone → separate table is correct
- `alternatives` — maps med-to-med; reason is a property of the relationship, not of either medication alone
- No data duplication: drug class is stored only in `medications`, allergy names only in `allergies`

---

## 12. Viva Preparation Points

Be ready to explain:

1. Why is the allergy check done in 3 cascading levels rather than one query?
2. What is the purpose of the `cross_reactivity_rules` table and the `risk_score` threshold?
3. Why does the trigger fire on `alert_log` insert instead of directly on `prescriptions`?
4. How would you extend this to handle multiple concurrent prescriptions for the same patient?
5. What normal form is the schema in, and why?
6. How does the `v_patient_allergy_risk` VIEW help the frontend dashboard?
7. What is the isolation principle, and how does M21 respect it?

---

*End of Specification — Module 21: Allergy-Aware Medication Alert System*
