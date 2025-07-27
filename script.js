document.getElementById("plannerForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const data = {
    source: form.source.value,
    destination: form.destination.value,
    start_date: form.start_date.value,
    end_date: form.end_date.value,
    budget: form.budget.value
  };

  const res = await fetch("/plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await res.json();
  document.getElementById("result").innerHTML = `
    <h3>🌤 Weather</h3><pre>${result.weather}</pre>
    <h3>✈ Flights</h3><pre>${result.flights}</pre>
    <h3>🏨 Hotel</h3><pre>${result.hotel}</pre>
    <h3>🧭 Itinerary</h3><pre>${result.itinerary}</pre>
    <h3>💰 Budget Summary</h3><pre>${result.summary}</pre>
  `;
});




