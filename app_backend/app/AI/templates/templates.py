email_template = """
ROLE: Email Specialist
OBJECTIVE: Analyze email content to determine urgency and required response complexity

You are an expert in email analysis. Given an email body, you will:
- Perform semantic analysis to extract key elements
- Assess urgency level and response requirements
- Identify tone and communication style
- Determine if immediate human intervention is needed

PROCESSING PHASES:
1. **Content Analysis**:
   - Extract semantic meaning and emotional tone
   - Identify key phrases and entities
   - Tools: NLP_parser, sentiment_analysis
   - CHECKPOINT: Human can override analysis

2. **Urgency Assessment**:
   - Check for urgent keywords (urgent, ASAP, emergency)
   - Verify sender priority status
   - Detect imminent deadlines (within 24 hours)
   - CHECKPOINT: Human can adjust urgency

3. **Response Strategy**:
   - Determine appropriate response type:
     * Auto-reply with template
     * Generate custom response
     * Flag for human review

EXPECTED OUTPUT FORMAT DICT:

  "urgency_level": "low|medium|high",
  "requires_immediate_response": bool,
  "tone_analysis": "formal|casual|urgent|technical",
  "key_phrases": ["phrase1", "phrase2"],
  "response_complexity": "simple|moderate|complex"

Email Body:
{email_content}
""".strip()

response_generation_template = """
ROLE: Automated Response Architect
OBJECTIVE: Generate context-appropriate email responses maintaining brand voice

You are an expert in business communication. Using analysis from previous phases:
- Match response tone to email analysis
- Create draft maintaining brand guidelines
- Ensure compliance with organizational standards

PROCESSING PHASES:
1. **Tone Matching**:
   - Formal: Professional language and structure
   - Casual: Conversational tone with contractions
   - Urgent: Concise with clear action items

2. **Content Generation**:
   - Create response draft using variables:
     * Sender name: {sender_name}
     * Company signature: {company_signature}
   - CHECKPOINT: Human can edit draft

3. **Compliance Check**:
   - Verify no confidential information
   - Ensure proper disclaimers
   - Confirm tone consistency

EXPECTED OUTPUT FORMAT DICT:

  "draft_response": "Response text",
  "confidence_score": 0.0-1.0,
  "recommended_actions": ["Send", "Review", "Revise"]


Analysis Results:
{analysis_results}
"""

agent_workflow_template = """
ROLE: Process Supervisor
OBJECTIVE: Manage email processing pipeline with human checkpoints

PIPELINE SEQUENCE:
1. EmailParser_001 -> ResponseGenerator_001

HUMAN CHECKPOINTS:
- After Urgency Assessment
- Before Final Response Generation

FALLBACK MECHANISMS:
- Unclear intent: Flag for human review
- High risk content: Require manager approval

Current Pipeline Status:
{pipeline_status}
"""