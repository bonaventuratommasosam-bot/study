#!/usr/bin/env bash
# ============================================================
#  Study Open Source — Setup Script
#  Crea un profilo Hermes "Study" in 2 minuti
#  Docs: https://github.com/hermesbro/study
# ============================================================
set -euo pipefail

# ── Colori ─────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; NC='\033[0m'

banner() {
    echo -e "${BLUE}"
    echo "  ╔══════════════════════════════════════════╗"
    echo "  ║  📚⚡ Study — Il Tutor Open Source      ║"
    echo "  ║  Feynman + Montessori + Socrate          ║"
    echo "  ╚══════════════════════════════════════════╝"
    echo -e "${NC}"
}

info()  { echo -e "${BLUE}→${NC} $1"; }
ok()    { echo -e "${GREEN}✓${NC} $1"; }
warn()  { echo -e "${YELLOW}⚠${NC} $1"; }
err()   { echo -e "${RED}✗${NC} $1"; }

# ── Prerequisiti ───────────────────────────────────────────
check_prereqs() {
    info "Verifica prerequisiti..."

    if ! command -v hermes &>/dev/null; then
        err "Hermes Agent non trovato."
        echo "  Installa Hermes: https://hermes-agent.nousresearch.com/docs"
        echo "  Poi riesegui questo script."
        exit 1
    fi
    ok "Hermes Agent trovato: $(hermes --version 2>/dev/null || echo 'OK')"

    if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
        err "Python 3 non trovato. Serve per alcune funzionalità."
        exit 1
    fi
    ok "Python trovato"
}

# ── Domande interattive ────────────────────────────────────
ask() {
    local prompt="$1" default="$2"
    local var_name="$3"
    read -r -p "$(echo -e "${BLUE}?${NC} ${prompt} [${default}]: ")" input
    input="${input:-$default}"
    declare -g "$var_name=$input"
}

ask_school_type() {
    echo ""
    echo -e "${BOLD}Scegli il tipo di scuola:${NC}"
    echo "  1) Liceo Artistico"
    echo "  2) Liceo Classico"
    echo "  3) Liceo Scientifico"
    echo "  4) Liceo delle Scienze Umane"
    echo "  5) Istituto Tecnico"
    echo "  6) Altro (specifica)"
    read -r -p "$(echo -e "${BLUE}?${NC} Scelta [1-6]: ")" choice

    case "$choice" in
        1) SCHOOL_TYPE="Liceo Artistico"
           SUBJECTS_SECTION=$(cat << 'EOF'
- **Italiano**: letteratura italiana dall'800 al '900, analisi del testo, figure retoriche, collegamenti con storia dell'arte e filosofia
- **Storia**: dalla Restaurazione al secondo dopoguerra, nessi causa-effetto, analisi delle fonti
- **Filosofia**: dall'Idealismo tedesco a Bergson, smontaggio delle argomentazioni, collegamenti con letteratura e scienza
- **Fisica**: meccanica, termodinamica, elettromagnetismo, onde. Approccio intuitivo prima delle formule
- **Discipline d'indirizzo**: plastiche, pittoriche, grafiche o audiovisive — la materia che dà il tono al colloquio
EOF
)
           EXAM_NAME="Maturità"
           ;;
        2) SCHOOL_TYPE="Liceo Classico"
           SUBJECTS_SECTION=$(cat << 'EOF'
- **Italiano**: letteratura italiana dall'800 al '900, analisi del testo poetico e prosastico
- **Latino**: storiografia imperiale, Seneca, romanzo e satira, poesia epica e lirica, cristianesimo
- **Storia**: dalla Restaurazione al secondo dopoguerra
- **Matematica**: funzioni, limiti, derivate, studio di funzione, integrali
EOF
)
           EXAM_NAME="Maturità"
           ;;
        3) SCHOOL_TYPE="Liceo Scientifico"
           SUBJECTS_SECTION=$(cat << 'EOF'
- **Italiano**: letteratura italiana dall'800 al '900
- **Matematica**: funzioni, limiti, derivate, studio completo di funzione, integrali, equazioni differenziali
- **Fisica**: elettrostatica, corrente, elettromagnetismo, equazioni di Maxwell, relatività ristretta, fisica quantistica
- **Latino**: Seneca, Tacito, Virgilio, Orazio (programma ridotto)
EOF
)
           EXAM_NAME="Maturità"
           ;;
        4) SCHOOL_TYPE="Liceo delle Scienze Umane"
           SUBJECTS_SECTION=$(cat << 'EOF'
- **Italiano**: letteratura italiana dall'800 al '900
- **Storia**: dalla Restaurazione al secondo dopoguerra
- **Filosofia**: dall'Idealismo tedesco a Bergson
- **Scienze Umane**: pedagogia (Rousseau, Montessori, Dewey), psicologia (Piaget, Vygotskij, Freud), sociologia (Durkheim, Weber, Bourdieu), antropologia (Boas, Malinowski, Lévi-Strauss)
EOF
)
           EXAM_NAME="Maturità"
           ;;
        5) SCHOOL_TYPE="Istituto Tecnico"
           SUBJECTS_SECTION=$(cat << 'EOF'
- **Italiano**: letteratura italiana dall'800 al '900
- **Storia**: dalla Restaurazione al secondo dopoguerra
- **Materia d'indirizzo**: [specifica tu — economia, informatica, turismo, etc.]
EOF
)
           EXAM_NAME="Maturità"
           ;;
        6) read -r -p "  Specifica il tipo di scuola: " SCHOOL_TYPE
           read -r -p "  Nome dell'esame (es. Maturità, Terza Media): " EXAM_NAME
           SUBJECTS_SECTION="- **Personalizza**: inserisci qui le tue materie d'esame"
           ;;
        *) warn "Scelta non valida, uso 'Altro'"
           SCHOOL_TYPE="Altro"
           EXAM_NAME="Esame"
           SUBJECTS_SECTION="- **Personalizza**: inserisci qui le tue materie"
           ;;
    esac
    ok "Scuola: ${SCHOOL_TYPE} | Esame: ${EXAM_NAME}"
}

