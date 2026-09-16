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

# Component with full question patterns, keyword extraction, and mutual exclusion
components.html(r"""
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
        intent: "introduction",
        questions_en: ["introduce yourself", "who are you", "tell me about yourself", "what can you do"],
        questions_hi: ["apna introduction do", "aap kaun ho", "apne bare mein batao", "tum kya kar sakte ho"],
        core_keywords: ["introduce"],
        en: "MY self Luna Aisa robot, designed to help students and participants with information about the Artificial Intelligence Students Association at DKTE.",
        hi: "Main AISA Club Voice Assistant hoon, jo DKTE mein Artificial Intelligence Students Association ke baare mein jaankari dene ke liye banaya gaya hoon."
    },
    {
        intent: "what_is_aisa",
        questions_en: ["what is aisa club", "what is aisa", "tell me about aisa club", "what is the full form of aisa"],
        questions_hi: ["aisa club kya hai", "aisa kya hai", "aisa ke bare me batao", "aisa club kya h"],
        core_keywords: ["aisa", "club"],
        en: "AISA stands for the Artificial Intelligence Students Association in the Department of Computer Science and Engineering AI and ML at DKTE.",
        hi: "AISA stands for the Artificial Intelligence Students Association in the Department of Computer Science and Engineering AI and ML at DKTE."
    },
    {
        intent: "president",
        questions_en: ["who is the president", "who is president", "who is the current president", "who is the president of aisa", "who is the aisa president"],
        questions_hi: ["president kaun hain", "president kon hai", "aisa ke president kaun hai", "adhyaksh kaun hai"],
        core_keywords: ["president"],
        exclude_words: ["ex", "vice", "purv", "first", "pehle", "pehla"],
        en: "Mr. Arjun Jadhav is the President of the AISA club.",
        hi: "Mr. Arjun Jadhav AISA club ke President hain."
    },
    {
        intent: "vice_president",
        questions_en: ["who is the vice president", "who is vice president", "who is the current vice president", "who is vp", "who is the vp of aisa"],
        questions_hi: ["vice president kaun hain", "vice president kon hai", "upadhyaksh kaun hai", "vp kaun hai"],
        core_keywords: ["vice", "president"],
        exclude_words: ["ex", "purv", "former"],
        en: "Miss. Trupti Varma is the Vice President of the AISA club.",
        hi: "Miss Trupti Varma AISA club ki Vice President hain."
    },
    {
        intent: "ex_president",
        questions_en: ["who was the aisa ex-president", "who was the ex president", "who was the former president of aisa", "who was the previous president"],
        questions_hi: ["aisa ki ex-president kaun thi", "ex-president kaun thi", "purv adhyaksh kaun thi", "pichli president kaun thi"],
        core_keywords: ["ex", "president"],
        exclude_words: ["vice"],
        en: "Miss Janhavi Kulkarni was the AISA EX-President.",
        hi: "Miss Janhavi Kulkarni AISA ki EX-President thi."
    },
    {
        intent: "ex_vice_president",
        questions_en: ["who were the ex- vice president of aisa", "who were the ex vice presidents", "who was the former vice president", "who were the previous vice presidents"],
        questions_hi: ["aisa ke ex-vice president kaun the", "ex-vice president kaun the", "pichle upadhyaksh kaun the", "purv upadhyaksh kaun the"],
        core_keywords: ["ex", "vice", "president"],
        en: "Miss Pranali Sawant and Mr. Athrav Koli were the AISA EX-Vice Presidents.",
        hi: "Miss Pranali Sawant aur Mr. Athrav Koli AISA ke EX-Vice Presidents the."
    },
    {
        intent: "secretaries",
        questions_en: ["who are the secretaries", "who is the secretary", "who are the secretaries of aisa", "names of secretaries"],
        questions_hi: ["secretaries kaun hain", "secretaries kon hai", "sachiv kaun hai", "aisa ke sachiv kaun hain"],
        core_keywords: ["secretary"],
        en: "Mr. Tanmay Chikhalikar and Mr. Ahmad Momin are the Secretaries of the AISA club.",
        hi: "Mr. Tanmay Chikhalikar aur Mr. Ahmad Momin AISA club ke Secretaries hain."
    },
    {
        intent: "treasurers",
        questions_en: ["who are the treasurers", "who is the treasurer", "who are the treasurers of aisa", "who handles finance"],
        questions_hi: ["treasurers kaun hain", "treasurers kon hai", "koshadhyaksh kaun hai", "khajanchi kaun hai"],
        core_keywords: ["treasurer"],
        en: "Miss. Siddhi Kurle and Mr. Farhan Sheikh are the Treasurers of the AISA club.",
        hi: "Miss Siddhi Kurle aur Mr. Farhan Sheikh AISA club ke Treasurers hain."
    },
    {
        intent: "technical_directors",
        questions_en: ["who are the technical directors", "who is the technical director", "technical directors of aisa"],
        questions_hi: ["technical directors kaun hain", "technical director kon hai", "takniki nideshak kaun hai"],
        core_keywords: ["technical", "director"],
        en: "Miss. Saniya Kolar and Mr. Gous Bahurupi are the Technical Directors of the AISA club.",
        hi: "Miss Saniya Kolar aur Mr. Gous Bahurupi AISA club ke Technical Directors hain."
    },
    {
        intent: "technical_team",
        questions_en: ["who are the technical team members", "who is in technical team", "technical team members of aisa", "names of technical team members"],
        questions_hi: ["technical team mein kaun kaun hai", "technical team kon hai", "takniki team ke members"],
        core_keywords: ["technical", "team"],
        exclude_words: ["director", "role", "responsibility", "work"],
        en: "The technical team members are Mr. Om Pakhale, Mr. Samad Latkar, and Miss. Shubhangi Teke.",
        hi: "Technical team mein Mr. Om Pakhale, Mr. Samad Latkar aur Miss Shubhangi Teke hain."
    },
    {
        intent: "social_media",
        questions_en: ["who is the social media head and social media team members", "who is the social media head", "social media team members"],
        questions_hi: ["social media head aur team members kaun hai", "social media head kon hai", "social media team kaun hai"],
        core_keywords: ["social", "media"],
        exclude_words: ["role", "responsibility"],
        en: "Mr. Manthan Warte is the Social Media Team Head and The social media team members include Mr. Sushil Sapakal and Mr. Yash Ghatage.",
        hi: "Mr. Manthan Warte Social Media Team ke Head hain aur team members mein Mr. Sushil Sapakal aur Mr. Yash Ghatage hain."
    },
    {
        intent: "coordinator",
        questions_en: ["who is the aisa coordinator", "who is the coordinator", "who is faculty coordinator", "aisa coordinator name"],
        questions_hi: ["aisa coordinator kaun hain", "coordinator kaun hai", "faculty coordinator kon hai"],
        core_keywords: ["coordinator"],
        en: "Mrs. D. M. Kulkarni is the AISA Coordinator.",
        hi: "Mrs. D. M. Kulkarni AISA Coordinator hain."
    },
    {
        intent: "hod",
        questions_en: ["who is the hod", "who is the hod of cse aiml", "who is head of department"],
        questions_hi: ["hod kaun hain", "aiml ke hod kaun hai", "hod kon hai"],
        core_keywords: ["hod"],
        en: "Prof. Dr. S. K. Shirgave is the HOD of CSE AIML.",
        hi: "Prof. Dr. S. K. Shirgave CSE AIML ke HOD hain."
    },
    {
        intent: "notice_date",
        questions_en: ["what is the date of the aisa notice", "date of notice", "when was aisa notice issued", "notice date"],
        questions_hi: ["aisa notice ki date kya hai", "notice kab aaya tha", "notice ki tarikh kya hai"],
        core_keywords: ["notice", "date"],
        en: "The notice was issued on 18/08/2026.",
        hi: "Notice 18 August 2026 ko jaari kiya gaya tha."
    },
    {
        intent: "techblitz_participants",
        questions_en: ["how many students participated in techblitz", "participants in techblitz", "how many teams participated in techblitz"],
        questions_hi: ["techblitz mein kitne students ne participate kiya", "kitne students ne participate kiya", "kitni teams ne participate kiya"],
        core_keywords: ["tech", "blitz", "participat"],
        en: "32 Teams were participated where 2 members per team.",
        hi: "32 Teams ne participate kiya tha jisme har team mein 2 members the."
    },
    {
        intent: "techblitz_date",
        questions_en: ["when was techblitz conducted", "what is the date of techblitz", "when did techblitz happen"],
        questions_hi: ["techblitz kab conduct kiya gaya", "techblitz kab hua tha", "techblitz ki date kya thi"],
        core_keywords: ["tech", "blitz", "date", "happen"],
        en: "TECHBLITZ was conducted on 1st September 2026.",
        hi: "TECHBLITZ 1 September 2026 ko conduct kiya gaya tha."
    },
    {
        intent: "techblitz_skills",
        questions_en: ["what skills were tested in techblitz", "skills tested in techblitz", "which skills were tested in techblitz"],
        questions_hi: ["techblitz mein kaun si skills test hui", "kaun si skills test hui", "techblitz me kya test hua"],
        core_keywords: ["tech", "blitz", "skill"],
        en: "The event tested logical reasoning, aptitude, problem-solving and technical skills.",
        hi: "Event mein logical reasoning, aptitude, problem-solving aur technical skills test ki gayi thi."
    },
    {
        intent: "techblitz_rounds",
        questions_en: ["how many rounds were there in techblitz", "rounds in techblitz", "how many rounds in techblitz"],
        questions_hi: ["techblitz mein kitne rounds the", "kitne rounds the techblitz me"],
        core_keywords: ["tech", "blitz", "round", "many"],
        exclude_words: ["what was", "kya tha"],
        en: "There were three rounds.",
        hi: "Usme teen rounds the."
    },
    {
        intent: "what_was_techblitz",
        questions_en: ["what was techblitz", "tell me about techblitz", "what were the rounds in techblitz"],
        questions_hi: ["techblitz kya tha", "techblitz event kya tha"],
        core_keywords: ["tech", "blitz", "kya", "tha"],
        en: "TechBlitz was a technical event organized by the AISA Artificial Intelligence Student Association which had The three rounds are Round 1 Aptitude Round, Round 2 Coding and Logic Challenge, and Round 3 Final or Surprise Round.",
        hi: "TechBlitz AISA dwara aayojit ek technical event tha jisme teen rounds the: Aptitude Round, Coding and Logic Challenge, aur Surprise Round."
    },
    {
        intent: "techblitz_2026",
        questions_en: ["what is techblitz 2026", "tell me about techblitz 2026", "what is entry fee of techblitz", "where was techblitz held"],
        questions_hi: ["techblitz 2026 kya hai", "techblitz 2026 kya h", "techblitz ke bare me batao"],
        core_keywords: ["tech", "blitz"],
        exclude_words: ["round", "skill", "date", "participat"],
        en: "TechBlitz 2026 is an inter-collegiate technical challenge provided by AISA, held on 1st September 2026 at CCL 2, consisting of three rounds with a team size of two and an entry fee of 100 rupees per team.",
        hi: "TechBlitz 2026 AISA dwara organized ek inter-collegiate technical challenge hai jo 1 September 2026 ko CCL 2 mein hua tha."
    },
    {
        intent: "previous_events",
        questions_en: ["what was the previous events of aisa", "previous events of aisa", "what were past events of aisa"],
        questions_hi: ["aisa ke pichle events kaun se the", "pichle events kaun se the", "aisa ke purane events kya the"],
        core_keywords: ["previous", "event"],
        en: "Previous events of AISA was The Legacy Exchange an alumni meet and TechBlitz a technical event.",
        hi: "AISA ke pichle events The Legacy Exchange jo ek alumni meet tha, aur TechBlitz jo ek technical event tha."
    },
    {
        intent: "japan_alumni",
        questions_en: ["who is the alumni joining virtually from japan", "alumni joining virtually from japan", "who joined from japan"],
        questions_hi: ["japan se virtually kaun join kar raha hai", "japan se kaun virtually juda tha", "japan se kaun hai"],
        core_keywords: ["japan", "virtuallty"],
        en: "Ms. Sejal Pandharpatte is participated virtually from Japan.",
        hi: "Ms. Sejal Pandharpatte Japan se virtually participate kar rahi hain."
    },
    {
        intent: "legacy_alumni",
        questions_en: ["who was the alumni of the legacy exchange", "alumni of the legacy exchange", "who were the alumni in legacy exchange"],
        questions_hi: ["legacy exchange ke alumni kaun the", "legacy exchange me alumni kaun the", "alumni kaun the"],
        core_keywords: ["alumni", "legacy"],
        exclude_words: ["japan", "meaning"],
        en: "Mr. Neeraj Mirashi, Sejal pandharpatte, Sanika Patil, Alisha Attar.",
        hi: "Alumni mein Mr. Neeraj Mirashi, Sejal Pandharpatte, Sanika Patil, aur Alisha Attar the."
    },
    {
        intent: "legacy_exchange",
        questions_en: ["what is the legacy exchange", "what is legacy exchange", "tell me about the legacy exchange"],
        questions_hi: ["legacy exchange kya hai", "the legacy exchange kya hai", "legacy exchange kya h"],
        core_keywords: ["legacy", "exchange"],
        exclude_words: ["alumni"],
        en: "The Legacy Exchange is an alumni interaction initiative organized by AISA based on the motto Reconnect, Inspire, Empower, hosted by AISA Club.",
        hi: "The Legacy Exchange AISA dwara aayojit ek alumni interaction initiative hai jiska motto Reconnect, Inspire, Empower hai."
    },
    {
        intent: "motto",
        questions_en: ["what is the motto of aisa", "motto of aisa", "what is aisa motto", "what is the tagline of aisa"],
        questions_hi: ["aisa ka motto kya hai", "motto kya hai aisa ka", "tagline kya hai"],
        core_keywords: ["motto"],
        en: "The motto of AISA is Unite, Excel, Achieve.",
        hi: "AISA ka motto hai Unite, Excel, Achieve."
    },
    {
        intent: "purpose",
        questions_en: ["what is the main purpose of aisa", "what is the purpose of aisa", "what is the objective of aisa", "aim of aisa"],
        questions_hi: ["aisa ka main purpose kya hai", "aisa ka uddeshya kya hai", "aisa ka maksad kya hai"],
        core_keywords: ["purpose", "main"],
        en: "AISA promotes learning, innovation, technical skills and collaborative growth among students in Artificial Intelligence and related technologies.",
        hi: "AISA Artificial Intelligence aur related technologies mein students ke beech learning, innovation, aur collaborative growth ko promote karta hai."
    },
    {
        intent: "upcoming_events",
        questions_en: ["what are the upcoming events of aisa", "upcoming events of aisa", "what are the next events of aisa"],
        questions_hi: ["aisa ke upcoming events kaun se hain", "upcoming events kaun se hain", "aane wale events kaun se hain"],
        core_keywords: ["upcoming", "events"],
        en: "The AISA Super Strikers A cricket battle, The freshers Party, TechSymposium Hackathon, and other technical and non-technical events will be organized soon by the AISA.",
        hi: "AISA jald hi The AISA Super Strikers cricket battle, Freshers Party, TechSymposium Hackathon, aur dusre events organize karega."
    },
    {
        intent: "volunteer_head",
        questions_en: ["who is the volunteer head in aisa", "who is volunteer head", "who is the head of volunteers"],
        questions_hi: ["aisa mein volunteer head kaun hai", "volunteer head kaun hai", "volunteers ka head kaun hai"],
        core_keywords: ["volunteer", "head"],
        en: "Rohit Jadhav is a Volunteer Head in AISA.",
        hi: "Rohit Jadhav AISA mein Volunteer Head hain."
    },
    {
        intent: "volunteers",
        questions_en: ["who are the volunteers", "who are the volunteers in aisa", "names of volunteers"],
        questions_hi: ["volunteers kaun hain", "volunteers kon hai", "aisa ke volunteers kaun hain"],
        core_keywords: ["volunteer"],
        exclude_words: ["head"],
        en: "Manthan Soni, Shravani Asawale, Pradnya Desai, Anuradha Jadhav, Shivraj Banne, Sanskar Govare, Rajvardhini Mane, Maitrayee Jadhav, Harshwardhan Jiddi, Aftab Momin.",
        hi: "Volunteers hain Manthan Soni, Shravani Asawale, Pradnya Desai, Anuradha Jadhav, Shivraj Banne, Sanskar Govare, Rajvardhini Mane, Maitrayee Jadhav, Harshwardhan Jiddi, aur Aftab Momin."
    },
    {
        intent: "founder",
        questions_en: ["founder of aisa", "who is the founder of aisa", "who was the first president of aisa"],
        questions_hi: ["aisa ka founder kaun hai", "pehle president kaun the", "aisa kisne shuru kiya"],
        core_keywords: ["founder"],
        en: "Prithviraj Banne was the first president of AISA.",
        hi: "Prithviraj Banne AISA ke pehle president the."
    },
    {
        intent: "who_am_i",
        questions_en: ["who am i", "what is my name", "do you know me"],
        questions_hi: ["mai kon hu", "main kaun hoon", "mera naam kya hai"],
        core_keywords: ["who am i"],
        en: "You are Om Pakhale, part of the AISA Technical Team.",
        hi: "Aapka naam Om Pakhale hai."
    },
    // --- Rule Book Topics ---
    {
        intent: "membership_eligibility",
        questions_en: ["who is eligible for membership", "what is the eligibility for aisa", "who can join aisa"],
        questions_hi: ["membership ke liye kaun eligible hai", "aisa kaun join kar sakta hai", "eligibility kya hai"],
        core_keywords: ["eligib"],
        exclude_words: ["fee", "dues", "cost", "free"],
        en: "Membership in AISA is open to all currently enrolled students of DKTE who maintain good academic standing and follow the college code of conduct.",
        hi: "DKTE ke sabhi enrolled students jo achhi academic standing maintain karte hain, AISA ke member ban sakte hain."
    },
    {
        intent: "membership_fees",
        questions_en: ["what is the membership fee", "is aisa free to join", "what are the membership dues", "how much is the fee for joining aisa"],
        questions_hi: ["aisa ki fees kitni hai", "kya aisa free hai", "membership charges kya hain"],
        core_keywords: ["fee"],
        en: "Membership in AISA is currently completely free of charge for all eligible members.",
        hi: "AISA ki membership sabhi eligible students ke liye bilkul free hai."
    },
    {
        intent: "membership_types",
        questions_en: ["what are the types of membership", "what are the membership categories in aisa", "explain regular associate honorary membership"],
        questions_hi: ["membership ke types kya hain", "membership categories kya hain", "kitne type ki membership hoti hai"],
        core_keywords: ["types", "membership"],
        en: "AISA offers Regular or Executive Members for enrolled students, Associate Members for individuals like alumni, and Honorary Members or Mentors.",
        hi: "AISA mein teen types ki membership hoti hai: Regular Members, Associate Members, aur Honorary Members ya Mentors."
    },
    {
        intent: "membership_termination",
        questions_en: ["what is the rule for membership termination", "what happens if a member is terminated", "can terminated members join other clubs"],
        questions_hi: ["membership terminate hone par kya hota hai", "terminate kaise hote hain", "membership cancel hone par kya hoga"],
        core_keywords: ["terminat" , "membership"],
        en: "Terminated members forfeit all rights and privileges and are banned from joining any other club on the college campus.",
        hi: "Terminate hone par member ke sabhi rights khatam ho jaate hain aur use campus ke kisi doosre club mein join karne par ban laga diya jaata hai."
    },
    {
        intent: "executive_structure",
        questions_en: ["what is the structure of the executive committee", "what are the posts in executive committee", "what are the roles in aisa"],
        questions_hi: ["executive committee ka structure kya hai", "aisa mein kaun kaun si posts hain", "committee structure kya hai"],
        core_keywords: ["structure", "executive"],
        exclude_words: ["meeting", "bi-weekly"],
        en: "The Executive Committee consists of the President, Vice President, Secretary, Treasurer, Event Coordinator, Technical Team, Media Team, Planning Team, and Mentors.",
        hi: "Executive Committee mein President, Vice President, Secretary, Treasurer, Event Coordinator, Technical Team, Media Team, Planning Team, aur Mentors shamil hain."
    },
    {
        intent: "technical_team_role",
        questions_en: ["what is the role of technical team", "what are technical team responsibilities", "who manages the aisa website"],
        questions_hi: ["technical team ka kaam kya hai", "technical team ki responsibility kya hai", "website kaun manage karta hai"],
        core_keywords: ["technical", "team", "role"],
        en: "The Technical Team leads the technical events conducted by AISA and manages the development and maintenance of AISA's official website.",
        hi: "Technical Team technical events lead karti hai aur AISA ki official website develop aur manage karti hai."
    },
    {
        intent: "media_team_role",
        questions_en: ["what is the role of media team", "what are media team responsibilities", "who manages social media"],
        questions_hi: ["media team ka kaam kya hai", "media team ki responsibility kya hai", "social media kaun sambhalta hai"],
        core_keywords: ["media", "team", "role"],
        en: "The Media Team is responsible for maintaining the online and offline reputation of AISA through social media and official communication channels.",
        hi: "Media Team official communication channels aur social media ke zariye AISA ki online aur offline reputation maintain karti hai."
    },
    {
        intent: "planning_team_role",
        questions_en: ["what is the role of planning team", "what are planning team responsibilities", "who allocates event coordinator"],
        questions_hi: ["planning team ka kaam kya hai", "planning team kya karti hai", "planning team ki responsibility kya hai"],
        core_keywords: ["planning", "team", "role"],
        en: "The Planning Team assists the secretary with event records and allocates the event coordinator for each event.",
        hi: "Planning Team secretary ko event records maintain karne mein madad karti hai aur har event ke liye coordinator allocate karti hai."
    },
    {
        intent: "meeting_frequency",
        questions_en: ["how often are executive committee meetings held", "what is the meeting frequency", "how often does aisa meet"],
        questions_hi: ["meetings kitne din me hoti hain", "meetings kab hoti hain", "committee meetings kab hoti hain"],
        core_keywords: ["meeting", "frequency" , "committee", "held"],
        en: "The Executive Committee holds regular meetings, typically on a bi-weekly basis.",
        hi: "Executive Committee ki regular meetings aam taur par bi-weekly basis par hoti hain."
    },
    {
        intent: "tie_vote",
        questions_en: ["who breaks a tie in voting", "what happens in case of a tie vote", "who casts the deciding vote in a tie"],
        questions_hi: ["voting mein tie hone par kya hota hai", "tie hone par faisla kaun leta hai", "tie breaking vote kaun dalta hai"],
        core_keywords: ["tie", "voting"],
        en: "Decisions are made by majority vote. In the event of a tie, the President casts the deciding vote.",
        hi: "Faisle majority vote se hote hain, aur tie hone par President decisive vote daalte hain."
    },
    {
        intent: "reimbursement_timeline",
        questions_en: ["what is the reimbursement timeline", "how long do reimbursements take", "within how many days are reimbursements processed"],
        questions_hi: ["reimbursement kitne din me milta hai", "paise wapas kab milte hain", "reimbursement timeline kya hai"],
        core_keywords: ["reimbursement" , "timeline"],
        en: "Out-of-pocket reimbursements must be processed by the Treasurer within one week of submission.",
        hi: "Kharch kiye gaye paise Treasurer dwara submission ke ek hafte ke andar process kiye jaate hain."
    },
    {
        intent: "official_email",
        questions_en: ["what is the official email address of aisa", "what is the contact email of aisa", "email of aisa"],
        questions_hi: ["aisa ka official email kya hai", "aisa ka email address kya hai", "aisa ko mail kaise kare"],
        core_keywords: ["email", "official"],
        en: "The official email address of AISA is aisadkte@gmail.com.",
        hi: "AISA ka official email address aisadkte@gmail.com hai."
    },
    {
        intent: "alcohol_substance_policy",
        questions_en: ["what is the alcohol and substance policy", "are drugs and alcohol allowed in aisa", "what is the substance abuse rule"],
        questions_hi: ["alcohol aur drugs par kya rule hai", "substance policy kya hai", "kya alcohol allowed hai"],
        core_keywords: ["alcohol", "policy"],
        en: "Consumption of alcohol or illegal substances during association events or activities is strictly prohibited.",
        hi: "AISA ke kisi bhi event ya activity mein alcohol ya illegal substances ka sevan sakht mana hai."
    },
    {
        intent: "rule_book_authors",
        questions_en: ["who wrote the rule book", "who is the author of the rule book", "who edited the aisa rulebook"],
        questions_hi: ["rule book kisne likhi hai", "rulebook kisne banayi", "rule book ke author kaun hai"],
        core_keywords: ["author", "rule" , "book"],
        en: "The rule book was authored by Yash Rajesh Kapse and edited by Shreyash Shinde and Pruthviraj Banne, under the guidance of Dr. S.K. Shirgave and Mrs. D.M. Kulkarni.",
        hi: "Rule book Yash Rajesh Kapse ne likhi hai aur Shreyash Shinde aur Pruthviraj Banne ne edit ki hai, Dr. S.K. Shirgave aur Mrs. D.M. Kulkarni ki guidance mein."
    },
    {
        intent: "dissolution_procedure",
        questions_en: ["what is the dissolution procedure of aisa", "how can aisa be dissolved", "what vote is required to dissolve aisa"],
        questions_hi: ["aisa ko dissolve kaise kiya ja sakta hai", "dissolution process kya hai", "club band kaise ho sakta hai"],
        core_keywords: ["dissolv"],
        en: "Dissolution of AISA requires a formal proposal approved by a two-thirds majority vote of the general body members present.",
        hi: "AISA ko dissolve karne ke liye General Body ke do-tihaai sadasyon ka majority vote zaroori hota hai."
    }
];

function cleanText(text) {
    let q = text.toLowerCase().trim();

    // 1. Break down phonetic mergers and abbreviations
    q = q.replace(/\b(techblitz|tech blitz|techbleeds|tech blades|text blades|tech bridge|tag blitz)\b/g, "tech blitz");
    q = q.replace(/\b(aiml|ai ml|ai & ml|ai and ml)\b/g, "aiml");
    q = q.replace(/\b(ex vice president|ex-vice president|former vice president|pichle upadhyaksh)\b/g, "ex vice president");
    q = q.replace(/\b(ex president|ex-president|former president|pichli president)\b/g, "ex president");
    q = q.replace(/\b(vp|vc president|upadhyaksh)\b/g, "vice president");
    q = q.replace(/\b(alumni|alumnus|alumni meet|aluminate)\b/g, "alumni");
    q = q.replace(/\b(hod|head of department)\b/g, "hod");
    q = q.replace(/\b(coordinator|co-ordinator)\b/g, "coordinator");

    // 2. Normalize Club Name mishearings
    q = q.replace(/\b(usa|arc|asia|assam|asha|asi|cyclic)\s+club\b/g, "aisa");
    q = q.replace(/\b(aisa club|aisa)\b/g, "aisa");

    return q;
}

// Strict Hindi/Hinglish token detector using regex word boundaries
function isHindiSpeech(rawText) {
    if (/[\u0900-\u097F]/.test(rawText)) return true;
    const cleanRaw = rawText.toLowerCase();
    const hindiWordsRegex = /\b(kaun|kon|kya|kab|kitne|kitni|pichle|pichli|pehle|pehla|hai|hain|the|thi|mein|me|kisne|kisko|hoga|hogi|batao|bataiye|sunao|kripya)\b/;
    return hindiWordsRegex.test(cleanRaw);
}

// Consecutive fallback tracking
let failureCount = 0;

function getRandomSampleQuestions(count = 5) {
    let samples = [];
    let pool = [...RULES];
    for (let i = 0; i < count && pool.length > 0; i++) {
        let randomIndex = Math.floor(Math.random() * pool.length);
        samples.push(pool[randomIndex].questions_en[0]);
        pool.splice(randomIndex, 1);
    }
    return samples;
}

function getAnswer(rawQuery) {
    const q = cleanText(rawQuery);
    const spokenHindi = isHindiSpeech(rawQuery);

    // Tier 1: Question Pattern Matching
    for (let rule of RULES) {
        for (let targetQuestion of rule.questions_en) {
            if (q.includes(cleanText(targetQuestion))) {
                failureCount = 0; // Reset counter on success
                return { text: rule.en, lang: "en" };
            }
        }
        for (let targetQuestion of rule.questions_hi) {
            if (q.includes(cleanText(targetQuestion))) {
                failureCount = 0; // Reset counter on success
                return { text: rule.hi, lang: "hi" };
            }
        }
    }

    // Tier 2: Keyword Fallback Matching
    for (let rule of RULES) {
        if (rule.exclude_words && rule.exclude_words.some(ex => q.includes(ex))) {
            continue;
        }

        const allKeywordsPresent = rule.core_keywords.every(kw => q.includes(kw));
        if (allKeywordsPresent) {
            failureCount = 0; // Reset counter on success
            return {
                text: spokenHindi ? rule.hi : rule.en,
                lang: spokenHindi ? "hi" : "en"
            };
        }
    }

    // If no match found, increment failure counter
    failureCount++;

    if (failureCount >= 3) {
        failureCount = 0; // Reset counter after triggering suggestion flow
        const randomQuestions = getRandomSampleQuestions(5);
        const suggestionText = (spokenHindi ? "माफ़ कीजिए, मैं आपका सवाल समझ नहीं पाया। आप इस तरह के सवाल पूछ सकते हैं: " : "Sorry, I cannot understand the question you asked. You can ask me questions like: ") + randomQuestions.join(", ");
        return {
            text: suggestionText,
            lang: spokenHindi ? "hi" : "en"
        };
    }

    // Standard repeat prompt for 1st or 2nd failure
    return {
        text: spokenHindi ? "माफ़ कीजिए, क्या आप सवाल दोबारा दोहरा सकते हैं?" : "Can you repeat the question again?",
        lang: spokenHindi ? "hi" : "en"
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

    speakAnswer("Hello! I am the AISA Club voice assistant. You can ask me anything.", "en", () => {
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
            speakAnswer("Hello! I am the Luna AISA Club   voice Robot. You can ask me anything.", "en", () => {
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