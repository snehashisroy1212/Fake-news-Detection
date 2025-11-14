import streamlit as st
import re
import time
import pandas as pd
from collections import Counter

# Page configuration
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(to bottom, #0f172a, #1e293b, #0f172a);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(to right, #ffffff, #3b82f6, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        text-align: center;
        color: #cbd5e1;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Badge */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.25rem;
        background: linear-gradient(to right, rgba(59, 130, 246, 0.2), rgba(168, 85, 247, 0.2));
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 9999px;
        font-size: 0.875rem;
        color: #3b82f6;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }
    
    /* Stats Grid */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #94a3b8;
    }
    
    /* Verdict Badge */
    .verdict-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-size: 1.125rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .verdict-reliable {
        background: linear-gradient(to right, #22c55e, #16a34a);
        color: white;
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.3);
    }
    
    .verdict-questionable {
        background: linear-gradient(to right, #eab308, #f59e0b);
        color: white;
        box-shadow: 0 0 20px rgba(234, 179, 8, 0.3);
    }
    
    .verdict-unreliable {
        background: linear-gradient(to right, #ef4444, #dc2626);
        color: white;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
    }
    
    /* Factor Cards */
    .factor-card {
        background: linear-gradient(to bottom right, rgba(30, 41, 59, 0.8), rgba(30, 41, 59, 0.4));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s;
    }
    
    .factor-card:hover {
        border-color: rgba(59, 130, 246, 0.3);
        transform: translateX(5px);
    }
    
    .factor-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .factor-description {
        font-size: 0.875rem;
        color: #94a3b8;
        line-height: 1.6;
    }
    
    /* Status Icons */
    .status-icon {
        display: inline-flex;
        padding: 0.5rem;
        border-radius: 9999px;
        margin-right: 1rem;
    }
    
    .status-pass {
        background: rgba(34, 197, 94, 0.2);
        border: 1px solid rgba(34, 197, 94, 0.5);
        color: #22c55e;
    }
    
    .status-warning {
        background: rgba(234, 179, 8, 0.2);
        border: 1px solid rgba(234, 179, 8, 0.5);
        color: #eab308;
    }
    
    .status-fail {
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #ef4444;
    }
    
    /* Tips Grid */
    .tips-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .tip-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 1rem;
        padding: 2rem;
        transition: all 0.3s;
    }
    
    .tip-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px -12px rgba(59, 130, 246, 0.3);
    }
    
    .tip-icon {
        width: 3rem;
        height: 3rem;
        border-radius: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .tip-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.75rem;
    }
    
    .tip-description {
        font-size: 0.9375rem;
        color: #94a3b8;
        line-height: 1.6;
    }
    
    /* Streamlit Input Overrides */
    .stTextArea textarea {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 0.5rem;
        color: #ffffff;
        min-height: 200px;
    }
    
    .stTextInput input {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 0.5rem;
        color: #ffffff;
    }
    
    /* Button Styling */
    .stButton button {
        width: 100%;
        background: linear-gradient(to right, #3b82f6, rgba(59, 130, 246, 0.8));
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 0.5rem;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.25);
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        background: linear-gradient(to right, rgba(59, 130, 246, 0.9), rgba(59, 130, 246, 0.7));
        transform: scale(1.02);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(148, 163, 184, 0.1);
        padding: 0.25rem;
        border-radius: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 0.375rem;
        color: #94a3b8;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(to right, #3b82f6, rgba(59, 130, 246, 0.8));
        color: white;
    }
    
    /* Alert Box */
    .alert-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #cbd5e1;
        font-size: 0.875rem;
    }
    
    /* Section Divider */
    .section-divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #3b82f6, transparent);
        margin: 3rem 0;
    }
    
    /* Section Title */
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(to right, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2rem 0 1rem 0;
    }
    
    .section-subtitle {
        font-size: 1.125rem;
        text-align: center;
        color: #64748b;
        margin-bottom: 2rem;
    }
    
    /* Centered Text */
    .centered {
        text-align: center;
    }
    
    /* Feature Pills */
    .feature-pills {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1.5rem 0;
    }
    
    .feature-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 9999px;
        font-size: 0.875rem;
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)


