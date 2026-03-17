// ⚠️ IMPORTANT: Replace with your backend URL (NOT localhost)
const BASE_URL = "https://your-backend-url.onrender.com";


// ✅ Save Patient (POST)
function savePatient() {

  let name = document.getElementById("pname").value.trim();
  let allergy = document.getElementById("pallergy").value.trim();

  if (name === "" || allergy === "") {
    alert("Fill all fields");
    return;
  }

  fetch(`${BASE_URL}/patients`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ name, allergy })
  })
  .then(res => {
    if (!res.ok) throw new Error("Server error");
    return res.json();
  })
  .then(() => {
    alert("✅ Patient saved");
    document.getElementById("pname").value = "";
    document.getElementById("pallergy").value = "";
  })
  .catch(err => {
    console.error(err);
    alert("❌ Cannot connect to backend");
  });
}


// ✅ Load Patients (GET)
function loadPatients() {

  let table = document.getElementById("patientTable");

  fetch(`${BASE_URL}/patients`)
  .then(res => {
    if (!res.ok) throw new Error("Fetch failed");
    return res.json();
  })
  .then(patients => {

    table.innerHTML = "";

    if (patients.length === 0) {
      let row = table.insertRow();
      row.insertCell(0).innerText = "No patients found";
      return;
    }

    patients.forEach(p => {

      let row = table.insertRow();

      row.insertCell(0).innerText = p.name;
      row.insertCell(1).innerText = p.allergy;

      let btn = document.createElement("button");
      btn.innerText = "Check";

      btn.onclick = function () {
        localStorage.setItem("selectedAllergy", p.allergy);
        window.location.href = "medication.html";
      };

      row.insertCell(2).appendChild(btn);

    });

  })
  .catch(err => {
    console.error(err);
    alert("❌ Cannot load patients");
  });
}


// ✅ Search Patient (Frontend)
function searchPatient() {

  let filter = document.getElementById("search").value.toLowerCase();
  let rows = document.querySelectorAll("#patientTable tr");

  rows.forEach(r => {

    if (r.cells.length > 0) {
      let name = r.cells[0].innerText.toLowerCase();

      r.style.display = name.includes(filter) ? "" : "none";
    }

  });
}


// ✅ Medication Check (POST)
function checkMedication() {

  let allergy = document.getElementById("allergy").value.trim();
  let drug = document.getElementById("drug").value.trim();

  if (allergy === "" || drug === "") {
    alert("Enter details");
    return;
  }

  fetch(`${BASE_URL}/check-medication`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ allergy, drug })
  })
  .then(res => {
    if (!res.ok) throw new Error("Server error");
    return res.json();
  })
  .then(data => {

    document.getElementById("result").innerHTML = `
      <p><strong>Alert:</strong> ${data.alert}</p>
      <p><strong>Alternative:</strong> ${data.alternative || "None"}</p>
    `;

  })
  .catch(err => {
    console.error(err);
    alert("❌ Backend error");
  });
}


// ✅ Auto-fill Allergy from Dashboard
window.onload = function () {

  let allergy = localStorage.getItem("selectedAllergy");

  if (document.getElementById("allergy") && allergy) {
    document.getElementById("allergy").value = allergy;
  }

};
