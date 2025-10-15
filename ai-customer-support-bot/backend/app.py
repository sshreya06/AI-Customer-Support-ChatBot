from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from database import Database
from llm_service import LLMService
from models import Conversation

app = Flask(__name__)
CORS(app)

# Initialize database and LLM service
db = Database()
llm_service = LLMService()

# Store active conversations in memory
active_conversations = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.json
    user_message = data.get('message')
    session_id = data.get('session_id')
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Create new session if not provided
    if not session_id:
        session_id = str(uuid.uuid4())
        active_conversations[session_id] = Conversation(session_id)
    
    # Get or create conversation
    if session_id not in active_conversations:
        # Try to load from database
        saved_conv = db.get_conversation(session_id)
        if saved_conv:
            conv = Conversation(session_id)
            conv.messages = saved_conv['messages']
            conv.escalated = saved_conv['escalated']
            active_conversations[session_id] = conv
        else:
            active_conversations[session_id] = Conversation(session_id)
    
    conversation = active_conversations[session_id]
    
    # Add user message
    conversation.add_message('user', user_message)
    
    # Generate AI response
    result = llm_service.generate_response(user_message, conversation.get_history())
    
    # Add AI response
    conversation.add_message('assistant', result['response'])
    
    # Check for escalation
    if result['needs_escalation']:
        conversation.escalate()
    
    # Get suggested next actions
    suggested_actions = result.get('suggested_actions', [])
    
    # Save to database
    db.save_conversation(session_id, conversation.messages, conversation.escalated)
    
    return jsonify({
        'session_id': session_id,
        'response': result['response'],
        'escalated': conversation.escalated,
        'suggested_actions': suggested_actions
    })

@app.route('/api/conversation/<session_id>', methods=['GET'])
def get_conversation(session_id):
    """Get conversation history"""
    if session_id in active_conversations:
        conversation = active_conversations[session_id]
        return jsonify({
            'session_id': session_id,
            'messages': conversation.messages,
            'escalated': conversation.escalated
        })
    
    # Try database
    saved_conv = db.get_conversation(session_id)
    if saved_conv:
        return jsonify({
            'session_id': session_id,
            'messages': saved_conv['messages'],
            'escalated': saved_conv['escalated']
        })
    
    return jsonify({'error': 'Conversation not found'}), 404

@app.route('/api/conversation/<session_id>', methods=['DELETE'])
def delete_conversation(session_id):
    """Delete a conversation"""
    try:
        # Remove from active conversations
        if session_id in active_conversations:
            del active_conversations[session_id]
        
        # Delete from database
        success = db.delete_conversation(session_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Conversation deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Conversation not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting conversation: {str(e)}'
        }), 500

@app.route('/api/conversation/<session_id>/summary', methods=['GET'])
def get_summary(session_id):
    """Get a summary of the conversation"""
    if session_id in active_conversations:
        conversation = active_conversations[session_id]
    else:
        saved_conv = db.get_conversation(session_id)
        if not saved_conv:
            return jsonify({'error': 'Conversation not found'}), 404
        conversation = Conversation(session_id)
        conversation.messages = saved_conv['messages']
    
    # Generate summary using LLM
    summary = llm_service.summarize_conversation(conversation.messages)
    
    return jsonify({
        'session_id': session_id,
        'summary': summary,
        'message_count': len(conversation.messages)
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

@app.route('/api/conversations', methods=['GET'])
def get_all_conversations():
    """Get list of all conversations"""
    conversations = db.get_all_conversations()
    return jsonify({
        'conversations': conversations,
        'count': len(conversations)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

@app.route('/api/conversation/<session_id>', methods=['DELETE'])
def delete_conversation(session_id):
    db = Database()
    success = db.delete_conversation(session_id)
    if success:
        return jsonify({'message': 'Conversation deleted successfully'}), 200
    return jsonify({'error': 'Conversation not found'}), 404
