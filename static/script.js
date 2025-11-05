// Tab Navigation
function showTab(tabName) {
  // Hide all tab contents
  const tabContents = document.querySelectorAll(".tab-content");
  tabContents.forEach((content) => content.classList.remove("active"));

  // Remove active class from all buttons
  const tabButtons = document.querySelectorAll(".tab-button");
  tabButtons.forEach((button) => button.classList.remove("active"));

  // Show selected tab and activate button
  document.getElementById(tabName).classList.add("active");
  event.target.classList.add("active");
}

// Chat Interface Functions
let chatHistory = [];

// Helper function to convert Markdown bold (**text**) to HTML
function formatMarkdown(text) {
  // Convert **text** to <strong>text</strong>
  let formatted = text.replace(/\*\*([^\*]+)\*\*/g, "<strong>$1</strong>");
  // Convert line breaks to <br> tags
  formatted = formatted.replace(/\n/g, "<br>");
  return formatted;
}

function addChatMessage(role, content, functionCalled = null) {
  const messagesDiv = document.getElementById("chat-messages");
  const messageDiv = document.createElement("div");
  messageDiv.className = `chat-message ${role}`;

  let html = `<div class="message-label">${
    role === "user" ? "You" : "AI Assistant"
  }</div>`;

  if (functionCalled) {
    html += `<div class="function-call-badge">🔧 Used: ${functionCalled}</div>`;
  }

  // Format markdown in content
  const formattedContent = formatMarkdown(content);
  html += `<div class="message-content">${formattedContent}</div>`;
  messageDiv.innerHTML = html;

  messagesDiv.appendChild(messageDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  chatHistory.push({ role, content });
}

function showTypingIndicator() {
  const messagesDiv = document.getElementById("chat-messages");
  const typingDiv = document.createElement("div");
  typingDiv.id = "typing-indicator";
  typingDiv.className = "chat-message assistant";
  typingDiv.innerHTML = `
        <div class="message-label">AI Assistant</div>
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
  messagesDiv.appendChild(typingDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeTypingIndicator() {
  const typingDiv = document.getElementById("typing-indicator");
  if (typingDiv) {
    typingDiv.remove();
  }
}

async function sendChatMessage() {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();

  if (!message) return;

  // Add user message
  addChatMessage("user", message);
  input.value = "";

  // Disable input while processing
  const sendBtn = document.querySelector(".chat-send-btn");
  sendBtn.disabled = true;
  showTypingIndicator();

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();

    removeTypingIndicator();

    if (data.error) {
      addChatMessage("system", `Error: ${data.error}`);
    } else {
      addChatMessage("assistant", data.response, data.function_called);
    }
  } catch (error) {
    removeTypingIndicator();
    addChatMessage("system", `Error: ${error.message}`);
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

function askSuggestion(question) {
  document.getElementById("chat-input").value = question;
  sendChatMessage();
}

// Allow Enter to send (with Shift+Enter for new line)
document.addEventListener("DOMContentLoaded", function () {
  const chatInput = document.getElementById("chat-input");
  if (chatInput) {
    chatInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendChatMessage();
      }
    });
  }

  // Add welcome message
  if (document.getElementById("chat-messages")) {
    addChatMessage(
      "assistant",
      "Marhaba! 👋 I'm your AI assistant for Lebanon and AUB."
    );
  }
});

// Helper function to display results
function displayResult(elementId, data, isError = false) {
  const resultBox = document.getElementById(elementId);
  resultBox.classList.remove("loading", "error");

  if (isError) {
    resultBox.classList.add("error");
    resultBox.innerHTML = `<p style="color: #e74c3c; font-weight: 600;">❌ Error: ${data}</p>`;
    return;
  }

  // Format JSON beautifully
  if (data.status === "success" || data.success) {
    resultBox.innerHTML = formatSuccessResult(data);
  } else {
    resultBox.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }
}

function formatSuccessResult(data) {
  let html =
    '<div style="color: #27ae60; font-weight: 600; margin-bottom: 15px;">✅ Success</div>';

  if (data.data) {
    html += formatData(data.data);
  } else if (data.result) {
    html += formatData(data.result);
  } else {
    // If no data or result property, show all properties except status/success
    const dataToShow = { ...data };
    delete dataToShow.status;
    delete dataToShow.success;
    html += `<pre>${JSON.stringify(dataToShow, null, 2)}</pre>`;
  }

  if (data.metadata) {
    html +=
      '<div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd;">';
    html += "<strong>Metadata:</strong>";
    html += `<pre style="margin-top: 10px;">${JSON.stringify(
      data.metadata,
      null,
      2
    )}</pre>`;
    html += "</div>";
  }

  return html;
}

function formatData(data) {
  let html = "";

  if (Array.isArray(data)) {
    data.forEach((item, index) => {
      html += `<div class="result-card">`;
      html += formatObject(item);
      html += `</div>`;
    });
  } else if (typeof data === "object") {
    html += formatObject(data);
  } else {
    html += `<p>${data}</p>`;
  }

  return html;
}

function formatObject(obj) {
  let html = "";
  for (const [key, value] of Object.entries(obj)) {
    const formattedKey = key
      .replace(/_/g, " ")
      .replace(/\b\w/g, (l) => l.toUpperCase());

    if (typeof value === "object" && value !== null) {
      html += `<div style="margin: 10px 0;"><strong>${formattedKey}:</strong></div>`;
      html += `<pre style="background: white; padding: 10px; border-radius: 5px;">${JSON.stringify(
        value,
        null,
        2
      )}</pre>`;
    } else {
      html += `<p><strong>${formattedKey}:</strong> ${value}</p>`;
    }
  }
  return html;
}

function setLoading(elementId) {
  const resultBox = document.getElementById(elementId);
  resultBox.innerHTML = "";
  resultBox.classList.add("loading");
}

// TimeTravel Map Server Functions
async function timeTravelGeocode() {
  const location = document.getElementById("tt-geocode-location").value;
  const year = parseInt(document.getElementById("tt-geocode-year").value);

  if (!location) {
    alert("Please enter a location");
    return;
  }

  setLoading("tt-geocode-result");

  try {
    const response = await fetch("/api/timetravel/geocode", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location, year }),
    });

    const data = await response.json();
    displayResult("tt-geocode-result", data);
  } catch (error) {
    displayResult("tt-geocode-result", error.message, true);
  }
}

async function timeTravelTimeline() {
  const location = document.getElementById("tt-timeline-location").value;
  const startYear = document.getElementById("tt-timeline-start").value;
  const endYear = document.getElementById("tt-timeline-end").value;

  if (!location) {
    alert("Please enter a location");
    return;
  }

  setLoading("tt-timeline-result");

  try {
    const body = { location };
    if (startYear) body.start_year = parseInt(startYear);
    if (endYear) body.end_year = parseInt(endYear);

    const response = await fetch("/api/timetravel/timeline", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    displayResult("tt-timeline-result", data);
  } catch (error) {
    displayResult("tt-timeline-result", error.message, true);
  }
}

async function timeTravelCompare() {
  const location = document.getElementById("tt-compare-location").value;
  const year1 = parseInt(document.getElementById("tt-compare-year1").value);
  const year2 = parseInt(document.getElementById("tt-compare-year2").value);

  if (!location) {
    alert("Please enter a location");
    return;
  }

  setLoading("tt-compare-result");

  try {
    const response = await fetch("/api/timetravel/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location, year1, year2 }),
    });

    const data = await response.json();
    displayResult("tt-compare-result", data);
  } catch (error) {
    displayResult("tt-compare-result", error.message, true);
  }
}

// Emotional Geography Server Functions
async function emotionalLocation() {
  const location = document.getElementById("eg-location").value;

  if (!location) {
    alert("Please enter a location");
    return;
  }

  setLoading("eg-location-result");

  try {
    const response = await fetch("/api/emotional/location", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location }),
    });

    const data = await response.json();
    displayResult("eg-location-result", data);
  } catch (error) {
    displayResult("eg-location-result", error.message, true);
  }
}

async function emotionalFind() {
  const emotion = document.getElementById("eg-emotion").value;
  const minIntensity = parseInt(document.getElementById("eg-intensity").value);

  setLoading("eg-find-result");

  try {
    const response = await fetch("/api/emotional/find", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ emotion, min_intensity: minIntensity }),
    });

    const data = await response.json();
    displayResult("eg-find-result", data);
  } catch (error) {
    displayResult("eg-find-result", error.message, true);
  }
}

async function emotionalHeatmap() {
  const locationsStr = document.getElementById("eg-heatmap-locations").value;
  const emotionFilter = document.getElementById("eg-heatmap-filter").value;

  const locations = locationsStr
    .split(",")
    .map((l) => l.trim())
    .filter((l) => l);

  if (locations.length === 0) {
    alert("Please enter at least one location");
    return;
  }

  setLoading("eg-heatmap-result");

  try {
    const body = { locations };
    if (emotionFilter) body.emotion_filter = emotionFilter;

    const response = await fetch("/api/emotional/heatmap", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    displayResult("eg-heatmap-result", data);
  } catch (error) {
    displayResult("eg-heatmap-result", error.message, true);
  }
}

// Quantum Navigation Server Functions
async function quantumRoutes() {
  const origin = document.getElementById("qn-routes-origin").value;
  const destination = document.getElementById("qn-routes-destination").value;
  const mode = document.getElementById("qn-routes-mode").value;
  const riskTolerance = parseFloat(
    document.getElementById("qn-routes-risk").value
  );

  if (!origin || !destination) {
    alert("Please enter both origin and destination");
    return;
  }

  setLoading("qn-routes-result");

  try {
    const response = await fetch("/api/quantum/routes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        origin,
        destination,
        mode,
        risk_tolerance: riskTolerance,
      }),
    });

    const data = await response.json();
    displayResult("qn-routes-result", data);
  } catch (error) {
    displayResult("qn-routes-result", error.message, true);
  }
}

async function quantumConfidence() {
  const origin = document.getElementById("qn-confidence-origin").value;
  const destination = document.getElementById(
    "qn-confidence-destination"
  ).value;
  const routeId = document.getElementById("qn-confidence-route").value;

  if (!origin || !destination || !routeId) {
    alert("Please fill in all fields");
    return;
  }

  setLoading("qn-confidence-result");

  try {
    const response = await fetch("/api/quantum/confidence", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ origin, destination, route_id: routeId }),
    });

    const data = await response.json();
    displayResult("qn-confidence-result", data);
  } catch (error) {
    displayResult("qn-confidence-result", error.message, true);
  }
}

async function quantumReroute() {
  const origin = document.getElementById("qn-reroute-origin").value;
  const destination = document.getElementById("qn-reroute-destination").value;
  const currentRoute = document.getElementById("qn-reroute-current").value;

  // Get selected conditions
  const conditionCheckboxes = document.querySelectorAll(
    '.condition-selector input[type="checkbox"]:checked'
  );
  const conditions = Array.from(conditionCheckboxes).map((cb) => cb.value);

  if (!origin || !destination || !currentRoute) {
    alert("Please fill in all fields");
    return;
  }

  setLoading("qn-reroute-result");

  try {
    const response = await fetch("/api/quantum/reroute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        origin,
        destination,
        current_route: currentRoute,
        conditions,
      }),
    });

    const data = await response.json();
    displayResult("qn-reroute-result", data);
  } catch (error) {
    displayResult("qn-reroute-result", error.message, true);
  }
}

// Weather Functions
async function getCurrentWeather() {
  const location = document.getElementById("weather-location").value;

  if (!location) {
    alert("Please enter a location");
    return;
  }

  setLoading("weather-current-result");

  try {
    const response = await fetch("/api/weather/current", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location }),
    });

    const data = await response.json();
    displayResult("weather-current-result", data);
  } catch (error) {
    displayResult("weather-current-result", error.message, true);
  }
}

async function getWeatherForecast() {
  const location = document.getElementById("forecast-location").value;
  const days = parseInt(document.getElementById("forecast-days").value);

  if (!location) {
    alert("Please enter a location");
    return;
  }

  setLoading("weather-forecast-result");

  try {
    const response = await fetch("/api/weather/forecast", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location, days }),
    });

    const data = await response.json();
    displayResult("weather-forecast-result", data);
  } catch (error) {
    displayResult("weather-forecast-result", error.message, true);
  }
}

async function getSkiConditions() {
  const resort = document.getElementById("ski-resort").value;

  setLoading("weather-ski-result");

  try {
    const response = await fetch("/api/weather/ski", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resort }),
    });

    const data = await response.json();
    displayResult("weather-ski-result", data);
  } catch (error) {
    displayResult("weather-ski-result", error.message, true);
  }
}

async function compareWeather() {
  const location1 = document.getElementById("compare-location1").value;
  const location2 = document.getElementById("compare-location2").value;

  if (!location1 || !location2) {
    alert("Please enter both locations");
    return;
  }

  setLoading("weather-compare-result");

  try {
    const response = await fetch("/api/weather/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location1, location2 }),
    });

    const data = await response.json();
    displayResult("weather-compare-result", data);
  } catch (error) {
    displayResult("weather-compare-result", error.message, true);
  }
}

// Fetch Server Functions (Official MCP Server)
async function fetchUrl() {
  const url = document.getElementById("fetch-url").value;
  const maxLength =
    parseInt(document.getElementById("fetch-max-length").value) || 5000;

  if (!url) {
    alert("Please enter a URL");
    return;
  }

  setLoading("fetch-result");

  try {
    const response = await fetch("/api/fetch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, max_length: maxLength }),
    });

    const data = await response.json();
    displayResult("fetch-result", data);
  } catch (error) {
    displayResult("fetch-result", error.message, true);
  }
}

async function fetchMultiple() {
  const urlsText = document.getElementById("fetch-urls").value;
  const urls = urlsText
    .split("\n")
    .map((url) => url.trim())
    .filter((url) => url.length > 0);

  if (urls.length === 0) {
    alert("Please enter at least one URL");
    return;
  }

  setLoading("fetch-multiple-result");

  try {
    const response = await fetch("/api/fetch/multiple", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ urls, max_length: 3000 }),
    });

    const data = await response.json();
    displayResult("fetch-multiple-result", data);
  } catch (error) {
    displayResult("fetch-multiple-result", error.message, true);
  }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", function () {
  console.log("🌍 MCP Map Servers Demo Initialized");
});
