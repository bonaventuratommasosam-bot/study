#!/usr/bin/env python3
"""
Study Open Source — Setup Script (Python)
Crea un profilo Hermes "Study" — funziona su Windows, Mac, Linux.
Docs: https://github.com/bonaventuratommasosam-bot/study
"""
import os
import sys
import shutil
from pathlib import Path

# Default free API key for zero-friction onboarding (Gemini)
# Students can press Enter to use this shared key.
# For heavy use, get your own: https://aistudio.google.com/apikey
# Override: set STUDY_GEMINI_KEY environment variable
import base64 as _b64
DEFAULT_GEMINI_KEY = os.environ.get("STUDY_GEMINI_KEY",
    _b64.b64decode("QVEuQWI4Uk42S19HdVZfOGhsUkdwLXU3QXYxUkZvc3BXSmtkcGg1cmpndDE4MUUwN01sa0E=").decode())

TEMPLATE_DIR = Path(__file__).resolve().parent / "profile"
# Hermes profile directory
HERMES_HOME = Path(os.environ.get("HERMES_HOME", ""))
if HERMES_HOME and HERMES_HOME.is_dir():
    PROFILE_DIR = HERMES_HOME / "profiles" / "study"
else:
    # Auto-detect: Windows uses AppData, everything else uses ~/.hermes
    appdata = Path.home() / "AppData" / "Local" / "hermes"
    if appdata.is_dir():
        PROFILE_DIR = appdata / "profiles" / "study"
    else:
        PROFILE_DIR = Path.home() / ".hermes" / "profiles" / "study"

def banner():
    print("""
  ╔══════════════════════════════════════════╗
  ║  📚⚡ Study — Il Tutor Gratuito         ║
  ║  Feynman + Montessori + Socrate          ║
  ║  L'unico prodotto free di HermesBro      ║
  ╚══════════════════════════════════════════╝
""")

def check_prereqs():
    print("→ Verifica prerequisiti...")
    # Find hermes — might not be in PATH on Windows
    hermes_path = shutil.which("hermes")
    if not hermes_path:
        # Check common Hermes install locations
        candidates = [
            Path.home() / "AppData" / "Local" / "hermes" / "hermes-agent" / "venv" / "Scripts" / "hermes.exe",
            Path.home() / ".local" / "bin" / "hermes",
            Path("/usr/local/bin/hermes"),
        ]
        for p in candidates:
            if p.exists():
                hermes_path = str(p)
                os.environ["PATH"] = str(p.parent) + os.pathsep + os.environ.get("PATH", "")
                break
    if hermes_path:
        print("✓ Hermes Agent trovato")
    else:
        print("✗ Hermes Agent non trovato.")
        print("  Installa: https://hermes-agent.nousresearch.com/docs")
        sys.exit(1)
    print("✓ Python OK")

def ask(prompt, default=""):
    if default:
        val = input(f"? {prompt} [{default}]: ").strip()
        return val if val else default
    return input(f"? {prompt}: ").strip()

def pick(prompt, choices, default="1"):
    """Ask for a numeric choice, validate, return the choice string."""
    while True:
        val = ask(prompt, default)
        if val in choices:
            return val
        print(f"  ⚠ Enter a number ({', '.join(choices)})")

def ask_language():
    print("\nChoose your language / Scegli la lingua:")
    print("  1) English")
    print("  2) Italiano")
    print("  3) Français")
    print("  4) Deutsch")
    print("  5) Español")
    print("  6) Polski")
    print("  7) Magyar")
    choice = pick("Choice / Scelta [1-7]", ["1","2","3","4","5","6","7"], "1")

    langs = {
        "1": ("en", "English"), "2": ("it", "Italiano"), "3": ("fr", "Français"),
        "4": ("de", "Deutsch"), "5": ("es", "Español"), "6": ("pl", "Polski"), "7": ("hu", "Magyar"),
    }
    code, name = langs[choice]
    print(f"  Language: {name}")
    return code, name

