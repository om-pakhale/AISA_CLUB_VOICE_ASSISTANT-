import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AISA Club Voice Assistant", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 720px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎙️ AISA Club Voice Assistant")
st.caption("Department of CSE (AI & ML) - DKTE")

components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    body {
        margin: 0;
        padding: 10px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background: transparent;
        color: #f8fafc;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .orb-wrapper {
        position: relative;
        width: 150px;
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px auto 10px auto;
    }

    /* Unified Cyan-Blue Base */
    .voice-orb {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background: radial-gradient(circle, #0ea5e9 0%, #0284c7 50%, #0369a1 100%);
        box-shadow: 0 0 16px rgba(14, 165, 233, 0.4);
        transition: all 0.25s ease;
    }

    .orb-idle {
        box-shadow: 0 0 16px rgba(14, 165, 233, 0.4);
        animation: gentle-corners 3s infinite ease-in-out;
    }

    /* Subtle edge movement during input and output */
    .orb-active {
        box-shadow: 0 0 25px rgba(14, 165, 233, 0.75), 0 0 42px rgba(2, 132, 199, 0.45);
        animation: subtle-corner-vibrate 0.35s infinite alternate ease-in-out;
    }

    @keyframes gentle-corners {
        0% { border-radius: 50% 50% 50% 50%; transform: scale(0.98); }
        50% { border-radius: 48% 52% 49% 51%; transform: scale(1.02); }
        100% { border-radius: 50% 50% 50% 50%; transform: scale(0.98); }
    }

    @keyframes subtle-corner-vibrate {
        0% {
            border-radius: 49% 51% 50% 50%;
            transform: scale(1.02) rotate(-0.5deg);
        }
        50% {
            border-radius: 52% 48% 51% 49%;
            transform: scale(1.05) rotate(0.5deg);
        }
        100% {
            border-radius: 50% 50% 48% 52%;
            transform: scale(1.03) rotate(-0.5deg);
        }
    }

    #status-hint {
        color: #94a3b8;
        font-size: 0.88rem;
        margin-top: 8px;
        height: 20px;
    }

    #answer-card {
        width: 92%;
        max-width: 600px;
        margin-top: 18px;
        padding: 16px 20px;
        background-color: #0b221a;
        border: 1.5px solid #10b981;
        border-radius: 10px;
        color: #a7f3d0;
        font-size: 1.1rem;
        line-height: 1.5;
        text-align: center;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        display: none;
    }
</style>
</head>
<body>

<div class="orb-wrapper">
    <div id="orb" class="voice-orb orb-idle"></div>
</div>
<div id="status-hint">Starting assistant...</div>
<div id="answer-card"></div>

<audio id="tts-player" style="display:none;"></audio>

