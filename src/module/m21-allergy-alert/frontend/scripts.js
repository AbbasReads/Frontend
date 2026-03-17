// 🔴 Replace with your backend API URL
const BASE_URL = "https://your-backend-url.onrender.com";


// ================= PATIENT =================

// Save Patient
function savePatient() {
  let name = document.getElementById("pname").value.trim();
  let allergy = document.getElementById("pallergy").value.trim();

  if (name === "" || allergy === "") {
    alert("Fill all fields");
    return;
  }

  fetch(`${BASE_URL}/patients`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, allergy })
  })
  .then(res => res.json())
  .then(() => alert("Patient added"))
  .catch(() => alert("Error connecting to backend"));
}


// Load Patients
function loadPatients() {
  let table = document.getElementById("patientTable");

  fetch(`${BASE_URL}/patients`)
  .then(res => res.json())
  .then(data => {

    table.innerHTML = "";

    if(data.length === 0){
      let row = table.insertRow();
      row.insertCell(0).innerText = "No patients found";
      return;
    }

    data.forEach(p => {
      let row = table.insertRow();

      row.insertCell(0).innerText = p.name;
      row.insertCell(1).innerText = p.allergy;

      let btn = document.createElement("button");
      btn.innerText = "Check";

      btn.onclick = () => {
        localStorage.setItem("selectedAllergy", p.allergy);
        window.location.href = "medication.html";
      };

      row.insertCell(2).appendChild(btn);
    });

  })
  .catch(() => alert("Cannot load patients"));
}


// Search Patient
function searchPatient() {
  let filter = document.getElementById("search").value.toLowerCase();
  let rows = document.querySelectorAll("#patientTable tr");

  rows.forEach(r => {
    if(r.cells.length > 0){
      let name = r.cells[0].innerText.toLowerCase();
      r.style.display = name.includes(filter) ? "" : "none";
    }
  });
}


// ================= MEDICATION =================

function checkMedication() {
  let allergy = document.getElementById("allergy").value;
  let drug = document.getElementById("drug").value;

  if(allergy === "" || drug === "") {
    alert("Enter details");
    return;
  }

  fetch(`${BASE_URL}/check-medication`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ allergy, drug })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("result").innerHTML =
      `<strong>Alert:</strong> ${data.alert} <br> <strong>Alternative:</strong> ${data.alternative || "None"}`;
  })
  .catch(() => alert("Backend error"));
}


// Auto-fill allergy in medication page
window.onload = function () {
  let allergy = localStorage.getItem("selectedAllergy");
  if(document.getElementById("allergy") && allergy){
    document.getElementById("allergy").value = allergy;
  }
}


// ================= DOCTOR =================

// Add Doctor
function addDoctor() {
  let name = document.getElementById("dname").value.trim();
  let specialization = document.getElementById("dspecialization").value.trim();

  if(name === "" || specialization === "") {
    alert("Fill all fields");
    return;
  }

  fetch(`${BASE_URL}/doctors`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, specialization })
  })
  .then(res => res.json())
  .then(() => {
    alert("Doctor added");
    document.getElementById("dname").value = "";
    document.getElementById("dspecialization").value = "";
  })
  .catch(() => alert("Backend error"));
}


// Load Doctors
function loadDoctors() {
  let list = document.getElementById("doctorList");

  fetch(`${BASE_URL}/doctors`)
  .then(res => res.json())
  .then(data => {
    list.innerHTML = "";
    data.forEach(d => {
      let li = document.createElement("li");
      li.innerText = `${d.name} - ${d.specialization}`;
      list.appendChild(li);
    });
  })
  .catch(() => alert("Cannot load doctors"));
}
