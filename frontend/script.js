const API_URL = "http://127.0.0.1:8000/metrics/";

document.addEventListener("DOMContentLoaded", () => {
    fetchMetrics();

    document.getElementById("metric-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const name = document.getElementById("name").value;
        const value = document.getElementById("value").value;

        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, value })
        });

        if (response.ok) {
            fetchMetrics();
            document.getElementById("metric-form").reset();
        } else {
            alert("Error adding metric.");
        }
    });
});

async function fetchMetrics() {
    const response = await fetch(API_URL);
    const metrics = await response.json();

    const metricsList = document.getElementById("metrics-list");
    metricsList.innerHTML = "";
    metrics.forEach(metric => {
        const li = document.createElement("li");
        li.textContent = `${metric.name}: ${metric.value}`;
        metricsList.appendChild(li);
    });
}
