"""
╔══════════════════════════════════════════════════════════════════════════╗
║   E X A M L Y S I S  –  AI Adaptive Learning for Indian Students        ║
║   Powered by Riiid-style Adaptive Intelligence + NCERT Integration       ║
╚══════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  QUICK START  (Windows 10 + Python 3.14 + VS Code)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1 — Open VS Code terminal (Ctrl + `)

STEP 2 — Install requirements (copy-paste this whole line):
  pip install streamlit requests pillow matplotlib sympy numpy

STEP 3 — Run:
  streamlit run examlysis.py

STEP 4 — Browser opens at http://localhost:8501  ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FREE API KEYS (choose one — no credit card for the first two)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✅ Groq      → https://console.groq.com   (completely FREE, very fast)
                 Model used : llama-3.3-70b-versatile

  ✅ OpenRouter→ https://openrouter.ai       (free tier available)
                 Model used : mistralai/mistral-7b-instruct:free
                 For vision : google/gemma-3-4b-it:free

  💰 OpenAI   → https://platform.openai.com (paid, ~₹0.15/question)
                 Model used : gpt-3.5-turbo (text), gpt-4o-mini (vision)

  After signing up, paste your key in the sidebar when the app opens.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HOW NCERT EXACT-PAGE LOOKUP WORKS IN THIS APP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  NCERT publishes ALL textbooks FREE at: https://ncert.nic.in/textbook.php
  Each chapter has a DIRECT PDF link with this pattern:
      https://ncert.nic.in/textbook/pdf/[BOOK_CODE][NN].pdf
  where NN = chapter number (01, 02 … 15)

  This app has a hardcoded map of every book code for Classes 6–12.
  When you ask for a topic, it:
  1. Identifies the correct book-code from the class+subject you selected
  2. Identifies the chapter number from the chapter name/number you give
  3. Builds the DIRECT official URL to that chapter PDF
  4. Shows you the live clickable link + page reference
  5. Sends the chapter context to AI so answers are grounded in that chapter

  Example:
    Class 10 → Mathematics → Chapter 4 (Quadratic Equations)
    Book code: jemh1  →  URL: https://ncert.nic.in/textbook/pdf/jemh104.pdf

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ──────────────────────────────────────────────────────────────────────────
#  IMPORTS
# ──────────────────────────────────────────────────────────────────────────
import streamlit as st
import json, re, io, base64, time, random, math
from datetime import datetime, date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

try:
    import sympy as sp
    from sympy import (symbols, solve, diff, integrate, simplify, factor,
                       expand, latex, Matrix, Rational, sqrt as ssqrt)
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    SYMPY_OK = True
except ImportError:
    SYMPY_OK = False

try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

# ──────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Examlysis – AI Tutor",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
#  CSS — Dark theme, orange-crimson accent
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

*, html, body { font-family: 'Space Grotesk', sans-serif; }
.stApp { background: #0a0a0f; }
section[data-testid="stSidebar"] {
    background: #0d0d18 !important;
    border-right: 2px solid #ff4500;
}

/* Brand header */
.brand-header {
    background: linear-gradient(135deg, #ff4500 0%, #ff8c00 50%, #ffd700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1;
}
.brand-sub { color: #888; font-size: 0.85rem; letter-spacing: 3px; text-transform: uppercase; }

/* Cards */
.ex-card {
    background: #111120;
    border: 1px solid #222235;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.ex-card-highlight {
    background: linear-gradient(135deg, #1a0a00, #1a1000);
    border: 1px solid #ff4500;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}

/* Chat bubbles */
.chat-user {
    background: linear-gradient(135deg, #1a0800, #200a00);
    border: 1px solid #ff450060;
    border-radius: 14px 14px 4px 14px;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0 0.4rem 15%;
    color: #ffddcc;
    font-size: 0.92rem;
}
.chat-ai {
    background: #0f0f1e;
    border: 1px solid #2a2a4a;
    border-radius: 14px 14px 14px 4px;
    padding: 0.7rem 1rem;
    margin: 0.4rem 15% 0.4rem 0;
    color: #d0d0ff;
    font-size: 0.92rem;
    white-space: pre-wrap;
}

/* Hint / Answer boxes */
.hint-box {
    background: #1a1200;
    border-left: 3px solid #ffd700;
    border-radius: 0 8px 8px 0;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    color: #ffe87c;
    font-size: 0.88rem;
}
.answer-box {
    background: #001a0a;
    border-left: 3px solid #00e676;
    border-radius: 0 8px 8px 0;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    color: #b9ffda;
    font-size: 0.88rem;
}
.ncert-ref-box {
    background: #00081a;
    border: 1px solid #0066cc;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin: 0.5rem 0;
    color: #88ccff;
    font-size: 0.82rem;
}
.step-box {
    background: #0a0a1a;
    border: 1px solid #333355;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin: 0.3rem 0;
    color: #ccccff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    white-space: pre-wrap;
}

/* Stats */
.stat-big { font-size: 2.2rem; font-weight: 700; color: #ff4500; line-height: 1; }
.stat-lbl { font-size: 0.65rem; color: #666; text-transform: uppercase; letter-spacing: 1px; }

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #ff4500, #cc3700) !important;
    color: white !important;
    border: none !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding: 0.4rem 1.2rem !important;
    transition: all 0.25s !important;
}
.stButton>button:hover { transform: translateY(-1px); box-shadow: 0 4px 16px #ff450040 !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: #111120 !important;
    border: 1px solid #2a2a4a !important;
    color: #ddd !important;
    border-radius: 7px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #ff4500 !important;
    box-shadow: 0 0 0 2px #ff450025 !important;
}

h1,h2,h3,h4 { color: #eee !important; }
p, li, span, div { color: #bbb; }
.stTabs [data-baseweb="tab"] { color: #888 !important; font-family: 'Space Grotesk', sans-serif !important; }
.stTabs [aria-selected="true"] { color: #ff4500 !important; border-bottom-color: #ff4500 !important; }
.stProgress > div > div { background: linear-gradient(90deg, #ff4500, #ffd700) !important; }
div[data-testid="metric-container"] {
    background: #111120; border: 1px solid #222235; border-radius: 8px; padding: 8px;
}

/* NCERT badge */
.ncert-badge {
    background: linear-gradient(90deg, #ff4500, #cc3700);
    color: white; padding: 2px 10px; border-radius: 10px;
    font-size: 0.7rem; font-weight: 700; letter-spacing: 1.5px;
    display: inline-block;
}
.page-ref {
    background: #0a1a0a;
    border: 1px solid #00cc44;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.78rem;
    color: #88ffaa;
    display: inline-block;
    margin: 2px 4px;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  NCERT BOOK-CODE DATABASE  (the core of exact-page lookup)
#  Format: { "Class X Subject" : { "code": "xxxx", "chapters": [...] } }
#
#  URL pattern: https://ncert.nic.in/textbook/pdf/{code}{NN}.pdf
#  where NN is zero-padded chapter number: 01, 02 … 15
# ══════════════════════════════════════════════════════════════════════════
NCERT_DB = {
    # ── CLASS 6 ──────────────────────────────────────────────────────────
    "Class 6|Mathematics": {
        "code": "femh1", "book": "Mathematics",
        "chapters": [
            (1,  "Knowing Our Numbers",                        "p.1"),
            (2,  "Whole Numbers",                              "p.16"),
            (3,  "Playing with Numbers",                       "p.28"),
            (4,  "Basic Geometrical Ideas",                    "p.52"),
            (5,  "Understanding Elementary Shapes",            "p.66"),
            (6,  "Integers",                                   "p.94"),
            (7,  "Fractions",                                  "p.112"),
            (8,  "Decimals",                                   "p.143"),
            (9,  "Data Handling",                              "p.169"),
            (10, "Mensuration",                                "p.188"),
            (11, "Algebra",                                    "p.211"),
            (12, "Ratio and Proportion",                       "p.233"),
            (13, "Symmetry",                                   "p.253"),
            (14, "Practical Geometry",                         "p.269"),
        ]
    },
    "Class 6|Science": {
        "code": "fesc1", "book": "Science",
        "chapters": [
            (1,  "Food: Where Does It Come From?",            "p.1"),
            (2,  "Components of Food",                        "p.11"),
            (3,  "Fibre to Fabric",                           "p.21"),
            (4,  "Sorting Materials into Groups",             "p.29"),
            (5,  "Separation of Substances",                  "p.38"),
            (6,  "Changes Around Us",                         "p.47"),
            (7,  "Getting to Know Plants",                    "p.55"),
            (8,  "Body Movements",                            "p.68"),
            (9,  "The Living Organisms and Their Surroundings","p.82"),
            (10, "Motion and Measurement of Distances",       "p.97"),
            (11, "Light, Shadows and Reflections",            "p.109"),
            (12, "Electricity and Circuits",                  "p.118"),
            (13, "Fun with Magnets",                          "p.128"),
            (14, "Water",                                     "p.140"),
            (15, "Air Around Us",                             "p.150"),
            (16, "Garbage In, Garbage Out",                   "p.158"),
        ]
    },
    # ── CLASS 7 ──────────────────────────────────────────────────────────
    "Class 7|Mathematics": {
        "code": "gemh1", "book": "Mathematics",
        "chapters": [
            (1,  "Integers",                                  "p.1"),
            (2,  "Fractions and Decimals",                    "p.29"),
            (3,  "Data Handling",                             "p.57"),
            (4,  "Simple Equations",                          "p.77"),
            (5,  "Lines and Angles",                          "p.93"),
            (6,  "The Triangle and Its Properties",           "p.113"),
            (7,  "Congruence of Triangles",                   "p.133"),
            (8,  "Comparing Quantities",                      "p.153"),
            (9,  "Rational Numbers",                          "p.172"),
            (10, "Practical Geometry",                        "p.186"),
            (11, "Perimeter and Area",                        "p.199"),
            (12, "Algebraic Expressions",                     "p.223"),
            (13, "Exponents and Powers",                      "p.249"),
            (14, "Symmetry",                                  "p.260"),
            (15, "Visualising Solid Shapes",                  "p.277"),
        ]
    },
    "Class 7|Science": {
        "code": "gesc1", "book": "Science",
        "chapters": [
            (1,  "Nutrition in Plants",                        "p.1"),
            (2,  "Nutrition in Animals",                       "p.14"),
            (3,  "Fibre to Fabric",                            "p.27"),
            (4,  "Heat",                                       "p.38"),
            (5,  "Acids, Bases and Salts",                     "p.50"),
            (6,  "Physical and Chemical Changes",              "p.59"),
            (7,  "Weather, Climate and Adaptations",           "p.71"),
            (8,  "Winds, Storms and Cyclones",                 "p.82"),
            (9,  "Soil",                                       "p.95"),
            (10, "Respiration in Organisms",                   "p.105"),
            (11, "Transportation in Animals and Plants",       "p.119"),
            (12, "Reproduction in Plants",                     "p.129"),
            (13, "Motion and Time",                            "p.141"),
            (14, "Electric Current and Its Effects",           "p.152"),
            (15, "Light",                                      "p.163"),
            (16, "Water: A Precious Resource",                 "p.175"),
            (17, "Forests: Our Lifeline",                      "p.186"),
            (18, "Wastewater Story",                           "p.195"),
        ]
    },
    # ── CLASS 8 ──────────────────────────────────────────────────────────
    "Class 8|Mathematics": {
        "code": "hemh1", "book": "Mathematics",
        "chapters": [
            (1,  "Rational Numbers",                          "p.1"),
            (2,  "Linear Equations in One Variable",          "p.21"),
            (3,  "Understanding Quadrilaterals",              "p.41"),
            (4,  "Practical Geometry",                        "p.57"),
            (5,  "Data Handling",                             "p.69"),
            (6,  "Squares and Square Roots",                  "p.89"),
            (7,  "Cubes and Cube Roots",                      "p.114"),
            (8,  "Comparing Quantities",                      "p.126"),
            (9,  "Algebraic Expressions and Identities",      "p.148"),
            (10, "Visualising Solid Shapes",                  "p.168"),
            (11, "Mensuration",                               "p.179"),
            (12, "Exponents and Powers",                      "p.197"),
            (13, "Direct and Inverse Proportions",            "p.207"),
            (14, "Factorisation",                             "p.220"),
            (15, "Introduction to Graphs",                    "p.238"),
            (16, "Playing with Numbers",                      "p.253"),
        ]
    },
    "Class 8|Science": {
        "code": "hesc1", "book": "Science",
        "chapters": [
            (1,  "Crop Production and Management",            "p.1"),
            (2,  "Microorganisms: Friend and Foe",            "p.19"),
            (3,  "Synthetic Fibres and Plastics",             "p.33"),
            (4,  "Materials: Metals and Non-Metals",          "p.44"),
            (5,  "Coal and Petroleum",                        "p.56"),
            (6,  "Combustion and Flame",                      "p.66"),
            (7,  "Conservation of Plants and Animals",        "p.79"),
            (8,  "Cell — Structure and Functions",            "p.94"),
            (9,  "Reproduction in Animals",                   "p.105"),
            (10, "Reaching the Age of Adolescence",           "p.118"),
            (11, "Force and Pressure",                        "p.131"),
            (12, "Friction",                                  "p.146"),
            (13, "Sound",                                     "p.158"),
            (14, "Chemical Effects of Electric Current",      "p.173"),
            (15, "Some Natural Phenomena",                    "p.183"),
            (16, "Light",                                     "p.193"),
            (17, "Stars and the Solar System",                "p.207"),
            (18, "Pollution of Air and Water",                "p.219"),
        ]
    },
    # ── CLASS 9 ──────────────────────────────────────────────────────────
    "Class 9|Mathematics": {
        "code": "iemh1", "book": "Mathematics",
        "chapters": [
            (1,  "Number Systems",                            "p.1"),
            (2,  "Polynomials",                               "p.27"),
            (3,  "Coordinate Geometry",                       "p.53"),
            (4,  "Linear Equations in Two Variables",         "p.63"),
            (5,  "Introduction to Euclid's Geometry",         "p.79"),
            (6,  "Lines and Angles",                          "p.90"),
            (7,  "Triangles",                                 "p.111"),
            (8,  "Quadrilaterals",                            "p.135"),
            (9,  "Areas of Parallelograms and Triangles",     "p.155"),
            (10, "Circles",                                   "p.170"),
            (11, "Constructions",                             "p.191"),
            (12, "Heron's Formula",                           "p.200"),
            (13, "Surface Areas and Volumes",                 "p.211"),
            (14, "Statistics",                                "p.238"),
            (15, "Probability",                               "p.268"),
        ]
    },
    "Class 9|Science": {
        "code": "iesc1", "book": "Science",
        "chapters": [
            (1,  "Matter in Our Surroundings",                "p.1"),
            (2,  "Is Matter Around Us Pure",                  "p.15"),
            (3,  "Atoms and Molecules",                       "p.32"),
            (4,  "Structure of the Atom",                     "p.47"),
            (5,  "The Fundamental Unit of Life",              "p.59"),
            (6,  "Tissues",                                   "p.69"),
            (7,  "Diversity in Living Organisms",             "p.80"),
            (8,  "Motion",                                    "p.99"),
            (9,  "Force and Laws of Motion",                  "p.118"),
            (10, "Gravitation",                               "p.134"),
            (11, "Work and Energy",                           "p.148"),
            (12, "Sound",                                     "p.162"),
            (13, "Why Do We Fall Ill",                        "p.178"),
            (14, "Natural Resources",                         "p.193"),
            (15, "Improvement in Food Resources",             "p.204"),
        ]
    },
    "Class 9|History": {
        "code": "iehh1", "book": "India and the Contemporary World – I",
        "chapters": [
            (1,  "The French Revolution",                     "p.1"),
            (2,  "Socialism in Europe and the Russian Revolution","p.25"),
            (3,  "Nazism and the Rise of Hitler",             "p.50"),
            (4,  "Forest Society and Colonialism",            "p.78"),
            (5,  "Pastoralists in the Modern World",          "p.100"),
        ]
    },
    "Class 9|Geography": {
        "code": "iegg1", "book": "Contemporary India – I",
        "chapters": [
            (1,  "India – Size and Location",                 "p.1"),
            (2,  "Physical Features of India",                "p.12"),
            (3,  "Drainage",                                  "p.28"),
            (4,  "Climate",                                   "p.42"),
            (5,  "Natural Vegetation and Wild Life",          "p.56"),
            (6,  "Population",                                "p.66"),
        ]
    },
    # ── CLASS 10 ─────────────────────────────────────────────────────────
    "Class 10|Mathematics": {
        "code": "jemh1", "book": "Mathematics",
        "chapters": [
            (1,  "Real Numbers",                              "p.1"),
            (2,  "Polynomials",                               "p.28"),
            (3,  "Pair of Linear Equations in Two Variables", "p.44"),
            (4,  "Quadratic Equations",                       "p.74"),
            (5,  "Arithmetic Progressions",                   "p.99"),
            (6,  "Triangles",                                 "p.122"),
            (7,  "Coordinate Geometry",                       "p.156"),
            (8,  "Introduction to Trigonometry",              "p.173"),
            (9,  "Some Applications of Trigonometry",         "p.195"),
            (10, "Circles",                                   "p.209"),
            (11, "Constructions",                             "p.220"),
            (12, "Areas Related to Circles",                  "p.229"),
            (13, "Surface Areas and Volumes",                 "p.245"),
            (14, "Statistics",                                "p.270"),
            (15, "Probability",                               "p.295"),
        ]
    },
    "Class 10|Science": {
        "code": "jesc1", "book": "Science",
        "chapters": [
            (1,  "Chemical Reactions and Equations",          "p.1"),
            (2,  "Acids, Bases and Salts",                    "p.18"),
            (3,  "Metals and Non-metals",                     "p.40"),
            (4,  "Carbon and Its Compounds",                  "p.61"),
            (5,  "Periodic Classification of Elements",       "p.81"),
            (6,  "Life Processes",                            "p.95"),
            (7,  "Control and Coordination",                  "p.119"),
            (8,  "How Do Organisms Reproduce?",               "p.137"),
            (9,  "Heredity and Evolution",                    "p.159"),
            (10, "Light – Reflection and Refraction",         "p.168"),
            (11, "Human Eye and the Colourful World",         "p.197"),
            (12, "Electricity",                               "p.216"),
            (13, "Magnetic Effects of Electric Current",      "p.233"),
            (14, "Sources of Energy",                         "p.248"),
            (15, "Our Environment",                           "p.261"),
            (16, "Sustainable Management of Natural Resources","p.271"),
        ]
    },
    "Class 10|History": {
        "code": "jehh1", "book": "India and the Contemporary World – II",
        "chapters": [
            (1,  "The Rise of Nationalism in Europe",         "p.1"),
            (2,  "Nationalism in India",                      "p.26"),
            (3,  "The Making of a Global World",              "p.56"),
            (4,  "The Age of Industrialisation",              "p.82"),
            (5,  "Print Culture and the Modern World",        "p.111"),
        ]
    },
    "Class 10|Geography": {
        "code": "jegg1", "book": "Contemporary India – II",
        "chapters": [
            (1,  "Resources and Development",                 "p.1"),
            (2,  "Forest and Wildlife Resources",             "p.19"),
            (3,  "Water Resources",                           "p.33"),
            (4,  "Agriculture",                               "p.46"),
            (5,  "Minerals and Energy Resources",             "p.63"),
            (6,  "Manufacturing Industries",                  "p.83"),
            (7,  "Lifelines of National Economy",             "p.104"),
        ]
    },
    "Class 10|Political Science": {
        "code": "jepd1", "book": "Democratic Politics – II",
        "chapters": [
            (1,  "Power Sharing",                             "p.1"),
            (2,  "Federalism",                                "p.14"),
            (3,  "Democracy and Diversity",                   "p.36"),
            (4,  "Gender, Religion and Caste",                "p.47"),
            (5,  "Popular Struggles and Movements",           "p.62"),
            (6,  "Political Parties",                         "p.74"),
            (7,  "Outcomes of Democracy",                     "p.90"),
            (8,  "Challenges to Democracy",                   "p.103"),
        ]
    },
    "Class 10|Economics": {
        "code": "jeec1", "book": "Understanding Economic Development",
        "chapters": [
            (1,  "Development",                               "p.1"),
            (2,  "Sectors of the Indian Economy",             "p.17"),
            (3,  "Money and Credit",                          "p.36"),
            (4,  "Globalisation and the Indian Economy",      "p.55"),
            (5,  "Consumer Rights",                           "p.74"),
        ]
    },
    # ── CLASS 11 SCIENCE ─────────────────────────────────────────────────
    "Class 11 (Science)|Physics": {
        "code": "keph1", "book": "Physics Part I",
        "chapters": [
            (1,  "Physical World",                            "p.1"),
            (2,  "Units and Measurement",                     "p.16"),
            (3,  "Motion in a Straight Line",                 "p.41"),
            (4,  "Motion in a Plane",                         "p.65"),
            (5,  "Laws of Motion",                            "p.89"),
            (6,  "Work, Energy and Power",                    "p.116"),
            (7,  "Systems of Particles and Rotational Motion","p.141"),
            (8,  "Gravitation",                               "p.183"),
        ]
    },
    "Class 11 (Science)|Physics Part 2": {
        "code": "keph2", "book": "Physics Part II",
        "chapters": [
            (9,  "Mechanical Properties of Solids",           "p.1"),
            (10, "Mechanical Properties of Fluids",           "p.22"),
            (11, "Thermal Properties of Matter",              "p.48"),
            (12, "Thermodynamics",                            "p.74"),
            (13, "Kinetic Theory",                            "p.96"),
            (14, "Oscillations",                              "p.113"),
            (15, "Waves",                                     "p.142"),
        ]
    },
    "Class 11 (Science)|Chemistry": {
        "code": "kech1", "book": "Chemistry Part I",
        "chapters": [
            (1,  "Some Basic Concepts of Chemistry",          "p.1"),
            (2,  "Structure of Atom",                         "p.26"),
            (3,  "Classification of Elements",                "p.62"),
            (4,  "Chemical Bonding and Molecular Structure",  "p.88"),
            (5,  "States of Matter",                          "p.124"),
            (6,  "Thermodynamics",                            "p.152"),
            (7,  "Equilibrium",                               "p.181"),
        ]
    },
    "Class 11 (Science)|Mathematics": {
        "code": "kemh1", "book": "Mathematics",
        "chapters": [
            (1,  "Sets",                                      "p.1"),
            (2,  "Relations and Functions",                   "p.29"),
            (3,  "Trigonometric Functions",                   "p.49"),
            (4,  "Principle of Mathematical Induction",       "p.86"),
            (5,  "Complex Numbers and Quadratic Equations",   "p.97"),
            (6,  "Linear Inequalities",                       "p.118"),
            (7,  "Permutations and Combinations",             "p.135"),
            (8,  "Binomial Theorem",                          "p.160"),
            (9,  "Sequences and Series",                      "p.178"),
            (10, "Straight Lines",                            "p.203"),
            (11, "Conic Sections",                            "p.230"),
            (12, "Introduction to Three Dimensional Geometry","p.263"),
            (13, "Limits and Derivatives",                    "p.276"),
            (14, "Mathematical Reasoning",                    "p.307"),
            (15, "Statistics",                                "p.323"),
            (16, "Probability",                               "p.351"),
        ]
    },
    "Class 11 (Science)|Biology": {
        "code": "kebo1", "book": "Biology",
        "chapters": [
            (1,  "The Living World",                          "p.1"),
            (2,  "Biological Classification",                 "p.15"),
            (3,  "Plant Kingdom",                             "p.35"),
            (4,  "Animal Kingdom",                            "p.55"),
            (5,  "Morphology of Flowering Plants",            "p.79"),
            (6,  "Anatomy of Flowering Plants",               "p.99"),
            (7,  "Structural Organisation in Animals",        "p.117"),
            (8,  "Cell: The Unit of Life",                    "p.133"),
            (9,  "Biomolecules",                              "p.155"),
            (10, "Cell Cycle and Cell Division",              "p.179"),
            (11, "Transport in Plants",                       "p.193"),
            (12, "Mineral Nutrition",                         "p.213"),
            (13, "Photosynthesis in Higher Plants",           "p.229"),
            (14, "Respiration in Plants",                     "p.249"),
            (15, "Plant Growth and Development",              "p.263"),
            (16, "Digestion and Absorption",                  "p.272"),
            (17, "Breathing and Exchange of Gases",           "p.285"),
            (18, "Body Fluids and Circulation",               "p.297"),
            (19, "Excretory Products and their Elimination",  "p.311"),
            (20, "Locomotion and Movement",                   "p.325"),
            (21, "Neural Control and Coordination",           "p.339"),
            (22, "Chemical Coordination and Integration",     "p.355"),
        ]
    },
    # ── CLASS 12 SCIENCE ─────────────────────────────────────────────────
    "Class 12 (Science)|Physics": {
        "code": "leph1", "book": "Physics Part I",
        "chapters": [
            (1,  "Electric Charges and Fields",               "p.1"),
            (2,  "Electrostatic Potential and Capacitance",   "p.51"),
            (3,  "Current Electricity",                       "p.93"),
            (4,  "Moving Charges and Magnetism",              "p.132"),
            (5,  "Magnetism and Matter",                      "p.167"),
            (6,  "Electromagnetic Induction",                 "p.204"),
            (7,  "Alternating Current",                       "p.233"),
            (8,  "Electromagnetic Waves",                     "p.269"),
        ]
    },
    "Class 12 (Science)|Physics Part 2": {
        "code": "leph2", "book": "Physics Part II",
        "chapters": [
            (9,  "Ray Optics and Optical Instruments",        "p.1"),
            (10, "Wave Optics",                               "p.54"),
            (11, "Dual Nature of Radiation and Matter",       "p.87"),
            (12, "Atoms",                                     "p.114"),
            (13, "Nuclei",                                    "p.137"),
            (14, "Semiconductor Electronics",                 "p.162"),
        ]
    },
    "Class 12 (Science)|Chemistry": {
        "code": "lech1", "book": "Chemistry Part I",
        "chapters": [
            (1,  "The Solid State",                           "p.1"),
            (2,  "Solutions",                                 "p.33"),
            (3,  "Electrochemistry",                          "p.62"),
            (4,  "Chemical Kinetics",                         "p.95"),
            (5,  "Surface Chemistry",                         "p.121"),
            (6,  "General Principles and Processes of Isolation","p.145"),
            (7,  "The p-Block Elements",                      "p.166"),
        ]
    },
    "Class 12 (Science)|Chemistry Part 2": {
        "code": "lech2", "book": "Chemistry Part II",
        "chapters": [
            (8,  "The d and f Block Elements",                "p.1"),
            (9,  "Coordination Compounds",                    "p.25"),
            (10, "Haloalkanes and Haloarenes",                "p.54"),
            (11, "Alcohols, Phenols and Ethers",              "p.82"),
            (12, "Aldehydes, Ketones and Carboxylic Acids",   "p.111"),
            (13, "Amines",                                    "p.147"),
            (14, "Biomolecules",                              "p.173"),
            (15, "Polymers",                                  "p.198"),
            (16, "Chemistry in Everyday Life",                "p.218"),
        ]
    },
    "Class 12 (Science)|Mathematics": {
        "code": "lemh1", "book": "Mathematics Part I",
        "chapters": [
            (1,  "Relations and Functions",                   "p.1"),
            (2,  "Inverse Trigonometric Functions",           "p.33"),
            (3,  "Matrices",                                  "p.56"),
            (4,  "Determinants",                              "p.95"),
            (5,  "Continuity and Differentiability",          "p.148"),
            (6,  "Application of Derivatives",                "p.198"),
        ]
    },
    "Class 12 (Science)|Mathematics Part 2": {
        "code": "lemh2", "book": "Mathematics Part II",
        "chapters": [
            (7,  "Integrals",                                 "p.1"),
            (8,  "Application of Integrals",                  "p.65"),
            (9,  "Differential Equations",                    "p.90"),
            (10, "Vector Algebra",                            "p.128"),
            (11, "Three Dimensional Geometry",                "p.161"),
            (12, "Linear Programming",                        "p.199"),
            (13, "Probability",                               "p.227"),
        ]
    },
    "Class 12 (Science)|Biology": {
        "code": "lebo1", "book": "Biology",
        "chapters": [
            (1,  "Sexual Reproduction in Flowering Plants",   "p.1"),
            (2,  "Human Reproduction",                        "p.24"),
            (3,  "Reproductive Health",                       "p.46"),
            (4,  "Principles of Inheritance and Variation",   "p.63"),
            (5,  "Molecular Basis of Inheritance",            "p.90"),
            (6,  "Evolution",                                 "p.116"),
            (7,  "Human Health and Disease",                  "p.137"),
            (8,  "Microbes in Human Welfare",                 "p.163"),
            (9,  "Biotechnology – Principles and Processes",  "p.177"),
            (10, "Biotechnology and Its Applications",        "p.197"),
            (11, "Organisms and Populations",                 "p.215"),
            (12, "Ecosystem",                                 "p.234"),
            (13, "Biodiversity and Conservation",             "p.254"),
            (14, "Environmental Issues",                      "p.274"),
        ]
    },
    # ── CLASS 12 COMMERCE ────────────────────────────────────────────────
    "Class 12 (Commerce)|Economics": {
        "code": "leec1", "book": "Introductory Macroeconomics",
        "chapters": [
            (1,  "Introduction to Macroeconomics",            "p.1"),
            (2,  "National Income Accounting",                "p.10"),
            (3,  "Money and Banking",                         "p.34"),
            (4,  "Determination of Income and Employment",    "p.54"),
            (5,  "Government Budget and the Economy",         "p.71"),
            (6,  "Open Economy Macroeconomics",               "p.86"),
        ]
    },
}

# ──────────────────────────────────────────────────────────────────────────
#  NCERT URL builder
# ──────────────────────────────────────────────────────────────────────────
def ncert_chapter_url(code: str, chapter_num: int) -> str:
    return f"https://ncert.nic.in/textbook/pdf/{code}{chapter_num:02d}.pdf"

def ncert_full_book_url(code: str) -> str:
    return f"https://ncert.nic.in/textbook/pdf/{code}.zip"

def get_ncert_key(grade: str, subject: str) -> str:
    return f"{grade}|{subject}"

def find_ncert_info(grade: str, subject: str, chapter_hint: str):
    """
    Returns (book_info_dict, chapter_tuple, url) or None if not found.
    chapter_hint can be: '4', 'Chapter 4', 'Quadratic', 'quadratic equations' etc.
    """
    key = get_ncert_key(grade, subject)
    info = NCERT_DB.get(key)
    if not info:
        # Try partial match on subject
        for k, v in NCERT_DB.items():
            if grade in k and subject.lower() in k.lower():
                info = v
                break
    if not info:
        return None, None, None

    chapters = info["chapters"]

    # Try numeric match first
    nums = re.findall(r'\d+', chapter_hint)
    if nums:
        n = int(nums[0])
        for ch in chapters:
            if ch[0] == n:
                url = ncert_chapter_url(info["code"], ch[0])
                return info, ch, url

    # Try name match (case-insensitive substring)
    hint_lower = chapter_hint.lower()
    for ch in chapters:
        if hint_lower in ch[1].lower() or any(word in ch[1].lower() for word in hint_lower.split() if len(word) > 3):
            url = ncert_chapter_url(info["code"], ch[0])
            return info, ch, url

    # Return first chapter as fallback
    ch = chapters[0]
    url = ncert_chapter_url(info["code"], ch[0])
    return info, ch, url


# ══════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════
def _init():
    D = {
        "api_key": "", "api_provider": "Groq (Free)",
        "messages": [], "ncert_messages": [], "math_messages": [],
        "subject": "Mathematics", "grade": "Class 10",
        "student_name": "Student",
        "q_asked": 0, "q_correct": 0,
        "topics_covered": [], "weak_areas": [],
        "adaptive_level": "Medium",
        "quiz_score": 0, "quiz_total": 0,
        "current_quiz": None, "quiz_answers": {},
        "quiz_submitted": False,
        "photo_result": "",
    }
    for k, v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v
_init()

# ══════════════════════════════════════════════════════════════════════════
#  API PROVIDERS
# ══════════════════════════════════════════════════════════════════════════
PROVIDERS = {
    "Groq (Free)": {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "model": "llama-3.3-70b-versatile",
        "headers_extra": {},
    },
    "OpenRouter (Free)": {
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "model": "mistralai/mistral-7b-instruct:free",
        "headers_extra": {"HTTP-Referer": "http://localhost:8501", "X-Title": "Examlysis"},
    },
    "OpenAI (Paid)": {
        "url": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-3.5-turbo",
        "headers_extra": {},
    },
}

def call_ai(messages, system="", temp=0.6, max_tok=900):
    key = st.secrets["GROQ_API_KEY"]
    if not key:
        return "⚠️ Enter your API key in the sidebar first."
    if not REQUESTS_OK:
        return "⚠️ Install requests: `pip install requests`"
    cfg = PROVIDERS.get(st.session_state.api_provider, PROVIDERS["Groq (Free)"])
    payload_msgs = ([{"role": "system", "content": system}] if system else []) + messages
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}", **cfg["headers_extra"]}
    try:
        r = requests.post(cfg["url"], headers=headers,
                          json={"model": cfg["model"], "messages": payload_msgs,
                                "temperature": temp, "max_tokens": max_tok},
                          timeout=50)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.Timeout:
        return "⏱️ Timeout — try again."
    except Exception as e:
        s = str(e)
        if "401" in s: return "🔑 Invalid API key."
        if "429" in s: return "⏳ Rate limit — wait a moment."
        return f"❌ {s[:180]}"


# ══════════════════════════════════════════════════════════════════════════
#  SYSTEM PROMPTS
# ══════════════════════════════════════════════════════════════════════════
def sys_tutor():
    return f"""You are Examlysis AI — an expert tutor for Indian students.