def ask_llm():
    print("\nScegli il provider LLM:")
    print("  1) Gemini — FREE (Gemini 2.5 Flash — press Enter to use shared key)")
    print("  2) DeepSeek — cheap (~$3-5/month, best value)")
    print("  3) OpenAI — GPT-4o (paid, best quality)")
    print("  4) Anthropic — Claude Sonnet 4 (paid, reasoning)")
    print("  5) OpenRouter — any model, one API key")
    print("  6) Local (Ollama) — no API key needed")
    print("  7) Custom — your own API endpoint")
    choice = pick("Scelta [1-7]", ["1","2","3","4","5","6","7"], "1")

    providers = {
        "1": ("openai", "https://generativelanguage.googleapis.com/v1beta/openai", "gemini-2.5-flash", "Gemini (FREE)", "8192"),
        "2": ("openai", "https://api.deepseek.com/v1", "deepseek-chat", "DeepSeek (~$3-5/mo)", "8192"),
        "3": ("openai", "https://api.openai.com/v1", "gpt-4o", "OpenAI (paid)", "16384"),
        "4": ("anthropic", "https://api.anthropic.com/v1", "claude-sonnet-4-20250514", "Anthropic (paid)", "8192"),
        "5": ("openai", "https://openrouter.ai/api/v1", "openai/gpt-4o", "OpenRouter", "16384"),
        "6": ("openai", "http://localhost:11434/v1", "llama3.2", "Local (Ollama)", "4096"),
    }

    if choice in providers:
        api_mode, base_url, model, label, max_tokens = providers[choice]
        if choice == "6":
            print("  Make sure Ollama is running: ollama serve")
            print("  Default model: llama3.2 (change in config.yaml after setup)")
            print("  (no API key needed for local models)")
            return {"api_mode": api_mode, "api_key": "ollama", "base_url": base_url, "model": model, "label": label, "max_tokens": max_tokens}
        if choice == "5":
            key = ask("  OpenRouter API key (https://openrouter.ai/keys)")
            model_choice = ask("  Model", "openai/gpt-4o")
            return {"api_mode": api_mode, "api_key": key, "base_url": base_url, "model": model_choice, "label": "OpenRouter", "max_tokens": max_tokens}
        if choice == "1":
            # Gemini — shared free key for zero-friction onboarding
            key = ask(f"  Gemini API key (press Enter for free default)")
            if not key:
                key = DEFAULT_GEMINI_KEY
                print("  ✓ Using shared free key (rate-limited, 2M tokens/day)")
                print("    For heavy use, get your own: https://aistudio.google.com/apikey")
            return {"api_mode": api_mode, "api_key": key, "base_url": base_url, "model": model, "label": label, "max_tokens": max_tokens}
        key = ask(f"  API key for {label}")
        if not key:
            print("  WARNING: No API key provided. Add it later in config.yaml")
            key = "YOUR_API_KEY_HERE"
        print(f"  {label}")
        return {"api_mode": api_mode, "api_key": key, "base_url": base_url, "model": model, "label": label, "max_tokens": max_tokens}
    elif choice == "7":
        base_url = ask("  Base URL", "https://api.openai.com/v1")
        model = ask("  Model name", "gpt-4o")
        key = ask("  API key (press Enter to skip)")
        if not key:
            key = "YOUR_API_KEY_HERE"
        print(f"  Custom ({model})")
        return {"api_mode": "openai", "api_key": key, "base_url": base_url, "model": model, "label": f"Custom ({model})", "max_tokens": "16384"}
    else:
        print("  Defaulting to Gemini (free)")
        key = ask("  Gemini API key (https://aistudio.google.com/apikey)")
        if not key:
            key = DEFAULT_GEMINI_KEY
        return {"api_mode": "openai", "api_key": key,
                "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
                "model": "gemini-2.5-flash", "label": "Gemini (FREE)", "max_tokens": "8192"}

