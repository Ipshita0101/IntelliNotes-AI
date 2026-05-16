import streamlit as st
from groq import Groq
import requests
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

load_dotenv()


# ---------------- API KEYS ---------------- #

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OCR_API_KEY = os.getenv("OCR_API_KEY")


# ---------------- GROQ CLIENT ---------------- #

client = Groq(
    api_key=GROQ_API_KEY
)


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="IntelliNotes AI",
    page_icon="🧠",
    layout="wide"
)


# ---------------- PREMIUM UI ---------------- #

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ================= MAIN APP ================= */

.stApp {

    background:
    radial-gradient(circle at top left, rgba(124,58,237,0.18), transparent 25%),
    radial-gradient(circle at bottom right, rgba(6,182,212,0.12), transparent 25%),
    linear-gradient(135deg, #050816 0%, #0b1023 100%);

    color: white;
}

/* ================= MAIN CONTAINER ================= */

.block-container {

    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {

    background: rgba(255,255,255,0.03);

    border-right: 1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(12px);
}

section[data-testid="stSidebar"] * {

    color: white !important;
}

/* ================= HIDE STREAMLIT ================= */

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ================= TITLE ================= */

.main-title {

    font-size: 64px;

    font-weight: 800;

    line-height: 1.1;

    margin-bottom: 10px;

    background: linear-gradient(90deg,#8b5cf6,#06b6d4);

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}

.subtitle {

    color: #cbd5e1;

    font-size: 20px;

    line-height: 1.8;

    margin-bottom: 25px;
}

/* ================= HERO CARD ================= */

.hero-card {

    background: rgba(255,255,255,0.04);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 28px;

    padding: 38px;

    backdrop-filter: blur(16px);

    margin-bottom: 30px;

    box-shadow: 0 10px 35px rgba(0,0,0,0.3);
}

/* ================= METRIC CARDS ================= */

.metric-card {

    background: rgba(255,255,255,0.04);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 22px;

    padding: 24px;

    transition: 0.3s ease;

    backdrop-filter: blur(12px);

    box-shadow: 0 5px 25px rgba(0,0,0,0.2);
}

.metric-card:hover {

    transform: translateY(-5px);

    border-color: rgba(139,92,246,0.4);

    box-shadow: 0 12px 30px rgba(124,58,237,0.18);
}

.metric-label {

    color: #94a3b8;

    font-size: 13px;

    margin-bottom: 10px;

    letter-spacing: 1px;

    font-weight: 600;
}

.metric-val {

    font-size: 30px;

    font-weight: 700;

    color: white;
}

/* ================= FILE UPLOADER ================= */

[data-testid="stFileUploader"] {

    background: linear-gradient(
        135deg,
        rgba(15,23,42,0.95),
        rgba(2,6,23,0.95)
    ) !important;

    border: 1px solid rgba(139,92,246,0.18) !important;

    border-radius: 28px !important;

    padding: 28px !important;

    box-shadow:
        0 0 25px rgba(124,58,237,0.12),
        inset 0 0 30px rgba(255,255,255,0.02);

    backdrop-filter: blur(14px);

    transition: 0.3s ease;
}

[data-testid="stFileUploader"]:hover {

    border: 1px solid rgba(6,182,212,0.35) !important;

    box-shadow:
        0 0 35px rgba(6,182,212,0.15),
        0 0 20px rgba(124,58,237,0.15);
}

/* ================= INNER DROPZONE ================= */

[data-testid="stFileUploaderDropzone"] {

    background: rgba(255,255,255,0.06) !important;

    border: 2px dashed rgba(255,255,255,0.12) !important;

    border-radius: 22px !important;

    padding: 32px !important;

    transition: 0.3s ease;
}

/* ================= UPLOAD ICON ================= */

[data-testid="stFileUploader"] svg {

    color: #8B5CF6 !important;

    fill: #8B5CF6 !important;

    width: 34px !important;

    height: 34px !important;
}

/* ================= LABEL ================= */

[data-testid="stFileUploader"] label {

    color: #F8FAFC !important;

    font-size: 18px !important;

    font-weight: 700 !important;

    margin-bottom: 10px !important;
}

/* ================= UPLOAD TEXT ================= */

[data-testid="stFileUploaderDropzoneInstructions"] div {

    color: #E2E8F0 !important;

    font-size: 18px !important;

    font-weight: 500 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] span {

    color: #94A3B8 !important;

    font-size: 15px !important;
}

/* ================= ALL BUTTONS FIX ================= */

.stButton > button,
[data-testid="baseButton-secondary"] {

    background: linear-gradient(
        135deg,
        #7C3AED,
        #06B6D4
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 14px !important;

    font-size: 16px !important;

    font-weight: 700 !important;

    padding: 12px 24px !important;

    min-height: 50px !important;

    transition: all 0.3s ease !important;

    box-shadow:
        0 0 18px rgba(124,58,237,0.25);

    outline: none !important;
}

/* ================= BUTTON TEXT ================= */

.stButton > button p,
.stButton > button span,
[data-testid="baseButton-secondary"] span {

    color: white !important;

    font-weight: 700 !important;
}

/* ================= BUTTON HOVER ================= */

.stButton > button:hover,
[data-testid="baseButton-secondary"]:hover {

    background: linear-gradient(
        135deg,
        #111827,
        #020617
    ) !important;

    color: white !important;

    border: 1px solid rgba(139,92,246,0.4) !important;

    transform: translateY(-2px);

    box-shadow:
        0 0 30px rgba(124,58,237,0.35),
        0 0 18px rgba(6,182,212,0.15);
}

/* ================= BUTTON ACTIVE ================= */

.stButton > button:active,
[data-testid="baseButton-secondary"]:active {

    transform: scale(0.98);
}

/* ================= REMOVE WHITE STATES ================= */

button[kind="secondary"],
button[kind="primary"] {

    background: linear-gradient(
        135deg,
        #7C3AED,
        #06B6D4
    ) !important;

    color: white !important;

    border: none !important;
}

/* ================= EXPANDER ================= */

[data-testid="stExpander"] {

    background: rgba(255,255,255,0.04);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 18px;

    overflow: hidden;
}

/* ================= SUCCESS ================= */

.stSuccess {

    background: rgba(16,185,129,0.08) !important;

    border: 1px solid rgba(16,185,129,0.2) !important;

    border-radius: 16px !important;

    color: #6ee7b7 !important;
}

/* ================= OUTPUT BOX ================= */

.summary-box {

    background: rgba(255,255,255,0.04);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 30px;

    margin-top: 24px;

    line-height: 1.9;

    color: #e2e8f0;

    backdrop-filter: blur(12px);

    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

/* ================= SCROLLBAR ================= */

::-webkit-scrollbar {

    width: 8px;
}

::-webkit-scrollbar-thumb {

    background: rgba(139,92,246,0.35);

    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- TITLE ---------------- #

st.markdown("""
<div class="main-title">
🧠 IntelliNotes AI
</div>

<div class="subtitle">
AI-Powered Smart Notes & Exam Preparation Assistant
</div>
""", unsafe_allow_html=True)
st.info("⚠️ Best results are achieved with clear digital notes, PDFs, or typed images.")

# ---------------- CLEAN TEXT ---------------- #

def clean_text(text):

    text = text.replace("\n", " ")

    text = " ".join(text.split())

    return text

 #---------- PDF TEXT EXTRACTION ---------- #

def extract_text_from_pdf(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted

    return text


# ---------------- OCR TEXT EXTRACTION ---------------- #

def extract_text_from_image(file):

    url_api = "https://api.ocr.space/parse/image"

    response = requests.post(
        url_api,
        files={"file": file},
        data={
            "apikey": OCR_API_KEY,
            "language": "eng"
        }
    )

    result = response.json()


    # ---------- SAFE CHECK ---------- #

    if "ParsedResults" in result:

        extracted_text = result['ParsedResults'][0]['ParsedText']

        return extracted_text

    else:

        return "OCR extraction failed. Please check API key or uploaded file."


# ---------------- AI SUMMARY ---------------- #

def generate_summary(text):

    text = text[:4000]

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",
                "content": """
                You are an intelligent study assistant.

                Your task:
                - summarize notes accurately
                - do NOT invent information
                - do NOT create fake topics
                - keep original meaning
                - make output clean and exam-friendly
                """
            },

            {
                "role": "user",
                "content": f"""
                Summarize these notes into:
                1. Key Concepts
                2. Important Points
                3. Easy Exam Revision Notes

                Notes:
                {text}
                """
            }
        ],

        temperature=0.3
    )

    return response.choices[0].message.content

# ---------- QUIZ FUNCTION ---------- #

def generate_quiz(text):

    text = text[:4000]

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "system",
                "content": """
                You are an AI quiz generator.

                Generate:
                - Multiple Choice Questions
                - Short Questions
                - Important Exam Questions

                Make questions clear and educational.
                """
            },

            {
                "role": "user",
                "content": f"""
                Generate quiz questions from these notes:

                {text}
                """
            }
        ],

        temperature=0.5
    )

    return response.choices[0].message.content

# ---------------- FILE UPLOADER ---------------- #

uploaded_file = st.file_uploader(
    "📄 Upload Notes",
    type=["pdf", "png", "jpg", "jpeg"]
)


# ---------------- PROCESS FILE ---------------- #

if uploaded_file:

    file_type = uploaded_file.name.split(".")[-1].lower()

    # ---------- PDF ---------- #

    if file_type == "pdf":

        raw_text = extract_text_from_pdf(uploaded_file)

    # ---------- IMAGE OCR ---------- #

    else:

        raw_text = extract_text_from_image(uploaded_file)

    extracted_text = clean_text(raw_text)

    st.success("✅ File Uploaded Successfully")


    # ---------- VIEW EXTRACTED TEXT ---------- #

    with st.expander("📖 View Extracted Text"):

        st.write(extracted_text[:5000])

    # ---------- SUMMARY BUTTON ---------- #

    if st.button("📝 Generate AI Summary"):
        with st.spinner("Generating AI Summary..."):
            summary = generate_summary(extracted_text)

        st.markdown("## 🧠 AI Summary")

        st.write(summary)

    # ---------- QUIZ BUTTON ---------- #

    if st.button("❓ Generate AI Quiz"):
        with st.spinner("Generating Quiz..."):
            quiz = generate_quiz(extracted_text)

        st.markdown("## ❓ AI Quiz")

        st.write(quiz)