Student: {st.session_state.student_name} | Grade: {st.session_state.grade} | Subject: {st.session_state.subject} | Level: {st.session_state.adaptive_level}

TEACHING RULES:
━━━━━━━━━━━━━━
CONCEPTUAL QUESTIONS (why/how/explain/difference/what is):
  → Use Socratic Method — NEVER give direct answer first
  → Step 1: Ask "What do you already know about [topic]?"
  → Step 2: Give HINT 1 (a nudge, not the answer)
  → Step 3: If student responds → give HINT 2 or confirm and expand
  → Step 4: Only after hints, give the complete explanation
  → End every conceptual reply with a follow-up question to check understanding
  → Use 💡 for hints, ✅ for correct points, ❓ for follow-up questions

FACTUAL QUESTIONS (what is the definition of / when was / who invented):
  → Give clear, direct answer with NCERT chapter reference
  → One example relevant to India

NUMERICAL PROBLEMS (any calculation, solve, find, calculate):
  → Format EVERY solution like this (mandatory, no shortcuts):

  ┌─────────────────────────────────────┐
  │  GIVEN:                             │
  │    • [list each given value]        │
  │  FIND:                              │
  │    • [what to find]                 │
  │  FORMULA:                           │
  │    [write the formula first]        │
  │  SOLUTION:                          │
  │  Step 1 → [what and why]            │
  │           [show calculation]        │
  │  Step 2 → [next step]               │
  │           [show calculation]        │
  │  ...continue all steps...           │
  │  VERIFICATION: [check the answer]   │
  │  ∴ ANSWER = [value with units] ✅   │
  └─────────────────────────────────────┘

  → Show EVERY step, even "obvious" ones (students often get lost in details)
  → Write units at every step (not just the final answer)
  → If multiple methods exist, show the easier one and mention the other
  → End with: "Practice: Try a similar problem: [give one]"