ask_channel() {
    echo ""
    echo -e "${BOLD}Scegli il canale:${NC}"
    echo "  1) CLI / Web (terminale Hermes — nessuna configurazione extra)"
    echo "  2) Telegram (bot — devi creare un bot con @BotFather)"
    echo "  3) Entrambi"
    read -r -p "$(echo -e "${BLUE}?${NC} Scelta [1-3]: ")" choice

    case "$choice" in
        1) CHANNEL="cli"
           TELEGRAM_TOOLSET=""
           NOTIFY_CHANNEL="CLI"
           ;;
        2) CHANNEL="telegram"
           TELEGRAM_TOOLSET="  telegram:\n  - hermes-telegram"
           NOTIFY_CHANNEL="Telegram"
           read -r -p "  Token del bot Telegram (da @BotFather): " TELEGRAM_BOT_TOKEN
           read -r -p "  Chat ID autorizzata (es. 123456789): " TELEGRAM_ALLOWED_CHATS
           ;;
        3) CHANNEL="both"
           TELEGRAM_TOOLSET="  telegram:\n  - hermes-telegram"
           NOTIFY_CHANNEL="Telegram"
           read -r -p "  Token del bot Telegram (da @BotFather): " TELEGRAM_BOT_TOKEN
           read -r -p "  Chat ID autorizzata (es. 123456789): " TELEGRAM_ALLOWED_CHATS
           ;;
        *) CHANNEL="cli"
           TELEGRAM_TOOLSET=""
           NOTIFY_CHANNEL="CLI"
           ;;
    esac
    ok "Canale: ${CHANNEL}"
}

ask_api_key() {
    echo ""
    info "Serve una API key LLM. Study funziona con DeepSeek (economico, ~3-5€/mese)."
    echo "  Ottieni la key: https://platform.deepseek.com/api_keys"
    read -r -s -p "$(echo -e "${BLUE}?${NC} DeepSeek API key (input nascosto): ")" DEEPSEEK_API_KEY
    echo ""
    if [ -z "$DEEPSEEK_API_KEY" ]; then
        err "API key obbligatoria. Riavvia lo script quando ce l'hai."
        exit 1
    fi
    ok "API key registrata"
}

