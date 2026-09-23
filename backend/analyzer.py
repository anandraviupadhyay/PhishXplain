import re
import ipaddress
from urllib.parse import urlparse


# ============================================================
# PHISHXPLAIN - CYBERSECURITY ANALYZER
# ============================================================

class PhishAnalyzer:

    def __init__(self):

        # Suspicious words commonly associated with phishing URLs
        self.url_keywords = [
            "login",
            "signin",
            "verify",
            "verification",
            "account",
            "secure",
            "security",
            "update",
            "confirm",
            "password",
            "credential",
            "bank",
            "payment",
            "wallet",
            "billing",
            "unlock",
            "suspend",
            "recover",
            "authenticate"
        ]

        # Urgency-related words/phrases
        self.urgency_keywords = [
            "urgent",
            "immediately",
            "act now",
            "action required",
            "verify now",
            "respond immediately",
            "limited time",
            "expires today",
            "account blocked",
            "account suspended",
            "final warning"
        ]

        # Credential/payment related terms
        self.credential_keywords = [
            "password",
            "otp",
            "one time password",
            "pin",
            "cvv",
            "card number",
            "credit card",
            "debit card",
            "bank account",
            "username",
            "login",
            "credentials"
        ]

        # Suspicious URL shorteners
        self.url_shorteners = [
            "bit.ly",
            "tinyurl.com",
            "t.co",
            "goo.gl",
            "is.gd",
            "cutt.ly",
            "shorturl.at",
            "rebrand.ly"
        ]


    # ========================================================
    # MAIN ANALYZER
    # ========================================================

    def analyze(self, input_type: str, user_input: str):

        input_type = input_type.lower().strip()
        user_input = user_input.strip()

        if input_type == "url":
            return self.analyze_url(user_input)

        elif input_type == "message":
            return self.analyze_message(user_input)

        else:
            return {
                "score": 0,
                "classification": "UNKNOWN",
                "reasons": ["Unsupported input type"],
                "recommendation": "Please provide a URL or message."
            }


    # ========================================================
    # URL ANALYSIS
    # ========================================================

    def analyze_url(self, url: str):

        score = 0
        reasons = []

        url_lower = url.lower()

        # ----------------------------------------------------
        # Basic URL validation
        # ----------------------------------------------------

        try:
            parsed = urlparse(url)

        except Exception:

            return {
                "score": 90,
                "classification": "HIGH RISK",
                "reasons": ["Invalid or malformed URL"],
                "recommendation":
                    "Do not open the URL."
            }

        if not parsed.netloc:

            return {
                "score": 90,
                "classification": "HIGH RISK",
                "reasons": ["URL does not contain a valid domain"],
                "recommendation":
                    "Do not open the URL."
            }


        hostname = parsed.hostname or ""


        # ----------------------------------------------------
        # HTTPS CHECK
        # ----------------------------------------------------

        if parsed.scheme.lower() != "https":

            score += 15

            reasons.append(
                "URL does not use HTTPS"
            )


        # ----------------------------------------------------
        # IP ADDRESS CHECK
        # ----------------------------------------------------

        try:

            ipaddress.ip_address(hostname)

            score += 30

            reasons.append(
                "URL uses an IP address instead of a domain"
            )

        except ValueError:
            pass


        # ----------------------------------------------------
        # URL LENGTH
        # ----------------------------------------------------

        if len(url) > 120:

            score += 15

            reasons.append(
                "URL is unusually long"
            )

        elif len(url) > 80:

            score += 8

            reasons.append(
                "URL is longer than typical"
            )


        # ----------------------------------------------------
        # SUBDOMAIN CHECK
        # ----------------------------------------------------

        domain_parts = hostname.split(".")

        if len(domain_parts) >= 4:

            score += 10

            reasons.append(
                "URL contains an unusually large number of subdomains"
            )


        # ----------------------------------------------------
        # @ SYMBOL CHECK
        # ----------------------------------------------------

        if "@" in url:

            score += 20

            reasons.append(
                "URL contains '@', which can hide the actual destination"
            )


        # ----------------------------------------------------
        # SUSPICIOUS CHARACTER CHECK
        # ----------------------------------------------------

        suspicious_chars = ["%", "{", "}", "\\"]

        found_chars = [
            char for char in suspicious_chars
            if char in url
        ]

        if found_chars:

            score += 10

            reasons.append(
                "URL contains suspicious encoded or special characters"
            )


        # ----------------------------------------------------
        # URL KEYWORDS
        # ----------------------------------------------------

        detected_keywords = []

        for keyword in self.url_keywords:

            if keyword in url_lower:

                detected_keywords.append(keyword)


        # Avoid excessive scoring when many keywords appear
        if detected_keywords:

            keyword_score = min(
                len(detected_keywords) * 10,
                30
            )

            score += keyword_score

            for keyword in detected_keywords[:5]:

                reasons.append(
                    f"Suspicious keyword detected: {keyword}"
                )


        # ----------------------------------------------------
        # URL SHORTENER CHECK
        # ----------------------------------------------------

        for shortener in self.url_shorteners:

            if shortener in hostname:

                score += 20

                reasons.append(
                    "URL uses a link-shortening service"
                )

                break


        # ----------------------------------------------------
        # DOMAIN LOOKALIKE INDICATORS
        # ----------------------------------------------------

        if "-" in hostname:

            score += 5

            reasons.append(
                "Domain contains hyphens often seen in lookalike domains"
            )


        # ----------------------------------------------------
        # MULTIPLE DOTS / DECEPTIVE DOMAIN STRUCTURE
        # ----------------------------------------------------

        if hostname.count(".") >= 3:

            score += 8

            reasons.append(
                "Domain structure may be designed to resemble another domain"
            )


        # ----------------------------------------------------
        # QUERY STRING
        # ----------------------------------------------------

        if parsed.query:

            suspicious_query_words = [
                "login",
                "password",
                "verify",
                "account",
                "token",
                "session"
            ]

            found_query_words = [
                word
                for word in suspicious_query_words
                if word in parsed.query.lower()
            ]

            if found_query_words:

                score += 15

                reasons.append(
                    "URL query contains sensitive-action parameters"
                )


        # ----------------------------------------------------
        # FINAL SCORE
        # ----------------------------------------------------

        score = min(score, 100)


        # ----------------------------------------------------
        # CLASSIFICATION
        # ----------------------------------------------------

        classification = self.get_classification(score)


        # ----------------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------------

        recommendation = self.get_recommendation(
            score,
            "url"
        )


        # ----------------------------------------------------
        # DEFAULT REASON
        # ----------------------------------------------------

        if not reasons:

            reasons.append(
                "No major phishing indicators detected"
            )


        return {
            "score": score,
            "classification": classification,
            "reasons": reasons,
            "recommendation": recommendation
        }


    # ========================================================
    # MESSAGE ANALYSIS
    # ========================================================

    def analyze_message(self, message: str):

        score = 0
        reasons = []

        text = message.lower()


        # ----------------------------------------------------
        # URGENCY DETECTION
        # ----------------------------------------------------

        detected_urgency = []

        for keyword in self.urgency_keywords:

            if keyword in text:

                detected_urgency.append(keyword)


        if detected_urgency:

            score += min(
                len(detected_urgency) * 15,
                30
            )

            for keyword in detected_urgency[:3]:

                reasons.append(
                    f"Urgency indicator detected: {keyword}"
                )


        # ----------------------------------------------------
        # CREDENTIAL REQUEST
        # ----------------------------------------------------

        detected_credentials = []

        for keyword in self.credential_keywords:

            if keyword in text:

                detected_credentials.append(keyword)


        if detected_credentials:

            score += min(
                len(detected_credentials) * 15,
                40
            )

            for keyword in detected_credentials[:4]:

                reasons.append(
                    f"Sensitive information request detected: {keyword}"
                )


        # ----------------------------------------------------
        # URL IN MESSAGE
        # ----------------------------------------------------

        urls = re.findall(
            r"https?://[^\s]+",
            message
        )

        if urls:

            score += 20

            reasons.append(
                "Message contains a clickable URL"
            )


        # ----------------------------------------------------
        # PAYMENT / MONEY REQUEST
        # ----------------------------------------------------

        payment_words = [
            "payment",
            "pay now",
            "refund",
            "transfer",
            "upi",
            "money",
            "invoice",
            "transaction"
        ]

        detected_payment = []

        for keyword in payment_words:

            if keyword in text:

                detected_payment.append(keyword)


        if detected_payment:

            score += 20

            reasons.append(
                "Message contains payment or financial request"
            )


        # ----------------------------------------------------
        # IMPERSONATION INDICATORS
        # ----------------------------------------------------

        impersonation_words = [
            "bank",
            "government",
            "tax department",
            "support team",
            "customer care",
            "admin",
            "security team",
            "microsoft",
            "google",
            "amazon"
        ]

        detected_impersonation = []

        for keyword in impersonation_words:

            if keyword in text:

                detected_impersonation.append(keyword)


        if detected_impersonation:

            score += 10

            reasons.append(
                "Message may be impersonating a trusted organization or service"
            )


        # ----------------------------------------------------
        # EXCESSIVE CAPITALIZATION
        # ----------------------------------------------------

        letters = [
            char
            for char in message
            if char.isalpha()
        ]

        if len(letters) > 20:

            uppercase_letters = [
                char
                for char in letters
                if char.isupper()
            ]

            uppercase_ratio = (
                len(uppercase_letters) /
                len(letters)
            )

            if uppercase_ratio > 0.60:

                score += 5

                reasons.append(
                    "Message uses unusually high capitalization"
                )


        # ----------------------------------------------------
        # EXCLAMATION MARKS
        # ----------------------------------------------------

        if message.count("!") >= 3:

            score += 5

            reasons.append(
                "Message uses excessive exclamation marks"
            )


        # ----------------------------------------------------
        # FINAL SCORE
        # ----------------------------------------------------

        score = min(score, 100)


        classification = self.get_classification(score)

        recommendation = self.get_recommendation(
            score,
            "message"
        )


        if not reasons:

            reasons.append(
                "No major phishing indicators detected"
            )


        return {
            "score": score,
            "classification": classification,
            "reasons": reasons,
            "recommendation": recommendation
        }


    # ========================================================
    # CLASSIFICATION
    # ========================================================

    def get_classification(self, score):

        if score >= 70:

            return "HIGH RISK"

        elif score >= 40:

            return "SUSPICIOUS"

        else:

            return "LOW RISK"


    # ========================================================
    # RECOMMENDATION
    # ========================================================

    def get_recommendation(self, score, input_type):

        if score >= 70:

            if input_type == "url":

                return (
                    "Do not open this URL or enter personal information. "
                    "Verify the website through an official source."
                )

            return (
                "Do not click links or provide passwords, OTPs, "
                "payment details, or other sensitive information."
            )


        elif score >= 40:

            return (
                "Verify the sender and destination through an official "
                "channel before taking action."
            )


        else:

            return (
                "No major phishing indicators were detected. "
                "Continue to use normal security precautions."
            )


# ============================================================
# SINGLE ANALYZER INSTANCE
# ============================================================

analyzer = PhishAnalyzer()