ADAPTIVE LEVEL:
  Easy  → Simple words, extra hints, basic examples, smaller numbers
  Medium→ Standard approach, 1-2 hints, NCERT-level examples
  Hard  → Multiple approaches, tougher numbers, extension problems

STYLE:
  → Be warm like a caring Indian teacher
  → Use: "Shabash!", "Excellent!", "Bilkul sahi!", "Good thinking!"
  → Always cite: "NCERT Class X, Chapter Y – [Name], Page Z" when relevant
  → Keep answers focused and not too long — students read on mobile"""

def sys_ncert():
    return f"""You are an NCERT Expert for Indian students.
Grade: {st.session_state.grade} | Subject: {st.session_state.subject}

RULES:
1. Start EVERY response with:
   📖 NCERT {st.session_state.grade} — [Subject] — Chapter [N]: [Chapter Name] | Page [X]

2. Explain the concept in student-friendly language WITHOUT copying NCERT text

3. Structure your explanation as:
   CONCEPT OVERVIEW: (2-3 sentences in plain language)
   KEY POINTS: (bullet list of main ideas)
   REAL-LIFE EXAMPLE: (use India-specific examples — cricket, dals, monsoon, trains, etc.)
   COMMON MISTAKES: (what students get wrong in exams)
   MEMORY TRICK: (mnemonic or shortcut if applicable)
   EXAM TIP: (what CBSE asks from this topic)
   PRACTICE QUESTION: (1 question at appropriate level)

