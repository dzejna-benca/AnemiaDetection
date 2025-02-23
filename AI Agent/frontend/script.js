const BASE_URL = "http://127.0.0.1:5000";

document.getElementById("predict-form").addEventListener("submit", async function (e) {
    e.preventDefault();

  const gender = parseInt(document.getElementById("gender").value);
  const redPixel = parseFloat(document.getElementById("redPixel").value);
  const greenPixel = parseFloat(document.getElementById("greenPixel").value);
  const bluePixel = parseFloat(document.getElementById("bluePixel").value);
  const hb = parseFloat(document.getElementById("hb").value);

  console.log("Gender:", gender, "RedPixel:", redPixel, "GreenPixel:", greenPixel, "BluePixel:", bluePixel, "Hb:", hb);
  try {
    const response = await fetch(`${BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ gender, redPixel, greenPixel, bluePixel,hb }),
    });

    const result = await response.json();
    console.log(result);
    document.getElementById("result").style.display = "block";
    document.getElementById("result").innerText = `Is this person at risk of being anaemic: ${(result.Anaemic === 1 || result.Anaemic === '1') ? 'Yes' : 'No'}`;

  } catch (error) {
    document.getElementById("result").style.display = "block";
    document.getElementById("result").innerText = `Error: ${error.message}`;
  }
});

function showMessage(type, message) {
  const successMessage = document.getElementById("success-message");
  const errorMessage = document.getElementById("error-message");

  if (type === "success") {
    successMessage.innerText = message;
    successMessage.style.display = "block";
    errorMessage.style.display = "none";
  } else {
    errorMessage.innerText = message;
    errorMessage.style.display = "block";
    successMessage.style.display = "none";
  }
}

document.getElementById("add-data-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const gender = parseInt(document.getElementById("add-gender").value);
  const redPixel = parseFloat(document.getElementById("add-redPixel").value);
  const greenPixel = parseFloat(document.getElementById("add-greenPixel").value);
  const bluePixel = parseFloat(document.getElementById("add-bluePixel").value);
  const hb = parseFloat(document.getElementById("add-hb").value);
  const anaemic = document.getElementById("add-anemia").value;

  const newData = [
    { 
      Gender: gender, 
      RedPixel: redPixel, 
      GreenPixel: greenPixel, 
      BluePixel: bluePixel, 
      Hb: hb,
      Anaemic: anaemic
    },
  ];

  try {
    console.log("Data being sent:", newData);

    const response = await fetch(`${BASE_URL}/add_data`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newData),
    });

    const result = await response.json();
    if (response.ok) {
      showMessage("success", result.message || "New data added successfully.");
    } else {
      showMessage("error", result.message || "Failed to add data.");
    }
  } catch (error) {
    showMessage("error", `Error: ${error.message}`);
  }
});


document.getElementById("retrain-button").addEventListener("click", async function (e) {
  e.preventDefault();

  try {
    const response = await fetch(`${BASE_URL}/retrain`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();
    if (response.ok) {
      showMessage("success", result.message || "Model retrained successfully.");
    } else {
      showMessage("error", result.error || "Retraining failed.");
    }
  } catch (error) {
    showMessage("error", `Error: ${error.message}`);
  }
});