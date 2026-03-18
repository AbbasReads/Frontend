# 🧪 M21 Allergy Alert System - Testing Guide

## 🚀 Quick Health Check (2 minutes)

### 1. Initial Connection Test
- **✅ Check**: Sidebar shows "✅ Database Connected"
- **❌ If not**: Check MongoDB connection string in Streamlit secrets

### 2. Navigation Test
- **✅ Check**: All 5 pages load without errors:
  - 💊 Prescription Validator
  - 👤 Patient Allergies  
  - 📋 Alert Log
  - 📊 Statistics
  - 💊 Medications

## 🎯 Comprehensive Functionality Testing

### Test 1: Database Auto-Initialization
**Expected**: System should auto-create collections with test data

**Steps**:
1. Go to **📊 Statistics** page
2. **✅ Verify**: Shows these metrics:
   - **👥 Total Patients**: 5
   - **💊 Total Medications**: 16
   - **📋 Total Prescriptions**: 8
   - **⚠️ High Risk Rules**: Should show a number > 0

**❌ If failed**: Database didn't initialize - check MongoDB Atlas connection

---

### Test 2: Patient Data Verification
**Expected**: 5 test patients with varied profiles

**Steps**:
1. Go to **👤 Patient Allergies** page
2. **✅ Verify**: Dropdown shows 5 patients:
   - Arjun Sharma (Age: 33, M)
   - Priya Singh (Age: 40, F)
   - Rahul Verma (Age: 25, M)
   - Anita Gupta (Age: 47, F)
   - Vikram Patel (Age: 30, M)

3. **Select**: "Arjun Sharma"
4. **✅ Verify**: Shows allergies:
   - 🚨 Penicillin (Drug)
   - 🚨 Peanuts (Food)

---

### Test 3: Allergy Alert System (Critical Test)

#### Test 3A: EXACT MATCH Alert
**Expected**: Direct allergy match triggers alert

**Steps**:
1. Go to **💊 Prescription Validator**
2. **Select Patient**: "Arjun Sharma (Age: 33, M)"
3. **Select Medication**: "Amoxicillin (Penicillin)" or "Penicillin V (Penicillin)"
4. **Enter**: Dose: "500mg", Frequency: "Twice daily"
5. **Click**: "🔍 Check & Submit Prescription"

**✅ Expected Result**: 
- **Red Alert Box**: "⚠️ ALLERGY ALERT"
- **Alert Type**: "EXACT_MATCH"
- **Message**: Contains "directly allergic" or "exact match"
- **Alternatives**: Shows safe medication options

#### Test 3B: CLASS MATCH Alert
**Expected**: Drug class allergy triggers alert

**Steps**:
1. **Select Patient**: "Priya Singh (Age: 40, F)" (allergic to NSAIDs)
2. **Select Medication**: "Ibuprofen (NSAID)" or "Aspirin (NSAID)"
3. **Enter**: Dose: "400mg", Frequency: "Every 8 hours"
4. **Click**: "🔍 Check & Submit Prescription"

**✅ Expected Result**:
- **Red Alert Box**: "⚠️ ALLERGY ALERT"
- **Alert Type**: "CLASS_MATCH"
- **Message**: Contains "drug class" or "class match"

#### Test 3C: CROSS-REACTIVITY Alert
**Expected**: High cross-reactivity risk triggers alert

**Steps**:
1. **Select Patient**: "Arjun Sharma (Age: 33, M)" (allergic to Penicillin)
2. **Select Medication**: "Cephalexin (Cephalosporin)" (cross-reacts with Penicillin)
3. **Enter**: Dose: "250mg", Frequency: "Four times daily"
4. **Click**: "🔍 Check & Submit Prescription"

**✅ Expected Result**:
- **Red Alert Box**: "⚠️ ALLERGY ALERT"
- **Alert Type**: "CROSS_REACTIVITY"
- **Message**: Contains "cross-reactivity" or "cross-reactive"

#### Test 3D: SAFE Prescription
**Expected**: No allergies = safe approval

**Steps**:
1. **Select Patient**: "Arjun Sharma (Age: 33, M)"
2. **Select Medication**: "Azithromycin (Macrolide)" (safe alternative)
3. **Enter**: Dose: "500mg", Frequency: "Once daily"
4. **Click**: "🔍 Check & Submit Prescription"

**✅ Expected Result**:
- **Green Success Box**: "✅ PRESCRIPTION APPROVED"
- **Status**: "SAFE"
- **Message**: Contains "no allergy conflicts" or "safe"
- **Approval Token**: Shows a generated token

---

### Test 4: Alert Logging System
**Expected**: All checks are logged for audit trail

**Steps**:
1. After running Tests 3A-3D above
2. Go to **📋 Alert Log** page
3. **✅ Verify**: Shows recent alerts with:
   - Patient names
   - Medication names
   - Alert types (EXACT_MATCH, CLASS_MATCH, CROSS_REACTIVITY, SAFE)
   - Timestamps
   - Alert messages

4. **Test Filtering**:
   - Filter by Alert Type: "EXACT_MATCH"
   - Filter by Patient: "Arjun Sharma"
   - **✅ Verify**: Filters work correctly

