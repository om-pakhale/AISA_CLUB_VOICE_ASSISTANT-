import os
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AISA Voice Assistant", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0.8rem;
        padding-bottom: 0.8rem;
        max-width: 720px;
    }
    .club-header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .club-logo {
        width: 78px;
        height: 78px;
        object-fit: contain;
        border-radius: 50%;
        margin-bottom: 6px;
        box-shadow: 0 0 16px rgba(14, 165, 233, 0.4);
        border: 2px solid rgba(14, 165, 233, 0.6);
    }
    .main-title {
        font-size: 1.55rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0;
        line-height: 1.25;
    }
    .sub-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #38bdf8;
        margin-top: 3px;
        margin-bottom: 2px;
    }
    .dept-caption {
        font-size: 0.84rem;
        color: #94a3b8;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Detect and base64-encode logo file
logo_base64 = ""
for filename in ["logo.png", "aisa_logo.png", "logo.jpg", "logo.jpeg"]:
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            ext = filename.split(".")[-1]
            logo_base64 = f"data:image/{ext};base64,{encoded}"
        break

logo_html = f'<img src="{logo_base64}" class="club-logo" alt="AISA Logo">' if logo_base64 else ""

st.markdown(f"""
<div class="club-header-container">
    {logo_html}
    <h1 class="main-title">Artificial Intelligence Students Association</h1>
    <div class="sub-title">AISA Voice Assistant</div>
    <p class="dept-caption">Department of CSE (AI & ML) - DKTE</p>
</div>
""", unsafe_allow_html=True)

# Component with 680px frame and auto-fit inner containment
components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    html, body {
        margin: 0;
        padding: 4px 6px 16px 6px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background: transparent;
        color: #f8fafc;
        display: flex;
        flex-direction: column;
        align-items: center;
        user-select: none;
        box-sizing: border-box;
    }

    #start-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(15, 23, 42, 0.96);
        display: none;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        text-align: center;
        padding: 20px;
        box-sizing: border-box;
    }

    #start-btn {
        background: linear-gradient(135deg, #0ea5e9, #0284c7);
        color: #ffffff;
        border: none;
        padding: 16px 36px;
        font-size: 1.25rem;
        font-weight: 600;
        border-radius: 50px;
        cursor: pointer;
        box-shadow: 0 0 25px rgba(14, 165, 233, 0.6);
        outline: none;
        transition: transform 0.2s ease;
    }

    #start-btn:active {
        transform: scale(0.96);
    }

    .orb-wrapper {
        position: relative;
        width: 125px;
        height: 125px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 4px auto;
        flex-shrink: 0;
    }

    .voice-orb {
        width: 88px;
        height: 88px;
        border-radius: 50%;
        background: radial-gradient(circle, #0ea5e9 0%, #0284c7 50%, #0369a1 100%);
        box-shadow: 0 0 16px rgba(14, 165, 233, 0.4);
        transition: all 0.25s ease;
    }

    .orb-idle {
        box-shadow: 0 0 15px rgba(14, 165, 233, 0.4);
        animation: orb-idle-spin 8s infinite linear, gentle-corners 3s infinite ease-in-out;
    }

    .orb-active {
        box-shadow: 0 0 26px rgba(14, 165, 233, 0.8), 0 0 42px rgba(2, 132, 199, 0.5);
        animation: orb-rotate-corners 2.4s infinite linear, orb-bounce 0.8s infinite alternate ease-in-out;
    }

    @keyframes orb-idle-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes gentle-corners {
        0% { border-radius: 50% 50% 50% 50%; }
        50% { border-radius: 48% 52% 49% 51%; }
        100% { border-radius: 50% 50% 50% 50%; }
    }

    @keyframes orb-rotate-corners {
        0% {
            border-radius: 45% 55% 52% 48% / 54% 46% 54% 46%;
            transform: rotate(0deg);
        }
        50% {
            border-radius: 54% 46% 47% 53% / 46% 54% 48% 52%;
            transform: rotate(180deg);
        }
        100% {
            border-radius: 45% 55% 52% 48% / 54% 46% 54% 46%;
            transform: rotate(360deg);
        }
    }

    @keyframes orb-bounce {
        0% { transform: scale(1.0); }
        50% { transform: scale(1.08); }
        100% { transform: scale(1.03); }
    }

    #status-hint {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 2px;
        height: 18px;
        flex-shrink: 0;
    }

    /* Auto-scrolling, high-visibility box for lengthy text */
    #answer-card {
        width: 92%;
        max-width: 580px;
        margin-top: 8px;
        padding: 14px 18px;
        background-color: #0b221a;
        border: 1.5px solid #10b981;
        border-radius: 10px;
        color: #a7f3d0;
        font-size: 1.02rem;
        line-height: 1.5;
        text-align: center;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        display: none;
        max-height: 220px;
        overflow-y: auto;
        word-wrap: break-word;
        box-sizing: border-box;
    }

    /* Custom smooth green scrollbar */
    #answer-card::-webkit-scrollbar {
        width: 5px;
    }
    #answer-card::-webkit-scrollbar-thumb {
        background: #10b981;
        border-radius: 4px;
    }
    #answer-card::-webkit-scrollbar-track {
        background: rgba(11, 34, 26, 0.8);
    }

    .word-stream {
        display: inline-block;
        opacity: 0;
        transform: translateY(3px);
        animation: word-fade-in 0.16s forwards ease-out;
        margin-right: 3px;
    }

    @keyframes word-fade-in {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
</head>
<body>

<div id="start-overlay">
    <button id="start-btn">🎙️ Tap to Start Assistant</button>
    <p style="color:#94a3b8; font-size: 0.95rem; margin-top: 15px;">One-time tap required for mobile mic & audio</p>
</div>

<div class="orb-wrapper">
    <div id="orb" class="voice-orb orb-idle"></div>
</div>
<div id="status-hint">Initializing assistant...</div>
<div id="answer-card"></div>

<script>
const RULES = [
    {
        intent: "what_is_aisa",
        en_tokens: ["what is aisa club", "what is aisa", "aisa club kya hai", "about aisa"],
        hi_tokens: ["aisa club kya hai", "aisa kya hai", "aisa ke bare me batao", "aisa kya h"],
        en: "AISA stands for the Artificial Intelligence Students Association in the Department of Computer Science and Engineering AI and ML at DKTE.",
        hi: "AISA stands for the Artificial Intelligence Students Association in the Department of Computer Science and Engineering AI and ML at DKTE."
    },
    {
        intent: "president",
        en_tokens: ["who is the president", "president", "adhyaksh", "current president", "who is president of aisa"],
        hi_tokens: ["president kaun hain", "president kon hai", "aisa ke president", "adhyaksh kaun hai"],
        en: "Mr. Arjun Jadhav is the President of the AISA club.",
        hi: "Mr. Arjun Jadhav AISA club ke President hain."
    },
    {
        intent: "vice_president",
        en_tokens: ["who is the vice president", "vice president", "upadhyaksh", "vc president", "who is vp"],
        hi_tokens: ["vice president kaun hain", "vice president kon hai", "upadhyaksh kaun hai"],
        en: "Miss. Trupti Varma is the Vice President of the AISA club.",
        hi: "Miss Trupti Varma AISA club ki Vice President hain."
    },
    {
        intent: "secretaries",
        en_tokens: ["who are the secretaries", "secretaries", "secretary", "sachiv"],
        hi_tokens: ["secretaries kaun hain", "secretaries kon hai", "sachiv kaun hai"],
        en: "Mr. Tanmay Chikhalikar and Mr. Ahmad Momin are the Secretaries of the AISA club.",
        hi: "Mr. Tanmay Chikhalikar aur Mr. Ahmad Momin AISA club ke Secretaries hain."
    },
    {
        intent: "treasurers",
        en_tokens: ["who are the treasurers", "treasurers", "treasurer", "koshadhyaksh"],
        hi_tokens: ["treasurers kaun hain", "treasurers kon hai", "koshadhyaksh kaun hai"],
        en: "Miss. Siddhi Kurle and Mr. Farhan Sheikh are the Treasurers of the AISA club.",
        hi: "Miss Siddhi Kurle aur Mr. Farhan Sheikh AISA club ke Treasurers hain."
    },
    {
        intent: "technical_directors",
        en_tokens: ["who are the technical directors", "technical directors", "technical director", "takniki nideshak"],
        hi_tokens: ["technical directors kaun hain", "technical director kon hai", "takniki nideshak"],
        en: "Miss. Saniya Kolar and Mr. Gous Bahurupi are the Technical Directors of the AISA club.",
        hi: "Miss Saniya Kolar aur Mr. Gous Bahurupi AISA club ke Technical Directors hain."
    },
    {
        intent: "technical_team",
        en_tokens: ["who are the technical team members", "technical team", "technical team members", "takniki team"],
        hi_tokens: ["technical team mein kaun kaun hai", "technical team kon hai", "takniki team"],
        en: "The technical team members are Mr. Om Pakhale, Mr. Samad Latkar, and Miss. Shubhangi Teke.",
        hi: "Technical team mein Mr. Om Pakhale, Mr. Samad Latkar aur Miss Shubhangi Teke hain."
    },
    {
        intent: "social_media",
        en_tokens: ["social media head", "social media team", "social media team members", "social media"],
        hi_tokens: ["social media head aur team members kaun hai", "social media head kon hai"],
        en: "Mr. Manthan Warte is the Social Media Team Head and The social media team members include Mr. Sushil Sapakal and Mr. Yash Ghatage.",
        hi: "Mr. Manthan Warte Social Media Team ke Head hain aur team members mein Mr. Sushil Sapakal aur Mr. Yash Ghatage hain."
    },
    {
        intent: "coordinator",
        en_tokens: ["who is the aisa coordinator", "aisa coordinator", "coordinator", "faculty coordinator", "kulkarni"],
        hi_tokens: ["aisa coordinator kaun hain", "coordinator kaun hai"],
        en: "Mrs. D. M. Kulkarni is the AISA Coordinator.",
        hi: "Mrs. D. M. Kulkarni AISA Coordinator hain."
    },
    {
        intent: "hod",
        en_tokens: ["who is the hod", "hod", "head of department", "hod of aiml", "shirgave"],
        hi_tokens: ["hod kaun hain", "aiml ke hod kaun hai"],
        en: "Prof. Dr. S. K. Shirgave is the HOD of CSE AIML.",
        hi: "Prof. Dr. S. K. Shirgave CSE AIML ke HOD hain."
    },
    {
        intent: "notice_date",
        en_tokens: ["date of the aisa notice", "aisa notice date", "notice date", "notice kab aaya"],
        hi_tokens: ["aisa notice ki date kya hai", "notice kab aaya tha"],
        en: "The notice was issued on 18/08/2026.",
        hi: "Notice 18 August 2026 ko jaari kiya gaya tha."
    },
    {
        intent: "techblitz_2026",
        en_tokens: ["what is techblitz 2026", "what is techblitz", "techblitz 2026 kya hai"],
        hi_tokens: ["techblitz 2026 kya hai", "techblitz ke bare me"],
        en: "TechBlitz 2026 is an inter-collegiate technical challenge provided by AISA, held on 1st September 2026 at CCL 2, consisting of three rounds with a team size of two and an entry fee of 100 rupees per team.",
        hi: "TechBlitz 2026 AISA dwara organized ek inter-collegiate technical challenge hai jo 1 September 2026 ko CCL 2 mein hua tha."
    },
    {
        intent: "previous_events",
        en_tokens: ["previous events of aisa", "past events", "pichle events", "what was the previous events"],
        hi_tokens: ["aisa ke pichle events kaun se the", "pichle events kaun se the"],
        en: "Previous events of AISA was The Legacy Exchange an alumni meet and TechBlitz a technical event.",
        hi: "AISA ke pichle events The Legacy Exchange jo ek alumni meet tha, aur TechBlitz jo ek technical event tha."
    },
    {
        intent: "what_was_techblitz",
        en_tokens: ["what was techblitz", "techblitz kya tha", "about techblitz"],
        hi_tokens: ["techblitz kya tha", "techblitz event kya tha"],
        en: "TechBlitz was a technical event organized by the AISA Artificial Intelligence Student Association which had The three rounds are Round 1 Aptitude Round, Round 2 Coding and Logic Challenge, and Round 3 Final or Surprise Round.",
        hi: "TechBlitz AISA dwara aayojit ek technical event tha jisme teen rounds the: Aptitude Round, Coding and Logic Challenge, aur Surprise Round."
    },
    {
        intent: "legacy_exchange",
        en_tokens: ["what is the legacy exchange", "legacy exchange kya hai", "what is legacy exchange", "legacy exchange"],
        hi_tokens: ["legacy exchange kya hai", "the legacy exchange kya hai"],
        en: "The Legacy Exchange is an alumni interaction initiative organized by AISA based on the motto Reconnect, Inspire, Empower, hosted by Tanmay and Drushti.",
        hi: "The Legacy Exchange AISA dwara aayojit ek alumni interaction initiative hai jiska motto Reconnect, Inspire, Empower hai."
    },
    {
        intent: "legacy_alumni",
        en_tokens: ["who was the alumni of the legacy exchange", "alumni of the legacy exchange", "alumni kaun the", "alumni of legacy"],
        hi_tokens: ["legacy exchange ke alumni kaun the", "alumni kaun the"],
        en: "Mr. Neeraj Mirashi, Sejal pandharpatte, Sanika Patil, Alisha Attar.",
        hi: "Alumni mein Mr. Neeraj Mirashi, Sejal Pandharpatte, Sanika Patil, aur Alisha Attar the."
    },
    {
        intent: "japan_alumni",
        en_tokens: ["alumni joining virtually from japan", "virtually from japan", "japan se kaun"],
        hi_tokens: ["japan se virtually kaun join kar raha hai", "japan se kaun"],
        en: "Ms. Sejal Pandharpatte is participating virtually from Japan.",
        hi: "Ms. Sejal Pandharpatte Japan se virtually participate kar rahi hain."
    },
    {
        intent: "motto",
        en_tokens: ["what is the motto of aisa", "motto of aisa", "aisa motto", "motto"],
        hi_tokens: ["aisa ka motto kya hai", "motto kya hai"],
        en: "The motto of AISA is Unite, Excel, Achieve.",
        hi: "AISA ka motto hai Unite, Excel, Achieve."
    },
    {
        intent: "purpose",
        en_tokens: ["what is the main purpose of aisa", "purpose of aisa", "main purpose", "objective of aisa"],
        hi_tokens: ["aisa ka main purpose kya hai", "aisa ka uddeshya kya hai"],
        en: "AISA promotes learning, innovation, technical skills and collaborative growth among students in Artificial Intelligence and related technologies.",
        hi: "AISA Artificial Intelligence aur related technologies mein students ke beech learning, innovation, aur collaborative growth ko promote karta hai."
    },
    {
        intent: "techblitz_participants",
        en_tokens: ["how many students participated in techblitz", "kitne students ne participate kiya", "participants in techblitz"],
        hi_tokens: ["techblitz mein kitne students ne participate kiya", "kitne students ne participate kiya"],
        en: "32 Teams were participated where 2 members per team.",
        hi: "32 Teams ne participate kiya tha jisme har team mein 2 members the."
    },
    {
        intent: "techblitz_date",
        en_tokens: ["when was techblitz conducted", "techblitz kab conduct kiya gaya", "date of techblitz"],
        hi_tokens: ["techblitz kab conduct kiya gaya", "techblitz kab hua tha"],
        en: "TECHBLITZ was conducted on 1st September 2026.",
        hi: "TECHBLITZ 1 September 2026 ko conduct kiya gaya tha."
    },
    {
        intent: "techblitz_skills",
        en_tokens: ["what skills were tested in techblitz", "skills were tested", "skills tested in techblitz"],
        hi_tokens: ["techblitz mein kaun si skills test hui", "kaun si skills test hui"],
        en: "The event tested logical reasoning, aptitude, problem-solving and technical skills.",
        hi: "Event mein logical reasoning, aptitude, problem-solving aur technical skills test ki gayi thi."
    },
    {
        intent: "techblitz_rounds",
        en_tokens: ["how many rounds were there in techblitz", "rounds were there in techblitz", "kitne rounds the"],
        hi_tokens: ["techblitz mein kitne rounds the", "kitne rounds the"],
        en: "There were three rounds.",
        hi: "Usme teen rounds the."
    },
    {
        intent: "ex_president",
        en_tokens: ["who was the aisa ex-president", "aisa ex-president", "ex president", "former president", "pichli president", "janhavi"],
        hi_tokens: ["aisa ki ex-president kaun thi", "ex-president kaun thi", "pichli president kaun thi"],
        en: "Miss Janhavi Kulkarni was the AISA EX-President.",
        hi: "Miss Janhavi Kulkarni AISA ki EX-President thi."
    },
    {
        intent: "ex_vice_president",
        en_tokens: ["who were the ex- vice president of aisa", "ex vice president", "former vice president", "pichle upadhyaksh"],
        hi_tokens: ["aisa ke ex-vice president kaun the", "ex-vice president kaun the"],
        en: "Miss Pranali Sawant and Mr. Athrav Koli were the AISA EX-Vice Presidents.",
        hi: "Miss Pranali Sawant aur Mr. Athrav Koli AISA ke EX-Vice Presidents the."
    },
    {
        intent: "upcoming_events",
        en_tokens: ["what are the upcoming events of aisa", "upcoming events", "aane wale events"],
        hi_tokens: ["aisa ke upcoming events kaun se hain", "upcoming events kaun se hain"],
        en: "The AISA Super Strikers A cricket battle, The freshers Party, TechSymposium Hackathon, and other technical and non-technical events will be organized soon by the AISA.",
        hi: "AISA jald hi The AISA Super Strikers cricket battle, Freshers Party, TechSymposium Hackathon, aur dusre events organize karega."
    },
    {
        intent: "volunteer_head",
        en_tokens: ["who is the volunteer head in aisa", "volunteer head", "volunteer head in aisa"],
        hi_tokens: ["aisa mein volunteer head kaun hai", "volunteer head kaun hai"],
        en: "Rohit Jadhav is a Volunteer Head in AISA.",
        hi: "Rohit Jadhav AISA mein Volunteer Head hain."
    },
    {
        intent: "volunteers",
        en_tokens: ["who are the volunteers", "volunteers kaun hain", "volunteers"],
        hi_tokens: ["volunteers kaun hain", "volunteers kon hai", "aisa ke volunteers"],
        en: "Manthan Soni, Shravani Asawale, Pradnya Desai, Anuradha Jadhav, Shivraj Banne, Sanskar Govare, Rajvardhini Mane, Maitrayee Jadhav, Harshwardhan Jiddi, Aftab Momin.",
        hi: "Volunteers hain Manthan Soni, Shravani Asawale, Pradnya Desai, Anuradha Jadhav, Shivraj Banne, Sanskar Govare, Rajvardhini Mane, Maitrayee Jadhav, Harshwardhan Jiddi, aur Aftab Momin."
    },
    {
        intent: "founder",
        en_tokens: ["founder of aisa", "founder", "first president"],
        hi_tokens: ["aisa ka founder kaun hai", "pehle president"],
        en: "Prithviraj Banne was the first president of AISA.",
        hi: "Prithviraj Banne AISA ke pehle president the."
    },
    {
        intent: "who_am_i",
        en_tokens: ["who am i", "mai kon hu", "main kaun hoon"],
        hi_tokens: ["mai kon hu", "main kaun hoon"],
        en: "You are Om Pakhale, part of the AISA Technical Team.",
        hi: "Aapka naam Om Pakhale hai."
    }
];

function cleanText(text) {
    let q = text.toLowerCase().trim();
    q = q.replace(/\\b(usa club|arc club|a circle|asia club|assam|asha|asi club|aisa club|cyclic hello|cyclic)\\b/g, "aisa");
    q = q.replace(/\\b(vc president|vic president|vice-president)\\b/g, "vice president");
    q = q.replace(/\\b(ex-vice president|ex vice president|pichle upadhyaksh)\\b/g, "ex vice president");
    q = q.replace(/\\b(ex president|former president|previous president|past president|experiment)\\b/g, "ex president");
    q = q.replace(/\\b(aluminium|illumines|value money)\\b/g, "alumni");
    q = q.replace(/\\b(tech bleeds|tech blades|text blade|text blades|bloods rates)\\b/g, "techblitz");
    q = q.replace(/\\b(hd of am|head of aiml)\\b/g, "hod of aiml");
    q = q.replace(/\\b(traders|traidors)\\b/g, "treasurers");
    q = q.replace(/\\b(legal exchange|legislature|legis|lega)\\b/g, "legacy exchange");
    return q;
}

function detectLang(q) {
    const hindiWords = ["kaun", "kya", "kab", "kisko", "kitne", "pichle", "pehle", "hai", "hain", "the", "thi", "mein"];
    const words = q.split(/\\s+/);
    if (words.some(w => hindiWords.includes(w)) || /[\\u0900-\\u097F]/.test(q)) {
        return "hi";
    }
    return "en";
}

function getAnswer(rawQuery) {
    const q = cleanText(rawQuery);
    const lang = detectLang(q);

    if (q.includes("ex vice president")) return { text: RULES.find(r => r.intent === "ex_vice_president")[lang], lang };
    if (q.includes("ex president")) return { text: RULES.find(r => r.intent === "ex_president")[lang], lang };
    if (q.includes("vice president")) return { text: RULES.find(r => r.intent === "vice_president")[lang], lang };
    if (q.includes("president") && !q.includes("vice")) return { text: RULES.find(r => r.intent === "president")[lang], lang };
    if (q.includes("alumni")) return { text: RULES.find(r => r.intent === "legacy_alumni")[lang], lang };
    if (q.includes("legacy exchange")) return { text: RULES.find(r => r.intent === "legacy_exchange")[lang], lang };

    for (let rule of RULES) {
        for (let token of rule.en_tokens) {
            if (q.includes(token)) {
                return { text: rule[lang], lang };
            }
        }
    }
    return {
        text: lang === "hi" ? "माफ़ कीजिए, मुझे इस सवाल की जानकारी नहीं है।" : "I don't have information on that specific question yet.",
        lang
    };
}

const orb = document.getElementById("orb");
const statusHint = document.getElementById("status-hint");
const answerCard = document.getElementById("answer-card");
const startOverlay = document.getElementById("start-overlay");
const startBtn = document.getElementById("start-btn");

let isSpeaking = false;
let recognition = null;
let streamInterval = null;

const isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
                       (navigator.maxTouchPoints && navigator.maxTouchPoints > 2);

function streamWordsToUI(text) {
    if (streamInterval) clearInterval(streamInterval);
    answerCard.innerHTML = "";
    answerCard.style.display = "block";

    const words = text.split(" ");
    let wordIndex = 0;
    const approxDurationPerWord = 250; 

    streamInterval = setInterval(() => {
        if (wordIndex < words.length) {
            const span = document.createElement("span");
            span.className = "word-stream";
            span.textContent = words[wordIndex] + " ";
            answerCard.appendChild(span);
            answerCard.scrollTop = answerCard.scrollHeight;
            wordIndex++;
        } else {
            clearInterval(streamInterval);
        }
    }, approxDurationPerWord);
}

function speakAnswer(text, lang, callback) {
    isSpeaking = true;
    if (recognition) {
        try { recognition.abort(); } catch(e) {}
    }

    orb.className = "voice-orb orb-active";
    statusHint.textContent = "Speaking...";

    streamWordsToUI(text);

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang === "hi" ? "hi-IN" : "en-IN";
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    utterance.onend = () => {
        if (streamInterval) clearInterval(streamInterval);
        answerCard.textContent = text;
        answerCard.scrollTop = answerCard.scrollHeight;
        isSpeaking = false;
        orb.className = "voice-orb orb-idle";
        statusHint.textContent = "Listening via mic...";
        if (callback) callback();
    };

    utterance.onerror = () => {
        if (streamInterval) clearInterval(streamInterval);
        answerCard.textContent = text;
        isSpeaking = false;
        orb.className = "voice-orb orb-idle";
        statusHint.textContent = "Listening via mic...";
        if (callback) callback();
    };

    window.speechSynthesis.speak(utterance);
}

function startListeningEngine() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        statusHint.textContent = "Web Speech API not supported. Please use Chrome/Edge.";
        return;
    }

    if (recognition) {
        try { recognition.abort(); } catch(e) {}
    }

    recognition = new SpeechRecognition();
    recognition.continuous = !isMobileDevice;
    recognition.interimResults = !isMobileDevice;
    recognition.lang = "en-IN";

    recognition.onstart = () => {
        if (!isSpeaking) {
            statusHint.textContent = "Listening via mic...";
            orb.className = "voice-orb orb-idle";
        }
    };

    recognition.onspeechstart = () => {
        if (!isSpeaking) {
            orb.className = "voice-orb orb-active";
            statusHint.textContent = "Hearing voice...";
        }
    };

    recognition.onspeechend = () => {
        if (!isSpeaking) {
            orb.className = "voice-orb orb-idle";
            statusHint.textContent = "Analyzing question...";
        }
    };

    recognition.onresult = (event) => {
        if (isSpeaking) return;

        let finalTranscript = "";
        if (isMobileDevice) {
            finalTranscript = event.results[0][0].transcript;
        } else {
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                }
            }
        }

        if (finalTranscript && finalTranscript.trim().length > 2) {
            const { text, lang } = getAnswer(finalTranscript);
            speakAnswer(text, lang, () => {
                restartListeningEngine();
            });
        } else if (isMobileDevice) {
            restartListeningEngine();
        }
    };

    recognition.onerror = () => {
        restartListeningEngine();
    };

    recognition.onend = () => {
        if (!isSpeaking) {
            restartListeningEngine();
        }
    };

    try {
        recognition.start();
    } catch(e) {}
}