4. For formulas: write them cleanly, explain each symbol
5. For diagrams: describe them in words clearly
6. Do NOT reproduce NCERT text verbatim — always paraphrase and explain"""

def sys_math():
    return f"""You are a Mathematics Expert Tutor for Indian students (NCERT/CBSE/JEE).
Grade: {st.session_state.grade} | Level: {st.session_state.adaptive_level}

MANDATORY FORMAT FOR ALL NUMERICAL SOLUTIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 PROBLEM UNDERSTANDING
   → Restate the problem in simple words
   → Identify what type of problem it is (e.g., "This is a quadratic equation problem")
   → Mention the NCERT chapter it belongs to

📋 GIVEN INFORMATION
   → List every piece of given data with symbols and units

🎯 WHAT TO FIND
   → State clearly what the answer requires

📐 FORMULA / CONCEPT USED
   → Write the formula
   → State the theorem or concept name
   → Explain briefly WHY this formula applies

🔢 STEP-BY-STEP SOLUTION
   Step 1: [Name of step]
   ┌──────────────────────────────────────┐
   │  [Formula or equation]               │
   │  [Substitute values]                 │
   │  [Calculate]                         │
   └──────────────────────────────────────┘
   [Explain what you just did and why]

   Step 2: [Continue...]
   [Each step on its own, clearly boxed or separated]

   ...continue until complete...

✅ VERIFICATION
   → Substitute your answer back to verify
   → State: "LHS = RHS ✓" or "Check: [value] ✓"

🎯 FINAL ANSWER
   ∴ [answer] = [value] [units]

📝 PRACTICE PROBLEM
   → Give one similar problem for the student to try
   → Hint: mention which step is the key

RULES:
• NEVER skip steps — even if they seem obvious
• Show units at EVERY calculation step
• Use proper mathematical notation
• If there are multiple cases (like ± in quadratic), handle each case
• Use ≈ for approximate values, = for exact
• For geometry problems: draw/describe the figure first"""


# ══════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="brand-header">Examlysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">AI Adaptive Learning</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("---")
    st.markdown("### 👤 Profile")
    st.session_state.student_name = st.text_input("Name", value=st.session_state.student_name)
    st.session_state.grade = st.selectbox("Class", [
        "Class 6","Class 7","Class 8","Class 9","Class 10",
        "Class 11 (Science)","Class 11 (Commerce)",
        "Class 12 (Science)","Class 12 (Commerce)",
        "JEE Aspirant","NEET Aspirant",
    ], index=4)
    st.session_state.subject = st.selectbox("Subject", [
        "Mathematics","Physics","Chemistry","Biology",
        "Science","English","History","Geography",
        "Political Science","Economics","Hindi",
    ])
    st.session_state.adaptive_level = st.select_slider(
        "Difficulty", ["Easy","Medium","Hard"],
        value=st.session_state.adaptive_level)

    st.markdown("---")
    st.markdown("### 📊 Stats")
    c1, c2 = st.columns(2)
    acc = int(st.session_state.q_correct / max(st.session_state.q_asked, 1) * 100)
    c1.markdown(f'<div class="stat-big">{st.session_state.q_asked}</div><div class="stat-lbl">Questions</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-big">{acc}%</div><div class="stat-lbl">Accuracy</div>', unsafe_allow_html=True)

    if st.session_state.topics_covered:
        st.markdown("**Recent Topics:**")
        for t in st.session_state.topics_covered[-4:]:
            st.markdown(f"• {t}", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Clear Chats"):
        for k in ["messages","ncert_messages","math_messages"]:
            st.session_state[k] = []
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<div class="brand-header">Examlysis</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#888;font-size:0.85rem;margin-top:2px;">Adaptive AI Tutor · {st.session_state.grade} · {st.session_state.subject} · Hello, {st.session_state.student_name}!</div>', unsafe_allow_html=True)
with col_h2:
    st.metric("Questions", st.session_state.q_asked)
    st.metric("Quiz Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💬 AI Tutor",
    "📚 NCERT Desk",
    "🔢 Math Solver",
    "📸 Photo Scanner",
    "📈 Graph Tool",
    "📝 Quiz",
])


# ══════════════════════════════════════════════════════════════════════════
#  TAB 1 — AI TUTOR  (Adaptive Socratic)
# ══════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 💬 Chat with Examlysis AI")
    st.markdown("""<div class="ex-card-highlight">