---

### Test 5: Statistics Dashboard
**Expected**: Real-time analytics and charts

**Steps**:
1. Go to **📊 Statistics** page
2. **✅ Verify Charts Display**:
   - **Alert Type Distribution**: Bar chart showing alert counts
   - **Alert Breakdown**: Metrics for each alert type
   - **Prescription Status**: Approved/Rejected/Pending counts

3. **✅ Verify KPIs**:
   - **Safety Rate**: Should show percentage
   - **Alert Rate**: Should show percentage  
   - **Total Checks**: Should match number of tests run

---

### Test 6: Medication Browser
**Expected**: Complete drug database with alternatives

**Steps**:
1. Go to **💊 Medications** page
2. **✅ Verify**: Shows medication list with drug classes
3. **Click**: Any medication (e.g., "Amoxicillin (Penicillin)")
4. **✅ Verify**: Shows:
   - Medication details
   - Safe alternatives (if available)
   - Cross-reactivity warnings (if any)

5. **Test Drug Class Filter**:
   - Select "Penicillin" from dropdown
   - **✅ Verify**: Only shows Penicillin medications

---

## 🔍 Advanced Testing Scenarios

### Scenario A: High-Risk Patient
**Patient**: Rahul Verma (allergic to Sulfonamides + Ibuprofen)

**Test Cases**:
1. **Sulfonamide Drug**: "Trimethoprim-Sulfamethoxazole" → Should trigger EXACT_MATCH
2. **NSAID Drug**: "Naproxen" → Should trigger CLASS_MATCH  
3. **Safe Drug**: "Acetaminophen" → Should be SAFE

### Scenario B: Multiple Allergy Patient
**Patient**: Anita Gupta (allergic to Cephalosporins + Latex)

**Test Cases**:
1. **Cephalosporin**: "Cefuroxime" → Should trigger CLASS_MATCH
2. **Safe Alternative**: "Ciprofloxacin" → Should be SAFE

### Scenario C: Cross-Reactivity Testing
**Patient**: Vikram Patel (allergic to Codeine)

**Test Cases**:
1. **Related Opioid**: "Morphine" → May trigger CROSS_REACTIVITY
2. **Non-Opioid**: "Acetaminophen" → Should be SAFE

---

## 🚨 Error Testing

### Test Database Connection Issues
1. **Temporarily break connection**: Change one character in MongoDB URL in secrets
2. **Expected**: Sidebar shows "❌ Database Disconnected"
3. **Fix**: Restore correct connection string
4. **Expected**: Sidebar shows "✅ Database Connected"

### Test Invalid Inputs
1. **Empty Fields**: Try submitting prescription with missing fields
2. **Expected**: Error message asking to fill required fields

---

## 📊 Performance Testing

### Load Testing
1. **Rapid Clicks**: Submit multiple prescriptions quickly
2. **Expected**: System handles requests without crashing
3. **Page Switching**: Rapidly switch between all 5 pages
4. **Expected**: Smooth navigation, no errors

### Data Consistency
1. **Submit Prescription**: Create a new prescription
2. **Check Alert Log**: Verify it appears immediately
3. **Check Statistics**: Verify counts update
4. **Expected**: Real-time data consistency

---

## ✅ Success Criteria

Your M21 system is working perfectly if:

### Core Functionality ✅
- [x] All 5 pages load without errors
- [x] Database shows "Connected" status
- [x] 5 test patients load correctly
- [x] 16 medications display properly

### Allergy Detection ✅
- [x] EXACT_MATCH alerts trigger correctly
- [x] CLASS_MATCH alerts work for drug classes
- [x] CROSS_REACTIVITY alerts show for high-risk combinations
- [x] SAFE prescriptions get approved with tokens

### Data Management ✅
- [x] All alerts logged to audit trail
- [x] Statistics update in real-time
- [x] Filtering and search work properly
- [x] Alternative medications suggested

### User Experience ✅
- [x] Professional UI with clear alerts
- [x] Responsive design works on mobile
- [x] Fast loading times
- [x] Intuitive navigation

---

## 🎯 Quick Test Checklist (5 minutes)

1. **✅ Connection**: Sidebar shows "Database Connected"
2. **✅ Data**: Statistics show 5 patients, 16 medications
3. **✅ Alert**: Test one EXACT_MATCH (Arjun + Amoxicillin)
4. **✅ Safe**: Test one SAFE prescription (Arjun + Azithromycin)  
5. **✅ Log**: Check Alert Log shows both tests
6. **✅ Charts**: Statistics page shows updated charts

If all 6 items pass → **🎉 Your M21 system is fully functional!**

---

## 🆘 Troubleshooting

**Problem**: No data showing
**Solution**: Check MongoDB Atlas network access allows 0.0.0.0/0

**Problem**: Alerts not triggering  
**Solution**: Verify test data loaded correctly in Statistics page

**Problem**: Charts not displaying
**Solution**: Check browser console for JavaScript errors

**Problem**: Slow performance
**Solution**: Check MongoDB Atlas cluster status and connection

Your M21 Allergy Alert System is now ready for production use! 🚀