# ── Generazione profilo ────────────────────────────────────
generate_profile() {
    local PROFILE_DIR
    PROFILE_DIR="$HOME/.hermes/profiles/study"
    local TEMPLATE_DIR
    TEMPLATE_DIR="$(dirname "$0")/profile"

    info "Creazione profilo Study..."

    # Crea il profilo Hermes
    hermes profile create study 2>/dev/null || warn "Il profilo 'study' esiste già — lo aggiorno"

    # Assicurati che la directory esista
    mkdir -p "$PROFILE_DIR/skills/education/study-tutoring/references"

    # Funzione per sostituire variabili in un file
    replace_vars() {
        local infile="$1" outfile="$2"
        sed \
            -e "s|{{STUDENT_NAME}}|${STUDENT_NAME}|g" \
            -e "s|{{SCHOOL_TYPE}}|${SCHOOL_TYPE}|g" \
            -e "s|{{EXAM_NAME}}|${EXAM_NAME}|g" \
            -e "s|{{CONNECTION_EXAMPLE}}|Leopardi|g" \
            -e "s|{{OUT_OF_SCOPE_EXAMPLES}}|trading, cucina, programmazione|g" \
            -e "s|{{NOTIFY_CHANNEL}}|${NOTIFY_CHANNEL}|g" \
            "$infile" > "$outfile"
    }

    # SOUL.md
    replace_vars "$TEMPLATE_DIR/SOUL.md" "$PROFILE_DIR/SOUL.md"
    # Inietta SUBJECTS_SECTION
    sed -i "s|{{SUBJECTS_SECTION}}|${SUBJECTS_SECTION}|" "$PROFILE_DIR/SOUL.md"

    # GOAL.md
    local telegram_section=""
    local bus_section=""
    if [ "$CHANNEL" = "telegram" ] || [ "$CHANNEL" = "both" ]; then
        telegram_section="| **Bot Telegram** | Alert e notifiche: reminder sessione, scadenze, planner. |"
    fi
    replace_vars "$TEMPLATE_DIR/GOAL.md" "$PROFILE_DIR/GOAL.md"
    sed -i "s|{{TELEGRAM_SECTION}}|${telegram_section}|" "$PROFILE_DIR/GOAL.md"
    sed -i "s|{{BUS_SECTION}}||" "$PROFILE_DIR/GOAL.md"

    # Config
    replace_vars "$TEMPLATE_DIR/config.template.yaml" "$PROFILE_DIR/config.yaml"
    sed -i "s|{{DEEPSEEK_API_KEY}}|${DEEPSEEK_API_KEY}|" "$PROFILE_DIR/config.yaml"
    sed -i "s|{{TELEGRAM_TOOLSET}}|${TELEGRAM_TOOLSET}|" "$PROFILE_DIR/config.yaml"
    sed -i "s|{{TELEGRAM_ALLOWED_CHATS}}|${TELEGRAM_ALLOWED_CHATS:-}|" "$PROFILE_DIR/config.yaml"

    # Skill
    cp "$TEMPLATE_DIR/skills/education/study-tutoring/SKILL.md" \
       "$PROFILE_DIR/skills/education/study-tutoring/SKILL.md"
    cp "$TEMPLATE_DIR/skills/education/study-tutoring/references/"*.md \
       "$PROFILE_DIR/skills/education/study-tutoring/references/"

    # Telegram bot token nel .env se serve
    if [ "$CHANNEL" = "telegram" ] || [ "$CHANNEL" = "both" ]; then
        cat >> "$PROFILE_DIR/.env" << EOF
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
GATEWAY_ALLOW_ALL_USERS=true
EOF
        ok "Token Telegram configurato in .env"
    fi

    ok "Profilo creato in: $PROFILE_DIR"
}

# ── Main ────────────────────────────────────────────────────
main() {
    banner

    check_prereqs

    echo ""
    info "Configuriamo Study per te. 6 domande e sei pronto."
    echo ""

    ask "Come ti chiami?" "Studente" STUDENT_NAME
    ask_school_type
    ask_channel

    # Variabili derivate
    CONNECTION_EXAMPLE="Leopardi"
    OUT_OF_SCOPE_EXAMPLES="trading, cucina, programmazione"

    ask_api_key

    echo ""
    info "Riepilogo:"
    echo "  Nome:      ${STUDENT_NAME}"
    echo "  Scuola:    ${SCHOOL_TYPE}"
    echo "  Esame:     ${EXAM_NAME}"
    echo "  Canale:    ${CHANNEL}"
    echo ""

    read -r -p "$(echo -e "${BLUE}?${NC} Procedo? [S/n]: ")" confirm
    if [ "$confirm" = "n" ] || [ "$confirm" = "N" ]; then
        info "Setup annullato. Riesegui quando vuoi."
        exit 0
    fi

    generate_profile

    echo ""
    echo -e "${GREEN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}${BOLD}  🎉 Study è vivo!${NC}"
    echo -e "${GREEN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "  Per iniziare a studiare:"
    echo "    hermes profile use study"
    echo "    hermes chat"
    echo ""
    echo "  Prova con: 'Ciao Study, aiutami a preparare l'esame'"
    echo ""
    if [ "$CHANNEL" = "telegram" ] || [ "$CHANNEL" = "both" ]; then
        echo "  Su Telegram: apri il tuo bot e scrivigli!"
        echo "  (Assicurati che il gateway sia attivo: hermes gateway start)"
        echo ""
    fi
    echo -e "  📚⚡ Buono studio, ${STUDENT_NAME}!"
}

main
