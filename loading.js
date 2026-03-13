window.onload = async () => {
  try {
    const processesRaw = localStorage.getItem("processes");
    const algo = localStorage.getItem("algorithm") || "fcfs";
    let quantum = localStorage.getItem("quantum") || "2";

    if (!processesRaw) throw new Error("No process data found.");
    const processes = JSON.parse(processesRaw);

    // --- CRITICAL FIX: ENSURE ABSOLUTE URL ---
    const baseUrl = "http://127.0.0.1:8000";
    let endpoint = "";

    if (algo === "compare") {
      endpoint = `/schedule/compare/${quantum}`;
    } else if (algo === "rr") {
      endpoint = `/schedule/rr/${quantum}`;
    } else {
      endpoint = `/schedule/${algo}`;
    }

    const fullUrl = baseUrl + endpoint;
    console.log("Fetching from:", fullUrl);

    const res = await fetch(fullUrl, { // Use the absolute fullUrl
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ processes: processes })
    });

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Server Error (${res.status}): ${errText}`);
    }

    const data = await res.json();

    // Normalize for result.js
    let finalData = data.results ? data : {
        results: [data],
        best_algorithm: data.algorithm,
        worst_algorithm: data.algorithm
    };

    localStorage.setItem("results", JSON.stringify(finalData));
    
    setTimeout(() => {
      window.location.href = "result.html";
    }, 500);

  } catch (error) {
    console.error("FATAL ERROR:", error);
    document.body.innerHTML = `
      <div style="color: white; text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h1 style="color: #ff4b4b;">⚠️ Connection Failed</h1>
        <p>${error.message}</p>
        <button onclick="window.location.href='index.html'" style="padding:10px 20px; margin-top:20px;">Try Again</button>
      </div>
    `;
  }
};