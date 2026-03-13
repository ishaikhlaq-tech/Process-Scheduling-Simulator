const data = JSON.parse(localStorage.getItem("results"));
const container = document.getElementById("results");

if (!data || !data.results) {
  alert("No results found. Run simulation again.");
  window.location.href = "index.html";
}

// ------------------------------------
// NORMALIZE RESULTS TO ARRAY
// ------------------------------------
// If results is an object (compare mode), convert to array
let resultsArray = [];

if (Array.isArray(data.results)) {
  // Single mode
  resultsArray = data.results;
} else {
  // Compare mode: object -> array
  resultsArray = Object.keys(data.results).map(key => {
    const obj = data.results[key];
    return {
      algorithm: key,
      ...obj
    };
  });
}

// ------------------------------------
// FIND MAX EFFICIENCY
// ------------------------------------
// Safely handle 0 wait time to prevent Infinity issues
const maxEfficiency = Math.max(
  ...resultsArray.map(r => r.average_waiting_time === 0 ? 1 : (1 / r.average_waiting_time))
);

// ------------------------------------
// RENDER EACH ALGORITHM
// ------------------------------------
resultsArray.forEach(r => {
  const div = document.createElement("div");
  div.className = "algorithm";

  if (r.algorithm === data.best_algorithm) div.classList.add("best");
  if (r.algorithm === data.worst_algorithm) div.classList.add("worst");

  div.innerHTML = `
    <h2>${r.algorithm}</h2>
    <p>Avg Waiting: ${r.average_waiting_time.toFixed(2)}</p>
    <p>Avg Turnaround: ${r.average_turnaround_time.toFixed(2)}</p>
  `;

  // -----------------------------
  // GANTT CHART
  // -----------------------------
  const gantt = document.createElement("div");
  gantt.className = "gantt";

  // Support both key names safely
  const ganttData = r.gantt || r.gantt_chart || [];

  if (ganttData.length === 0) {
    const msg = document.createElement("p");
    msg.innerText = "No Gantt data";
    gantt.appendChild(msg);
  } else {
    // 🛡️ BROWSER CRASH PROTECTION: Max 60 blocks per algorithm
    const MAX_BLOCKS = 60;
    const blocksToDraw = ganttData.length > MAX_BLOCKS ? ganttData.slice(0, MAX_BLOCKS) : ganttData;
    
    // Find the total time of this specific algorithm to scale it properly
    const totalTime = ganttData[ganttData.length - 1].end;

    blocksToDraw.forEach(block => {
      // 1. Extract safely (using !== undefined prevents the '0' bug)
      const pid = block.pid !== undefined ? block.pid : (block.process || "P");
      const start = block.start !== undefined ? block.start : 0;
      const end = block.end !== undefined ? block.end : start;

      // 2. Create the block
      const span = document.createElement("span");
      span.className = "block";
      
      // 3. Responsive sizing: If total time is huge, use % so it doesn't span millions of pixels
      if (totalTime > 100) {
          let percentage = ((end - start) / totalTime) * 100;
          span.style.width = `${percentage}%`;
          span.style.minWidth = "50px"; // Ensure the block doesn't squish too small to read text
      } else {
          span.style.width = `${(end - start) * 40}px`;
      }
      
      // 4. Inject BOTH the PID and the Start-End times
      span.innerHTML = `
        <div style="font-weight: bold; font-size: 1.2em;">${pid}</div>
        <div style="font-size: 0.8em; opacity: 0.8;">${start} - ${end}</div>
      `;

      gantt.appendChild(span);
    });

    // 🚨 If there were too many blocks, add a warning block at the end
    if (ganttData.length > MAX_BLOCKS) {
      const remainingBlocks = ganttData.length - MAX_BLOCKS;
      const warnSpan = document.createElement("span");
      warnSpan.className = "block warning";
      warnSpan.style.minWidth = "120px";
      warnSpan.style.backgroundColor = "rgba(239, 68, 68, 0.2)"; 
      warnSpan.style.border = "1px dashed #ef4444";
      warnSpan.style.display = "flex";
      warnSpan.style.flexDirection = "column";
      warnSpan.style.justifyContent = "center";
      
      warnSpan.innerHTML = `
        <div style="font-weight: bold; font-size: 1.2em;">...</div>
        <div style="font-size: 0.7em; opacity: 0.9;">+ ${remainingBlocks} more blocks</div>
      `;
      gantt.appendChild(warnSpan);
    }
  }

  // -----------------------------
  // ACCURACY / EFFICIENCY BAR
  // -----------------------------
  let efficiency = 0;
  if (r.average_waiting_time === 0) {
      efficiency = 100; // If wait time is 0, efficiency is perfect
  } else {
      efficiency = ((1 / r.average_waiting_time) / maxEfficiency) * 100;
  }
  
  const bar = document.createElement("div");
  bar.className = "bar";
  bar.style.width = efficiency + "%";

  // -----------------------------
  // APPEND EVERYTHING
  // -----------------------------
  div.appendChild(gantt);
  div.appendChild(bar);
  container.appendChild(div);
});