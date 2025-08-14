from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import requests
import json
from typing import Dict, Any
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS setup for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IBM Granite model configuration
GRANITE_MODEL_ID = "ibm-granite/granite-3.0-1b-a400m-instruct"

# Global variables for model and tokenizer
tokenizer = None
model = None

def load_granite_model():
    """Load IBM Granite model and tokenizer"""
    global tokenizer, model
    try:
        logger.info(f"Loading Granite model: {GRANITE_MODEL_ID}")
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(GRANITE_MODEL_ID, trust_remote_code=True)
        
        # Load model with appropriate device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        
        model = AutoModelForCausalLM.from_pretrained(
            GRANITE_MODEL_ID,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=True
        )
        
        if device == "cpu":
            model = model.to(device)
            
        logger.info("Granite model loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load Granite model: {e}")
        return False

def is_finance_related(query: str) -> bool:
    """Check if query is related to finance, tax, savings, loans, or financial laws"""
    finance_keywords = [
        # Core financial terms
        'finance', 'financial', 'money', 'budget', 'budgeting', 'income', 'expense', 'expenses',
        'savings', 'save', 'saving', 'investment', 'invest', 'investing', 'portfolio',
        'loan', 'loans', 'credit', 'debt', 'mortgage', 'interest', 'rate', 'rates',
        
        # Tax related
        'tax', 'taxes', 'taxation', 'deduction', 'deductions', 'refund', 'irs',
        'filing', 'return', 'exemption', 'taxable', 'income tax', 'gst', 'vat',
        
        # Banking and accounts
        'bank', 'banking', 'account', 'checking', 'deposit', 'withdrawal',
        'atm', 'card', 'payment', 'transaction', 'balance', 'statement',
        
        # Insurance and financial products
        'insurance', 'policy', 'premium', 'claim', 'retirement', 'pension',
        '401k', 'ira', 'mutual fund', 'etf', 'stock', 'stocks', 'bond', 'bonds',
        
        # Financial planning
        'goal', 'goals', 'planning', 'wealth', 'asset', 'assets', 'liability',
        'net worth', 'cash flow', 'emergency fund', 'financial plan',
        
        # Business finance
        'business', 'startup', 'revenue', 'profit', 'loss', 'accounting',
        'bookkeeping', 'invoice', 'payroll', 'entrepreneur',
        
        # Economic terms
        'economy', 'economic', 'inflation', 'recession', 'market', 'currency',
        'exchange', 'forex', 'commodity', 'real estate', 'property'
    ]
    
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in finance_keywords)

def run_granite_model(prompt: str, system_prompt: str = None) -> str:
    """
    Run IBM Granite 3.0 1B model for report generation
    """
    global tokenizer, model
    
    # Check if query is finance-related
    if not is_finance_related(prompt):
        return "I'm a specialized financial report generator. I can only analyze and generate reports for finance, tax, savings, loans, investments, and financial planning topics. Please provide financial data for report generation!"
    
    try:
        # Load model if not already loaded
        if model is None or tokenizer is None:
            if not load_granite_model():
                return f"[Granite Model Error] Failed to load model. Using structured report instead.\n\n{generate_structured_report(prompt)}"
        
        # Prepare the prompt with financial focus (ultra-short for speed)
        if system_prompt:
            full_prompt = f"Analyze: {prompt[:200]}... Report:"
        else:
            full_prompt = f"Financial Report: {prompt[:200]}... Analysis:"
        
        # Tokenize input with minimal context for maximum speed
        inputs = tokenizer(full_prompt, return_tensors="pt", truncation=True, max_length=512)
        
        # Move to same device as model
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate response with ultra-fast parameters
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,  # Even shorter for speed
                temperature=0.5,     # Lower for consistency
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.05,
                top_p=0.7,          # More focused sampling
                num_beams=1,        # Single beam for speed
                early_stopping=True  # Stop early when possible
            )
        
        # Decode the response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part (after "Assistant:")
        if "Assistant:" in response:
            generated_text = response.split("Assistant:")[-1].strip()
        else:
            generated_text = response[len(full_prompt):].strip()
        
        # Combine with structured report for comprehensive output
        structured_report = generate_structured_report(prompt)
        final_response = f"[IBM Granite 3.0-1B Analysis]\n{generated_text}\n\n{structured_report}"
        
        return final_response
        
    except Exception as e:
        logger.error(f"Granite model inference error: {e}")
        return f"[Granite Model Error] {str(e)}\n\nFallback to structured report:\n\n{generate_structured_report(prompt)}"

