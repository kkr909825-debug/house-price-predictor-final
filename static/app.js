let cityData = {};

function showPrice(number) {
  if (number >= 10000000) {
    return "Rs " + (number / 10000000).toFixed(2) + " Cr";
  }
  return "Rs " + (number / 100000).toFixed(2) + " Lakh";
}

function fillLocations() {
  const city = document.getElementById("city").value;
  const locations = cityData[city];
  let html = "";
  for (let i = 0; i < locations.length; i++) {
    html += "<option value='" + locations[i] + "'>" + locations[i] + "</option>";
  }
  document.getElementById("location").innerHTML = html;
}

async function loadOptions() {
  const response = await fetch("/api/options");
  const data = await response.json();
  cityData = data.cities;

  let cityHtml = "";
  for (const city in cityData) {
    cityHtml += "<option value='" + city + "'>" + city + "</option>";
  }
  document.getElementById("city").innerHTML = cityHtml;
  fillLocations();

  let facilityHtml = "";
  for (const key in data.amenities) {
    facilityHtml += "<label class='check'><input type='checkbox' name='" + key + "'> " + data.amenities[key] + "</label>";
  }
  document.getElementById("facilities").innerHTML = facilityHtml;

  document.getElementById("modelinfo").textContent =
    "Model: " + data.model.name + " | R2 score: " + data.model.r2_score +
    " | Average error: " + data.model.error_percent + "%";
}

document.getElementById("city").addEventListener("change", fillLocations);

document.getElementById("form").addEventListener("submit", async function (event) {
  event.preventDefault();
  document.getElementById("error").textContent = "";

  const form = event.target;
  const details = {
    city: form.city.value,
    location: form.location.value,
    area_sqft: form.area_sqft.value,
    bedrooms: form.bedrooms.value,
    resale: form.resale.value,
  };
  const boxes = form.querySelectorAll("#facilities input");
  for (let i = 0; i < boxes.length; i++) {
    details[boxes[i].name] = boxes[i].checked;
  }

  const button = document.getElementById("button");
  button.disabled = true;
  button.textContent = "Please wait...";

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(details),
    });
    const result = await response.json();

    if (!response.ok) {
      document.getElementById("error").textContent = result.error;
    } else {
      document.getElementById("price").textContent = showPrice(result.price);
      document.getElementById("persqft").textContent =
        "About Rs " + result.price_per_sqft.toLocaleString("en-IN") + " per sq ft";
      document.getElementById("range").textContent =
        "Likely range: " + showPrice(result.low) + " to " + showPrice(result.high);
      document.getElementById("message").hidden = true;
      document.getElementById("answer").hidden = false;
    }
  } catch (error) {
    document.getElementById("error").textContent = "Could not reach the server. Try again.";
  }

  button.disabled = false;
  button.textContent = "Predict price";
});

loadOptions();