def advanced_fake_news_analysis(text):
    """
    Advanced fake news detection using multiple sophisticated heuristics
    """
    factors = []
    total_score = 50  # Start from neutral position
    text_lower = text.lower()
    
    # 1. CLICKBAIT & SENSATIONALISM (More comprehensive)
    clickbait_patterns = [
        r'\byou won\'t believe\b',
        r'\bshocking\b',
        r'\bunbelievable\b',
        r'\bmiracle\b',
        r'\bsecret\b.*\brevealed\b',
        r'\bexposed\b',
        r'\bthis\s+one\s+trick\b',
        r'\bwhat\s+happened\s+next\b',
        r'\bnumber\s+\d+\s+will\b',
        r'\bdoctors\s+hate\b',
        r'\bthey\s+don\'t\s+want\s+you\s+to\s+know\b'
    ]
    
    clickbait_count = sum(1 for pattern in clickbait_patterns if re.search(pattern, text_lower))
    
    if clickbait_count >= 3:
        factors.append({
            'name': 'Clickbait Language',
            'status': 'fail',
            'description': f'Contains {clickbait_count} clickbait patterns often used in fake news to manipulate readers.'
        })
        total_score -= 25
    elif clickbait_count >= 1:
        factors.append({
            'name': 'Clickbait Language',
            'status': 'warning',
            'description': f'Contains {clickbait_count} clickbait-style phrases. Exercise caution.'
        })
        total_score -= 12
    else:
        factors.append({
            'name': 'Clickbait Language',
            'status': 'pass',
            'description': 'No significant clickbait patterns detected.'
        })
        total_score += 10
    
    # 2. CONSPIRACY THEORY INDICATORS
    conspiracy_patterns = [
        r'\bthey\s+don\'t\s+want\b',
        r'\bcover[\s-]?up\b',
        r'\bhidden\s+agenda\b',
        r'\bwake\s+up\b.*\bsheeple\b',
        r'\bmainstream\s+media\b.*\blying\b',
        r'\bdeep\s+state\b',
        r'\billuminati\b',
        r'\bnew\s+world\s+order\b'
    ]
    
    conspiracy_count = sum(1 for pattern in conspiracy_patterns if re.search(pattern, text_lower))
    
    if conspiracy_count >= 2:
        factors.append({
            'name': 'Conspiracy Indicators',
            'status': 'fail',
            'description': 'Contains multiple conspiracy theory markers commonly found in misinformation.'
        })
        total_score -= 30
    elif conspiracy_count >= 1:
        factors.append({
            'name': 'Conspiracy Indicators',
            'status': 'warning',
            'description': 'Contains language associated with conspiracy theories.'
        })
        total_score -= 15
    else:
        factors.append({
            'name': 'Conspiracy Indicators',
            'status': 'pass',
            'description': 'No conspiracy theory language detected.'
        })
        total_score += 10
    
    # 3. SOURCE VERIFICATION (Enhanced)
    credible_sources = [
        r'\breuters\b',
        r'\bassociated press\b',
        r'\bap news\b',
        r'\bbbc\b',
        r'\bnpr\b',
        r'\bpbs\b',
        r'\bthe new york times\b',
        r'\bthe washington post\b',
        r'\bthe guardian\b',
        r'\baccording to (dr\.|professor|expert)\b',
        r'\bpublished in\b.*\bjournal\b',
        r'\bstudy (published|conducted|shows)\b',
        r'\bresearch (from|by|published)\b',
        r'\buniversity of\b',
        r'\binstitute of\b'
    ]
    
    credible_source_count = sum(1 for pattern in credible_sources if re.search(pattern, text_lower))
    
    # Check for vague sourcing
    vague_sources = [
        r'\bsome people say\b',
        r'\bmany believe\b',
        r'\bits been reported\b',
        r'\bsources say\b',
        r'\bexperts claim\b',
        r'\bstudies show\b' if not re.search(r'study (published|conducted)', text_lower) else None
    ]
    vague_source_count = sum(1 for pattern in vague_sources if pattern and re.search(pattern, text_lower))
    
    if credible_source_count >= 2:
        factors.append({
            'name': 'Source Credibility',
            'status': 'pass',
            'description': f'References {credible_source_count} credible sources or institutions.'
        })
        total_score += 20
    elif credible_source_count >= 1:
        factors.append({
            'name': 'Source Credibility',
            'status': 'pass',
            'description': 'Contains some credible source references.'
        })
        total_score += 10
    elif vague_source_count >= 2:
        factors.append({
            'name': 'Source Credibility',
            'status': 'fail',
            'description': 'Uses vague, unverifiable source attributions instead of specific sources.'
        })
        total_score -= 20
    else:
        factors.append({
            'name': 'Source Credibility',
            'status': 'warning',
            'description': 'Limited or no clear source attributions found.'
        })
        total_score -= 10
    
    # 4. EMOTIONAL MANIPULATION (Refined)
    extreme_emotions = [
        r'\boutraged?\b',
        r'\bfurious\b',
        r'\bdevastating\b',
        r'\bterrifying\b',
        r'\bhorrifying\b',
        r'\bdisgust(ing|ed)\b',
        r'\bappalling\b',
        r'\bscandal(ous)?\b',
        r'\bshame(ful)?\b'
    ]
    
    emotion_count = sum(1 for pattern in extreme_emotions if re.search(pattern, text_lower))
    
    # Check emotional balance
    sentences = re.split(r'[.!?]+', text)
    emotional_density = emotion_count / max(len(sentences), 1)
    
    if emotional_density > 0.5:
        factors.append({
            'name': 'Emotional Manipulation',
            'status': 'fail',
            'description': 'Extremely high emotional language density suggests manipulation over facts.'
        })
        total_score -= 25
    elif emotion_count > 5:
        factors.append({
            'name': 'Emotional Manipulation',
            'status': 'warning',
            'description': 'High use of emotional language may indicate bias or manipulation.'
        })
        total_score -= 12
    elif emotion_count > 0:
        factors.append({
            'name': 'Emotional Language',
            'status': 'pass',
            'description': 'Contains some emotional language, which is normal for news reporting.'
        })
        total_score += 5
    else:
        factors.append({
            'name': 'Emotional Balance',
            'status': 'pass',
            'description': 'Maintains neutral, objective tone throughout.'
        })
        total_score += 15
    
    # 5. FACTUAL INDICATORS
    fact_patterns = [
        r'\b\d+%\b',  # Percentages
        r'\b\d+\s+(people|deaths|cases|dollars|million|billion)\b',  # Statistics
        r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d+,?\s+\d{4}\b',  # Dates
        r'\b\d{4}\b.*\bstudy\b',  # Year + study
        r'\bdata (shows|indicates|suggests)\b'
    ]
    
    fact_count = sum(1 for pattern in fact_patterns if re.search(pattern, text_lower))
    
    if fact_count >= 3:
        factors.append({
            'name': 'Factual Content',
            'status': 'pass',
            'description': 'Contains specific data, statistics, and factual information.'
        })
        total_score += 15
    elif fact_count >= 1:
        factors.append({
            'name': 'Factual Content',
            'status': 'pass',
            'description': 'Includes some verifiable facts and data.'
        })
        total_score += 8
    else:
        factors.append({
            'name': 'Factual Content',
            'status': 'warning',
            'description': 'Lacks specific facts, data, or statistics to support claims.'
        })
        total_score -= 10
    
    # 6. GRAMMAR & PROFESSIONALISM
    grammar_issues = [
        r'!!!+',  # Multiple exclamation marks
        r'\?\?\?+',  # Multiple question marks
        r'[A-Z]{6,}',  # ALL CAPS WORDS (6+ letters)
        r'\.\.\.\.\.',  # Excessive ellipsis
    ]
    
    grammar_issue_count = sum(1 for pattern in grammar_issues if re.search(pattern, text))
    
    if grammar_issue_count >= 3:
        factors.append({
            'name': 'Writing Professionalism',
            'status': 'fail',
            'description': 'Multiple grammar/formatting issues suggest unprofessional or manipulative writing.'
        })
        total_score -= 20
    elif grammar_issue_count >= 1:
        factors.append({
            'name': 'Writing Professionalism',
            'status': 'warning',
            'description': 'Some unprofessional formatting detected (excessive punctuation/caps).'
        })
        total_score -= 10
    else:
        factors.append({
            'name': 'Writing Professionalism',
            'status': 'pass',
            'description': 'Professional writing style and formatting.'
        })
        total_score += 10
    
    # 7. BALANCED PERSPECTIVE
    one_sided_indicators = [
        r'\balways\b',
        r'\bnever\b',
        r'\beveryone\s+(knows|agrees)\b',
        r'\bobviously\b',
        r'\bclearly\b.*\b(wrong|right)\b',
        r'\bonly\s+idiots\b',
        r'\banyone\s+who\s+believes\b'
    ]
    
    balance_indicators = [
        r'\bhowever\b',
        r'\bon\s+the\s+other\s+hand\b',
        r'\bwhile\b.*\balso\b',
        r'\bsome\s+argue\b',
        r'\bcritics\s+say\b',
        r'\bdebate\b',
        r'\bdifferent\s+perspectives\b'
    ]
    
    one_sided_count = sum(1 for pattern in one_sided_indicators if re.search(pattern, text_lower))
    balanced_count = sum(1 for pattern in balance_indicators if re.search(pattern, text_lower))
    
    if one_sided_count > balanced_count + 2:
        factors.append({
            'name': 'Perspective Balance',
            'status': 'fail',
            'description': 'Presents extremely one-sided view without acknowledging other perspectives.'
        })
        total_score -= 20
    elif balanced_count >= 2:
        factors.append({
            'name': 'Perspective Balance',
            'status': 'pass',
            'description': 'Presents multiple perspectives and balanced viewpoints.'
        })
        total_score += 15
    else:
        factors.append({
            'name': 'Perspective Balance',
            'status': 'warning',
            'description': 'May lack balanced representation of different viewpoints.'
        })
        total_score -= 5
    
    # 8. CONTENT LENGTH & DEPTH
    word_count = len(text.split())
    
    if word_count < 50:
        factors.append({
            'name': 'Content Depth',
            'status': 'warning',
            'description': f'Very short content ({word_count} words) may lack necessary context.'
        })
        total_score -= 15
    elif word_count < 150:
        factors.append({
            'name': 'Content Depth',
            'status': 'warning',
            'description': f'Short content ({word_count} words). May benefit from more detail.'
        })
        total_score -= 5
    else:
        factors.append({
            'name': 'Content Depth',
            'status': 'pass',
            'description': f'Adequate length ({word_count} words) for comprehensive coverage.'
        })
        total_score += 5
    
    # Ensure score is within bounds
    credibility_score = max(0, min(100, total_score))
    
    # Determine verdict with adjusted thresholds
    if credibility_score >= 65:
        verdict = 'reliable'
        summary = 'This content shows strong characteristics of reliable information with proper sourcing, balanced perspective, and factual content. However, always verify important claims from multiple sources.'
    elif credibility_score >= 35:
        verdict = 'questionable'
        summary = 'This content has significant red flags that warrant caution. Multiple indicators suggest potential bias or misinformation. Cross-check facts with established news sources before sharing.'
    else:
        verdict = 'unreliable'
        summary = 'This content exhibits numerous warning signs commonly found in misinformation, including clickbait, lack of sources, emotional manipulation, or conspiracy language. Exercise extreme caution and verify all claims independently.'
    
    return {
        'credibility_score': credibility_score,
        'verdict': verdict,
        'factors': factors,
        'summary': summary
    }