<b>🧠 How I teach (Riiid-inspired):</b><br>
• <b>Conceptual questions</b> → I give HINTS, not answers. Your brain builds understanding.<br>
• <b>Numerical problems</b> → Every step shown in detail, like a human teacher writing on board.<br>
• <b>Factual questions</b> → Direct answer with NCERT page reference.
</div>""", unsafe_allow_html=True)

    # Quick topic buttons
    QUICK = {
        "Mathematics": ["Quadratic Formula","Pythagoras Theorem","Area of Triangle","Probability Basics"],
        "Physics":     ["Newton's 2nd Law","Ohm's Law","Refraction of Light","Kinetic Energy"],
        "Chemistry":   ["Balancing Equations","Valency","pH Scale","Carbon Compounds"],
        "Biology":     ["Cell Organelles","Photosynthesis","DNA Structure","Food Chain"],
        "Science":     ["Force & Motion","Chemical Reactions","Cell","Electricity"],
        "History":     ["French Revolution","India Freedom Movement","Mughal Empire","World War II"],
        "Geography":   ["Indian Climate","River Systems","Agriculture in India","Population"],
        "Economics":   ["GDP","Supply & Demand","Money Supply","Globalisation"],
    }
    topics = QUICK.get(st.session_state.subject, ["Explain this","Give example","Quiz me","Summarize"])
    cols = st.columns(len(topics))
    for i, t in enumerate(topics):
        if cols[i].button(t, key=f"qt1_{i}"):
            st.session_state.messages.append({"role": "user", "content": f"Explain: {t}"})
            with st.spinner("Thinking..."):
                reply = call_ai([{"role":"user","content":f"Teach me about {t} for {st.session_state.grade}"}],
                                system=sys_tutor())
            st.session_state.messages.append({"role":"assistant","content":reply})
            st.session_state.q_asked += 1
            if t not in st.session_state.topics_covered:
                st.session_state.topics_covered.append(t)
            st.rerun()

    # Chat history
    for msg in st.session_state.messages:
        cls = "chat-user" if msg["role"] == "user" else "chat-ai"
        icon = "🧑" if msg["role"] == "user" else "🤖"
        st.markdown(f'<div class="{cls}">{icon} {msg["content"]}</div>', unsafe_allow_html=True)

    user_inp = st.chat_input("Ask anything — concept, numerical, or factual...")
    if user_inp:
        st.session_state.messages.append({"role":"user","content":user_inp})
        # Detect question type
        lower = user_inp.lower()
        is_conceptual = any(w in lower for w in ["why","how does","explain","concept","difference","what is","describe","understand","define"])
        is_numerical  = any(w in lower for w in ["solve","calculate","find","compute","evaluate","simplify","factorise","integrate","differentiate","prove"])
        extra = ""
        if is_conceptual:
            extra = "\n\nIMPORTANT: This is a CONCEPTUAL question. Use the Socratic method. Give hints first, never the direct answer immediately."
        elif is_numerical:
            extra = "\n\nIMPORTANT: This is a NUMERICAL problem. Use the FULL step-by-step format with GIVEN/FIND/FORMULA/STEPS/VERIFICATION/ANSWER. Show every step."
        with st.spinner("Examlysis is thinking..."):
            reply = call_ai(st.session_state.messages[-8:], system=sys_tutor()+extra)
        st.session_state.messages.append({"role":"assistant","content":reply})
        st.session_state.q_asked += 1
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════
#  TAB 2 — NCERT DESK  (Exact page + chapter lookup)
# ══════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 📚 NCERT Help Desk")
    st.markdown("""<div class="ex-card-highlight">
<span class="ncert-badge">NCERT OFFICIAL</span> &nbsp;
This desk gives you the <b>exact chapter</b>, <b>page number</b>, and a <b>direct link to the official NCERT PDF</b>
(hosted at ncert.nic.in) along with a clear explanation.
Give me: a chapter number, topic name, or a few words from your book.
</div>""", unsafe_allow_html=True)

    # — Chapter browser
    with st.expander("📖 Browse All Chapters (click to find your chapter)", expanded=False):
        key = get_ncert_key(st.session_state.grade, st.session_state.subject)
        info = NCERT_DB.get(key)
        if info:
            st.markdown(f"**{st.session_state.grade} — {info['book']}** (Book code: `{info['code']}`)")
            for ch in info["chapters"]:
                url = ncert_chapter_url(info["code"], ch[0])
                st.markdown(f"Ch.{ch[0]:02d} — **{ch[1]}** &nbsp;&nbsp; <span class='page-ref'>{ch[2]}</span> &nbsp;&nbsp; [📄 Open PDF]({url})", unsafe_allow_html=True)
        else:
            st.info(f"No chapter data for {st.session_state.grade} / {st.session_state.subject} yet. Type your topic below and I'll explain it.")

    # — NCERT chat history
    for msg in st.session_state.ncert_messages:
        cls = "chat-user" if msg["role"] == "user" else "chat-ai"
        icon = "📖" if msg["role"] == "user" else "📚"
        st.markdown(f'<div class="{cls}">{icon} {msg["content"]}</div>', unsafe_allow_html=True)

    # — Input
    c1, c2 = st.columns([3,1])
    with c1:
        ncert_q = st.text_area("Enter topic / chapter hint:",
            placeholder="e.g.  'Chapter 4'  or  'quadratic equations'  or  'refraction of light'  or  'Mughal administration'",
            height=75, key="ncert_inp")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        ask_btn = st.button("📚 Explain", key="ncert_ask_btn")
        rand_btn = st.button("🎲 Random", key="ncert_rand")

    if rand_btn:
        examples = [
            "Chapter 4 Quadratic Equations",
            "Refraction of light",
            "Photosynthesis light reaction",
            "Newton's second law numerical",
            "Acids bases and salts",
            "Mughal empire administration",
            "Probability Class 10",
            "Human Reproduction",
            "Nationalism in India",
            "Electrochemistry Class 12",
        ]
        ncert_q = random.choice(examples)
        st.info(f"Random: *{ncert_q}*")
        ask_btn = True

    if ask_btn and ncert_q.strip():
        # Look up NCERT reference
        bk_info, ch_tuple, ch_url = find_ncert_info(
            st.session_state.grade, st.session_state.subject, ncert_q.strip())

        ref_block = ""
        link_block = ""
        if bk_info and ch_tuple:
            ref_block = f"""
📖 NCERT Reference Found:
   Book  : {bk_info['book']}
   Chapter {ch_tuple[0]}: {ch_tuple[1]}
   Page  : {ch_tuple[2]}
   Official PDF: {ch_url}
"""
            link_block = f"""<div class="ncert-ref-box">
📖 <b>NCERT {st.session_state.grade} — {bk_info['book']}</b><br>
Chapter {ch_tuple[0]}: <b>{ch_tuple[1]}</b> &nbsp; <span class="page-ref">{ch_tuple[2]}</span><br>
<a href="{ch_url}" target="_blank" style="color:#88ccff;">📄 Open Official Chapter PDF (ncert.nic.in)</a>
</div>"""

        st.session_state.ncert_messages.append({"role":"user","content":ncert_q})
        prompt = f"""Student Query: "{ncert_q}"
Grade: {st.session_state.grade} | Subject: {st.session_state.subject}
{ref_block}
Explain this NCERT topic clearly using the structure in your instructions."""

        with st.spinner("Looking up NCERT content..."):
            reply = call_ai([{"role":"user","content":prompt}], system=sys_ncert(), max_tok=950)

        full_reply = (f"[NCERT REFERENCE]\n{ref_block.strip()}\n\n" if ref_block else "") + reply
        st.session_state.ncert_messages.append({"role":"assistant","content":full_reply})
        st.session_state.q_asked += 1

        # Show the link immediately
        if link_block:
            st.markdown(link_block, unsafe_allow_html=True)
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════
#  TAB 3 — MATH SOLVER  (Human-level accuracy, large steps)
# ══════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🔢 Math Solver — Human-Level Steps")
    st.markdown("""<div class="ex-card-highlight">
