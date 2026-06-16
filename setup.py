#!/usr/bin/env python3
"""
Study Open Source — Setup Script (Python)
Crea un profilo Hermes "Study" — funziona su Windows, Mac, Linux.
Docs: https://github.com/bonaventuratommasosam-bot/study
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent / "profile"
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
    try:
        subprocess.run(["hermes", "--version"], capture_output=True, check=True)
        print("✓ Hermes Agent trovato")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Hermes Agent non trovato.")
        print("  Installa: https://hermes-agent.nousresearch.com/docs")
        sys.exit(1)
    print("✓ Python OK")

def ask(prompt, default=""):
    if default:
        val = input(f"? {prompt} [{default}]: ").strip()
        return val if val else default
    return input(f"? {prompt}: ").strip()

def ask_llm():
    print("\nScegli il provider LLM:")
    print("  1) 🆓  Groq — GRATUITO (Llama 3.3 70B, nessun costo, key gratis)")
    print("  2) 💰  DeepSeek — economico (~3-5€/mese, miglior rapporto qualità/prezzo)")
    print("  3) 🔧  Custom — scegli tu provider e modello")
    choice = ask("Scelta [1-3]", "2")

    if choice == "1":
        print("  Ottieni la API key gratuita: https://console.groq.com/keys")
        key = ask("Groq API key")
        if not key:
            print("✗ API key obbligatoria.")
            sys.exit(1)
        print("✓ Groq (FREE) — Llama 3.3 70B")
        return {"api_key": key, "base_url": "https://api.groq.com/openai/v1",
                "model": "llama-3.3-70b-versatile", "label": "Groq (FREE)"}
    elif choice == "2":
        print("  Ottieni la API key: https://platform.deepseek.com/api_keys")
        key = ask("DeepSeek API key")
        if not key:
            print("✗ API key obbligatoria.")
            sys.exit(1)
        print("✓ DeepSeek (€3-5/mese)")
        return {"api_key": key, "base_url": "https://api.deepseek.com/v1",
                "model": "deepseek-chat", "label": "DeepSeek"}
    else:
        base_url = ask("  Base URL", "https://api.openai.com/v1")
        model = ask("  Modello", "gpt-4o")
        key = ask("  API key")
        if not key:
            print("✗ API key obbligatoria.")
            sys.exit(1)
        print(f"✓ Custom — {model}")
        return {"api_key": key, "base_url": base_url, "model": model, "label": f"Custom ({model})"}

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

    country = ask("Scelta [1-9]", "1")

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
    print("\nScegli il canale:")
    print("  1) CLI / Web (terminale Hermes)")
    print("  2) Telegram (bot — @BotFather)")
    print("  3) Entrambi")
    choice = ask("Scelta [1-3]", "1")
    if choice == "1":
        return "cli", "", "CLI", None, None
    elif choice == "2":
        token = ask("  Token del bot Telegram")
        chat_id = ask("  Chat ID autorizzata")
        return "telegram", "  telegram:\n  - hermes-telegram", "Telegram", token, chat_id
    else:
        token = ask("  Token del bot Telegram")
        chat_id = ask("  Chat ID autorizzata")
        return "both", "  telegram:\n  - hermes-telegram", "Telegram", token, chat_id

def replace_vars(content, **kwargs):
    for key, val in kwargs.items():
        content = content.replace("{{" + key + "}}", val)
    return content

def generate_profile(vars):
    print("\n→ Creazione profilo Study...")
    subprocess.run(["hermes", "profile", "create", "study"], capture_output=True)
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

    student_name = ask("Come ti chiami?", "Studente")
    country, school_type, exam_name, subjects = ask_country_and_school()
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
        "SCHOOL_TYPE": school_type,
        "EXAM_NAME": exam_name,
        "SUBJECTS_SECTION": subjects,
        "CONNECTION_EXAMPLE": "Leopardi",
        "OUT_OF_SCOPE_EXAMPLES": "trading, cucina, programmazione",
        "NOTIFY_CHANNEL": notify_channel,
        "TELEGRAM_TOOLSET": telegram_toolset,
        "TELEGRAM_ALLOWED_CHATS": chat_id or "",
        "LLM_API_KEY": llm["api_key"],
        "LLM_BASE_URL": llm["base_url"],
        "LLM_MODEL": llm["model"],
        "TELEGRAM_BOT_TOKEN": bot_token or "",
    })

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎉 Study è vivo!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Per iniziare a studiare:
    hermes profile use study
    hermes chat

  Prova con: 'Ciao Study, aiutami a preparare l'esame'
""")
    if bot_token:
        print("""  Su Telegram: apri il tuo bot e scrivigli!
  (Assicurati che il gateway sia attivo: hermes gateway start)
""")
    print(f"  📚⚡ Buono studio, {student_name}!")

if __name__ == "__main__":
    main()
