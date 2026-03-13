/* Show Professional Error Toast */
function showError(message) {
  // Remove existing toast if there is one
  const existingToast = document.querySelector('.toast-error');
  if (existingToast) existingToast.remove();

  // Create new toast
  const toast = document.createElement("div");
  toast.className = "toast-error";
  toast.innerHTML = `<span>⚠️</span> <span>${message}</span>`;
  
  document.body.appendChild(toast);

  // Trigger the slide-in animation
  setTimeout(() => toast.classList.add("show"), 10);

  // Remove it automatically after 3.5 seconds
  setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 400); // Wait for slide-out animation to finish
  }, 3500);
}

/* 🛡️ NEW: Prevent math symbols (+, -, e, .) from being typed in ANY number input */
document.addEventListener("keydown", function(e) {
    if (e.target.type === "number") {
        if (["e", "E", "+", "-", "."].includes(e.key)) {
            e.preventDefault();
        }
    }
});

let pidCounter = 2;

// Run on load to set initial state
window.onload = function() {
  toggleInputs();
};

/* Handle visibility of Quantum Input AND Priority Column */
function toggleInputs() {
  const algo = document.getElementById("algorithm").value;
  
  const quantumWrapper = document.getElementById("quantum-wrapper");
  const priorityHeader = document.getElementById("priorityHeader");
  const priorityCells = document.querySelectorAll(".priority-cell");

  // Show/Hide Quantum
  if (algo === "rr" || algo === "compare") {
    quantumWrapper.style.display = "flex"; 
  } else {
    quantumWrapper.style.display = "none";
  }

  // Show/Hide Priority
  const showPriority = (algo === "priority" || algo === "compare");
  
  if (showPriority) {
      priorityHeader.classList.remove("hidden");
      priorityCells.forEach(cell => cell.classList.remove("hidden"));
  } else {
      priorityHeader.classList.add("hidden");
      priorityCells.forEach(cell => cell.classList.add("hidden"));
  }
}

/* Add new process row */
function addProcess() {
  const table = document.getElementById("processTable");
  const row = table.insertRow();
  
  const isPriorityHidden = document.getElementById("priorityHeader").classList.contains("hidden");
  const priorityClass = isPriorityHidden ? "priority-cell hidden" : "priority-cell";

  row.innerHTML = `
    <td>P${pidCounter}</td>
    <td><input type="number" value="${pidCounter-1}" min="0"></td>
    <td><input type="number" value="1" min="1"></td>
    <td class="${priorityClass}"><input type="number" value="1" min="1"></td>
    <td><button onclick="deleteRow(this)">❌</button></td>
  `;

  pidCounter++;
}

/* Delete a process row */
function deleteRow(btn) {
  const row = btn.parentElement.parentElement;
  if (row.rowIndex === 1 && document.getElementById("processTable").rows.length <= 2) {
      showError("You need at least one process!");
      return;
  }
  row.remove();
}

/* Start simulation */
function startScheduling() {
  const table = document.getElementById("processTable");
  const rows = table.querySelectorAll("tr");
  const algorithm = document.getElementById("algorithm").value;
  const quantumInput = document.getElementById("quantum").value;

  // 🛡️ GUARD RAIL 1: Empty Table
  if (rows.length <= 1) { 
      showError("Wait! Please add at least one process to the table.");
      return;
  }

  // 🛡️ GUARD RAIL 2: Time Quantum Validation
  if (algorithm === "rr" || algorithm === "compare") {
      const tq = parseInt(quantumInput);
      if (quantumInput === "" || isNaN(tq) || tq <= 0) {
          showError("Time Quantum must be 1 or greater!");
          return;
      }
  }

  const processes = [];

  // Start loop from 1 to skip header
  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].querySelectorAll("td");
    
    // Grab raw string values first to check if they are empty
    const arrivalRaw = cells[1].querySelector("input").value;
    const burstRaw = cells[2].querySelector("input").value;
    
    const priorityCell = cells[3];
    const priorityInput = priorityCell ? priorityCell.querySelector("input") : null;
    const priorityRaw = priorityInput ? priorityInput.value : "0"; 

    // 🛡️ GUARD RAIL 3: Empty Inputs in Rows
    if (arrivalRaw === "" || burstRaw === "") {
        showError(`Stop! Please fill in both Arrival & Burst Time for Row ${i}.`);
        return;
    }

    const arrival = parseInt(arrivalRaw);
    const burst = parseInt(burstRaw);
    const priority = parseInt(priorityRaw);

    // 🛡️ NEW: Catch symbols or letters that were copy-pasted
    if (isNaN(arrival) || isNaN(burst) || isNaN(priority)) {
        showError(`Invalid symbols detected! Please use only whole numbers in Row ${i}.`);
        return;
    }

    // 🛡️ GUARD RAIL 4: Negative Numbers (Time Travel)
    if (arrival < 0 || burst < 0 || priority < 0) {
        showError(`No time travel allowed! Numbers cannot be negative in Row ${i}.`);
        return;
    }

    // 🛡️ GUARD RAIL 5: Zero Burst Time
    if (burst === 0) {
        showError(`Burst time must be at least 1 ms in Row ${i}.`);
        return;
    }

    // 🛡️ GUARD RAIL 6: Prevent Browser Crash (Max Limit)
    if (burst > 99999 || arrival > 99999) {
        showError(`For browser performance, please keep Arrival and Burst times under 99999 (Row ${i}).`);
        return;
    }

    processes.push({
        pid: i, 
        arrival_time: arrival,
        burst_time: burst,
        priority: priority
    });
  }

  let quantum = parseInt(quantumInput);
  if (isNaN(quantum) || quantum < 1) quantum = 2;

  localStorage.setItem("processes", JSON.stringify(processes));
  localStorage.setItem("algorithm", algorithm);
  localStorage.setItem("quantum", quantum);

  window.location.href = "loading.html";
}