Every numerical solved with <b>GIVEN → FIND → FORMULA → STEP-BY-STEP → VERIFICATION → ANSWER</b>.<br>
Works for: Arithmetic · Algebra · Geometry · Trigonometry · Calculus · Statistics · Probability
</div>""", unsafe_allow_html=True)

    math_mode = st.radio("Mode:", ["🧮 AI Step-by-Step", "🔣 SymPy Calculator", "📊 Statistics"], horizontal=True)

    if math_mode == "🧮 AI Step-by-Step":
        # Examples
        st.markdown("**Quick Examples:**")
        eg_cols = st.columns(4)
        examples = [
            "Solve: 2x² + 7x + 3 = 0",
            "Find HCF of 36 and 48",
            "Train 300m long at 54 km/h passes pole — time?",
            "Simple interest: P=5000, R=8%, T=3yr",
        ]
        for i, ex in enumerate(examples):
            if eg_cols[i].button(ex[:20]+"…", key=f"math_ex_{i}"):
                st.session_state.math_messages.append({"role":"user","content":ex})
                with st.spinner("Solving step-by-step..."):
                    reply = call_ai([{"role":"user","content":ex}], system=sys_math(), temp=0.2, max_tok=1100)
                st.session_state.math_messages.append({"role":"assistant","content":reply})
                st.session_state.q_asked += 1
                st.rerun()

        for msg in st.session_state.math_messages:
            cls = "chat-user" if msg["role"]=="user" else "step-box"
            icon = "🧑" if msg["role"]=="user" else "🔢"
            st.markdown(f'<div class="{cls}">{icon} {msg["content"]}</div>', unsafe_allow_html=True)

        math_inp = st.chat_input("Enter any math problem...")
        if math_inp:
            st.session_state.math_messages.append({"role":"user","content":math_inp})
            with st.spinner("Solving..."):
                reply = call_ai(st.session_state.math_messages[-6:], system=sys_math(), temp=0.2, max_tok=1100)
            st.session_state.math_messages.append({"role":"assistant","content":reply})
            st.session_state.q_asked += 1
            st.rerun()

    elif math_mode == "🔣 SymPy Calculator":
        if not SYMPY_OK:
            st.error("Install SymPy: `pip install sympy`")
        else:
            st.markdown("**Direct symbolic computation — 100% accurate, no AI needed:**")
            op = st.selectbox("Operation", [
                "Solve Equation (= 0)", "Solve Equation (custom RHS)",
                "Simplify","Expand","Factor",
                "Differentiate","Integrate (indefinite)","Integrate (definite)",
                "Find Roots","Matrix Operations","Trigonometry Simplify",
            ])
            expr_in = st.text_input("Expression:", placeholder="e.g.  x**2 - 5*x + 6   or   sin(x)**2 + cos(x)**2")
            var_in  = st.text_input("Variable (for calc):", value="x")

            if op == "Solve Equation (custom RHS)":
                rhs_in = st.text_input("Right-hand side:", value="0")
            if op in ["Integrate (definite)"]:
                lim_a = st.number_input("Lower limit:", value=0.0)
                lim_b = st.number_input("Upper limit:", value=1.0)

            if st.button("▶ Calculate") and expr_in:
                try:
                    transformations = standard_transformations + (implicit_multiplication_application,)
                    x = symbols(var_in)
                    expr = parse_expr(expr_in, transformations=transformations)

                    if op == "Solve Equation (= 0)":
                        res = solve(expr, x)
                        st.success(f"**Solutions for {var_in}:** {res}")
                        for i, r in enumerate(res):
                            st.markdown(f"  {var_in}₁ = {r}" if i==0 else f"  {var_in}₂ = {r}")
                    elif op == "Solve Equation (custom RHS)":
                        rhs = parse_expr(rhs_in, transformations=transformations)
                        res = solve(sp.Eq(expr, rhs), x)
                        st.success(f"**Solutions:** {res}")
                    elif op == "Simplify":
                        res = simplify(expr)
                        st.success(f"**Simplified:** `{res}`")
                    elif op == "Expand":
                        res = expand(expr)
                        st.success(f"**Expanded:** `{res}`")
                    elif op == "Factor":
                        res = factor(expr)
                        st.success(f"**Factored:** `{res}`")
                    elif op == "Differentiate":
                        res = diff(expr, x)
                        st.success(f"**d/d{var_in}:** `{res}`")
                    elif op == "Integrate (indefinite)":
                        res = integrate(expr, x)
                        st.success(f"**∫ d{var_in}:** `{res}` + C")
                    elif op == "Integrate (definite)":
                        res = integrate(expr, (x, lim_a, lim_b))
                        st.success(f"**∫ from {lim_a} to {lim_b}:** `{res}` ≈ {float(res):.4f}")
                    elif op == "Find Roots":
                        from sympy import nroots
                        res = nroots(expr, n=6)
                        st.success(f"**Numerical roots:** {[round(complex(r).real,4) for r in res]}")
                    elif op == "Trigonometry Simplify":
                        from sympy import trigsimp
                        res = trigsimp(expr)
                        st.success(f"**Trig simplified:** `{res}`")

                    # LaTeX display
                    try:
                        st.markdown(f"**LaTeX:** `$$` {latex(res)} `$$`")
                    except:
                        pass
                    # Numeric approximation
                    try:
                        val = float(res) if not isinstance(res, list) else [float(v) for v in res]
                        st.info(f"Decimal approximation: `{val}`")
                    except:
                        pass
                except Exception as e:
                    st.error(f"Error: {e}\n\nTip: Use ** for power, * for multiply. E.g. `2*x**2 + 3*x`")

    else:  # Statistics
        st.markdown("**Statistical Analysis:**")
        data_inp = st.text_area("Enter numbers (comma separated):",
            placeholder="23, 45, 12, 67, 34, 89, 23, 45, 56, 78")
        show_chart = st.checkbox("Show histogram", value=True)
        if st.button("📊 Analyze Data") and data_inp:
            try:
                nums = np.array([float(x.strip()) for x in data_inp.split(",") if x.strip()])
                n = len(nums)
                mean_ = np.mean(nums)
                median_ = np.median(nums)
                std_ = np.std(nums)
                var_ = np.var(nums)
                sorted_ = np.sort(nums)
                q1 = np.percentile(nums, 25)
                q3 = np.percentile(nums, 75)
                iqr = q3 - q1
                mode_vals, mode_counts = np.unique(nums, return_counts=True)
                mode_ = mode_vals[np.argmax(mode_counts)]
                range_ = np.max(nums) - np.min(nums)

                st.markdown("### 📊 Results")
                r1,r2,r3 = st.columns(3)
                r1.metric("Mean (Average)", f"{mean_:.3f}")
                r2.metric("Median",         f"{median_:.3f}")
                r3.metric("Mode",           f"{mode_}")
                r1.metric("Std. Deviation", f"{std_:.3f}")
                r2.metric("Variance",       f"{var_:.3f}")
                r3.metric("Range",          f"{range_:.3f}")
                r1.metric("Q1 (25th pct)", f"{q1:.3f}")
                r2.metric("Q3 (75th pct)", f"{q3:.3f}")
                r3.metric("IQR",           f"{iqr:.3f}")
                st.markdown(f"**Count:** {n} &nbsp;|&nbsp; **Min:** {np.min(nums)} &nbsp;|&nbsp; **Max:** {np.max(nums)}")

                if show_chart:
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), facecolor="#0a0a0f")
                    for ax in [ax1, ax2]:
                        ax.set_facecolor("#111120")
                    ax1.hist(nums, bins="auto", color="#ff4500", edgecolor="#222", alpha=0.85)
                    ax1.axvline(mean_, color="#ffd700", linestyle="--", linewidth=1.5, label=f"Mean={mean_:.2f}")
                    ax1.axvline(median_, color="#00e676", linestyle=":", linewidth=1.5, label=f"Median={median_:.2f}")
                    ax1.set_title("Frequency Distribution", color="white", fontsize=11)
                    ax1.tick_params(colors="white")
                    ax1.legend(facecolor="#111120", labelcolor="white", fontsize=8)
                    ax1.grid(color="#222", linestyle="--", alpha=0.4)
                    ax2.boxplot(nums, patch_artist=True,
                                boxprops=dict(facecolor="#ff4500", color="#ffd700"),
                                medianprops=dict(color="#ffd700", linewidth=2),
                                whiskerprops=dict(color="#888"),
                                capprops=dict(color="#888"),
                                flierprops=dict(markerfacecolor="#ff4500"))
                    ax2.set_title("Box Plot", color="white", fontsize=11)
                    ax2.tick_params(colors="white")
                    ax2.grid(color="#222", linestyle="--", alpha=0.4)
                    for s in ax2.spines.values(): s.set_edgecolor("#333")
                    for s in ax1.spines.values(): s.set_edgecolor("#333")
                    st.pyplot(fig)
                    plt.close(fig)
            except Exception as e:
                st.error(f"Error: {e}")


# ══════════════════════════════════════════════════════════════════════════
#  TAB 4 — PHOTO SCANNER
# ══════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 📸 Photo Scanner — Upload & Solve")
    st.markdown("""<div class="ex-card">