<script>
const RULES = [
    {
        intent: "what_is_aisa",
        tokens: ["what is aisa club", "what is aisa", "aisa club kya hai", "about aisa"],
        en: "AISA stands for the Artificial Intelligence Students Association in the Department of Computer Science and Engineering AI and ML at DKTE.",
        hi: "AISA, DKTE ke Computer Science and Engineering AI and ML department mein Artificial Intelligence Students Association hai."
    },
    {
        intent: "president",
        tokens: ["who is the president", "president", "adhyaksh", "current president", "who is president of aisa"],
        en: "Mr. Arjun Jadhav is the President of the AISA club.",
        hi: "Mr. Arjun Jadhav AISA club ke President hain."
    },
    {
        intent: "vice_president",
        tokens: ["who is the vice president", "vice president", "upadhyaksh", "vc president", "who is vp"],
        en: "Miss. Trupti Varma is the Vice President of the AISA club.",
        hi: "Miss Trupti Varma AISA club ki Vice President hain."
    },
    {
        intent: "secretaries",
        tokens: ["who are the secretaries", "secretaries", "secretary", "sachiv"],
        en: "Mr. Tanmay Chikhalikar and Mr. Ahmad Momin are the Secretaries of the AISA club.",
        hi: "Mr. Tanmay Chikhalikar aur Mr. Ahmad Momin AISA club ke Secretaries hain."
    },
    {
        intent: "treasurers",
        tokens: ["who are the treasurers", "treasurers", "treasurer", "koshadhyaksh"],
        en: "Miss. Siddhi Kurle and Mr. Farhan Sheikh are the Treasurers of the AISA club.",
        hi: "Miss Siddhi Kurle aur Mr. Farhan Sheikh AISA club ke Treasurers hain."
    },
    {
        intent: "technical_directors",
        tokens: ["who are the technical directors", "technical directors", "technical director", "takniki nideshak"],
        en: "Miss. Saniya Kolar and Mr. Gous Bahurupi are the Technical Directors of the AISA club.",
        hi: "Miss Saniya Kolar aur Mr. Gous Bahurupi AISA club ke Technical Directors hain."
    },
    {
        intent: "technical_team",
        tokens: ["who are the technical team members", "technical team", "technical team members", "takniki team"],
        en: "The technical team members are Mr. Om Pakhale, Mr. Samad Latkar, and Miss. Shubhangi Teke.",
        hi: "Technical team mein Mr. Om Pakhale, Mr. Samad Latkar aur Miss Shubhangi Teke hain."
    },
    {
        intent: "social_media",
        tokens: ["social media head", "social media team", "social media team members", "social media"],
        en: "Mr. Manthan Warte is the Social Media Team Head and The social media team members include Mr. Sushil Sapakal and Mr. Yash Ghatage.",
        hi: "Mr. Manthan Warte Social Media Team ke Head hain aur team members mein Mr. Sushil Sapakal aur Mr. Yash Ghatage hain."
    },
    {
        intent: "coordinator",
        tokens: ["who is the aisa coordinator", "aisa coordinator", "coordinator", "faculty coordinator", "kulkarni"],
        en: "Mrs. D. M. Kulkarni is the AISA Coordinator.",
        hi: "Mrs. D. M. Kulkarni AISA Coordinator hain."
    },
    {
        intent: "hod",
        tokens: ["who is the hod", "hod", "head of department", "hod of aiml", "shirgave"],
        en: "Prof. Dr. S. K. Shirgave is the HOD of CSE AIML.",
        hi: "Prof. Dr. S. K. Shirgave CSE AIML ke HOD hain."
    },
    {
        intent: "notice_date",
        tokens: ["date of the aisa notice", "aisa notice date", "notice date", "notice kab aaya"],
        en: "The notice was issued on 18/08/2026.",
        hi: "Notice 18 August 2026 ko jaari kiya gaya tha."
    },
    {
        intent: "techblitz_2026",
        tokens: ["what is techblitz 2026", "what is techblitz", "techblitz 2026 kya hai"],
        en: "TechBlitz 2026 is an inter-collegiate technical challenge provided by AISA, held on 1st September 2026 at CCL 2, consisting of three rounds with a team size of two and an entry fee of 100 rupees per team.",
        hi: "TechBlitz 2026 AISA dwara organized ek inter-collegiate technical challenge hai jo 1 September 2026 ko CCL 2 mein hua tha."
    },
    {
        intent: "previous_events",
        tokens: ["previous events of aisa", "past events", "pichle events", "what was the previous events"],
        en: "Previous events of AISA was The Legacy Exchange an alumni meet and TechBlitz a technical event.",
        hi: "AISA ke pichle events The Legacy Exchange jo ek alumni meet tha, aur TechBlitz jo ek technical event tha."
    },
    {
        intent: "what_was_techblitz",
        tokens: ["what was techblitz", "techblitz kya tha", "about techblitz"],
        en: "TechBlitz was a technical event organized by the AISA Artificial Intelligence Student Association which had The three rounds are Round 1 Aptitude Round, Round 2 Coding and Logic Challenge, and Round 3 Final or Surprise Round.",
        hi: "TechBlitz AISA dwara aayojit ek technical event tha jisme teen rounds the: Aptitude Round, Coding and Logic Challenge, aur Surprise Round."
    },
    {
        intent: "legacy_exchange",
        tokens: ["what is the legacy exchange", "legacy exchange kya hai", "what is legacy exchange", "legacy exchange"],
        en: "The Legacy Exchange is an alumni interaction initiative organized by AISA based on the motto Reconnect, Inspire, Empower, hosted by Tanmay and Drushti.",
        hi: "The Legacy Exchange AISA dwara aayojit ek alumni interaction initiative hai jiska motto Reconnect, Inspire, Empower hai."
    },
    {
        intent: "legacy_alumni",
        tokens: ["who was the alumni of the legacy exchange", "alumni of the legacy exchange", "alumni kaun the", "alumni of legacy"],
        en: "Mr. Neeraj Mirashi, Sejal pandharpatte, Sanika Patil, Alisha Attar.",
        hi: "Alumni mein Mr. Neeraj Mirashi, Sejal Pandharpatte, Sanika Patil, aur Alisha Attar the."
    },
    {
        intent: "japan_alumni",
        tokens: ["alumni joining virtually from japan", "virtually from japan", "japan se kaun"],
        en: "Ms. Sejal Pandharpatte is participating virtually from Japan.",
        hi: "Ms. Sejal Pandharpatte Japan se virtually participate kar rahi hain."
    },
    {
        intent: "motto",
        tokens: ["what is the motto of aisa", "motto of aisa", "aisa motto", "motto"],
        en: "The motto of AISA is Unite, Excel, Achieve.",
        hi: "AISA ka motto hai Unite, Excel, Achieve."
    },
    {
        intent: "purpose",
        tokens: ["what is the main purpose of aisa", "purpose of aisa", "main purpose", "objective of aisa"],
        en: "AISA promotes learning, innovation, technical skills and collaborative growth among students in Artificial Intelligence and related technologies.",
        hi: "AISA Artificial Intelligence aur related technologies mein students ke beech learning, innovation, aur collaborative growth ko promote karta hai."
    },
    {
        intent: "techblitz_participants",
        tokens: ["how many students participated in techblitz", "kitne students ne participate kiya", "participants in techblitz"],
        en: "32 Teams were participated where 2 members per team.",
        hi: "32 Teams ne participate kiya tha jisme har team mein 2 members the."
    },
    {
        intent: "techblitz_date",
        tokens: ["when was techblitz conducted", "techblitz kab conduct kiya gaya", "date of techblitz"],
        en: "TECHBLITZ was conducted on 1st September 2026.",
        hi: "TECHBLITZ 1 September 2026 ko conduct kiya gaya tha."
    },
    {
        intent: "techblitz_skills",
        tokens: ["what skills were tested in techblitz", "skills were tested", "skills tested in techblitz"],
        en: "The event tested logical reasoning, aptitude, problem-solving and technical skills.",
        hi: "Event mein logical reasoning, aptitude, problem-solving aur technical skills test ki gayi thi."
    },
    {
        intent: "techblitz_rounds",
        tokens: ["how many rounds were there in techblitz", "rounds were there in techblitz", "kitne rounds the"],
        en: "There were three rounds.",
        hi: "Usme teen rounds the."
    },
    {
        intent: "ex_president",
        tokens: ["who was the aisa ex-president", "aisa ex-president", "ex president", "former president", "pichli president", "janhavi"],
        en: "Miss Janhavi Kulkarni was the AISA EX-President.",
        hi: "Miss Janhavi Kulkarni AISA ki EX-President thi."
    },
    {
        intent: "ex_vice_president",
        tokens: ["who were the ex- vice president of aisa", "ex vice president", "former vice president", "pichle upadhyaksh"],
        en: "Miss Pranali Sawant and Mr. Athrav Koli were the AISA EX-Vice Presidents.",
        hi: "Miss Pranali Sawant aur Mr. Athrav Koli AISA ke EX-Vice Presidents the."
    },
    {
        intent: "upcoming_events",
        tokens: ["what are the upcoming events of aisa", "upcoming events", "aane wale events"],
        en: "The AISA Super Strikers A cricket battle, The freshers Party, TechSymposium Hackathon, and other technical and non-technical events will be organized soon by the AISA.",
        hi: "AISA jald hi The AISA Super Strikers cricket battle, Freshers Party, TechSymposium Hackathon, aur dusre events organize karega."
    },
    {
        intent: "volunteer_head",
        tokens: ["who is the volunteer head in aisa", "volunteer head", "volunteer head in aisa"],
        en: "Rohit Jadhav is a Volunteer Head in AISA.",
        hi: "Rohit Jadhav AISA mein Volunteer Head hain."
    },
    {
        intent: "volunteers",
        tokens: ["who are the volunteers", "volunteers kaun hain", "volunteers"],
        en: "Manthan Soni, Shravani Asawale, Pradnya Desai, Anuradha Jadhav, Shivraj Banne, Sanskar Govare, Rajvardhini Mane, Maitrayee Jadhav, Harshwardhan Jiddi, Aftab Momin.",
        hi: "Volunteers hain Manthan Soni, Shravani Asawale, Pradnya Desai, Anuradha Jadhav, Shivraj Banne, Sanskar Govare, Rajvardhini Mane, Maitrayee Jadhav, Harshwardhan Jiddi, aur Aftab Momin."
    },
    {
        intent: "founder",
        tokens: ["founder of aisa", "founder", "first president"],
        en: "Prithviraj Banne was the first president of AISA.",
        hi: "Prithviraj Banne AISA ke pehle president the."
    },
    {
        intent: "who_am_i",
        tokens: ["who am i", "mai kon hu", "main kaun hoon"],
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
        for (let token of rule.tokens) {
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
const audioPlayer = document.getElementById("tts-player");

let isSpeaking = false;
let recognition = null;
let preferredFemaleVoice = null;

// Lock specifically onto natural Indian Female voice profiles
function pickFemaleVoice() {
    const voices = window.speechSynthesis.getVoices();
    preferredFemaleVoice = voices.find(v => 
        (v.name.includes("Neerja") || v.name.includes("Swara") || v.name.includes("Heera") || v.name.includes("Zira") || v.name.includes("Female")) &&
        (v.lang.includes("IN") || v.lang.includes("en"))
    ) || voices.find(v => v.lang.includes("en-IN") || v.lang.includes("hi-IN")) || voices[0];
}

window.speechSynthesis.onvoiceschanged = pickFemaleVoice;
pickFemaleVoice();

function playFemaleVoice(text, lang, onDone) {
    isSpeaking = true;
    if (recognition) {
        try { recognition.abort(); } catch(e) {}
    }

    orb.className = "voice-orb orb-active";
    statusHint.textContent = "Speaking...";

    answerCard.textContent = text;
    answerCard.style.display = "block";

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    if (preferredFemaleVoice) utterance.voice = preferredFemaleVoice;
    
    // Female pitch and natural cadence tuning
    utterance.pitch = 1.15;
    utterance.rate = 0.96;

    utterance.onend = () => {
        isSpeaking = false;
        orb.className = "voice-orb orb-idle";
        statusHint.textContent = "Listening via mic...";
        if (onDone) onDone();
    };

    utterance.onerror = () => {
        isSpeaking = false;
        orb.className = "voice-orb orb-idle";
        statusHint.textContent = "Listening via mic...";
        if (onDone) onDone();
    };

    window.speechSynthesis.speak(utterance);
}

function startListening() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        statusHint.textContent = "Web Speech API not supported. Use Google Chrome or Microsoft Edge.";
        return;
    }

    if (recognition) {
        try { recognition.abort(); } catch(e) {}
    }

    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
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
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            }
        }

        if (finalTranscript.trim().length > 2) {
            const { text, lang } = getAnswer(finalTranscript);
            playFemaleVoice(text, lang, () => {
                restartListening();
            });
        }
    };

    recognition.onerror = () => {
        restartListening();
    };

    recognition.onend = () => {
        if (!isSpeaking) {
            restartListening();
        }
    };

    try {
        recognition.start();
    } catch(e) {}
}

function restartListening() {
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
    }, 150);
}

document.addEventListener("visibilitychange", () => {
    if (!document.hidden && !isSpeaking) {
        statusHint.textContent = "Tab focused. Re-engaging mic...";
        restartListening();
    }
});

window.addEventListener("focus", () => {
    if (!isSpeaking) {
        restartListening();
    }
});

setInterval(() => {
    if (!isSpeaking && recognition) {
        try {
            recognition.start();
        } catch(e) {}
    }
}, 4000);

window.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        playFemaleVoice("Hello! I am the AISA Club voice assistant. I am listening, ask me anything.", "en", () => {
            startListening();
        });
    }, 600);
});
</script>
</body>
</html>
""", height=440)