function restartListeningEngine() {
    if (isSpeaking) return;
    setTimeout(() => {
        try {
            recognition.start();
        } catch(e) {
            try {
                recognition.abort();
                recognition.start();
            } catch(err) {}
        }
    }, isMobileDevice ? 200 : 150);
}

startBtn.addEventListener("click", () => {
    window.speechSynthesis.cancel();
    const unlockUtterance = new SpeechSynthesisUtterance("");
    window.speechSynthesis.speak(unlockUtterance);

    startOverlay.style.display = "none";
    statusHint.textContent = "Assistant active...";

    speakAnswer("Hello! I am the AISA Club voice assistant. I am listening, ask me anything.", "en", () => {
        startListeningEngine();
    });
});

window.addEventListener("DOMContentLoaded", () => {
    if (isMobileDevice) {
        startOverlay.style.display = "flex";
        statusHint.textContent = "Tap button to enable audio...";
    } else {
        startOverlay.style.display = "none";
        setTimeout(() => {
            speakAnswer("Hello! I am the AISA Club voice assistant. I am listening, ask me anything.", "en", () => {
                startListeningEngine();
            });
        }, 500);
    }
});

document.addEventListener("visibilitychange", () => {
    if (!document.hidden && !isSpeaking) {
        restartListeningEngine();
    }
});

window.addEventListener("focus", () => {
    if (!isSpeaking) {
        restartListeningEngine();
    }
});
</script>
</body>
</html>
""", height=680)