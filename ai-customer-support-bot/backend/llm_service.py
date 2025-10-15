import json
from groq import Groq
from config import Config

class LLMService:
    def __init__(self):
        self.faqs = self.load_faqs()
        self.client = Groq(api_key=Config.GROQ_API_KEY)
    
    def load_faqs(self):
        """Load FAQs from JSON file"""
        with open(Config.FAQ_FILE_PATH, 'r') as f:
            data = json.load(f)
            return data['faqs']
    
    def generate_response(self, user_message, conversation_history):
        """Generate AI response using Groq"""
        
        # Create FAQ context for the AI
        faq_context = "\n".join([
            f"Q: {faq['question']}\nA: {faq['answer']}" 
            for faq in self.faqs
        ])
        
        # Build the system prompt
        # Build the system prompt
        system_prompt = f"""You are a helpful customer support assistant. 

IMPORTANT: You must ONLY use information from the following FAQs to answer questions. Do NOT make up answers or use information not provided here.

FAQs:
{faq_context}

INSTRUCTIONS:
1. If the customer's question matches any FAQ above, provide EXACTLY the answer from the FAQ.
2. If the customer's question is NOT covered in the FAQs above, respond with: "I don't have specific information about that in my knowledge base. Let me connect you with a human agent who can better assist you."
3. Keep responses friendly and professional.
4. Do NOT invent or assume information not in the FAQs."""
        
        # Build messages for Groq API
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history (last 4 messages for context)
        for msg in conversation_history[-4:]:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call Groq API
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",  # Fast and powerful model
                temperature=0.7,
                max_tokens=300
            )
            
            ai_response = chat_completion.choices[0].message.content.strip()
            
            # Check if escalation is needed
            escalation_keywords = ["escalate", "human agent", "speak to someone", "transfer", "manager"]
            needs_escalation = any(keyword in ai_response.lower() for keyword in escalation_keywords)
            
            # Generate suggested actions
            suggested_actions = self.suggest_next_actions(user_message, ai_response)
            
            return {
                "response": ai_response,
                "needs_escalation": needs_escalation,
                "suggested_actions": suggested_actions
            }
                
        except Exception as e:
            print(f"Groq error: {e}")
            return {
                "response": "I'm experiencing technical difficulties. Let me connect you with a human agent.",
                "needs_escalation": True,
                "suggested_actions": ["Contact human support", "Check system status"]
            }
    
    def suggest_next_actions(self, user_message, ai_response):
        """Suggest next actions based on the conversation"""
        actions = []
        
        user_lower = user_message.lower()
        
        # Suggest actions based on topic
        if "password" in user_lower or "reset" in user_lower:
            actions = ["Reset password", "Contact support", "Check email"]
        elif "payment" in user_lower or "billing" in user_lower:
            actions = ["View payment methods", "Update billing info", "Contact billing support"]
        elif "shipping" in user_lower or "delivery" in user_lower:
            actions = ["Track order", "Update shipping address", "Contact shipping support"]
        elif "refund" in user_lower:
            actions = ["View refund policy", "Request refund", "Contact support"]
        elif "hours" in user_lower or "time" in user_lower:
            actions = ["View business hours", "Schedule callback", "Send email"]
        else:
            actions = ["View FAQs", "Contact support", "Return to main menu"]
        
        return actions[:3]  # Return max 3 actions
    
    def summarize_conversation(self, messages):
        """Summarize a conversation using Groq"""
        
        if len(messages) == 0:
            return "No conversation to summarize."
        
        # Build conversation text
        conversation_text = ""
        for msg in messages:
            role = "Customer" if msg['role'] == 'user' else "Support Agent"
            conversation_text += f"{role}: {msg['content']}\n"
        
        # Create summary prompt
        summary_messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes customer support conversations. Focus on the main issue, key points discussed, and resolution status."
            },
            {
                "role": "user",
                "content": f"Please provide a brief summary of the following customer support conversation:\n\n{conversation_text}"
            }
        ]
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=summary_messages,
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=200
            )
            
            summary = chat_completion.choices[0].message.content.strip()
            return summary
                
        except Exception as e:
            print(f"Summary error: {e}")
            return "Error generating summary."