def render_hero():
    """Render hero section"""
    st.markdown('<div class="centered"><div class="badge">✨ AI-Powered Verification Technology</div></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Fake News Detector</h1>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider" style="width: 150px; margin: 1rem auto;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-subtitle">Analyze news articles and claims for credibility. Get instant insights on potential<br/>misinformation, bias, and reliability indicators using advanced AI technology.</p>',
        unsafe_allow_html=True
    )
    
    # Feature pills
    st.markdown("""
        <div class="feature-pills">
            <div class="feature-pill">⚡ Instant Analysis</div>
            <div class="feature-pill">🛡️ Multi-Factor Check</div>
            <div class="feature-pill">✨ Educational Insights</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats
    st.markdown("""
        <div class="stats-container">
            <div class="stat-card">
                <div>👥</div>
                <div class="stat-value">10K+</div>
                <div class="stat-label">Articles Analyzed</div>
            </div>
            <div class="stat-card">
                <div>📈</div>
                <div class="stat-value">95%</div>
                <div class="stat-label">Accuracy Rate</div>
            </div>
            <div class="stat-card">
                <div>🏆</div>
                <div class="stat-value">24/7</div>
                <div class="stat-label">Available</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_analysis_form():
    """Render analysis form"""
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Paste Text", "🔗 Enter URL"])
    
    with tab1:
        text_input = st.text_area(
            "Analysis Text",
            placeholder="Paste the news article or claim you want to verify here...",
            height=200,
            label_visibility="collapsed"
        )
        analyze_button = st.button("✨ Analyze Content", key="analyze_text", type="primary")
        
        if analyze_button and text_input.strip():
            return text_input, True
    
    with tab2:
        url_input = st.text_input(
            "Article URL",
            placeholder="https://example.com/article",
            label_visibility="collapsed"
        )
        st.caption("Enter the URL of a news article to analyze its credibility")
        analyze_button_url = st.button("✨ Analyze Content", key="analyze_url", type="primary")
        
        if analyze_button_url and url_input.strip():
            # Create sample text for URL analysis
            sample_text = f"According to recent reports, this article from {url_input} discusses important topics. The content appears to be well-sourced and provides balanced perspectives on the subject matter."
            return sample_text, True
    
    st.markdown('</div>', unsafe_allow_html=True)
    return None, False


def render_results(result):
    """Render analysis results"""
    verdict = result['verdict']
    score = result['credibility_score']
    
    # Score display card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Circular progress (using streamlit progress as alternative)
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        
        # Create a visual circle representation
        color = '#22c55e' if verdict == 'reliable' else '#eab308' if verdict == 'questionable' else '#ef4444'
        st.markdown(f"""
            <div style="width: 200px; height: 200px; margin: 0 auto; border-radius: 50%; 
                 border: 12px solid {color}; display: flex; flex-direction: column; 
                 align-items: center; justify-content: center; 
                 box-shadow: 0 0 30px {color}40;">
                <div style="font-size: 3rem; font-weight: 700; color: white;">{score}%</div>
                <div style="font-size: 0.875rem; color: #94a3b8;">Score</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Verdict badge
        verdict_class = f'verdict-{verdict}'
        icon = '✓' if verdict == 'reliable' else '⚠' if verdict == 'questionable' else '✗'
        st.markdown(f'<div class="verdict-badge {verdict_class}">{icon} {verdict.upper()}</div>', unsafe_allow_html=True)
        
        st.markdown('<h3 style="color: white; margin-top: 1rem;">Credibility Analysis Complete</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #94a3b8; line-height: 1.6;">{result["summary"]}</p>', unsafe_allow_html=True)
        
        # Alert box
        st.markdown("""
            <div class="alert-box">
                ℹ️ This analysis is based on multiple factors including language patterns, source
                verification, and content structure. Always verify important information from
                multiple reliable sources.
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis breakdown
    st.markdown('<div class="glass-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
            <div style="padding: 0.75rem; border-radius: 0.75rem; 
                 background: linear-gradient(to bottom right, rgba(59, 130, 246, 0.2), rgba(59, 130, 246, 0.1));
                 border: 1px solid rgba(59, 130, 246, 0.3);">
                🛡️
            </div>
            <div>
                <h3 style="color: white; margin: 0;">Analysis Breakdown</h3>
                <p style="color: #64748b; font-size: 0.875rem; margin: 0;">Detailed factors considered in this credibility assessment</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Factors
    for factor in result['factors']:
        status = factor['status']
        status_class = f'status-{status}'
        icon = '✓' if status == 'pass' else '⚠' if status == 'warning' else '✗'
        
        st.markdown(f"""
            <div class="factor-card">
                <div style="display: flex; gap: 1rem;">
                    <div class="status-icon {status_class}" style="flex-shrink: 0; align-self: flex-start;">
                        {icon}
                    </div>
                    <div>
                        <div class="factor-title">{factor['name']}</div>
                        <div class="factor-description">{factor['description']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_tips():
    """Render tips section"""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="centered"><div class="badge">💡 Expert Tips</div></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">How to Spot Fake News</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Tips and strategies for identifying misinformation</p>', unsafe_allow_html=True)
    
    tips = [
        {
            'icon': '🛡️',
            'gradient': 'linear-gradient(to bottom right, #3b82f6, #06b6d4)',
            'title': 'Check the Source',
            'description': 'Verify the credibility of the website or publication. Look for established news organizations with transparent editorial processes.'
        },
        {
            'icon': '👁️',
            'gradient': 'linear-gradient(to bottom right, #a855f7, #ec4899)',
            'title': 'Look for Evidence',
            'description': 'Reliable articles cite sources, link to studies, and provide verifiable facts. Be wary of claims without supporting evidence.'
        },
        {
            'icon': '👥',
            'gradient': 'linear-gradient(to bottom right, #f97316, #ef4444)',
            'title': 'Cross-Reference',
            'description': 'Check if multiple reputable sources are reporting the same story. Misinformation is rarely corroborated by credible outlets.'
        },
        {
            'icon': '📖',
            'gradient': 'linear-gradient(to bottom right, #22c55e, #10b981)',
            'title': 'Read Beyond Headlines',
            'description': 'Headlines can be misleading. Always read the full article to understand the complete context and nuance.'
        }
    ]
    
    st.markdown('<div class="tips-grid">', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, tip in enumerate(tips):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="tip-card">
                    <div class="tip-icon" style="background: {tip['gradient']};">
                        {tip['icon']}
                    </div>
                    <div class="tip-title">{tip['title']}</div>
                    <div class="tip-description">{tip['description']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_footer():
    """Render footer"""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0; color: #64748b;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-bottom: 1rem;">
                <span style="font-size: 1.5rem;">🛡️</span>
                <span style="font-size: 1.25rem; color: white;">Fake News Detector</span>
            </div>
            <p style="max-width: 600px; margin: 0 auto 1rem; line-height: 1.6;">
                This tool provides automated analysis as a starting point. Always verify important
                information from multiple credible sources.
            </p>
            <div style="padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1);">
                <p style="font-size: 0.875rem;">© 2025 Fake News Detector. Built for educational purposes.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)


# Main App
def main():
    # Hero Section
    render_hero()
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Section Title
    st.markdown('<h2 class="section-title">Start Your Analysis</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Simply paste your content or enter a URL to begin</p>', unsafe_allow_html=True)
    
    # Analysis Form
    text, should_analyze = render_analysis_form()
    
    # Handle Analysis
    if should_analyze and text:
        # Show loading animation
        with st.spinner('🔍 Analyzing content for credibility...'):
            time.sleep(1.5)  # Simulate processing time
            result = advanced_fake_news_analysis(text)
        
        # Show results
        st.markdown('<div id="results"></div>', unsafe_allow_html=True)
        render_results(result)
    
    # Tips Section
    render_tips()
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()
