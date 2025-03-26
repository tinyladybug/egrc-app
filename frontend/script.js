// Define the API URL where metrics are stored
const API_URL = "http://127.0.0.1:8000/metrics/";

// Wait for the document (HTML page) to be fully loaded before executing scripts
document.addEventListener("DOMContentLoaded", () => {
    fetchMetrics(); // Load and display metrics when the page loads

    // Add event listener to handle form submission
    document.getElementById("metric-form").addEventListener("submit", async (e) => {
        e.preventDefault(); // Prevents the page from reloading on form submission

        // Get user input from form fields
        const name = document.getElementById("name").value;
        const value = document.getElementById("value").value;

        // Send a POST request to the API to add a new metric
        const response = await fetch(API_URL, {
            method: "POST", // HTTP method to send data
            headers: { "Content-Type": "application/json" }, // Specify JSON format
            body: JSON.stringify({ name, value }) // Convert input data to JSON format
        });

        // If the request succeeds, update the table and clear the form
        if (response.ok) {
            fetchMetrics(); // Reload the metrics table to show the new entry
            document.getElementById("metric-form").reset(); // Clear the form fields
        } else {
            alert("Error adding metric."); // Show an error message if the request fails
        }
    });
});

// Function to fetch metrics from the API and update the table
async function fetchMetrics() {
    const response = await fetch(API_URL); // Send a GET request to the API
    const metrics = await response.json(); // Convert the response to JSON format

    // Select the table body where metrics will be displayed
    const metricsTableBody = document.querySelector("#metrics-table tbody");
    metricsTableBody.innerHTML = ""; // Clear existing rows before updating

    // Loop through each metric and add it to the table
    metrics.forEach(metric => {
        const row = document.createElement("tr"); // Create a new table row

        row.innerHTML = `
            <td>${metric.id}</td> <!-- Display metric ID -->
            <td>${metric.name}</td> <!-- Display metric name -->
            <!-- <td>${metric.value}</td> Display metric value -->
            <td>${metric.unit || "N/A"}</td> <!-- Display unit, or "N/A" if not provided -->
            <td>${metric.status}</td> <!-- Display metric status -->
            <td>${new Date(metric.created_at).toLocaleString()}</td> <!-- Format creation date -->
            <td>
                <button onclick="deleteMetric(${metric.id})">❌ Delete</button> <!-- Delete button -->
            </td>
        `;

        metricsTableBody.appendChild(row); // Append the row to the table
    });
}

// Function to delete a metric by its ID (optional, for later)
async function deleteMetric(id) {
    if (confirm("Are you sure you want to delete this metric?")) { // Confirm deletion
        const response = await fetch(`${API_URL}${id}`, {
            method: "DELETE" // Send a DELETE request to remove the metric
        });

        // If the request is successful, refresh the metrics table
        if (response.ok) {
            fetchMetrics(); // Reload the table after deletion
        } else {
            alert("Error deleting metric."); // Show an error message if deletion fails
        }
    }
}
