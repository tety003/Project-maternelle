"""
Maternelle AI Chatbot Backend
Reads maternelle.csv and answers health-related questions for the website chatbot
"""

from flask import Flask, request, jsonify
import csv
import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

# ------------------------------
# HealthChatbot class (CSV Q&A)
# ------------------------------
class HealthChatbot:
    def __init__(self, csv_file_path: str = None):
        self.health_data = []
        self.csv_file_path = csv_file_path
        if csv_file_path:
            self.load_health_data(csv_file_path)

    def load_health_data(self, csv_file_path: str):
        """Load health data from CSV file"""
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                rows = list(csv_reader)

                for row_idx, row in enumerate(rows):
                    if row and any(cell.strip() for cell in row):  # Skip empty rows
                        content = ' '.join([cell.strip() for cell in row if cell.strip()])
                        if content and len(content) > 10:
                            self.health_data.append({
                                'content': content,
                                'row_index': row_idx,
                                'relevance_score': 0
                            })
            logger.info(f"✅ Loaded {len(self.health_data)} health data entries from {csv_file_path}")
        except Exception as e:
            logger.error(f"❌ Error loading health data: {str(e)}")
            self.health_data = []

    def search_health_data(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """Search health data for relevant information"""
        if not self.health_data:
            return []

        query_lower = query.lower()
        query_words = set(re.findall(r'\b\w+\b', query_lower))

        for item in self.health_data:
            content_lower = item['content'].lower()
            content_words = set(re.findall(r'\b\w+\b', content_lower))

            common_words = query_words.intersection(content_words)
            relevance_score = len(common_words) / max(len(query_words), 1)

            if query_lower in content_lower:
                relevance_score += 0.5

            item['relevance_score'] = relevance_score

        relevant_items = [item for item in self.health_data if item['relevance_score'] > 0]
        relevant_items.sort(key=lambda x: x['relevance_score'], reverse=True)

        return relevant_items[:max_results]

    def generate_response(self, user_message: str) -> str:
        """Generate a response based on user message"""
        if not user_message or not user_message.strip():
            return "👋 Hello! I'm your health assistant. How can I help you today?"

        relevant_data = self.search_health_data(user_message)

        if not relevant_data:
            return self._get_general_response(user_message)

        response_parts = []
        response_parts.append("📖 Based on the Mother & Child Health Handbook, here’s what I found:")

        for i, item in enumerate(relevant_data[:2], 1):
            content = item['content']
            content = re.sub(r'\s+', ' ', content).strip()
            if len(content) > 250:
                content = content[:250] + "..."
            response_parts.append(f"\n{i}. {content}")

        response_parts.append("\n\n❓ Anything else you’d like to ask?")
        return ''.join(response_parts)

    def _get_general_response(self, user_message: str) -> str:
        """Fallback responses if nothing is found"""
        message_lower = user_message.lower()
        health_responses = {
            'pregnancy': "🤰 During pregnancy, it's important to attend all antenatal clinic visits and eat healthy foods. The handbook has more details about nutrition, tests, and delivery preparation.",
            'breastfeeding': "🍼 Breastfeeding is key for your baby’s growth. The handbook explains correct latching, positions, and feeding schedules.",
            'vaccination': "💉 Vaccinations protect your baby from diseases. Follow the schedule in the handbook for safe immunization.",
            'nutrition': "🥗 Proper nutrition supports both mother and child. Include balanced meals and essential supplements as recommended.",
            'development': "📈 Tracking milestones helps you support your child’s growth. The handbook has charts to guide you.",
            'danger': "⚠️ If you notice danger signs (heavy bleeding, fever, severe pain), seek medical help immediately."
        }
        for topic, response in health_responses.items():
            if topic in message_lower:
                return response
        return "I can help with questions about pregnancy, breastfeeding, vaccinations, child development, and nutrition. What would you like to ask?"

# ------------------------------
# Flask App Setup
# ------------------------------
app = Flask(__name__)

# Load CSV when the server starts
chatbot = HealthChatbot("maternelle.csv")

@app.route("/ask", methods=["POST"])
def ask():
    """Endpoint to handle chatbot questions"""
    data = request.json
    user_message = data.get("question", "")
    response = chatbot.generate_response(user_message)
    return jsonify({"answer": response})

@app.route("/", methods=["GET"])
def home():
    return app.send_static_file('maternelle1.html')

@app.route("/<path:filename>")
def serve_static(filename):
    return app.send_static_file(filename)

# ------------------------------
# Run the Flask server on Replit
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