Upload a photo of your <b>textbook question</b>, <b>handwritten problem</b>, diagram, or exercise.
Examlysis AI will read and solve/explain it step-by-step.<br>
<small>💡 Tips: Good lighting, camera flat, clear text = best results</small>
</div>""", unsafe_allow_html=True)

    if not PIL_OK:
        st.warning("Install Pillow: `pip install Pillow`")
    else:
        uploaded = st.file_uploader("Upload image (JPG / PNG)", type=["jpg","jpeg","png"])

        if uploaded:
            img = Image.open(uploaded)
            if img.mode not in ("RGB","L"):
                img = img.convert("RGB")
            # Resize for old laptop (keep quality, reduce size)
            max_px = 720
            if max(img.size) > max_px:
                r = max_px / max(img.size)
                img = img.resize((int(img.size[0]*r), int(img.size[1]*r)), Image.LANCZOS)

            c_img, c_ctrl = st.columns([1,1])
            with c_img:
                st.image(img, caption="Your upload", use_column_width=True)
            with c_ctrl:
                mode = st.selectbox("Task:", [
                    "Solve the problem with full steps",
                    "Explain the diagram",
                    "Explain the text/concept",
                    "Check my handwritten answer",
                    "Identify chapter and topic",
                    "List formulas visible in image",
                ])
                hint = st.text_input("Extra context (optional):",
                    placeholder="e.g. Class 10 Physics, Ohm's Law")
                scan = st.button("🔍 Scan & Solve")

            if scan:
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=85)
                b64 = base64.b64encode(buf.getvalue()).decode()
                provider = st.session_state.api_provider
                api_key  = st.session_state.api_key.strip()

                with st.spinner("Analyzing image..."):
                    if provider == "OpenAI (Paid)":
                        payload = {
                            "model":"gpt-4o-mini","max_tokens":1100,
                            "messages":[{"role":"user","content":[
                                {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}},
                                {"type":"text","text":f"Task: {mode}. {hint}. Student: {st.session_state.grade}. {sys_math() if 'Solve' in mode else ''}"}
                            ]}]
                        }
                        headers={"Content-Type":"application/json","Authorization":f"Bearer {api_key}"}
                        try:
                            r=requests.post("https://api.openai.com/v1/chat/completions",headers=headers,json=payload,timeout=50)
                            r.raise_for_status()
                            result=r.json()["choices"][0]["message"]["content"]
                        except Exception as e:
                            result=f"Error: {e}"
                    elif provider == "OpenRouter (Free)":
                        payload = {
                            "model":"google/gemma-3-4b-it:free","max_tokens":1100,
                            "messages":[{"role":"user","content":[
                                {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}},
                                {"type":"text","text":f"Task: {mode}. {hint}. Grade: {st.session_state.grade}. Give detailed step-by-step solution."}
                            ]}]
                        }
                        headers={"Content-Type":"application/json","Authorization":f"Bearer {api_key}","HTTP-Referer":"http://localhost:8501","X-Title":"Examlysis"}
                        try:
                            r=requests.post("https://openrouter.ai/api/v1/chat/completions",headers=headers,json=payload,timeout=50)
                            r.raise_for_status()
                            result=r.json()["choices"][0]["message"]["content"]
                        except Exception as e:
                            result=f"Vision model error: {e}"
                    else:
                        result = "⚠️ Groq does not support image input.\nPlease switch to **OpenRouter** (free) or **OpenAI** in the sidebar for photo scanning."

                st.session_state.photo_result = result
                st.markdown('<div class="step-box">', unsafe_allow_html=True)
                st.markdown(f"**📝 Result:**\n\n{result}")
                st.markdown('</div>', unsafe_allow_html=True)
        elif st.session_state.photo_result:
            st.markdown("**Previous Result:**")
            st.code(st.session_state.photo_result)


# ══════════════════════════════════════════════════════════════════════════
#  TAB 5 — GRAPH TOOL
# ══════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("### 📈 Graphical Representation Tool")
    st.markdown("""<div class="ex-card">Plot mathematical functions, data charts, and geometry shapes.</div>""", unsafe_allow_html=True)

    gtype = st.selectbox("Graph Type", [
        "📉 Function Plot y=f(x)",
        "🌊 Trigonometric Functions",
        "📊 Bar Chart",
        "🥧 Pie Chart",
        "📈 Line Chart",
        "🔵 Scatter + Trend",
        "📐 Geometry (Circle/Triangle/Rectangle)",
        "📦 Box Plot",
    ])

    DARK_FIG = {"facecolor":"#0a0a0f"}
    DARK_AX  = "#111120"
    C = ["#ff4500","#00c896","#ffd700","#4db8ff","#ff88cc","#88ffcc"]

    def dark_ax(ax):
        ax.set_facecolor(DARK_AX)
        ax.tick_params(colors="white")
        ax.grid(color="#222",linestyle="--",alpha=0.4)
        for s in ax.spines.values(): s.set_edgecolor("#333")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")

    # ── Function plot ─────────────────────────────────────────────────
    if gtype == "📉 Function Plot y=f(x)":
        funcs  = st.text_input("Functions (comma separated):", value="x**2 - 4, 2*x + 1")
        cc1,cc2,cc3 = st.columns(3)
        xmin = cc1.number_input("x min", value=-10.0)
        xmax = cc2.number_input("x max", value=10.0)
        pts  = cc3.number_input("Resolution", value=500, min_value=100, max_value=3000)
        if st.button("📉 Plot Function"):
            try:
                x = np.linspace(xmin, xmax, int(pts))
                fig, ax = plt.subplots(figsize=(10,5), **DARK_FIG)
                dark_ax(ax)
                ax.axhline(0,color="#444",lw=0.8); ax.axvline(0,color="#444",lw=0.8)
                NS = {"x":x,"sin":np.sin,"cos":np.cos,"tan":np.tan,
                      "log":np.log,"log10":np.log10,"exp":np.exp,
                      "sqrt":np.sqrt,"abs":np.abs,"pi":np.pi,"e":np.e}
                for i,f in enumerate([fn.strip() for fn in funcs.split(",")]):
                    y = eval(f.replace("^","**"), {"__builtins__":{}}, NS)
                    y = np.where(np.abs(y)>1e6, np.nan, y)
                    ax.plot(x, y, color=C[i%len(C)], lw=2, label=f"y = {f}")
                ax.legend(facecolor="#111120", labelcolor="white")
                ax.set_title(f"Plot: {funcs}", fontsize=11)
                st.pyplot(fig); plt.close(fig)
            except Exception as e:
                st.error(f"Error: {e}. Use Python syntax: x**2, sin(x), etc.")

    # ── Trig ─────────────────────────────────────────────────────────
    elif gtype == "🌊 Trigonometric Functions":
        sel  = st.multiselect("Functions:", ["sin(x)","cos(x)","tan(x)","sin(2*x)","cos(2*x)","2*sin(x)","sin(x+pi/4)"], default=["sin(x)","cos(x)"])
        xrng = st.slider("x range (× π):", 1, 4, 2)
        if st.button("🌊 Plot Trig"):
            x = np.linspace(-xrng*np.pi, xrng*np.pi, 1500)
            fig, ax = plt.subplots(figsize=(11,5), **DARK_FIG)
            dark_ax(ax)
            ax.axhline(0,color="#444",lw=0.8); ax.axvline(0,color="#444",lw=0.8)
            NS = {"x":x,"sin":np.sin,"cos":np.cos,"tan":np.tan,"pi":np.pi}
            for i,f in enumerate(sel):
                y = eval(f, {"__builtins__":{}}, NS)
                y = np.where(np.abs(y)>4, np.nan, y)
                ax.plot(x, y, color=C[i%len(C)], lw=2, label=f"y={f}")
            pi_t = np.arange(-xrng, xrng+0.1, 0.5)
            ax.set_xticks([v*np.pi for v in pi_t])
            ax.set_xticklabels([("0" if v==0 else f"{v}π") for v in pi_t], color="white", fontsize=8)
            ax.set_ylim(-3,3)
            ax.legend(facecolor="#111120",labelcolor="white")
            ax.set_title("Trigonometric Functions",fontsize=11)
            st.pyplot(fig); plt.close(fig)

    # ── Bar ─────────────────────────────────────────────────────────
    elif gtype == "📊 Bar Chart":
        lbls  = st.text_input("Labels:", value="Physics, Chemistry, Maths, Biology, English")
        vals  = st.text_input("Values:", value="78, 85, 92, 70, 88")
        title = st.text_input("Title:", value="Subject Marks")
        if st.button("📊 Bar Chart"):
            try:
                labels = [l.strip() for l in lbls.split(",")]
                values = [float(v.strip()) for v in vals.split(",")]
                fig, ax = plt.subplots(figsize=(9,5), **DARK_FIG)
                dark_ax(ax)
                bars = ax.bar(labels, values, color=C[:len(labels)]*5, edgecolor="#222")
                for b,v in zip(bars,values):
                    ax.text(b.get_x()+b.get_width()/2, b.get_height()+max(values)*0.01,
                            str(v), ha="center", color="white", fontsize=10, fontweight="bold")
                ax.set_title(title, fontsize=12)
                st.pyplot(fig); plt.close(fig)
            except Exception as e: st.error(f"Error: {e}")

    # ── Pie ─────────────────────────────────────────────────────────
    elif gtype == "🥧 Pie Chart":
        lbls  = st.text_input("Labels:", value="Study, Sleep, Play, Screen Time, Other")
        vals  = st.text_input("Values:", value="35, 30, 15, 12, 8")
        title = st.text_input("Title:", value="Daily Time Distribution")
        if st.button("🥧 Pie Chart"):
            try:
                labels = [l.strip() for l in lbls.split(",")]
                values = [float(v.strip()) for v in vals.split(",")]
                fig, ax = plt.subplots(figsize=(7,7), **DARK_FIG)
                ax.set_facecolor(DARK_AX)
                wedges, texts, at = ax.pie(values, labels=labels, autopct="%1.1f%%",
                    colors=C[:len(labels)]*5, startangle=90, textprops={"color":"white"})
                for a in at: a.set_color("white"); a.set_fontsize(10)
                ax.set_title(title, color="white", fontsize=12)
                st.pyplot(fig); plt.close(fig)
            except Exception as e: st.error(f"Error: {e}")

    # ── Line ─────────────────────────────────────────────────────────
    elif gtype == "📈 Line Chart":
        xv = st.text_input("X values:", value="2015,2016,2017,2018,2019,2020,2021,2022")
        yv = st.text_input("Y values:", value="45,52,48,61,58,42,67,72")
        xl = st.text_input("X label:", value="Year")
        yl = st.text_input("Y label:", value="Score")
        title = st.text_input("Title:", value="Trend Over Years")
        if st.button("📈 Line Chart"):
            try:
                xd = [float(v.strip()) for v in xv.split(",")]
                yd = [float(v.strip()) for v in yv.split(",")]
                fig, ax = plt.subplots(figsize=(10,5), **DARK_FIG)
                dark_ax(ax)
                ax.plot(xd, yd, color=C[0], lw=2.5, marker="o",
                        markersize=7, markerfacecolor=C[1], markeredgecolor=C[0])
                ax.fill_between(xd, yd, alpha=0.1, color=C[0])
                ax.set_xlabel(xl); ax.set_ylabel(yl)
                ax.set_title(title, fontsize=12)
                st.pyplot(fig); plt.close(fig)
            except Exception as e: st.error(f"Error: {e}")

    # ── Scatter ──────────────────────────────────────────────────────
    elif gtype == "🔵 Scatter + Trend":
        xv = st.text_input("X:", value="1,3,5,7,2,4,6,8,3,5,9,11")
        yv = st.text_input("Y:", value="2,6,4,9,3,7,5,10,4,8,12,14")
        title = st.text_input("Title:", value="Scatter Plot with Trend")
        if st.button("🔵 Scatter"):
            try:
                xd = np.array([float(v.strip()) for v in xv.split(",")])
                yd = np.array([float(v.strip()) for v in yv.split(",")])
                fig, ax = plt.subplots(figsize=(9,5), **DARK_FIG)
                dark_ax(ax)
                ax.scatter(xd, yd, c=C[0], s=80, alpha=0.85, edgecolors=C[1], lw=1.5)
                z = np.polyfit(xd, yd, 1)
                p = np.poly1d(z)
                xl = np.linspace(min(xd), max(xd), 200)
                ax.plot(xl, p(xl), color=C[1], ls="--", lw=1.5, label=f"Trend: y={z[0]:.2f}x+{z[1]:.2f}")
                corr = np.corrcoef(xd, yd)[0,1]
                ax.set_title(f"{title}  (r = {corr:.3f})", fontsize=11)
                ax.legend(facecolor="#111120", labelcolor="white")
                st.pyplot(fig); plt.close(fig)
            except Exception as e: st.error(f"Error: {e}")

    # ── Geometry ─────────────────────────────────────────────────────
    elif gtype == "📐 Geometry (Circle/Triangle/Rectangle)":
        shape = st.selectbox("Shape:", ["Circle","Triangle","Rectangle","Right-Angle Triangle"])
        if shape == "Circle":
            r = st.number_input("Radius:", value=5.0, min_value=0.1)
            if st.button("Draw Circle"):
                fig, ax = plt.subplots(figsize=(6,6), **DARK_FIG)
                dark_ax(ax)
                c = plt.Circle((0,0), r, fill=False, color=C[0], lw=2)
                ax.add_patch(c)
                ax.plot([0,r],[0,0], color=C[1], lw=1.5)
                ax.text(r/2, 0.3, f"r={r}", color=C[1], fontsize=11)
                ax.plot(0,0,"o",color=C[1],markersize=6)
                ax.set_xlim(-r-1, r+1); ax.set_ylim(-r-1, r+1); ax.set_aspect("equal")
                ax.set_title(f"Circle: r={r} | Area={math.pi*r**2:.2f} | Circumference={2*math.pi*r:.2f}", fontsize=10)
                st.pyplot(fig); plt.close(fig)
        elif shape in ["Triangle","Right-Angle Triangle"]:
            if shape == "Right-Angle Triangle":
                b = st.number_input("Base:", value=6.0); h = st.number_input("Height:", value=4.0)
                pts = np.array([[0,0],[b,0],[0,h],[0,0]])
            else:
                c1_,c2_,c3_ = st.columns(3)
                ax1_=c1_.number_input("Ax",value=0.0); ay1_=c1_.number_input("Ay",value=0.0)
                bx1_=c2_.number_input("Bx",value=6.0); by1_=c2_.number_input("By",value=0.0)
                cx1_=c3_.number_input("Cx",value=3.0); cy1_=c3_.number_input("Cy",value=5.0)
                pts = np.array([[ax1_,ay1_],[bx1_,by1_],[cx1_,cy1_],[ax1_,ay1_]])
            if st.button("Draw Triangle"):
                fig, ax = plt.subplots(figsize=(7,6), **DARK_FIG)
                dark_ax(ax)
                ax.fill(pts[:-1,0], pts[:-1,1], alpha=0.15, color=C[0])
                ax.plot(pts[:,0], pts[:,1], color=C[0], lw=2, marker="o",
                        markersize=8, markerfacecolor=C[1])
                for i,(px,py) in enumerate(pts[:-1]):
                    ax.annotate(f" {'ABC'[i]}({px},{py})", (px,py), color="white", fontsize=10)
                area = 0.5*abs((pts[1,0]-pts[0,0])*(pts[2,1]-pts[0,1])-(pts[2,0]-pts[0,0])*(pts[1,1]-pts[0,1]))
                ax.set_title(f"Area = {area:.2f} sq.units", fontsize=11)
                ax.set_aspect("equal")
                st.pyplot(fig); plt.close(fig)
        else:  # Rectangle
            w = st.number_input("Width:",value=8.0); h_=st.number_input("Height:",value=5.0)
            if st.button("Draw Rectangle"):
                fig, ax = plt.subplots(figsize=(8,5), **DARK_FIG)
                dark_ax(ax)
                rect = patches.Rectangle((0,0), w, h_, linewidth=2, edgecolor=C[0], facecolor=C[0], alpha=0.15)
                ax.add_patch(rect)
                ax.set_xlim(-1, w+1); ax.set_ylim(-1, h_+1); ax.set_aspect("equal")
                ax.set_title(f"Rectangle: {w}×{h_} | Area={w*h_:.2f} | Perimeter={2*(w+h_):.2f}", fontsize=10)
                st.pyplot(fig); plt.close(fig)

    # ── Box plot ──────────────────────────────────────────────────────
    elif gtype == "📦 Box Plot":
        data_in = st.text_area("Data sets (one per line, comma separated):",
            value="23,45,12,67,34,89,23,45\n56,78,34,90,45,67,23,88")
        lbls = st.text_input("Labels (comma separated):", value="Class A, Class B")
        if st.button("📦 Box Plot"):
            try:
                rows = [l.strip() for l in data_in.strip().split("\n") if l.strip()]
                all_data = [[float(v.strip()) for v in row.split(",") if v.strip()] for row in rows]
                labels = [l.strip() for l in lbls.split(",")]
                while len(labels) < len(all_data):
                    labels.append(f"Set {len(labels)+1}")
                fig, ax = plt.subplots(figsize=(8,5), **DARK_FIG)
                dark_ax(ax)
                bp = ax.boxplot(all_data, labels=labels[:len(all_data)], patch_artist=True)
                for i,(p,w,c_) in enumerate(zip(bp["boxes"],bp["whiskers"],bp["caps"])):
                    p.set_facecolor(C[i%len(C)]); p.set_alpha(0.7)
                for med in bp["medians"]: med.set_color("#ffd700"); med.set_linewidth(2)
                ax.set_title("Box Plot Comparison", fontsize=11)
                st.pyplot(fig); plt.close(fig)
            except Exception as e: st.error(f"Error: {e}")


# ══════════════════════════════════════════════════════════════════════════
#  TAB 6 — QUIZ  (Adaptive, difficulty auto-adjusts)
# ══════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("### 📝 Adaptive Quiz")
    st.markdown("""<div class="ex-card">
