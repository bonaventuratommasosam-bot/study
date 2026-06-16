#!/usr/bin/env python3
"""
Study Open Source — Setup Script (Python)
Crea un profilo Hermes "Study" — funziona su Windows, Mac, Linux.
Docs: https://github.com/hermesbro/study
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

# ── Config ──────────────────────────────────────────────────
TEMPLATE_DIR = Path(__file__).resolve().parent / "profile"
PROFILE_DIR = Path.home() / ".hermes" / "profiles" / "study"

# ── Banner ──────────────────────────────────────────────────
def banner():
    print("""
  ╔══════════════════════════════════════════╗
  ║  📚⚡ Study — Il Tutor Open Source      ║
  ║  Feynman + Montessori + Socrate          ║
  ╚══════════════════════════════════════════╝
""")

# ── Prerequisiti ───────────────────────────────────────────
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

# ── Input helper ───────────────────────────────────────────
def ask(prompt, default=""):
    if default:
        val = input(f"? {prompt} [{default}]: ").strip()
        return val if val else default
    return input(f"? {prompt}: ").strip()

def ask_api_key():
    print("\n→ Serve una API key LLM. Study funziona con DeepSeek (~3-5€/mese).")
    print("  Ottieni la key: https://platform.deepseek.com/api_keys")
    key = ask("DeepSeek API key")
    if not key:
        print("✗ API key obbligatoria. Riavvia lo script quando ce l'hai.")
        sys.exit(1)
    print("✓ API key registrata")
    return key

# ── Scelta scuola ──────────────────────────────────────────
def ask_school_type():
    print("\nScegli il tipo di scuola:")
    print("  1) Liceo Artistico")
    print("  2) Liceo Classico")
    print("  3) Liceo Scientifico")
    print("  4) Liceo delle Scienze Umane")
    print("  5) Istituto Tecnico")
    print("  6) Altro (specifica)")

    choice = ask("Scelta [1-6]", "1")

    syllabi = {
        "1": ("Liceo Artistico", "Maturità",
              "- **Italiano**: letteratura italiana dall'800 al '900, analisi del testo, figure retoriche\n"
              "- **Storia**: dalla Restaurazione al secondo dopoguerra, nessi causa-effetto\n"
              "- **Filosofia**: dall'Idealismo tedesco a Bergson, smontaggio argomentazioni\n"
              "- **Fisica**: meccanica, termodinamica, elettromagnetismo, onde — prima intuizione, poi formule\n"
              "- **Discipline d'indirizzo**: plastiche, pittoriche, grafiche o audiovisive"),

        "2": ("Liceo Classico", "Maturità",
              "- **Italiano**: letteratura italiana dall'800 al '900\n"
              "- **Latino**: Tacito, Seneca, Petronio, Apuleio, Virgilio, Orazio, Agostino\n"
              "- **Storia**: dalla Restaurazione al secondo dopoguerra\n"
              "- **Matematica**: funzioni, limiti, derivate, studio di funzione, integrali"),

        "3": ("Liceo Scientifico", "Maturità",
              "- **Italiano**: letteratura italiana dall'800 al '900\n"
              "- **Matematica**: funzioni, limiti, derivate, studio completo, integrali, equazioni differenziali\n"
              "- **Fisica**: elettrostatica, corrente, elettromagnetismo, Maxwell, relatività, quantistica\n"
              "- **Latino**: Seneca, Tacito, Virgilio, Orazio (programma ridotto)"),

        "4": ("Liceo delle Scienze Umane", "Maturità",
              "- **Italiano**: letteratura italiana dall'800 al '900\n"
              "- **Storia**: dalla Restaurazione al secondo dopoguerra\n"
              "- **Filosofia**: dall'Idealismo tedesco a Bergson\n"
              "- **Scienze Umane**: pedagogia, psicologia, sociologia, antropologia"),

        "5": ("Istituto Tecnico", "Maturità",
              "- **Italiano**: letteratura italiana dall'800 al '900\n"
              "- **Storia**: dalla Restaurazione al secondo dopoguerra\n"
              "- **Materia d'indirizzo**: [specifica tu — economia, informatica, turismo...]"),
    }

    if choice in syllabi:
        school, exam, subjects = syllabi[choice]
    elif choice == "6":
        school = ask("  Tipo di scuola")
        exam = ask("  Nome esame", "Maturità")
        subjects = "- **Personalizza**: inserisci qui le tue materie d'esame"
    else:
        school, exam, subjects = "Altro", "Esame", "- **Personalizza**: materie d'esame"

    print(f"✓ Scuola: {school} | Esame: {exam}")
    return school, exam, subjects

# ── Scelta canale ──────────────────────────────────────────
def ask_channel():
    print("\nScegli il canale:")
    print("  1) CLI / Web (terminale Hermes — nessuna configurazione extra)")
    print("  2) Telegram (bot — devi creare un bot con @BotFather)")
    print("  3) Entrambi")

    choice = ask("Scelta [1-3]", "1")

    if choice == "1":
        return "cli", "", "CLI", None, None
    elif choice == "2":
        token = ask("  Token del bot Telegram (da @BotFather)")
        chat_id = ask("  Chat ID autorizzata (es. 123456789)")
        return "telegram", "  telegram:\n  - hermes-telegram", "Telegram", token, chat_id
    else:
        token = ask("  Token del bot Telegram (da @BotFather)")
        chat_id = ask("  Chat ID autorizzata (es. 123456789)")
        return "both", "  telegram:\n  - hermes-telegram", "Telegram", token, chat_id

# ── Generazione profilo ────────────────────────────────────
def replace_vars(content, **kwargs):
    for key, val in kwargs.items():
        content = content.replace("{{" + key + "}}", val)
    return content

def generate_profile(vars):
    print("\n→ Creazione profilo Study...")

    # Crea profilo Hermes
    subprocess.run(["hermes", "profile", "create", "study"],
                   capture_output=True)

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    skills_dir = PROFILE_DIR / "skills" / "education" / "study-tutoring" / "references"
    skills_dir.mkdir(parents=True, exist_ok=True)

    # SOUL.md
    soul = (TEMPLATE_DIR / "SOUL.md").read_text(encoding="utf-8")
    soul = replace_vars(soul, **vars)
    (PROFILE_DIR / "SOUL.md").write_text(soul, encoding="utf-8")

    # GOAL.md
    goal = (TEMPLATE_DIR / "GOAL.md").read_text(encoding="utf-8")
    telegram_section = ""
    if vars.get("TELEGRAM_TOOLSET"):
        telegram_section = "| **Bot Telegram** | Alert e notifiche: reminder sessione, scadenze, planner. |"
    goal = goal.replace("{{TELEGRAM_SECTION}}", telegram_section)
    goal = goal.replace("{{BUS_SECTION}}", "")
    goal = replace_vars(goal, **{k: v for k, v in vars.items() if k != "TELEGRAM_SECTION"})
    (PROFILE_DIR / "GOAL.md").write_text(goal, encoding="utf-8")

    # Config
    config = (TEMPLATE_DIR / "config.template.yaml").read_text(encoding="utf-8")
    config = replace_vars(config, **vars)
    (PROFILE_DIR / "config.yaml").write_text(config, encoding="utf-8")

    # Skill + references
    shutil.copy(TEMPLATE_DIR / "skills" / "education" / "study-tutoring" / "SKILL.md",
                PROFILE_DIR / "skills" / "education" / "study-tutoring" / "SKILL.md")
    for ref_file in (TEMPLATE_DIR / "skills" / "education" / "study-tutoring" / "references").glob("*.md"):
        shutil.copy(ref_file, skills_dir / ref_file.name)

    # Telegram .env
    if vars.get("TELEGRAM_BOT_TOKEN"):
        env_path = PROFILE_DIR / ".env"
        with open(env_path, "a", encoding="utf-8") as f:
            f.write(f"\nTELEGRAM_BOT_TOKEN={vars['TELEGRAM_BOT_TOKEN']}\n")
            f.write("GATEWAY_ALLOW_ALL_USERS=true\n")
        print("✓ Token Telegram configurato in .env")

    print(f"✓ Profilo creato in: {PROFILE_DIR}")

# ── Main ────────────────────────────────────────────────────
def main():
    banner()
    check_prereqs()

    print("\n→ Configuriamo Study per te. 6 domande e sei pronto.\n")

    student_name = ask("Come ti chiami?", "Studente")
    school_type, exam_name, subjects = ask_school_type()
    channel, telegram_toolset, notify_channel, bot_token, chat_id = ask_channel()
    api_key = ask_api_key()

    print(f"\n→ Riepilogo:")
    print(f"  Nome:      {student_name}")
    print(f"  Scuola:    {school_type}")
    print(f"  Esame:     {exam_name}")
    print(f"  Canale:    {channel}")
    print()

    confirm = ask("Procedo? [S/n]", "S")
    if confirm.lower() == "n":
        print("→ Setup annullato. Riesegui quando vuoi.")
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
        "DEEPSEEK_API_KEY": api_key,
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
