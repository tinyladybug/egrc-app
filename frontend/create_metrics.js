// Define the API URL where metrics are stored
const API_URL = "http://127.0.0.1:8000/metrics/";

document.getElementById("metric-form").addEventListener("submit", async (e) => {
    e.preventDefault(); // Prevent default form submission

    // Collect form data
    const metricData = {
        name: document.getElementById("name").value,
        value: parseFloat(document.getElementById("value").value),
        description: document.getElementById("description").value || null,
        unit: document.getElementById("unit").value || null,
        status: document.getElementById("status").value,
        warning_threshold: document.getElementById("warning_threshold").value ? parseFloat(document.getElementById("warning_threshold").value) : null,
        limit_threshold: document.getElementById("limit_threshold").value ? parseFloat(document.getElementById("limit_threshold").value) : null,
        risk_type: document.getElementById("risk_type").value || null,
        business_unit: document.getElementById("business_unit").value || null,
        created_by: document.getElementById("created_by").value || null,
    };

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(metricData)
        });

        if (response.ok) {
            document.getElementById("message").textContent = "Metric created successfully!";
            document.getElementById("metric-form").reset();
        } else {
            document.getElementById("message").textContent = "Error creating metric.";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("message").textContent = "Network error. Please try again.";
    }
});