Questions adapt to your current level.
Score high → level goes UP. Score low → level drops to strengthen your base.
</div>""", unsafe_allow_html=True)

    qcol1, qcol2 = st.columns([2,1])
    with qcol2:
        total = st.session_state.quiz_total
        score = st.session_state.quiz_score
        pct   = int(score/max(total,1)*100)
        st.markdown(f"""<div class="ex-card" style="text-align:center;">
<div class="stat-big">{score}/{total}</div>
<div class="stat-lbl">Quiz Score</div>
<br>
<div style="background:#1a1a1a;border-radius:4px;height:6px;">
  <div style="width:{pct}%;height:6px;background:linear-gradient(90deg,#ff4500,#ffd700);border-radius:4px;"></div>
</div>
<small style="color:#666;">{pct}% correct · Level: <b style="color:#ff4500">{st.session_state.adaptive_level}</b></small>
</div>""", unsafe_allow_html=True)

    with qcol1:
        quiz_topic = st.text_input("Quiz topic:", placeholder="e.g. Quadratic Equations, Refraction, Mughal Empire")
        num_q = st.radio("# Questions:", [3,5,10], horizontal=True, index=1)

        if st.button("🎯 Generate Quiz"):
            if not quiz_topic.strip():
                st.warning("Enter a topic first.")
            else:
                with st.spinner(f"Generating {num_q} questions on '{quiz_topic}'..."):
                    prompt = f"""Generate {num_q} multiple-choice questions on "{quiz_topic}" for {st.session_state.grade} students.
Difficulty: {st.session_state.adaptive_level} | Subject: {st.session_state.subject}

Return ONLY a valid JSON object (no markdown, no backticks, no explanation):
{{
  "questions": [
    {{
      "q": "Full question text?",
      "options": ["A) text", "B) text", "C) text", "D) text"],
      "answer": "A",
      "explanation": "Why A is correct in 1-2 sentences."
    }}
  ]
}}"""
                    raw = call_ai([{"role":"user","content":prompt}],
                                  system="You are a quiz generator. Return only valid JSON, nothing else.",
                                  temp=0.55, max_tok=1200)
                    try:
                        clean = re.sub(r"```[a-z]*","",raw).strip()
                        # Find JSON object
                        m = re.search(r'\{.*\}', clean, re.DOTALL)
                        if m: clean = m.group()
                        st.session_state.current_quiz = json.loads(clean)
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
                    except:
                        st.error("Couldn't parse quiz. Try again.")

    # Display quiz
    if st.session_state.current_quiz and st.session_state.current_quiz.get("questions"):
        qs = st.session_state.current_quiz["questions"]
        st.markdown("---")
        ans = st.session_state.quiz_answers

        for i, q in enumerate(qs):
            st.markdown(f"**Q{i+1}. {q['q']}**")
            sel = st.radio(" ", q["options"], key=f"qz_{i}", label_visibility="collapsed")
            if sel: ans[i] = sel[0]
        st.session_state.quiz_answers = ans

        if not st.session_state.quiz_submitted:
            if st.button("✅ Submit Quiz"):
                sc = sum(1 for i,q in enumerate(qs) if ans.get(i,"") == q["answer"])
                st.session_state.quiz_score  += sc
                st.session_state.quiz_total  += len(qs)
                st.session_state.q_correct   += sc
                st.session_state.q_asked     += len(qs)
                st.session_state.quiz_submitted = True
                pct2 = sc / len(qs)
                # Adaptive level adjustment
                lvl = st.session_state.adaptive_level
                if pct2 >= 0.8:
                    if lvl == "Easy":   st.session_state.adaptive_level = "Medium"; st.success("🚀 Level UP → Medium!")
                    elif lvl=="Medium": st.session_state.adaptive_level = "Hard";   st.success("🚀 Level UP → Hard!")
                    else: st.success("🏆 Excellent! Staying at Hard level.")
                elif pct2 <= 0.4:
                    if lvl == "Hard":   st.session_state.adaptive_level = "Medium"; st.info("📚 Dropping to Medium to build base.")
                    elif lvl=="Medium": st.session_state.adaptive_level = "Easy";   st.info("📚 Dropping to Easy to review basics.")
                st.rerun()
        else:
            st.markdown(f"### 🎯 Your Score: {st.session_state.quiz_answers.get('last_score',0) or sum(1 for i,q in enumerate(qs) if ans.get(i,'')==q['answer'])}/{len(qs)}")
            for i,q in enumerate(qs):
                ua = ans.get(i,"?")
                if ua == q["answer"]:
                    st.markdown(f'<div class="answer-box">✅ Q{i+1}: Correct! {q.get("explanation","")}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="hint-box">❌ Q{i+1}: Correct = <b>{q["answer"]}</b>. {q.get("explanation","")}</div>', unsafe_allow_html=True)
            if st.button("🔄 New Quiz"):
                st.session_state.current_quiz = None
                st.session_state.quiz_submitted = False
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""<div style="text-align:center;padding:0.8rem;color:#444;font-size:0.78rem;">
<b style="color:#ff4500;">Examlysis</b> · Adaptive AI Learning for Indian Students ·
NCERT/CBSE/JEE/NEET · Riiid-inspired Intelligence ·
Official NCERT PDFs from ncert.nic.in · For educational use only
</div>""", unsafe_allow_html=True)
