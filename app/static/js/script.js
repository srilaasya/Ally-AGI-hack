document.getElementById("form").addEventListener("submit", (event) => {
  event.preventDefault();
  const input = document.getElementById("input").value;

  // Send POST request to the Flask server
  fetch("/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ input }),
  })
    .then((response) => response.json())
    .then((data) => console.log("Success:", data))
    .catch((error) => console.error("Error:", error));
});
