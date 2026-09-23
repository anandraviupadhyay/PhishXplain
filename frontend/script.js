let currentMode = "url";

const inputText = document.getElementById("inputText");
const analyzeBtn = document.getElementById("analyzeBtn");
const loader = document.getElementById("loader");
const userInput = document.getElementById("userInput");
const charCount = document.getElementById("charCount");

userInput.addEventListener("input", () => {
    charCount.textContent = `${userInput.value.length} characters`;
});


function switchMode(mode) {

    currentMode = mode;

    const urlTab = document.getElementById("urlTab");
    const messageTab = document.getElementById("messageTab");

    const inputLabel = document.getElementById("inputLabel");
    const inputHint = document.getElementById("inputHint");

    if (mode === "url") {

        urlTab.classList.add("active");
        messageTab.classList.remove("active");

        inputLabel.textContent = "Enter a suspicious URL";

        userInput.placeholder =
            "https://example.com/login";

        inputHint.textContent =
            "We'll analyze the URL for suspicious characteristics.";

    } else {

        messageTab.classList.add("active");
        urlTab.classList.remove("active");

        inputLabel.textContent = "Paste a suspicious message";

        userInput.placeholder =
            "Your account will be blocked. Verify immediately...";

        inputHint.textContent =
            "We'll analyze the message for phishing indicators.";
    }

    userInput.value = "";
    charCount.textContent = "0 characters";
}


async function analyzeInput() {

    console.log("Analyze button clicked");

    const inputElement = document.getElementById("inputText");
    const analyzeButton = document.getElementById("analyzeBtn");
    const loadingElement = document.getElementById("loader");

    const input = inputElement.value.trim();

    if (!input) {
        alert("Please enter a URL or message.");
        return;
    }

    analyzeButton.disabled = true;
    loadingElement.classList.remove("hidden");

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/analyze",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    type: currentMode,
                    input: input
                })
            }
        );

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        const result = await response.json();

        console.log("API Result:", result);

        displayResult(result);

    } catch (error) {

        console.error("ERROR:", error);

        alert("API connection failed. Check FastAPI.");

    } finally {

        analyzeButton.disabled = false;
        loadingElement.classList.add("hidden");
    }
}


function generateDemoResult(input) {

    const lowerInput = input.toLowerCase();

    let score = 91;

    let reasons = [
        "Suspicious content pattern detected",
        "Urgency or verification language detected",
        "Potential phishing indicators found"
    ];

    let recommendation =
        "Do not click suspicious links or provide passwords, OTPs, or payment information.";


    // Basic demo logic

    if (
        lowerInput.includes("bank") ||
        lowerInput.includes("verify") ||
        lowerInput.includes("blocked") ||
        lowerInput.includes("urgent")
    ) {

        score = 94;

        reasons = [
            "Urgent or threatening language detected",
            "Account verification request detected",
            "Potential financial impersonation"
        ];

    }


    if (
        lowerInput.includes("google.com") ||
        lowerInput.includes("github.com") ||
        lowerInput.includes("microsoft.com")
    ) {

        score = 8;

        reasons = [
            "No obvious phishing indicators detected",
            "Known legitimate domain pattern",
            "No urgent credential request detected"
        ];

        recommendation =
            "No obvious phishing indicators were detected. Still verify the source before sharing sensitive information.";
    }


    let classification;

    if (score >= 70) {
        classification = "HIGH RISK";
    } else if (score >= 40) {
        classification = "SUSPICIOUS";
    } else {
        classification = "LOW RISK";
    }


    return {
        score,
        classification,
        reasons,
        recommendation
    };
}


function displayResult(result) {

    const resultSection =
        document.getElementById("resultSection");

    const riskScore =
        document.getElementById("riskScore");

    const riskBadge =
        document.getElementById("riskBadge");

    const riskLevel =
        document.getElementById("riskLevel");

    const riskDescription =
        document.getElementById("riskDescription");

    const reasonsList =
        document.getElementById("reasonsList");

    const recommendation =
        document.getElementById("recommendation");


    riskScore.textContent = result.score;

    riskBadge.textContent = result.classification;

    riskLevel.textContent = result.classification;


    if (result.score >= 70) {

        riskDescription.textContent =
            "Multiple phishing indicators were detected.";

        riskBadge.style.color = "#ff5f6d";

    } else if (result.score >= 40) {

        riskDescription.textContent =
            "Some suspicious characteristics were detected.";

        riskBadge.style.color = "#ffb84d";

    } else {

        riskDescription.textContent =
            "No obvious phishing indicators were detected.";

        riskBadge.style.color = "#35d49a";
    }


    reasonsList.innerHTML = "";

    result.reasons.forEach(reason => {

        const li = document.createElement("li");

        li.textContent = "✓ " + reason;

        reasonsList.appendChild(li);

    });


    recommendation.textContent =
        result.recommendation;


    resultSection.classList.remove("hidden");


    resultSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}