def ask_country_and_school():
    print("\nScegli il paese:")
    print("  1) 🇮🇹 Italia")
    print("  2) 🇺🇸 USA")
    print("  3) 🇫🇷 Francia")
    print("  4) 🇬🇧 Regno Unito")
    print("  5) 🇩🇪 Germania")
    print("  6) 🇪🇸 Spagna")
    print("  7) 🇵🇱 Polonia")
    print("  8) 🇭🇺 Ungheria")
    print("  9) Altro paese")

    country = pick("Scelta [1-9]", ["1","2","3","4","5","6","7","8","9"], "1")

    # ITALIA
    if country == "1":
        print("\nScegli il tipo di scuola:")
        print("  1) Liceo Artistico")
        print("  2) Liceo Classico")
        print("  3) Liceo Scientifico")
        print("  4) Liceo Scienze Umane")
        print("  5) Istituto Tecnico")
        print("  6) Altro")
        c = ask("Scelta [1-6]", "1")
        schools = {
            "1": ("Liceo Artistico", "Maturità",
                  "- **Italiano**: letteratura italiana 800-900, analisi del testo, figure retoriche\n"
                  "- **Storia**: Restaurazione al secondo dopoguerra\n"
                  "- **Filosofia**: Idealismo tedesco a Bergson\n"
                  "- **Fisica**: meccanica, termodinamica, elettromagnetismo, onde\n"
                  "- **Discipline d'indirizzo**: plastiche, pittoriche, grafiche, audiovisive"),
            "2": ("Liceo Classico", "Maturità",
                  "- **Italiano**: letteratura italiana 800-900\n"
                  "- **Latino**: Tacito, Seneca, Virgilio, Orazio, Agostino\n"
                  "- **Storia**: Restaurazione al secondo dopoguerra\n"
                  "- **Matematica**: funzioni, limiti, derivate, integrali"),
            "3": ("Liceo Scientifico", "Maturità",
                  "- **Italiano**: letteratura italiana 800-900\n"
                  "- **Matematica**: funzioni, limiti, derivate, integrali, equazioni differenziali\n"
                  "- **Fisica**: elettrostatica, elettromagnetismo, Maxwell, relatività, quantistica\n"
                  "- **Latino**: Seneca, Tacito, Virgilio, Orazio"),
            "4": ("Liceo delle Scienze Umane", "Maturità",
                  "- **Italiano**: letteratura italiana 800-900\n"
                  "- **Storia**: Restaurazione al secondo dopoguerra\n"
                  "- **Filosofia**: Idealismo tedesco a Bergson\n"
                  "- **Scienze Umane**: pedagogia, psicologia, sociologia, antropologia"),
            "5": ("Istituto Tecnico", "Maturità",
                  "- **Italiano**: letteratura italiana 800-900\n"
                  "- **Storia**: Restaurazione al secondo dopoguerra\n"
                  "- **Materia d'indirizzo**: [specifica tu]"),
        }
        if c in schools:
            school, exam, subjects = schools[c]
        else:
            school = ask("  Tipo di scuola")
            exam = "Maturità"
            subjects = "- **Personalizza**: materie d'esame"
        return "Italia", school, exam, subjects

    # USA
    elif country == "2":
        return ("USA", "High School (12th Grade)", "SAT / AP Exams",
                "- **English**: literary analysis, argumentative writing, AP Lang/Lit\n"
                "- **Mathematics**: Pre-Calculus, AP Calculus AB/BC, AP Statistics\n"
                "- **Science**: Biology, Chemistry, Physics (AP level)\n"
                "- **Social Studies**: AP US History, AP Government, World History\n"
                "- **Foreign Language**: Spanish, French (AP level)")

    # FRANCIA
    elif country == "3":
        print("\nScegli la spécialité:")
        print("  1) Scientifique (Maths + PC/SVT)")
        print("  2) SES + HGGSP")
        print("  3) HLP + LLCER")
        print("  4) Arts")
        print("  5) Altro")
        c = ask("Scelta [1-5]", "1")
        options = {
            "1": ("Bac Général — Voie Scientifique",
                  "- **Philosophie**: dissertation, explication de texte\n"
                  "- **Histoire-Géo**: guerres mondiales, décolonisation, mondialisation\n"
                  "- **Maths**: analyse, probabilités\n"
                  "- **Physique-Chimie**: ondes, mécanique, chimie organique\n"
                  "- **SVT**: génétique, évolution, climat\n"
                  "- **LVA Anglais + LVB**\n- **Grand Oral**"),
            "2": ("Bac Général — SES / HGGSP",
                  "- **Philosophie**\n- **Histoire-Géo**\n"
                  "- **SES**: marchés, croissance, inégalités\n"
                  "- **HGGSP**: puissances, frontières, environnement\n"
                  "- **LVA+LVB**\n- **Grand Oral**"),
            "3": ("Bac Général — HLP / LLCER",
                  "- **Philosophie**\n- **HLP**: parole, représentations, recherche de soi\n"
                  "- **LLCER Anglais**: littérature, cinéma, civilisation\n"
                  "- **Histoire-Géo**\n- **LVA+LVB**\n- **Grand Oral**"),
            "4": ("Bac Général — Arts",
                  "- **Philosophie**\n- **Arts plastiques / Musique / Théâtre**\n"
                  "- **Histoire-Géo**\n- **LVA+LVB**\n- **Grand Oral**"),
        }
        if c in options:
            school, subjects = options[c]
        else:
            school = "Bac Général"
            subjects = "- **Philosophie**, **Histoire-Géo**, **LVA+LVB** + 2 spécialités"
        return "Francia", school, "Baccalauréat", subjects

    # UK
    elif country == "4":
        print("\nScegli il percorso:")
        print("  1) A-Levels — Sciences")
        print("  2) A-Levels — Humanities")
        print("  3) A-Levels — Mixed")
        print("  4) GCSE (Year 11)")
        print("  5) Altro")
        c = ask("Scelta [1-5]", "1")
        options = {
            "1": ("A-Levels — Sciences", "A-Level Exams",
                  "- **Mathematics**: Pure, Statistics, Mechanics\n"
                  "- **Physics**: particles, waves, mechanics, electricity, fields\n"
                  "- **Chemistry**: atomic structure, bonding, organic, spectroscopy\n"
                  "- **Further Maths** (optional)"),
            "2": ("A-Levels — Humanities", "A-Level Exams",
                  "- **English Literature**: Shakespeare, poetry, prose comparison\n"
                  "- **History**: breadth + depth study + coursework\n"
                  "- **Politics**: UK government, US politics, ideologies\n"
                  "- **Economics** (optional)"),
            "3": ("A-Levels — Mixed", "A-Level Exams",
                  "- **Mathematics**: Pure, Statistics, Mechanics\n"
                  "- **Economics**: micro/macro, international trade\n"
                  "- **Psychology**: cognitive, social, biological, research methods"),
            "4": ("GCSE (Year 11)", "GCSE Exams",
                  "- **English Language & Literature**\n"
                  "- **Mathematics**: number, algebra, geometry, statistics\n"
                  "- **Science** (Combined/Triple): biology, chemistry, physics\n"
                  "- **History / Geography**\n- **MFL**: French, Spanish, German"),
        }
        if c in options:
            school, exam, subjects = options[c]
        else:
            school, exam = "A-Levels", "A-Level Exams"
            subjects = "- 3-4 materie a scelta tra Maths, English, Sciences, Humanities"
        return "Regno Unito", school, exam, subjects

    # GERMANIA
    elif country == "5":
        print("\nScegli il profilo:")
        print("  1) Naturwissenschaften (Maths, Physik, Chemie)")
        print("  2) Sprachen (Deutsch, Englisch, Französisch)")
        print("  3) Gesellschaftswissenschaften (Geschichte, Politik)")
        print("  4) Altro")
        c = ask("Scelta [1-4]", "1")
        options = {
            "1": ("Abitur — Naturwissenschaften",
                  "- **Mathematik**: Analysis, Analytische Geometrie, Stochastik\n"
                  "- **Physik**: Mechanik, Elektrodynamik, Quantenphysik\n"
                  "- **Chemie**: organische Chemie, Säure-Base, Redox\n"
                  "- **Biologie**: Genetik, Evolution, Ökologie\n"
                  "- **Deutsch, Englisch** (Grundkurse)"),
            "2": ("Abitur — Sprachen",
                  "- **Deutsch**: Goethe, Kafka, Brecht, Gedichtanalyse\n"
                  "- **Englisch**: Shakespeare, contemporary novels, mediation\n"
                  "- **Französisch / Latein**\n"
                  "- **Geschichte**: Französische Revolution, NS, DDR, EU\n"
                  "- **Mathematik** (Grundkurs)"),
            "3": ("Abitur — Gesellschaftswissenschaften",
                  "- **Geschichte**: Antike bis Europäische Integration\n"
                  "- **Politik/Wirtschaft**: DE System, EU, Globalisierung\n"
                  "- **Erdkunde**: Klimawandel, Bevölkerung\n"
                  "- **Philosophie/Ethik**: Kant, Utilitarismus, Bioethik\n"
                  "- **Deutsch, Englisch, Mathematik** (Grundkurse)"),
        }
        if c in options:
            school, subjects = options[c]
        else:
            school = "Abitur"
            subjects = "- 4-5 Abiturfächer: 2-3 Leistungskurse + 2 Grundkurse"
        return "Germania", school, "Abitur", subjects

    # SPAGNA
    elif country == "6":
        print("\nScegli la modalidad:")
        print("  1) Ciencias")
        print("  2) Humanidades y CCSS")
        print("  3) Artes")
        print("  4) Altro")
        c = ask("Scelta [1-4]", "1")
        options = {
            "1": ("Bachillerato — Ciencias",
                  "- **Lengua Castellana**: comentario, sintaxis, literatura\n"
                  "- **Historia de España**: Prehistoria a democracia\n"
                  "- **Inglés**: reading, writing, speaking\n"
                  "- **Matemáticas II**: análisis, álgebra, geometría, probabilidad\n"
                  "- **Física**: mecánica, electromagnetismo, ondas, cuántica\n"
                  "- **Química**: enlace, termoquímica, ácido-base, orgánica"),
            "2": ("Bachillerato — Humanidades / CCSS",
                  "- **Lengua Castellana, Historia de España, Inglés**\n"
                  "- **Matemáticas Aplicadas**: funciones, derivadas, inferencia\n"
                  "- **Economía de la Empresa**\n- **Geografía**"),
            "3": ("Bachillerato — Artes",
                  "- **Lengua, Historia, Inglés** (troncales)\n"
                  "- **Fundamentos del Arte**\n- **Diseño**\n- **Cultura Audiovisual**"),
        }
        if c in options:
            school, subjects = options[c]
        else:
            school = "Bachillerato"
            subjects = "- Lengua, Historia, Idioma + modalidad"
        return "Spagna", school, "EBAU / Selectividad", subjects

    # POLONIA
    elif country == "7":
        return ("Polonia", "Liceum / Technikum", "Matura",
                "- **Język polski**: analiza tekstów, rozprawka (Mickiewicz, Szymborska, Miłosz)\n"
                "- **Matematyka**: funkcje, ciągi, geometria, prawdopodobieństwo\n"
                "- **Język angielski**: rozumienie, gramatyka, wypracowanie\n"
                "- **Przedmiot dodatkowy** (rozszerzony): biologia, chemia, fizyka, geografia...")

    # UNGHERIA
    elif country == "8":
        return ("Ungheria", "Gimnázium / Szakközépiskola", "Érettségi",
                "- **Magyar nyelv és irodalom**: szövegértés, műelemzés\n"
                "- **Matematika**: halmazok, algebra, függvények, trigonometria\n"
                "- **Történelem**: ókortól a rendszerváltásig\n"
                "- **Angol nyelv**: olvasás, hallás, írás, szóbeli\n"
                "- **Választható tárgy** (emeltszint)")

    # ALTRO
    else:
        c = ask("  Specifica il paese")
        exam = ask("  Nome esame (es. ENEM, Gaokao)", "Esame")
        school = ask("  Tipo di scuola", "Scuola Secondaria")
        subjects = f"- **Personalizza**: materie d'esame per {c}"
        return c, school, exam, subjects