def generate_structured_report(raw_content: str) -> str:
    """
    Generate structured financial report from raw content
    This function processes the input and formats it into a proper structure
    """
    # Parse raw content to extract financial data
    lines = raw_content.strip().split('\n')
    report_data = {}
    
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            report_data[key.strip().lower()] = value.strip()
    
    # Generate structured report
    report = f"""
╔════════════════════════════════════════════════════════════╗
║                    FINANCIAL ANALYSIS REPORT               ║
╚════════════════════════════════════════════════════════════╝

📊 FINANCIAL OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Monthly Income:     ${report_data.get('income', 'N/A')}
Monthly Expenses:   ${report_data.get('expenses', 'N/A')}
Net Savings:        ${float(report_data.get('income', 0)) - float(report_data.get('expenses', 0)) if report_data.get('income') and report_data.get('expenses') else 'N/A'}

🎯 FINANCIAL GOALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Primary Goal:       {report_data.get('goal', 'No goal specified')}
Target Amount:      ${report_data.get('goal_amount', 'N/A')}
User Type:          {report_data.get('user_type', 'Not specified').title()}

📈 FINANCIAL ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{analyze_financial_health(report_data)}

💡 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{generate_recommendations(report_data)}

📋 ACTION ITEMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{generate_action_items(report_data)}

═══════════════════════════════════════════════════════════════
Report Generated by: IBM Granite 3.0-1B Financial Assistant
Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
═══════════════════════════════════════════════════════════════
"""
    return report

def analyze_financial_health(data: Dict[str, Any]) -> str:
    """Analyze financial health based on input data"""
    try:
        income = float(data.get('income', 0))
        expenses = float(data.get('expenses', 0))
        
        if income == 0:
            return "• Insufficient data for comprehensive analysis"
        
        savings_rate = ((income - expenses) / income) * 100
        
        analysis = []
        
        if savings_rate > 20:
            analysis.append(f"• Excellent savings rate: {savings_rate:.1f}% (Above recommended 20%)")
        elif savings_rate > 10:
            analysis.append(f"• Good savings rate: {savings_rate:.1f}% (Above minimum 10%)")
        elif savings_rate > 0:
            analysis.append(f"• Low savings rate: {savings_rate:.1f}% (Below recommended 10%)")
        else:
            analysis.append(f"• Negative savings: {savings_rate:.1f}% (Expenses exceed income)")
        
        expense_ratio = (expenses / income) * 100
        analysis.append(f"• Expense ratio: {expense_ratio:.1f}% of income")
        
        if expense_ratio > 80:
            analysis.append("• High expense ratio - requires immediate attention")
        elif expense_ratio > 70:
            analysis.append("• Moderate expense ratio - room for improvement")
        else:
            analysis.append("• Healthy expense ratio - good financial discipline")
            
        return '\n'.join(analysis)
        
    except (ValueError, TypeError):
        return "• Unable to analyze due to invalid financial data"

