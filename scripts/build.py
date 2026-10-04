#!/usr/bin/env python3
"""
IEM Radar Builder Script - Ultra Editorial Edition
Compiles data/iems.json into an interactive, collaborative single-page application
inspired by modern editorial Japanese web design (unifiersofjapan / tofudesign),
complete with shared wishlist encoding, interactive audio science vault, and EU pricing intelligence.
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "iems.json")
OUTPUT_HTML_DIST = os.path.join(BASE_DIR, "dist", "index.html")
OUTPUT_HTML_ROOT = os.path.join(BASE_DIR, "index.html")
ARTIFACT_DIR = "/home/sam/.gemini/antigravity-cli/brain/7967f2cc-b2f8-4ab7-b1d6-8fc310cf968e"
ARTIFACT_HTML = os.path.join(ARTIFACT_DIR, "iem_buyers_guide.html")

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_html(iems):
    json_data = json.dumps(iems, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IEM RADAR // 2026 Edition — Audio Science, Curated Rankings & EU Buying Guide</title>
  
  <!-- Modern Typography: Anton & Plus Jakarta Sans & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=JetBrains+Mono:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Font Awesome Pro Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            display: ['"Anton"', '"Syne"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          }},
          colors: {{
            carbon: {{
              950: '#080a0f',
              900: '#0d111a',
              850: '#121824',
              800: '#182133',
              700: '#222f47',
              600: '#324466'
            }},
            accent: {{
              blue: '#3b82f6',
              cyan: '#06b6d4',
              amber: '#f59e0b',
              emerald: '#10b981',
              rose: '#f43f5e',
              purple: '#8b5cf6'
            }}
          }}
        }}
      }}
    }}
  </script>
  
  <style>
    /* Editorial Texture & Custom Scrollbars */
    body {{
      background-color: #080a0f;
      color: #f1f5f9;
      background-image: 
        radial-gradient(circle at 15% 20%, rgba(59, 130, 246, 0.04) 0%, transparent 40%),
        radial-gradient(circle at 85% 70%, rgba(139, 92, 246, 0.04) 0%, transparent 40%),
        linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 48px 48px, 48px 48px;
    }}
    
    .editorial-border {{
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    
    .editorial-card {{
      background: rgba(13, 17, 26, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .editorial-card:hover {{
      border-color: rgba(255, 255, 255, 0.2);
      transform: translateY(-2px);
      box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.5);
    }}
    
    .custom-scrollbar::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scrollbar::-webkit-scrollbar-track {{
      background: #080a0f;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{
      background: #222f47;
      border-radius: 9999px;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
      background: #324466;
    }}
    
    .stamp-badge {{
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      font-weight: 700;
    }}
  </style>
</head>
<body class="min-h-screen custom-scrollbar antialiased selection:bg-blue-500 selection:text-white">

  <!-- TOP STATUS STRIP -->
  <aside class="bg-carbon-900 border-b border-white/5 py-1.5 px-4 text-[11px] font-mono text-slate-400">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <span class="inline-flex items-center gap-1.5 text-emerald-400">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          ACTIVE RESEARCH REPOSITORY
        </span>
        <span class="hidden sm:inline text-slate-600">|</span>
        <span class="hidden sm:inline">21 AUDIOPHILE MODELS ANALYZED</span>
      </div>
      <div class="flex items-center space-x-4">
        <span>NEXT BIG SALE: <strong class="text-amber-400">11.11 SINGLES' DAY</strong></span>
        <span class="text-slate-600">|</span>
        <a href="#vault" class="hover:text-white transition flex items-center gap-1">
          <i class="fa-solid fa-book-bookmark text-blue-400"></i>
          <span>AUDIO SCIENCE VAULT</span>
        </a>
      </div>
    </div>
  </aside>

  <!-- NAVIGATION HEADER -->
  <header class="sticky top-0 z-40 bg-carbon-950/85 backdrop-blur-md border-b border-white/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between gap-4">
      <div class="flex items-center space-x-3.5">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-500 flex items-center justify-center text-white shadow-lg shadow-blue-500/20 font-display text-xl tracking-wider">
          IR
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h1 class="text-xl font-display tracking-wide text-white uppercase">IEM RADAR</h1>
            <span class="stamp-badge text-[10px] px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/30">2026.1</span>
          </div>
          <p class="text-[11px] text-slate-400">Acoustic Targets, Fit Science & European Market Pricing</p>
        </div>
      </div>

      <nav class="flex items-center space-x-2.5">
        <a href="#finder" class="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-carbon-850 hover:bg-carbon-800 text-xs text-slate-200 border border-white/5 transition">
          <i class="fa-solid fa-compass text-blue-400"></i>
          <span>Finder</span>
        </a>
        <a href="#models" class="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-carbon-850 hover:bg-carbon-800 text-xs text-slate-200 border border-white/5 transition">
          <i class="fa-solid fa-list-check text-cyan-400"></i>
          <span>All IEMs</span>
        </a>
        <a href="#vault" class="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-carbon-850 hover:bg-carbon-800 text-xs text-slate-200 border border-white/5 transition">
          <i class="fa-solid fa-graduation-cap text-purple-400"></i>
          <span>Guides & Squigs</span>
        </a>
        <a href="#eu-guide" class="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-carbon-850 hover:bg-carbon-800 text-xs text-slate-200 border border-white/5 transition">
          <i class="fa-solid fa-tags text-amber-400"></i>
          <span>EU Customs</span>
        </a>
        <button id="open-wishlist-top-btn" class="relative px-3 py-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-medium transition flex items-center gap-1.5">
          <i class="fa-solid fa-heart text-rose-400"></i>
          <span>Shortlist</span>
          <span id="wishlist-counter-badge" class="px-1.5 py-0.2 rounded-full bg-rose-500 text-white font-mono text-[10px] ml-0.5">0</span>
        </button>
      </nav>
    </div>
  </header>

  <!-- SHARED SHORTLIST BANNER (Visible if URL contains ?picks=...) -->
  <div id="shared-picks-banner" class="hidden bg-gradient-to-r from-indigo-900/90 via-purple-900/90 to-carbon-900 border-b border-indigo-500/30 px-4 py-3 text-xs text-indigo-100">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
      <div class="flex items-center space-x-2.5">
        <span class="w-7 h-7 rounded-full bg-indigo-500/30 flex items-center justify-center text-indigo-300 text-sm">
          <i class="fa-solid fa-share-nodes"></i>
        </span>
        <div>
          <strong class="text-white font-semibold">Shared Shortlist Detected!</strong>
          <span class="text-indigo-200 ml-1">Your friend curated a custom shortlist of recommended IEMs for you.</span>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <button id="filter-shared-only-btn" class="px-3 py-1 rounded-md bg-white text-indigo-950 font-bold text-xs hover:bg-indigo-50 transition">
          View Friend's Picks Only
        </button>
        <button id="clear-shared-view-btn" class="px-3 py-1 rounded-md bg-indigo-950/60 text-indigo-200 text-xs hover:bg-indigo-900 transition">
          Show All 21 Models
        </button>
      </div>
    </div>
  </div>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">

    <!-- HERO SECTION (Editorial Brutalist Styling inspired by Unifiers of Japan) -->
    <section class="editorial-card rounded-3xl p-6 sm:p-10 relative overflow-hidden">
      <div class="absolute -right-16 -top-16 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -left-16 -bottom-16 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        <div class="lg:col-span-8 space-y-4">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 text-xs font-mono">
            <i class="fa-solid fa-wave-square"></i>
            INDEPENDENT AUDIO AUDIT & BUYER'S RADAR
          </div>
          
          <h2 class="text-4xl sm:text-6xl font-display uppercase tracking-tight text-white leading-none">
            PURITY IN SOUND.<br>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-300 to-cyan-300">
              ZERO MARKETING HYPE.
            </span>
          </h2>
          
          <p class="text-sm sm:text-base text-slate-300 leading-relaxed max-w-2xl">
            A comprehensive, data-driven companion for navigating the 2026 In-Ear Monitor market. We cross-reference scientific measurements from <strong class="text-white">Crinacle</strong>, <strong class="text-white">Super* Review</strong>, <strong class="text-white">Jay's Audio</strong>, and <strong class="text-white">Timmy (Gizaudio)</strong> with verified European retail pricing, AliExpress promotional cycles, and ear-canal fit warnings.
          </p>

          <div class="pt-2 flex flex-wrap items-center gap-3">
            <a href="#finder" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs tracking-wide transition shadow-lg shadow-blue-500/20 flex items-center gap-2">
              <i class="fa-solid fa-wand-magic-sparkles"></i>
              <span>Find Your Sound Match</span>
            </a>
            <a href="#models" class="px-5 py-2.5 rounded-xl bg-carbon-800 hover:bg-carbon-700 text-slate-200 font-semibold text-xs border border-white/10 transition flex items-center gap-2">
              <i class="fa-solid fa-table-list"></i>
              <span>Browse All 21 IEMs</span>
            </a>
            <button id="hero-share-btn" class="px-4 py-2.5 rounded-xl bg-carbon-850 hover:bg-carbon-800 text-slate-300 text-xs border border-white/5 transition flex items-center gap-2">
              <i class="fa-solid fa-paper-plane text-cyan-400"></i>
              <span>Share Tool</span>
            </button>
          </div>
        </div>

        <div class="lg:col-span-4 grid grid-cols-2 gap-3 font-mono text-center">
          <div class="p-4 rounded-2xl bg-carbon-900/90 border border-white/5">
            <span class="text-2xl font-bold text-blue-400">21</span>
            <span class="block text-[11px] text-slate-400 uppercase tracking-wider mt-1">Models Audited</span>
          </div>
          <div class="p-4 rounded-2xl bg-carbon-900/90 border border-white/5">
            <span class="text-2xl font-bold text-emerald-400 font-sans font-bold">€10 - €99</span>
            <span class="block text-[11px] text-slate-400 uppercase tracking-wider mt-1">EU Price Range</span>
          </div>
          <div class="p-4 rounded-2xl bg-carbon-900/90 border border-white/5">
            <span class="text-2xl font-bold text-amber-400">11.11</span>
            <span class="block text-[11px] text-slate-400 uppercase tracking-wider mt-1">Peak Sale Window</span>
          </div>
          <div class="p-4 rounded-2xl bg-carbon-900/90 border border-white/5">
            <span class="text-2xl font-bold text-purple-400">&lt; €150</span>
            <span class="block text-[11px] text-slate-400 uppercase tracking-wider mt-1">IOSS Tax-Free</span>
          </div>
        </div>
      </div>
    </section>

    <!-- CRITICAL ANATOMY ADVISORY (NOZZLE SIZE WARNING) -->
    <section class="rounded-2xl border border-amber-500/30 bg-amber-500/10 p-5 text-xs text-amber-200 flex flex-col sm:flex-row items-start gap-4">
      <div class="w-9 h-9 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0 mt-0.5">
        <i class="fa-solid fa-triangle-exclamation text-lg"></i>
      </div>
      <div class="space-y-1">
        <h4 class="font-bold text-amber-300 uppercase tracking-wider text-sm flex items-center gap-2">
          Anatomy & Nozzle Girth Alert: Don't Buy Blindly
        </h4>
        <p class="leading-relaxed text-slate-300">
          IEM nozzle diameter is the <strong class="text-white">#1 cause of discomfort and return rates</strong>. Standard IEMs measure 5.2mm to 5.5mm. Models like the <strong class="text-amber-300">Truthear x Crinacle Zero:RED</strong> have a massive <strong class="text-amber-300">6.2mm nozzle bore (6.8mm with outer lip)</strong> that causes physical ear-canal pain for small or medium ears after 30 minutes. 
          If you have smaller ears, look for the <span class="stamp-badge text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Small Ear Safe</span> badge or choose ultra-slim models like the <strong class="text-white">Moondrop Chu II</strong> or <strong class="text-white">Kefine Delci</strong>.
        </p>
      </div>
    </section>

    <!-- PERSONA FINDER / MATCHER -->
    <section id="finder" class="space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-2xl font-display uppercase tracking-wide text-white flex items-center gap-2.5">
            <i class="fa-solid fa-wand-magic-sparkles text-blue-400"></i>
            What Kind of Listener Are You?
          </h3>
          <p class="text-xs text-slate-400">Select a listening persona to instantly filter the catalog to your ideal sound signature</p>
        </div>
        <button id="reset-persona-btn" class="text-xs font-mono text-blue-400 hover:text-blue-300 transition hidden">
          Reset Filter [x]
        </button>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2.5" id="persona-button-group">
        <button data-persona="all" class="persona-btn active p-3 rounded-2xl border border-blue-500 bg-blue-500/20 text-white font-medium text-xs text-left transition hover:border-blue-400 flex flex-col justify-between h-24">
          <i class="fa-solid fa-border-all text-lg text-blue-400"></i>
          <div>
            <strong class="block text-white font-bold">All IEMs</strong>
            <span class="text-[10px] text-slate-400 font-mono">21 Models</span>
          </div>
        </button>
        
        <button data-persona="Tactical FPS Gaming" class="persona-btn p-3 rounded-2xl border border-white/5 bg-carbon-900 hover:bg-carbon-800 text-slate-300 font-medium text-xs text-left transition flex flex-col justify-between h-24">
          <i class="fa-solid fa-crosshairs text-lg text-rose-400"></i>
          <div>
            <strong class="block text-white font-bold">Tactical FPS</strong>
            <span class="text-[10px] text-slate-400 font-mono">Footstep Cues</span>
          </div>
        </button>

        <button data-persona="Vocal & Acoustic Lovers" class="persona-btn p-3 rounded-2xl border border-white/5 bg-carbon-900 hover:bg-carbon-800 text-slate-300 font-medium text-xs text-left transition flex flex-col justify-between h-24">
          <i class="fa-solid fa-microphone-lines text-lg text-pink-400"></i>
          <div>
            <strong class="block text-white font-bold">Vocal & Indie</strong>
            <span class="text-[10px] text-slate-400 font-mono">Sweet Midrange</span>
          </div>
        </button>

        <button data-persona="Audio Purists & Reference" class="persona-btn p-3 rounded-2xl border border-white/5 bg-carbon-900 hover:bg-carbon-800 text-slate-300 font-medium text-xs text-left transition flex flex-col justify-between h-24">
          <i class="fa-solid fa-sliders text-lg text-cyan-400"></i>
          <div>
            <strong class="block text-white font-bold">Studio Neutral</strong>
            <span class="text-[10px] text-slate-400 font-mono">Mixing & Critical</span>
          </div>
        </button>

        <button data-persona="Warm & Relaxed Daily" class="persona-btn p-3 rounded-2xl border border-white/5 bg-carbon-900 hover:bg-carbon-800 text-slate-300 font-medium text-xs text-left transition flex flex-col justify-between h-24">
          <i class="fa-solid fa-mug-hot text-lg text-amber-400"></i>
          <div>
            <strong class="block text-white font-bold">Warm & Musical</strong>
            <span class="text-[10px] text-slate-400 font-mono">Zero Fatigue</span>
          </div>
        </button>

        <button data-persona="Bassheads & Theatrical EDM" class="persona-btn p-3 rounded-2xl border border-white/5 bg-carbon-900 hover:bg-carbon-800 text-slate-300 font-medium text-xs text-left transition flex flex-col justify-between h-24">
          <i class="fa-solid fa-bolt text-lg text-orange-400"></i>
          <div>
            <strong class="block text-white font-bold">Basshead Slam</strong>
            <span class="text-[10px] text-slate-400 font-mono">EDM & Movies</span>
          </div>
        </button>

        <button data-persona="Smartphone USB-C Users" class="persona-btn p-3 rounded-2xl border border-white/5 bg-carbon-900 hover:bg-carbon-800 text-slate-300 font-medium text-xs text-left transition flex flex-col justify-between h-24">
          <i class="fa-brands fa-usb text-lg text-emerald-400"></i>
          <div>
            <strong class="block text-white font-bold">Type-C DSP</strong>
            <span class="text-[10px] text-slate-400 font-mono">DAC + App EQ</span>
          </div>
        </button>

        <button data-persona="Small Ears & Sleep" class="persona-btn p-3 rounded-2xl border border-white/5 bg-carbon-900 hover:bg-carbon-800 text-slate-300 font-medium text-xs text-left transition flex flex-col justify-between h-24">
          <i class="fa-solid fa-bed text-lg text-indigo-400"></i>
          <div>
            <strong class="block text-white font-bold">Petite Ears</strong>
            <span class="text-[10px] text-slate-400 font-mono">Side Sleeper Fit</span>
          </div>
        </button>
      </div>
    </section>

    <!-- SEARCH & CONTROLS TOOLBAR -->
    <div id="models" class="editorial-card rounded-2xl p-4 flex flex-col lg:flex-row items-center justify-between gap-4">
      <!-- Search Input -->
      <div class="relative w-full lg:w-96">
        <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
        <input type="text" id="search-input" placeholder="Search by model, brand, driver, nozzle..." class="w-full bg-carbon-900 border border-white/10 rounded-xl pl-10 pr-4 py-2 text-sm text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 transition font-sans">
      </div>

      <!-- Filter Controls -->
      <div class="flex flex-wrap items-center gap-2 w-full lg:w-auto">
        <!-- Price Tier -->
        <select id="price-filter" class="bg-carbon-900 border border-white/10 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-mono">
          <option value="all">Price: All Brackets</option>
          <option value="ultra-budget">Ultra-Budget (&lt;€25)</option>
          <option value="entry">Sweet-Spot (€25 - €50)</option>
          <option value="mid">Benchmark (€50 - €80)</option>
          <option value="upper">Premium Chi-Fi (€80+)</option>
        </select>

        <!-- Nozzle Size Safety -->
        <select id="nozzle-filter" class="bg-carbon-900 border border-white/10 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-mono">
          <option value="all">Fit: All Nozzles</option>
          <option value="safe">Small-Ear Safe (≤5.5mm)</option>
          <option value="warning">Wide Nozzle Alert (&gt;6.0mm)</option>
        </select>

        <!-- Sorting -->
        <select id="sort-select" class="bg-carbon-900 border border-white/10 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500 font-mono">
          <option value="score-desc">Sort: Community Score</option>
          <option value="price-ali-asc">Sort: 11.11 Price (Lowest)</option>
          <option value="price-amazon-asc">Sort: Amazon.de Price (Lowest)</option>
          <option value="comfort-desc">Sort: Comfort / Small Ears</option>
          <option value="gaming-desc">Sort: Tactical Gaming Score</option>
        </select>

        <!-- View Switcher -->
        <div class="flex items-center bg-carbon-900 border border-white/10 rounded-xl p-1 ml-auto">
          <button id="view-cards-btn" class="px-2.5 py-1 rounded-lg bg-blue-600 text-white text-xs transition" title="Card Grid View">
            <i class="fa-solid fa-grip"></i>
          </button>
          <button id="view-table-btn" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-white text-xs transition" title="Table Comparison View">
            <i class="fa-solid fa-table-list"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- CARDS GRID VIEW -->
    <div id="cards-view" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Injected via JavaScript -->
    </div>

    <!-- TABLE VIEW -->
    <div id="table-view" class="hidden overflow-x-auto rounded-2xl editorial-border editorial-card">
      <table class="w-full text-left text-xs text-slate-300">
        <thead class="bg-carbon-900/90 text-slate-400 font-mono uppercase text-[10px] tracking-wider border-b border-white/10">
          <tr>
            <th class="px-4 py-3">Model</th>
            <th class="px-4 py-3">Driver Config</th>
            <th class="px-4 py-3">Sound Signature</th>
            <th class="px-4 py-3 text-center">Nozzle</th>
            <th class="px-4 py-3 text-center">Comfort</th>
            <th class="px-4 py-3">Ali 11.11</th>
            <th class="px-4 py-3">Amazon DE</th>
            <th class="px-4 py-3 text-center">Score</th>
            <th class="px-4 py-3 text-right">Shortlist</th>
          </tr>
        </thead>
        <tbody id="table-body" class="divide-y divide-white/5 font-sans">
          <!-- Injected via JavaScript -->
        </tbody>
      </table>
    </div>

    <!-- AUDIO SCIENCE & EDUCATIONAL VAULT SECTION (Requested for deep-dive learning) -->
    <section id="vault" class="space-y-6 pt-6 border-t border-white/10">
      <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <span class="stamp-badge text-xs text-purple-400">KNOWLEDGE REPOSITORY</span>
          <h3 class="text-3xl font-display uppercase tracking-tight text-white mt-1">
            Audio Science & Reviewer Vault
          </h3>
          <p class="text-xs text-slate-400 max-w-xl mt-1">
            Essential educational databases, acoustic target curves, frequency range cheat-sheets, and coupler standards for audio enthusiasts.
          </p>
        </div>
      </div>

      <!-- Frequency Range Cheat Sheet -->
      <div class="editorial-card rounded-2xl p-6 space-y-4">
        <h4 class="text-sm font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
          <i class="fa-solid fa-chart-line text-cyan-400"></i>
          How to Read Frequency Ranges (The Audio Cheat Sheet)
        </h4>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5 text-xs">
          <div class="p-3.5 rounded-xl bg-carbon-900 border border-white/5 space-y-1">
            <span class="font-mono text-cyan-400 font-bold block text-[11px]">SUB-BASS (20Hz - 60Hz)</span>
            <p class="text-slate-300 leading-relaxed">The physical visceral vibration you <em>feel</em> more than hear. Crucial for cinematic explosions and electronic sub-drops.</p>
          </div>
          <div class="p-3.5 rounded-xl bg-carbon-900 border border-white/5 space-y-1">
            <span class="font-mono text-blue-400 font-bold block text-[11px]">MID-BASS (60Hz - 250Hz)</span>
            <p class="text-slate-300 leading-relaxed">The tactile punch of bass guitars and kick drums. Too much causes "mud" in male vocals; too little sounds thin and sterile.</p>
          </div>
          <div class="p-3.5 rounded-xl bg-carbon-900 border border-white/5 space-y-1">
            <span class="font-mono text-indigo-400 font-bold block text-[11px]">LOWER MIDS (250Hz - 1kHz)</span>
            <p class="text-slate-300 leading-relaxed">Fundamental tone of male and female voices. Gives body and warmth to acoustic instruments and dialogue.</p>
          </div>
          <div class="p-3.5 rounded-xl bg-carbon-900 border border-white/5 space-y-1">
            <span class="font-mono text-pink-400 font-bold block text-[11px]">PINNA GAIN / EAR GAIN (1kHz - 3kHz)</span>
            <p class="text-slate-300 leading-relaxed">Simulates the human ear's natural resonance. Boosts vocal intimacy. Too much 3kHz sounds "shouty"; too little sounds distant.</p>
          </div>
          <div class="p-3.5 rounded-xl bg-carbon-900 border border-white/5 space-y-1">
            <span class="font-mono text-amber-400 font-bold block text-[11px]">PRESENCE (4kHz - 8kHz)</span>
            <p class="text-slate-300 leading-relaxed">Crisp percussion attack, weapon reloads, and footsteps in gaming. Excessive 6kHz leads to sibilance (harsh "S" & "T" piercing sounds).</p>
          </div>
          <div class="p-3.5 rounded-xl bg-carbon-900 border border-white/5 space-y-1">
            <span class="font-mono text-purple-400 font-bold block text-[11px]">AIR & UPPER TREBLE (10kHz - 20kHz)</span>
            <p class="text-slate-300 leading-relaxed">Creates the illusion of soundstage width, room acoustic reverberation, and instrumental sparkle.</p>
          </div>
        </div>
      </div>

      <!-- Curated External Tools & Reviewer Vault -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Hangout.Audio -->
        <a href="https://graphs.hangout.audio" target="_blank" rel="noopener noreferrer" class="editorial-card rounded-2xl p-5 flex flex-col justify-between hover:border-blue-500/50 group">
          <div class="space-y-2">
            <div class="w-8 h-8 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-sm">
              <i class="fa-solid fa-chart-simple"></i>
            </div>
            <h5 class="font-bold text-white text-sm group-hover:text-blue-400 transition">Hangout.Audio Graphs</h5>
            <p class="text-xs text-slate-400 leading-relaxed">Crinacle's flagship database featuring modern B&K Type 5128 and IEC 711 coupler measurements.</p>
          </div>
          <div class="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-[11px] font-mono text-blue-400">
            <span>Explore Graphs</span>
            <i class="fa-solid fa-arrow-up-right-from-square"></i>
          </div>
        </a>

        <!-- Squiglink Hub -->
        <a href="https://squig.link" target="_blank" rel="noopener noreferrer" class="editorial-card rounded-2xl p-5 flex flex-col justify-between hover:border-purple-500/50 group">
          <div class="space-y-2">
            <div class="w-8 h-8 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center font-bold text-sm">
              <i class="fa-solid fa-network-wired"></i>
            </div>
            <h5 class="font-bold text-white text-sm group-hover:text-purple-400 transition">Squiglink Network</h5>
            <p class="text-xs text-slate-400 leading-relaxed">Super* Review (Mark Ryan), Timmy V, Jaytiss, and HBB's community-driven graph comparison network.</p>
          </div>
          <div class="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-[11px] font-mono text-purple-400">
            <span>Visit Squiglink</span>
            <i class="fa-solid fa-arrow-up-right-from-square"></i>
          </div>
        </a>

        <!-- Songbird Database -->
        <a href="https://songbird.rocks" target="_blank" rel="noopener noreferrer" class="editorial-card rounded-2xl p-5 flex flex-col justify-between hover:border-cyan-500/50 group">
          <div class="space-y-2">
            <div class="w-8 h-8 rounded-lg bg-cyan-500/20 text-cyan-400 flex items-center justify-center font-bold text-sm">
              <i class="fa-solid fa-dove"></i>
            </div>
            <h5 class="font-bold text-white text-sm group-hover:text-cyan-400 transition">Songbird.rocks</h5>
            <p class="text-xs text-slate-400 leading-relaxed">Independent multi-database aggregator with automatic sound signature classification and target matching.</p>
          </div>
          <div class="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-[11px] font-mono text-cyan-400">
            <span>Open Songbird</span>
            <i class="fa-solid fa-arrow-up-right-from-square"></i>
          </div>
        </a>

        <!-- Oratory1990 Research -->
        <a href="https://www.reddit.com/r/oratory1990/" target="_blank" rel="noopener noreferrer" class="editorial-card rounded-2xl p-5 flex flex-col justify-between hover:border-amber-500/50 group">
          <div class="space-y-2">
            <div class="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-sm">
              <i class="fa-solid fa-ear-listen"></i>
            </div>
            <h5 class="font-bold text-white text-sm group-hover:text-amber-400 transition">Oratory1990 PEQ</h5>
            <p class="text-xs text-slate-400 leading-relaxed">Acoustic engineer's scientific Harman curve measurements and precise Parametric EQ correction profiles.</p>
          </div>
          <div class="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-[11px] font-mono text-amber-400">
            <span>Explore PEQ</span>
            <i class="fa-solid fa-arrow-up-right-from-square"></i>
          </div>
        </a>
      </div>
    </section>

    <!-- GERMANY / EU SHOPPING & CUSTOMS GUIDE -->
    <section id="eu-guide" class="space-y-6 pt-6 border-t border-white/10">
      <div>
        <span class="stamp-badge text-xs text-emerald-400">SHOPPING INTELLIGENCE</span>
        <h3 class="text-3xl font-display uppercase tracking-tight text-white mt-1">
          German / EU Customs & Sales Guide
        </h3>
        <p class="text-xs text-slate-400">How to order safely with German 19% MwSt pre-handled and zero customs surcharges</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="editorial-card rounded-2xl p-6 space-y-3">
          <div class="w-8 h-8 rounded-xl bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-sm">
            <i class="fa-solid fa-shield-halved"></i>
          </div>
          <h4 class="font-bold text-white text-sm uppercase tracking-wider font-mono">AliExpress IOSS (&lt; €150)</h4>
          <p class="text-xs text-slate-300 leading-relaxed">
            AliExpress is fully registered with the EU <strong class="text-white">Import One-Stop Shop (IOSS)</strong>. For all orders under €150, German 19% MwSt is calculated and collected right at checkout. 
            Packages are cleared electronically through Frankfurt/Liege hubs and delivered by DHL directly to your door with <strong class="text-emerald-400">zero customs collection fees</strong> (no €6 Auslagenpauschale).
          </p>
        </div>

        <div class="editorial-card rounded-2xl p-6 space-y-3">
          <div class="w-8 h-8 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-sm">
            <i class="fa-solid fa-calendar-check"></i>
          </div>
          <h4 class="font-bold text-white text-sm uppercase tracking-wider font-mono">11.11 & Choice Days</h4>
          <p class="text-xs text-slate-300 leading-relaxed">
            <strong class="text-white">11.11 Singles' Day (Nov 11–18)</strong> is the Black Friday of Chi-Fi. Manufacturers discount 20% to 35% off MSRP. Stack store vouchers + platform coupons + coins.
            For urgent orders, <strong class="text-white">Choice Day (1st–5th of every month)</strong> offers expedited 7–9 business day delivery to Germany with automatic spend-and-save vouchers.
          </p>
        </div>

        <div class="editorial-card rounded-2xl p-6 space-y-3">
          <div class="w-8 h-8 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center font-bold text-sm">
            <i class="fa-solid fa-truck-fast"></i>
          </div>
          <h4 class="font-bold text-white text-sm uppercase tracking-wider font-mono">Amazon.de & Returns</h4>
          <p class="text-xs text-slate-300 leading-relaxed">
            Amazon.de carries a 15%–25% price premium over Chinese retail, but includes <strong class="text-emerald-300">30-day hassle-free returns</strong>.
            If you are trying an IEM with a wide nozzle (like the Zero:RED) or don't know your ear canal size, buying on Amazon.de is a risk-free way to audition the fit.
          </p>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="pt-8 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4 font-mono">
      <div>
        IEM RADAR FRAMEWORK // OPEN AUDIOPHILE DATASET
      </div>
      <div class="flex items-center space-x-3">
        <span>OCTOBER 2026 AUDIT</span>
        <span>•</span>
        <a href="#models" class="text-slate-400 hover:text-white transition">Back to Top ↑</a>
      </div>
    </footer>

  </main>

  <!-- FLOATING SHORTLIST / WISHLIST DRAWER TRIGGER -->
  <div id="floating-wishlist-pill" class="fixed bottom-6 right-6 z-40 hidden animate-in fade-in slide-in-from-bottom-6 duration-300">
    <button id="open-wishlist-modal-btn" class="px-5 py-3 rounded-2xl bg-gradient-to-r from-rose-600 to-indigo-600 text-white font-bold text-xs tracking-wide shadow-2xl shadow-rose-600/30 flex items-center gap-3 hover:scale-105 transition border border-white/20">
      <i class="fa-solid fa-heart text-base animate-pulse"></i>
      <span>Shortlist (<span id="wishlist-pill-count">0</span>)</span>
      <span class="text-white/60">|</span>
      <span id="wishlist-pill-total" class="font-mono text-emerald-300">~€0</span>
    </button>
  </div>

  <!-- SHORTLIST & COLLABORATION MODAL -->
  <div id="wishlist-modal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-md hidden flex items-center justify-center p-4">
    <div class="bg-carbon-900 border border-white/15 max-w-2xl w-full rounded-3xl shadow-2xl overflow-hidden max-h-[90vh] flex flex-col">
      <div class="p-6 border-b border-white/10 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 rounded-xl bg-rose-500/20 text-rose-400 flex items-center justify-center">
            <i class="fa-solid fa-heart"></i>
          </div>
          <div>
            <h3 class="text-lg font-bold text-white">Your Curated Shortlist</h3>
            <p class="text-xs text-slate-400">Share your favorite picks with your friend or compare them side-by-side</p>
          </div>
        </div>
        <button id="close-wishlist-btn" class="w-8 h-8 rounded-full bg-carbon-800 text-slate-400 hover:text-white flex items-center justify-center transition">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <div class="p-6 overflow-y-auto space-y-4 custom-scrollbar text-xs flex-grow" id="wishlist-modal-items">
        <!-- Injected via JavaScript -->
      </div>

      <!-- Action Footer -->
      <div class="p-6 border-t border-white/10 bg-carbon-950 space-y-3">
        <div class="flex items-center justify-between text-xs font-mono">
          <span class="text-slate-400">Est. 11.11 Total vs. Amazon.de:</span>
          <div>
            <span id="wishlist-total-ali" class="text-emerald-400 font-bold text-sm">€0</span>
            <span class="text-slate-500 ml-1.5 line-through" id="wishlist-total-amazon">€0</span>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
          <button id="copy-share-url-btn" class="py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition flex items-center justify-center gap-2">
            <i class="fa-solid fa-link"></i>
            <span>Copy Shareable Link</span>
          </button>
          <button id="copy-chat-summary-btn" class="py-2.5 px-4 rounded-xl bg-carbon-800 hover:bg-carbon-700 text-slate-200 border border-white/10 font-bold text-xs transition flex items-center justify-center gap-2">
            <i class="fa-solid fa-copy text-emerald-400"></i>
            <span>Copy Chat Message for Friend</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- DETAIL MODAL FOR SINGLE IEM -->
  <div id="detail-modal" class="fixed inset-0 z-50 bg-black/85 backdrop-blur-md hidden flex items-center justify-center p-4">
    <div class="bg-carbon-900 border border-white/15 max-w-2xl w-full rounded-3xl shadow-2xl overflow-hidden max-h-[92vh] flex flex-col">
      <div class="p-6 border-b border-white/10 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <span id="modal-brand-badge" class="stamp-badge text-xs px-2.5 py-1 rounded-md bg-blue-500/20 text-blue-400 border border-blue-500/30"></span>
          <h3 id="modal-title" class="text-xl font-bold text-white"></h3>
        </div>
        <button id="close-detail-modal-btn" class="w-8 h-8 rounded-full bg-carbon-800 text-slate-400 hover:text-white flex items-center justify-center transition">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <div class="p-6 overflow-y-auto space-y-6 custom-scrollbar text-xs">
        <!-- Quick Specs -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
          <div class="p-3 rounded-2xl bg-carbon-950 border border-white/5">
            <span class="text-slate-400 block text-[10px] uppercase font-mono">Driver</span>
            <span id="modal-driver" class="font-bold text-white text-xs mt-1 block"></span>
          </div>
          <div class="p-3 rounded-2xl bg-carbon-950 border border-white/5">
            <span class="text-slate-400 block text-[10px] uppercase font-mono">Nozzle Outer</span>
            <span id="modal-nozzle" class="font-bold text-white text-xs mt-1 block font-mono"></span>
          </div>
          <div class="p-3 rounded-2xl bg-carbon-950 border border-white/5">
            <span class="text-slate-400 block text-[10px] uppercase font-mono">Comfort Fit</span>
            <span id="modal-comfort" class="font-bold text-emerald-400 text-xs mt-1 block font-mono"></span>
          </div>
          <div class="p-3 rounded-2xl bg-carbon-950 border border-white/5">
            <span class="text-slate-400 block text-[10px] uppercase font-mono">Gaming Score</span>
            <span id="modal-gaming" class="font-bold text-blue-400 text-xs mt-1 block font-mono"></span>
          </div>
        </div>

        <!-- Sound Profile -->
        <div class="space-y-1.5">
          <h5 class="font-bold text-slate-400 uppercase tracking-wider font-mono text-[11px]">Tonal Identity & Signature</h5>
          <p id="modal-sound-desc" class="text-slate-200 leading-relaxed text-sm bg-carbon-950 p-4 rounded-2xl border border-white/5"></p>
        </div>

        <!-- Build & Accessories -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <h5 class="font-bold text-slate-400 uppercase tracking-wider font-mono text-[11px]">Housing & Connector</h5>
            <div class="bg-carbon-950 p-3.5 rounded-2xl border border-white/5 space-y-1">
              <div class="text-slate-200" id="modal-build"></div>
              <div class="text-slate-400 text-[11px]" id="modal-cable"></div>
            </div>
          </div>
          <div class="space-y-1.5">
            <h5 class="font-bold text-slate-400 uppercase tracking-wider font-mono text-[11px]">Included Accessories</h5>
            <div class="bg-carbon-950 p-3.5 rounded-2xl border border-white/5 space-y-1">
              <div class="text-slate-200" id="modal-accessories"></div>
              <div class="text-amber-400 font-mono text-[11px]" id="modal-accessories-rating"></div>
            </div>
          </div>
        </div>

        <!-- QC & Fit Alerts -->
        <div class="space-y-1.5">
          <h5 class="font-bold text-amber-400 uppercase tracking-wider font-mono text-[11px] flex items-center gap-1.5">
            <i class="fa-solid fa-wrench"></i>
            Reliability, Moisture & Fit Analysis
          </h5>
          <div id="modal-qc" class="text-slate-300 leading-relaxed bg-amber-500/10 border border-amber-500/20 p-4 rounded-2xl"></div>
        </div>

        <!-- Reviewer Verdicts -->
        <div class="space-y-2">
          <h5 class="font-bold text-slate-400 uppercase tracking-wider font-mono text-[11px]">Reviewer Consensus</h5>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
            <div class="bg-carbon-950 p-3 rounded-2xl border border-white/5">
              <span class="text-slate-500 block text-[10px] font-mono">Crinacle IEF</span>
              <span id="modal-crinacle" class="font-bold text-white mt-0.5 block"></span>
            </div>
            <div class="bg-carbon-950 p-3 rounded-2xl border border-white/5">
              <span class="text-slate-500 block text-[10px] font-mono">Super* Review</span>
              <span id="modal-super" class="font-bold text-white mt-0.5 block"></span>
            </div>
            <div class="bg-carbon-950 p-3 rounded-2xl border border-white/5">
              <span class="text-slate-500 block text-[10px] font-mono">Jay's Audio</span>
              <span id="modal-jays" class="font-bold text-white mt-0.5 block"></span>
            </div>
          </div>
        </div>

        <!-- Personal Notes Area -->
        <div class="space-y-2">
          <h5 class="font-bold text-slate-400 uppercase tracking-wider font-mono text-[11px] flex items-center gap-1.5">
            <i class="fa-solid fa-pen text-indigo-400"></i>
            Personal Note (Saved locally on your device)
          </h5>
          <textarea id="modal-personal-note" rows="2" placeholder="Write your own private thoughts or fit impressions here..." class="w-full bg-carbon-950 border border-white/10 rounded-xl p-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition"></textarea>
        </div>

        <!-- Pricing Grid -->
        <div class="space-y-2">
          <h5 class="font-bold text-slate-400 uppercase tracking-wider font-mono text-[11px]">Pricing in Germany / EU</h5>
          <div class="grid grid-cols-3 gap-3 text-center">
            <div class="p-3 rounded-2xl bg-carbon-950 border border-white/5">
              <span class="text-slate-400 text-[10px] block font-mono">Amazon.de (Prime)</span>
              <span id="modal-price-amazon" class="font-bold text-white text-sm mt-0.5 block font-mono"></span>
            </div>
            <div class="p-3 rounded-2xl bg-carbon-950 border border-white/5">
              <span class="text-slate-400 text-[10px] block font-mono">AliExpress Choice</span>
              <span id="modal-price-ali-choice" class="font-bold text-blue-400 text-sm mt-0.5 block font-mono"></span>
            </div>
            <div class="p-3 rounded-2xl bg-carbon-950 border border-emerald-500/30 bg-emerald-500/5">
              <span class="text-emerald-400 text-[10px] block font-mono font-semibold">11.11 Mega Sale</span>
              <span id="modal-price-ali-1111" class="font-bold text-emerald-400 text-sm mt-0.5 block font-mono"></span>
            </div>
          </div>
        </div>

        <!-- Store Links -->
        <div class="space-y-2 pt-2 border-t border-white/10">
          <h5 class="font-bold text-slate-400 uppercase tracking-wider font-mono text-[11px]">Verified Retail Channels</h5>
          <div id="modal-links" class="flex flex-wrap gap-2"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- TOAST NOTIFICATION -->
  <div id="toast" class="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 px-4 py-2.5 rounded-xl bg-carbon-850 border border-white/20 text-white text-xs font-mono shadow-2xl hidden flex items-center gap-2">
    <i class="fa-solid fa-circle-check text-emerald-400"></i>
    <span id="toast-message">Copied to clipboard!</span>
  </div>

  <!-- JAVASCRIPT APPLICATION CODE -->
  <script>
    const iemsData = {json_data};
    let currentFilter = 'all';
    let currentPriceTier = 'all';
    let currentNozzle = 'all';
    let currentSort = 'score-desc';
    let searchQuery = '';
    let viewingSharedOnly = false;
    let currentModalIemId = null;

    // Load Shortlist from LocalStorage or URL params
    let shortlist = JSON.parse(localStorage.getItem('iem_radar_shortlist') || '[]');
    let personalNotes = JSON.parse(localStorage.getItem('iem_radar_notes') || '{{}}');

    // Parse URL params for ?picks=iem1,iem2
    const urlParams = new URLSearchParams(window.location.search);
    const sharedPicks = urlParams.get('picks') ? urlParams.get('picks').split(',') : [];

    if (sharedPicks.length > 0) {{
      document.getElementById('shared-picks-banner').classList.remove('hidden');
      // Merge shared picks into local shortlist if empty
      if (shortlist.length === 0) {{
        shortlist = [...sharedPicks];
        localStorage.setItem('iem_radar_shortlist', JSON.stringify(shortlist));
      }}
    }}

    // Elements
    const cardsView = document.getElementById('cards-view');
    const tableView = document.getElementById('table-view');
    const tableBody = document.getElementById('table-body');
    const searchInput = document.getElementById('search-input');
    const priceFilter = document.getElementById('price-filter');
    const nozzleFilter = document.getElementById('nozzle-filter');
    const sortSelect = document.getElementById('sort-select');
    const personaButtons = document.querySelectorAll('.persona-btn');
    const resetPersonaBtn = document.getElementById('reset-persona-btn');
    const viewCardsBtn = document.getElementById('view-cards-btn');
    const viewTableBtn = document.getElementById('view-table-btn');

    // Modals
    const detailModal = document.getElementById('detail-modal');
    const closeDetailModalBtn = document.getElementById('close-detail-modal-btn');
    const wishlistModal = document.getElementById('wishlist-modal');
    const closeWishlistBtn = document.getElementById('close-wishlist-btn');
    const openWishlistTopBtn = document.getElementById('open-wishlist-top-btn');
    const openWishlistModalBtn = document.getElementById('open-wishlist-modal-btn');
    const floatingWishlistPill = document.getElementById('floating-wishlist-pill');
    const wishlistCounterBadge = document.getElementById('wishlist-counter-badge');
    const wishlistPillCount = document.getElementById('wishlist-pill-count');
    const wishlistPillTotal = document.getElementById('wishlist-pill-total');

    function showToast(msg) {{
      const toast = document.getElementById('toast');
      document.getElementById('toast-message').textContent = msg;
      toast.classList.remove('hidden');
      setTimeout(() => toast.classList.add('hidden'), 2500);
    }}

    function updateShortlistUI() {{
      const count = shortlist.length;
      wishlistCounterBadge.textContent = count;
      wishlistPillCount.textContent = count;

      if (count > 0) {{
        floatingWishlistPill.classList.remove('hidden');
        // Calculate estimated totals
        const totalAli = shortlist.reduce((sum, id) => {{
          const item = iemsData.find(i => i.id === id);
          return sum + (item ? item.price_eur_ali_1111 : 0);
        }}, 0);
        wishlistPillTotal.textContent = '~€' + totalAli.toFixed(1);
      }} else {{
        floatingWishlistPill.classList.add('hidden');
      }}
    }}

    window.toggleShortlist = function(id, event) {{
      if (event) event.stopPropagation();
      const idx = shortlist.indexOf(id);
      if (idx > -1) {{
        shortlist.splice(idx, 1);
        showToast('Removed from Shortlist');
      }} else {{
        shortlist.push(id);
        showToast('Added to Shortlist ❤️');
      }}
      localStorage.setItem('iem_radar_shortlist', JSON.stringify(shortlist));
      updateShortlistUI();
      render();
    }};

    function render() {{
      let filtered = iemsData.filter(iem => {{
        if (viewingSharedOnly && !sharedPicks.includes(iem.id)) return false;

        // Persona matching
        if (currentFilter !== 'all') {{
          if (currentFilter === 'Tactical FPS Gaming') {{
            if (iem.gaming_score < 8.4) return false;
          }} else if (currentFilter === 'Audio Purists & Reference') {{
            if (!iem.sound_signature.includes('Neutral') && !iem.name.includes('Hexa') && !iem.name.includes('RED')) return false;
          }} else if (currentFilter === 'Warm & Relaxed Daily') {{
            if (!iem.sound_signature.includes('Warm') && !iem.sound_signature.includes('Lush') && !iem.sound_signature.includes('Harman')) return false;
          }} else if (currentFilter === 'Bassheads & Theatrical EDM') {{
            if (!iem.sound_signature.includes('Bass') && !iem.sound_signature.includes('U-Curve') && !iem.name.includes('ZAR') && !iem.name.includes('Op.22') && !iem.name.includes('Titan X')) return false;
          }} else if (currentFilter === 'Smartphone USB-C Users') {{
            if (!iem.connection.includes('USB-C') && !iem.connection.includes('DSP')) return false;
          }} else if (currentFilter === 'Small Ears & Sleep') {{
            if (iem.comfort_rating < 9.0 || iem.nozzle_diameter_mm > 5.5) return false;
          }} else if (currentFilter === 'Vocal & Acoustic Lovers') {{
            if (!iem.target_personas.some(p => p.includes('Vocal') || p.includes('Acoustic')) && !iem.name.includes('Wan\'er') && !iem.name.includes('Cadenza') && !iem.name.includes('Gate')) return false;
          }}
        }}

        // Price Tier
        if (currentPriceTier === 'ultra-budget' && iem.price_eur_amazon > 30) return false;
        if (currentPriceTier === 'entry' && (iem.price_eur_amazon <= 30 || iem.price_eur_amazon > 55)) return false;
        if (currentPriceTier === 'mid' && (iem.price_eur_amazon <= 55 || iem.price_eur_amazon > 80)) return false;
        if (currentPriceTier === 'upper' && iem.price_eur_amazon <= 80) return false;

        // Nozzle Safety
        if (currentNozzle === 'safe' && iem.nozzle_diameter_mm > 5.5) return false;
        if (currentNozzle === 'warning' && iem.nozzle_diameter_mm <= 6.0) return false;

        // Search Query
        if (searchQuery) {{
          const q = searchQuery.toLowerCase();
          const match = iem.name.toLowerCase().includes(q) ||
                        iem.brand.toLowerCase().includes(q) ||
                        iem.driver_type.toLowerCase().includes(q) ||
                        iem.sound_signature.toLowerCase().includes(q) ||
                        iem.target_personas.some(p => p.toLowerCase().includes(q));
          if (!match) return false;
        }}

        return true;
      }});

      // Sorting
      filtered.sort((a, b) => {{
        if (currentSort === 'score-desc') return b.community_score - a.community_score;
        if (currentSort === 'price-ali-asc') return a.price_eur_ali_1111 - b.price_eur_ali_1111;
        if (currentSort === 'price-amazon-asc') return a.price_eur_amazon - b.price_eur_amazon;
        if (currentSort === 'comfort-desc') return b.comfort_rating - a.comfort_rating;
        if (currentSort === 'gaming-desc') return b.gaming_score - a.gaming_score;
        return 0;
      }});

      // Render Cards
      cardsView.innerHTML = filtered.map(iem => {{
        const isFavorited = shortlist.includes(iem.id);
        const hasNote = personalNotes[iem.id];

        return `
          <div class="editorial-card rounded-3xl p-5 flex flex-col justify-between relative group">
            <div>
              <!-- Header Bar inside Card -->
              <div class="flex items-center justify-between gap-2 mb-2">
                <span class="stamp-badge text-[10px] px-2 py-0.5 rounded-md bg-carbon-900 text-slate-300 border border-white/5">
                  ${{iem.brand}}
                </span>
                
                <div class="flex items-center gap-1.5">
                  ${{iem.nozzle_diameter_mm > 6.0 ? `
                    <span class="stamp-badge text-[9px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
                      ⚠️ 6.2mm Nozzle
                    </span>
                  ` : iem.comfort_rating >= 9.4 ? `
                    <span class="stamp-badge text-[9px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                      ✓ Small Ear Safe
                    </span>
                  ` : ''}}
                  
                  <button onclick="toggleShortlist('${{iem.id}}', event)" class="w-7 h-7 rounded-lg flex items-center justify-center transition ${{isFavorited ? 'bg-rose-500 text-white' : 'bg-carbon-900 text-slate-400 hover:text-rose-400'}} border border-white/5">
                    <i class="fa-solid fa-heart text-xs"></i>
                  </button>
                </div>
              </div>

              <!-- Title & Drivers -->
              <h4 class="text-xl font-bold text-white group-hover:text-blue-400 transition cursor-pointer" onclick="openModal('${{iem.id}}')">
                ${{iem.name}}
              </h4>
              <div class="flex items-center gap-2 mt-1 text-xs text-slate-400 font-mono">
                <span>${{iem.driver_type}}</span>
                <span>•</span>
                <span>${{iem.nozzle_diameter_mm}}mm outer bore</span>
              </div>

              <!-- Sound Signature Tag -->
              <div class="mt-3">
                <span class="inline-block px-2.5 py-1 rounded-lg bg-blue-500/10 text-blue-300 text-xs font-medium border border-blue-500/20">
                  ${{iem.sound_signature}}
                </span>
              </div>

              <!-- Sound Summary -->
              <p class="text-xs text-slate-300 mt-2.5 line-clamp-2 leading-relaxed">
                ${{iem.sound_description}}
              </p>

              <!-- Persona Pills -->
              <div class="flex flex-wrap gap-1 mt-3">
                ${{iem.target_personas.slice(0, 2).map(p => `
                  <span class="text-[10px] px-2 py-0.5 rounded-full bg-carbon-900 text-slate-400 border border-white/5 font-mono">
                    ${{p}}
                  </span>
                `).join('')}}
              </div>

              ${{hasNote ? `
                <div class="mt-3 text-[11px] p-2 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 italic">
                  <i class="fa-solid fa-pen text-[9px] mr-1"></i> "${{hasNote}}"
                </div>
              ` : ''}}
            </div>

            <!-- Pricing & Action -->
            <div class="mt-5 pt-4 border-t border-white/5 space-y-3">
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div class="bg-carbon-950 p-2.5 rounded-xl border border-white/5">
                  <span class="text-[10px] text-slate-400 block font-mono uppercase">Amazon.de</span>
                  <span class="font-bold text-white font-mono text-sm">~€${{iem.price_eur_amazon}}</span>
                </div>
                <div class="bg-emerald-500/10 p-2.5 rounded-xl border border-emerald-500/20">
                  <span class="text-[10px] text-emerald-400 block font-mono uppercase font-semibold">11.11 / Choice</span>
                  <span class="font-bold text-emerald-400 font-mono text-sm">~€${{iem.price_eur_ali_1111}}</span>
                </div>
              </div>

              <div class="flex items-center gap-2">
                <button onclick="openModal('${{iem.id}}')" class="w-full py-2 px-3 rounded-xl bg-carbon-800 hover:bg-carbon-700 text-slate-200 text-xs font-medium transition flex items-center justify-center gap-1.5 border border-white/5">
                  <i class="fa-solid fa-circle-info text-blue-400"></i>
                  <span>Inspect Details & Stores</span>
                </button>
              </div>
            </div>
          </div>
        `;
      }}).join('');

      // Render Table
      tableBody.innerHTML = filtered.map(iem => {{
        const isFavorited = shortlist.includes(iem.id);
        return `
          <tr class="hover:bg-carbon-800/50 transition cursor-pointer" onclick="openModal('${{iem.id}}')">
            <td class="px-4 py-3 font-semibold text-white">
              ${{iem.name}}
              <span class="block text-[10px] text-slate-400 font-normal font-mono">${{iem.brand}}</span>
            </td>
            <td class="px-4 py-3 text-slate-300 font-mono text-[11px]">${{iem.driver_type}}</td>
            <td class="px-4 py-3 text-slate-300">${{iem.sound_signature}}</td>
            <td class="px-4 py-3 font-mono text-center ${{iem.nozzle_diameter_mm > 6.0 ? 'text-rose-400 font-bold' : 'text-slate-300'}}">
              ${{iem.nozzle_diameter_mm}}mm
            </td>
            <td class="px-4 py-3 font-mono text-emerald-400 text-center">${{iem.comfort_rating}}/10</td>
            <td class="px-4 py-3 font-mono text-emerald-400 font-bold">~€${{iem.price_eur_ali_1111}}</td>
            <td class="px-4 py-3 font-mono text-slate-200">~€${{iem.price_eur_amazon}}</td>
            <td class="px-4 py-3 font-mono text-blue-400 font-bold text-center">★ ${{iem.community_score}}</td>
            <td class="px-4 py-3 text-right">
              <button onclick="toggleShortlist('${{iem.id}}', event)" class="p-2 rounded-lg text-xs ${{isFavorited ? 'text-rose-500' : 'text-slate-500 hover:text-white'}}">
                <i class="fa-solid fa-heart"></i>
              </button>
            </td>
          </tr>
        `;
      }}).join('');
    }}

    // Persona buttons
    personaButtons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        personaButtons.forEach(b => {{
          b.classList.remove('active', 'border-blue-500', 'bg-blue-500/20', 'text-white');
          b.classList.add('border-white/5', 'bg-carbon-900', 'text-slate-300');
        }});
        btn.classList.add('active', 'border-blue-500', 'bg-blue-500/20', 'text-white');
        btn.classList.remove('border-white/5', 'bg-carbon-900', 'text-slate-300');
        currentFilter = btn.dataset.persona;
        resetPersonaBtn.classList.remove('hidden');
        render();
      }});
    }});

    resetPersonaBtn.addEventListener('click', () => {{
      currentFilter = 'all';
      resetPersonaBtn.classList.add('hidden');
      personaButtons.forEach(b => {{
        b.classList.remove('active', 'border-blue-500', 'bg-blue-500/20', 'text-white');
        b.classList.add('border-white/5', 'bg-carbon-900', 'text-slate-300');
      }});
      document.querySelector('[data-persona="all"]').classList.add('active', 'border-blue-500', 'bg-blue-500/20', 'text-white');
      render();
    }});

    priceFilter.addEventListener('change', (e) => {{
      currentPriceTier = e.target.value;
      render();
    }});

    nozzleFilter.addEventListener('change', (e) => {{
      currentNozzle = e.target.value;
      render();
    }});

    sortSelect.addEventListener('change', (e) => {{
      currentSort = e.target.value;
      render();
    }});

    searchInput.addEventListener('input', (e) => {{
      searchQuery = e.target.value;
      render();
    }});

    viewCardsBtn.addEventListener('click', () => {{
      cardsView.classList.remove('hidden');
      tableView.classList.add('hidden');
      viewCardsBtn.classList.add('bg-blue-600', 'text-white');
      viewCardsBtn.classList.remove('text-slate-400');
      viewTableBtn.classList.remove('bg-blue-600', 'text-white');
      viewTableBtn.classList.add('text-slate-400');
    }});

    viewTableBtn.addEventListener('click', () => {{
      cardsView.classList.add('hidden');
      tableView.classList.remove('hidden');
      viewTableBtn.classList.add('bg-blue-600', 'text-white');
      viewTableBtn.classList.remove('text-slate-400');
      viewCardsBtn.classList.remove('bg-blue-600', 'text-white');
      viewCardsBtn.classList.add('text-slate-400');
    }});

    // Open Wishlist Modal
    function openWishlistModal() {{
      const itemsContainer = document.getElementById('wishlist-modal-items');
      if (shortlist.length === 0) {{
        itemsContainer.innerHTML = `
          <div class="text-center py-8 space-y-2 text-slate-400">
            <i class="fa-regular fa-heart text-3xl text-slate-600"></i>
            <p>Your shortlist is empty. Click the heart icon on any IEM card to add it!</p>
          </div>
        `;
        document.getElementById('wishlist-total-ali').textContent = '€0';
        document.getElementById('wishlist-total-amazon').textContent = '€0';
      }} else {{
        let totalAli = 0;
        let totalAmazon = 0;

        itemsContainer.innerHTML = shortlist.map(id => {{
          const item = iemsData.find(i => i.id === id);
          if (!item) return '';
          totalAli += item.price_eur_ali_1111;
          totalAmazon += item.price_eur_amazon;

          return `
            <div class="p-3.5 rounded-2xl bg-carbon-950 border border-white/5 flex items-center justify-between gap-3">
              <div class="space-y-0.5">
                <span class="stamp-badge text-[9px] text-blue-400 font-mono">${{item.brand}}</span>
                <h5 class="font-bold text-white text-sm">${{item.name}}</h5>
                <span class="text-[11px] text-slate-400 font-mono">${{item.sound_signature}} • ${{item.nozzle_diameter_mm}}mm nozzle</span>
              </div>
              <div class="flex items-center gap-3">
                <div class="text-right font-mono">
                  <span class="block text-emerald-400 font-bold text-sm">~€${{item.price_eur_ali_1111}}</span>
                  <span class="block text-[10px] text-slate-500 line-through">Amazon: €${{item.price_eur_amazon}}</span>
                </div>
                <button onclick="toggleShortlist('${{item.id}}'); openWishlistModal();" class="w-7 h-7 rounded-lg bg-carbon-800 text-rose-400 hover:bg-rose-500 hover:text-white transition flex items-center justify-center">
                  <i class="fa-solid fa-trash-can text-xs"></i>
                </button>
              </div>
            </div>
          `;
        }}).join('');

        document.getElementById('wishlist-total-ali').textContent = '€' + totalAli.toFixed(1);
        document.getElementById('wishlist-total-amazon').textContent = '€' + totalAmazon.toFixed(1);
      }}

      wishlistModal.classList.remove('hidden');
    }}

    openWishlistTopBtn.addEventListener('click', openWishlistModal);
    openWishlistModalBtn.addEventListener('click', openWishlistModal);
    closeWishlistBtn.addEventListener('click', () => wishlistModal.classList.add('hidden'));

    // Copy Shareable URL
    document.getElementById('copy-share-url-btn').addEventListener('click', () => {{
      const shareUrl = window.location.origin + window.location.pathname + '?picks=' + shortlist.join(',');
      navigator.clipboard.writeText(shareUrl).then(() => {{
        showToast('Shareable Link Copied to Clipboard!');
      }});
    }});

    // Copy Message for Chat
    document.getElementById('copy-chat-summary-btn').addEventListener('click', () => {{
      let text = "🎧 My Curated IEM Shortlist:\\n\\n";
      let totalAli = 0;
      let totalAmazon = 0;

      shortlist.forEach((id, idx) => {{
        const item = iemsData.find(i => i.id === id);
        if (item) {{
          totalAli += item.price_eur_ali_1111;
          totalAmazon += item.price_eur_amazon;
          text += `${{idx + 1}}. ${{item.name}} (${{item.brand}})\\n`;
          text += `   • Sound: ${{item.sound_signature}}\\n`;
          text += `   • 11.11 Sale Price: ~€${{item.price_eur_ali_1111}} (Amazon.de: ~€${{item.price_eur_amazon}})\\n`;
          text += `   • Nozzle: ${{item.nozzle_diameter_mm}}mm outer bore\\n\\n`;
        }}
      }});

      text += `Total Est. on 11.11: €${{totalAli.toFixed(1)}} (vs. €${{totalAmazon.toFixed(1)}} on Amazon)\\n`;
      text += `View full interactive comparison: ${{window.location.origin + window.location.pathname + '?picks=' + shortlist.join(',')}}`;

      navigator.clipboard.writeText(text).then(() => {{
        showToast('Chat Message Summary Copied!');
      }});
    }});

    // Shared Banner buttons
    const filterSharedBtn = document.getElementById('filter-shared-only-btn');
    if (filterSharedBtn) {{
      filterSharedBtn.addEventListener('click', () => {{
        viewingSharedOnly = true;
        render();
        showToast("Filtering to Friend's Picks");
      }});
    }}
    const clearSharedBtn = document.getElementById('clear-shared-view-btn');
    if (clearSharedBtn) {{
      clearSharedBtn.addEventListener('click', () => {{
        viewingSharedOnly = false;
        render();
        showToast('Displaying All 21 IEMs');
      }});
    }}

    // Detail Modal logic
    window.openModal = function(iemId) {{
      currentModalIemId = iemId;
      const iem = iemsData.find(i => i.id === iemId);
      if (!iem) return;

      document.getElementById('modal-title').textContent = iem.name;
      document.getElementById('modal-brand-badge').textContent = iem.brand;
      document.getElementById('modal-driver').textContent = iem.driver_type;
      document.getElementById('modal-nozzle').textContent = iem.nozzle_diameter_mm + ' mm';
      document.getElementById('modal-comfort').textContent = iem.comfort_rating + ' / 10';
      document.getElementById('modal-gaming').textContent = iem.gaming_score + ' / 10';
      document.getElementById('modal-sound-desc').textContent = iem.sound_description;
      document.getElementById('modal-build').textContent = iem.build_material;
      document.getElementById('modal-cable').textContent = iem.cable_detail;
      document.getElementById('modal-accessories').textContent = iem.accessories_included;
      document.getElementById('modal-accessories-rating').textContent = '★ Accessory Score: ' + iem.accessories_rating + '/10';
      document.getElementById('modal-qc').innerHTML = `
        <strong>QC, Fit & Reliability Profile:</strong><br>
        ${{iem.qc_and_known_issues}}<br>
        <div class="mt-2 text-slate-400 italic font-mono text-[10px]">${{iem.notes}}</div>
      `;
      document.getElementById('modal-crinacle').textContent = iem.crinacle_rank;
      document.getElementById('modal-super').textContent = iem.super_review_rating;
      document.getElementById('modal-jays').textContent = iem.jays_audio_rating;
      document.getElementById('modal-price-amazon').textContent = '€' + iem.price_eur_amazon;
      document.getElementById('modal-price-ali-choice').textContent = '€' + iem.price_eur_ali_choice;
      document.getElementById('modal-price-ali-1111').textContent = '€' + iem.price_eur_ali_1111;

      // Note
      const noteInput = document.getElementById('modal-personal-note');
      noteInput.value = personalNotes[iemId] || '';
      noteInput.oninput = (e) => {{
        personalNotes[iemId] = e.target.value;
        localStorage.setItem('iem_radar_notes', JSON.stringify(personalNotes));
        render();
      }};

      const linksContainer = document.getElementById('modal-links');
      linksContainer.innerHTML = iem.verified_stores.map(store => `
        <a href="${{store.url}}" target="_blank" rel="noopener noreferrer" class="px-3.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium text-xs transition flex items-center gap-1.5 shadow-sm">
          <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
          <span>Check ${{store.name}}</span>
        </a>
      `).join('');

      detailModal.classList.remove('hidden');
    }};

    closeDetailModalBtn.addEventListener('click', () => {{
      detailModal.classList.add('hidden');
    }});

    detailModal.addEventListener('click', (e) => {{
      if (e.target === detailModal) detailModal.classList.add('hidden');
    }});

    // Hero share button
    document.getElementById('hero-share-btn').addEventListener('click', () => {{
      if (navigator.share) {{
        navigator.share({{
          title: 'IEM Radar 2026',
          text: 'Check out this comprehensive Chi-Fi IEM comparison guide and pricing radar!',
          url: window.location.href,
        }});
      }} else {{
        navigator.clipboard.writeText(window.location.href).then(() => {{
          showToast('Website Link Copied to Clipboard!');
        }});
      }}
    }});

    // Init
    updateShortlistUI();
    render();
  </script>
</body>
</html>
"""
    return html

def main():
    os.makedirs(os.path.dirname(OUTPUT_HTML_DIST), exist_ok=True)
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    
    print(f"Loading IEM database from {DATA_FILE}...")
    iems = load_data()
    print(f"Loaded {len(iems)} models.")
    
    print("Generating refined editorial HTML dashboard...")
    html_content = generate_html(iems)
    
    with open(OUTPUT_HTML_DIST, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully wrote HTML to {OUTPUT_HTML_DIST}")

    with open(OUTPUT_HTML_ROOT, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully wrote HTML to {OUTPUT_HTML_ROOT} (for root GitHub Pages deployment)")
    
    with open(ARTIFACT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully mirrored HTML to conversation artifact: {ARTIFACT_HTML}")

if __name__ == "__main__":
    main()