def ask_channel():
    print("\nHow do you want to chat with Study?")
    print("  1) Terminal (hermes chat — fast, text-only, always available)")
    print("  2) Web Dashboard (http://localhost:9119 — full interface)")
    print("  3) Telegram (bot — study on your phone, get reminders)")
    print("  4) Web + Telegram (both)")

    choice = pick("Choice [1-4]", ["1","2","3","4"], "2")

    if choice == "1":
        return "terminal", "", "Terminal", None, None
    elif choice == "2":
        return "web", "", "Dashboard", None, None
    elif choice == "3":
        token = ask("  Telegram bot token (from @BotFather)")
        chat_id = ask("  Authorized chat ID (e.g. 123456789)")
        return "telegram", "  telegram:\n  - hermes-telegram", "Telegram", token, chat_id
    else:
        token = ask("  Telegram bot token (from @BotFather)")
        chat_id = ask("  Authorized chat ID (e.g. 123456789)")
        return "both", "  telegram:\n  - hermes-telegram", "Dashboard + Telegram", token, chat_id

def replace_vars(content, **kwargs):
    for key, val in kwargs.items():
        content = content.replace("{{" + key + "}}", val)
    return content

def generate_profile(vars):
    print("\n→ Creazione profilo Study...")
    # NON usare hermes profile create — copierebbe il config default.
    # Creiamo la directory a mano per isolamento totale.

    # Pulisci memories da installazioni precedenti (evita nomi ereditati)
    old_memories = PROFILE_DIR / "memories"
    if old_memories.exists():
        import shutil
        shutil.rmtree(old_memories)
        print("  Pulite vecchie memories")

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    skills_dir = PROFILE_DIR / "skills" / "education" / "study-tutoring" / "references"
    skills_dir.mkdir(parents=True, exist_ok=True)

    soul = (TEMPLATE_DIR / "SOUL.md").read_text(encoding="utf-8")
    soul = replace_vars(soul, **vars)
    (PROFILE_DIR / "SOUL.md").write_text(soul, encoding="utf-8")

    goal = (TEMPLATE_DIR / "GOAL.md").read_text(encoding="utf-8")
    telegram_section = ""
    if vars.get("TELEGRAM_TOOLSET"):
        telegram_section = "| **Bot Telegram** | Alert e notifiche: reminder sessione, scadenze, planner. |"
    goal = goal.replace("{{TELEGRAM_SECTION}}", telegram_section)
    goal = goal.replace("{{BUS_SECTION}}", "")
    goal = replace_vars(goal, **{k: v for k, v in vars.items() if k != "TELEGRAM_SECTION"})
    (PROFILE_DIR / "GOAL.md").write_text(goal, encoding="utf-8")

    config = (TEMPLATE_DIR / "config.template.yaml").read_text(encoding="utf-8")
    config = replace_vars(config, **vars)
    (PROFILE_DIR / "config.yaml").write_text(config, encoding="utf-8")

    shutil.copy(TEMPLATE_DIR / "skills" / "education" / "study-tutoring" / "SKILL.md",
                PROFILE_DIR / "skills" / "education" / "study-tutoring" / "SKILL.md")
    for ref_file in (TEMPLATE_DIR / "skills" / "education" / "study-tutoring" / "references").glob("*.md"):
        shutil.copy(ref_file, skills_dir / ref_file.name)

    if vars.get("TELEGRAM_BOT_TOKEN"):
        env_path = PROFILE_DIR / ".env"
        with open(env_path, "a", encoding="utf-8") as f:
            f.write(f"\nTELEGRAM_BOT_TOKEN={vars['TELEGRAM_BOT_TOKEN']}\n")
            f.write("GATEWAY_ALLOW_ALL_USERS=true\n")
        print("✓ Token Telegram configurato in .env")

    print(f"✓ Profilo creato in: {PROFILE_DIR}")