def generate_recommendations(data: Dict[str, Any]) -> str:
    """Generate personalized recommendations"""
    recommendations = []
    
    try:
        income = float(data.get('income', 0))
        expenses = float(data.get('expenses', 0))
        user_type = data.get('user_type', 'general')
        
        if income > expenses:
            recommendations.append("• Continue maintaining positive cash flow")
            recommendations.append("• Consider increasing savings rate to 20% if possible")
        else:
            recommendations.append("• Urgent: Review and reduce monthly expenses")
            recommendations.append("• Create a detailed budget to track spending")
        
        if user_type == 'student':
            recommendations.append("• Focus on building emergency fund (3-6 months expenses)")
            recommendations.append("• Consider part-time income opportunities")
            recommendations.append("• Look into student-specific financial products")
        elif user_type == 'professional':
            recommendations.append("• Maximize employer retirement contributions")
            recommendations.append("• Consider diversifying income streams")
            recommendations.append("• Review insurance coverage adequacy")
        
        goal_amount = data.get('goal_amount')
        if goal_amount:
            try:
                monthly_savings_needed = float(goal_amount) / 12
                recommendations.append(f"• To reach your goal in 1 year, save ${monthly_savings_needed:.2f} monthly")
            except (ValueError, TypeError):
                pass
    
    except (ValueError, TypeError):
        recommendations.append("• Ensure accurate financial data for better recommendations")
    
    return '\n'.join(recommendations) if recommendations else "• Please provide complete financial data for personalized recommendations"

def generate_action_items(data: Dict[str, Any]) -> str:
    """Generate specific action items"""
    actions = [
        "1. Set up automatic savings transfer for consistent saving habit",
        "2. Review and categorize all monthly expenses",
        "3. Create a monthly budget and stick to it",
        "4. Track progress toward financial goals weekly",
        "5. Review and update financial plan quarterly"
    ]
    
    try:
        income = float(data.get('income', 0))
        expenses = float(data.get('expenses', 0))
        
        if expenses >= income:
            actions.insert(0, "PRIORITY: Immediately reduce expenses or increase income")
        
        if data.get('goal') and not data.get('goal_amount'):
            actions.append("6. Define specific monetary target for your financial goal")
            
    except (ValueError, TypeError):
        pass
    
    return '\n'.join(actions)

@app.on_event("startup")
async def startup_event():
    """Load the Granite model on startup"""
    logger.info("Starting Financial Report Generator with IBM Granite 3.0-1B")
    load_granite_model()

@app.post("/generate-report")
async def generate_report(request: Request):
    """
    Generate structured financial report from raw content using IBM Granite model
    """
    data = await request.json()
    raw_content = data.get("raw_content", "")
    report_type = data.get("report_type", "financial_summary")
    
    if not raw_content:
        return {"error": "No raw content provided"}
    
    # System prompt for Granite model
    system_prompt = f"""You are a professional financial advisor using IBM Granite AI. 
    Generate a comprehensive, well-structured financial report based on the provided data. 
    Focus on clarity, actionable insights, and professional formatting.
    Report type: {report_type}"""
    
    # Generate report using Granite model
    report = run_granite_model(raw_content, system_prompt)
    
    return {
        "report": report,
        "model": GRANITE_MODEL_ID,
        "report_type": report_type,
        "status": "success"
    }

@app.post("/analyze-session")
async def analyze_session(request: Request):
    """
    Analyze saved session data and generate comprehensive report
    """
    data = await request.json()
    session_id = data.get("session_id")
    
    if not session_id:
        return {"error": "Session ID required"}
    
    try:
        # Retrieve session from database
        conn = sqlite3.connect("financebot.db")
        c = conn.cursor()
        c.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        row = c.fetchone()
        conn.close()
        
        if not row:
            return {"error": "Session not found"}
        
        # Convert session data to raw content format
        keys = ["id", "user_type", "chat_history", "income", "expenses", "goal", "goal_amount", "created_at"]
        session = dict(zip(keys, row))
        
        raw_content = f"""
user_type: {session['user_type']}
income: {session['income']}
expenses: {session['expenses']}
goal: {session['goal']}
goal_amount: {session['goal_amount']}
chat_history: {session['chat_history']}
        """.strip()
        
        # Generate report
        system_prompt = """You are a professional financial advisor using IBM Granite AI. 
        Generate a comprehensive financial analysis report based on the session data. 
        Include trends, patterns, and actionable recommendations."""
        
        report = run_granite_model(raw_content, system_prompt)
        
        return {
            "report": report,
            "session_data": session,
            "model": GRANITE_MODEL_ID,
            "status": "success"
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model": GRANITE_MODEL_ID,
        "service": "Financial Report Generator"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