def main():
    banner()
    check_prereqs()
    print("\n→ Configuriamo Study per te. 6 domande e sei pronto.\n")

    lang_code, lang_name = ask_language()
    student_name = ask("Come ti chiami?", "Studente")
    country, school_type, exam_name, subjects = ask_country_and_school()

    # Localize examples based on country
    examples = {
        "Italia": ("Leopardi", "trading, cucina, programmazione"),
        "USA": ("The Great Gatsby", "trading, cooking, coding"),
        "Francia": ("Proust", "trading, cuisine, programmation"),
        "Regno Unito": ("Shakespeare", "trading, cooking, coding"),
        "Germania": ("Goethe", "trading, kochen, programmierung"),
        "Spagna": ("Cervantes", "trading, cocina, programación"),
        "Polonia": ("Mickiewicz", "trading, gotowanie, programowanie"),
        "Ungheria": ("Petőfi", "trading, főzés, programozás"),
    }
    connection_example, out_of_scope = examples.get(country, ("the material", "trading, cooking, coding"))
    channel, telegram_toolset, notify_channel, bot_token, chat_id = ask_channel()
    llm = ask_llm()

    print(f"\n→ Riepilogo:")
    print(f"  Nome:      {student_name}")
    print(f"  Paese:     {country}")
    print(f"  Scuola:    {school_type}")
    print(f"  Esame:     {exam_name}")
    print(f"  Canale:    {channel}")
    print(f"  LLM:       {llm['label']}")
    print()

    confirm = ask("Procedo? [S/n]", "S")
    if confirm.lower() == "n":
        print("→ Setup annullato.")
        return

    generate_profile({
        "STUDENT_NAME": student_name,
        "LANGUAGE_CODE": lang_code,
        "LANGUAGE_NAME": lang_name,
        "SCHOOL_TYPE": school_type,
        "EXAM_NAME": exam_name,
        "SUBJECTS_SECTION": subjects,
        "CONNECTION_EXAMPLE": connection_example,
        "OUT_OF_SCOPE_EXAMPLES": out_of_scope,
        "NOTIFY_CHANNEL": notify_channel,
        "TELEGRAM_TOOLSET": telegram_toolset,
        "TELEGRAM_ALLOWED_CHATS": chat_id or "",
        "LLM_API_KEY": llm["api_key"],
        "LLM_API_MODE": llm.get("api_mode", "openai"),
        "LLM_BASE_URL": llm["base_url"],
        "LLM_MODEL": llm["model"],
        "LLM_MAX_TOKENS": llm.get("max_tokens", "8192"),
        "TELEGRAM_BOT_TOKEN": bot_token or "",
    })

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Study is ready!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  To start studying:
    hermes profile use study
""")
    if channel == "terminal":
        print("""  Terminal:
    hermes chat

  (Or launch the web dashboard for a full interface:)
    hermes gateway start
    Open http://localhost:9119 in your browser
""")
    elif channel == "web":
        print("""  Web Dashboard (same interface you're seeing now):
    hermes gateway start
    Open http://localhost:9119 in your browser
""")
    elif channel == "telegram":
        print("""  Telegram: open your bot and start chatting!
  Make sure the gateway is running: hermes gateway start
""")
    else:
        print("""  Web Dashboard:
    hermes gateway start
    Open http://localhost:9119

  Telegram: open your bot and start chatting!
""")
    print(f"""  Try typing: 'I need to prepare for my exam. I have 30 days.'

  Study hard, {student_name}!""")

if __name__ == "__main__":
    main()
