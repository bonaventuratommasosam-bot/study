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

ask_country_and_school() {
    echo ""
    echo -e "${BOLD}Scegli il paese:${NC}"
    echo "  1) 🇮🇹 Italia"
    echo "  2) 🇺🇸 USA"
    echo "  3) 🇫🇷 Francia"
    echo "  4) 🇬🇧 Regno Unito"
    echo "  5) 🇩🇪 Germania"
    echo "  6) 🇪🇸 Spagna"
    echo "  7) 🇵🇱 Polonia"
    echo "  8) 🇭🇺 Ungheria"
    echo "  9) Altro paese"
    read -r -p "$(echo -e "${BLUE}?${NC} Scelta [1-9]: ")" country

    case "$country" in
        # ── ITALIA ──
        1) COUNTRY="Italia"
           echo ""
           echo -e "${BOLD}Scegli il tipo di scuola:${NC}"
           echo "  1) Liceo Artistico"
           echo "  2) Liceo Classico"
           echo "  3) Liceo Scientifico"
           echo "  4) Liceo Scienze Umane"
           echo "  5) Istituto Tecnico"
           echo "  6) Altro"
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
                  EXAM_NAME="Maturità";;
               2) SCHOOL_TYPE="Liceo Classico"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Italiano**: letteratura italiana dall'800 al '900, analisi del testo poetico e prosastico
- **Latino**: storiografia imperiale, Seneca, romanzo e satira, poesia epica e lirica, cristianesimo
- **Storia**: dalla Restaurazione al secondo dopoguerra
- **Matematica**: funzioni, limiti, derivate, studio di funzione, integrali
EOF
)
                  EXAM_NAME="Maturità";;
               3) SCHOOL_TYPE="Liceo Scientifico"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Italiano**: letteratura italiana dall'800 al '900
- **Matematica**: funzioni, limiti, derivate, studio completo di funzione, integrali, equazioni differenziali
- **Fisica**: elettrostatica, corrente, elettromagnetismo, equazioni di Maxwell, relatività ristretta, fisica quantistica
- **Latino**: Seneca, Tacito, Virgilio, Orazio (programma ridotto)
EOF
)
                  EXAM_NAME="Maturità";;
               4) SCHOOL_TYPE="Liceo delle Scienze Umane"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Italiano**: letteratura italiana dall'800 al '900
- **Storia**: dalla Restaurazione al secondo dopoguerra
- **Filosofia**: dall'Idealismo tedesco a Bergson
- **Scienze Umane**: pedagogia (Rousseau, Montessori, Dewey), psicologia (Piaget, Vygotskij, Freud), sociologia (Durkheim, Weber, Bourdieu), antropologia (Boas, Malinowski, Lévi-Strauss)
EOF
)
                  EXAM_NAME="Maturità";;
               5) SCHOOL_TYPE="Istituto Tecnico"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Italiano**: letteratura italiana dall'800 al '900
- **Storia**: dalla Restaurazione al secondo dopoguerra
- **Materia d'indirizzo**: [specifica tu — economia, informatica, turismo, etc.]
EOF
)
                  EXAM_NAME="Maturità";;
               6|*) read -r -p "  Specifica il tipo di scuola: " SCHOOL_TYPE
                  EXAM_NAME="Maturità"
                  SUBJECTS_SECTION="- **Personalizza**: inserisci qui le tue materie d'esame";;
           esac
           ;;

        # ── USA ──
        2) COUNTRY="USA"
           echo ""
           echo -e "${BOLD}Scegli il percorso:${NC}"
           echo "  1) SAT + AP (standard college prep)"
           echo "  2) ACT + AP"
           echo "  3) Solo AP Exams"
           echo "  4) Altro"
           read -r -p "$(echo -e "${BLUE}?${NC} Scelta [1-4]: ")" choice
           SCHOOL_TYPE="High School (12th Grade)"
           EXAM_NAME="SAT / AP Exams"
           SUBJECTS_SECTION=$(cat << 'EOF'
- **English**: literary analysis, rhetorical analysis, argumentative writing (SAT essay, AP Lang/Lit)
- **Mathematics**: Pre-Calculus, Calculus (AP Calc AB/BC), Statistics (AP Stats)
- **Science**: Biology, Chemistry, Physics (AP level available)
- **Social Studies**: US History (APUSH), Government (AP Gov), World History
- **Foreign Language**: Spanish, French (AP level available)
EOF
)
           ;;

        # ── FRANCIA ──
        3) COUNTRY="Francia"
           echo ""
           echo -e "${BOLD}Scegli la série / spécialités:${NC}"
           echo "  1) Bac Général — spécialités scientifiques (Maths + PC/SVT)"
           echo "  2) Bac Général — spécialités SES + HGGSP"
           echo "  3) Bac Général — spécialités HLP + LLCER"
           echo "  4) Bac Général — spécialités Arts"
           echo "  5) Altro"
           read -r -p "$(echo -e "${BLUE}?${NC} Scelta [1-5]: ")" choice
           case "$choice" in
               1) SCHOOL_TYPE="Bac Général — Voie Scientifique"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Philosophie**: dissertation, explication de texte — le sujet, la conscience, le désir, la liberté, le bonheur, la justice
- **Histoire-Géographie**: guerres mondiales, totalitarismes, décolonisation, guerre froide, mondialisation
- **Mathématiques**: analyse (suites, fonctions, dérivées, intégrales, exponentielles, logarithmes), probabilités
- **Physique-Chimie**: ondes, mécanique, thermodynamique, chimie organique, énergie
- **SVT**: génétique, évolution, écosystèmes, corps humain, climat
- **LVA Anglais + LVB**: compréhension et expression écrite/orale
- **Grand Oral**: 20 min sur un projet lié aux spécialités
EOF
);;
               2) SCHOOL_TYPE="Bac Général — SES / HGGSP"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Philosophie**: dissertation, explication de texte
- **Histoire-Géographie**: comme ci-dessus
- **SES (Sciences Économiques et Sociales)**: marchés, croissance, inégalités, mondialisation, sociologie
- **HGGSP**: puissances internationales, frontières, guerres et paix, environnement
- **Mathématiques** (tronc commun): statistiques, probabilités, pourcentages
- **LVA Anglais + LVB**
- **Grand Oral**
EOF
);;
               3) SCHOOL_TYPE="Bac Général — HLP / LLCER"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Philosophie**: dissertation, explication de texte
- **HLP (Humanités, Littérature, Philosophie)**: pouvoirs de la parole, représentations du monde, recherche de soi
- **LLCER Anglais**: littérature, cinéma, civilisation anglophone
- **Histoire-Géographie**
- **LVA Anglais + LVB**
- **Grand Oral**
EOF
);;
               4) SCHOOL_TYPE="Bac Général — Arts"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Philosophie**: dissertation, explication de texte
- **Arts plastiques / Musique / Théâtre / Cinéma**: pratique et culture artistiques
- **Histoire-Géographie**
- **LVA Anglais + LVB**
- **Grand Oral**
EOF
);;
               *) SCHOOL_TYPE="Bac Général"
                  SUBJECTS_SECTION="- **Philosophie**, **Histoire-Géo**, **LVA+LVB**, **Enseignement Scientifique** + 2 spécialités au choix";;
           esac
           EXAM_NAME="Baccalauréat"
           ;;

        # ── UK ──
        4) COUNTRY="Regno Unito"
           echo ""
           echo -e "${BOLD}Scegli il percorso:${NC}"
           echo "  1) A-Levels — Sciences (Maths, Physics, Chemistry)"
           echo "  2) A-Levels — Humanities (English, History, Politics)"
           echo "  3) A-Levels — Mixed (Maths, Economics, Psychology)"
           echo "  4) GCSE (Year 11)"
           echo "  5) Altro"
           read -r -p "$(echo -e "${BLUE}?${NC} Scelta [1-5]: ")" choice
           case "$choice" in
               1) SCHOOL_TYPE="A-Levels — Sciences"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Mathematics**: Pure (algebra, functions, calculus, trigonometry), Statistics, Mechanics
- **Physics**: particles, waves, mechanics, electricity, fields, nuclear, astrophysics (optional)
- **Chemistry**: atomic structure, bonding, energetics, kinetics, equilibria, organic chemistry, spectroscopy
- **Further Maths** (optional): complex numbers, matrices, further calculus
EOF
);;
               2) SCHOOL_TYPE="A-Levels — Humanities"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **English Literature**: Shakespeare, poetry pre/post-1900, prose comparison, unseen analysis
- **History**: breadth study (Tudors/Russia) + depth study (French Revolution/Civil Rights) + coursework
- **Politics**: UK government, US politics, political ideologies
- **Economics** (optional): micro/macro, markets, policy
EOF
);;
               3) SCHOOL_TYPE="A-Levels — Mixed"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Mathematics**: Pure, Statistics, Mechanics
- **Economics**: microeconomics, macroeconomics, international trade
- **Psychology**: cognitive, social, biological, developmental, research methods
EOF
);;
               4) SCHOOL_TYPE="GCSE (Year 11)"
                  EXAM_NAME="GCSE Exams"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **English Language & Literature**: creative writing, Shakespeare, poetry, modern texts
- **Mathematics**: number, algebra, geometry, statistics, probability
- **Science** (Combined or Triple): biology, chemistry, physics
- **History / Geography**: one required
- **Modern Foreign Language**: French, Spanish, German
EOF
);;
               *) SCHOOL_TYPE="A-Levels"
                  EXAM_NAME="A-Level Exams"
                  SUBJECTS_SECTION="- Scegli 3-4 materie tra: Maths, Further Maths, English Lit, Biology, Chemistry, Physics, History, Geography, Economics, Psychology, etc.";;
           esac
           [ -z "$EXAM_NAME" ] && EXAM_NAME="A-Level Exams"
           ;;

        # ── GERMANIA ──
        5) COUNTRY="Germania"
           echo ""
           echo -e "${BOLD}Scegli il profilo:${NC}"
           echo "  1) Abitur — Naturwissenschaften (Maths, Physik, Chemie)"
           echo "  2) Abitur — Sprachen (Deutsch, Englisch, Französisch)"
           echo "  3) Abitur — Gesellschaftswissenschaften (Geschichte, Politik, Erdkunde)"
           echo "  4) Altro"
           read -r -p "$(echo -e "${BLUE}?${NC} Scelta [1-4]: ")" choice
           case "$choice" in
               1) SCHOOL_TYPE="Abitur — Naturwissenschaften"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Mathematik**: Analysis, Analytische Geometrie, Stochastik
- **Physik**: Mechanik, Elektrodynamik, Quantenphysik, Kernphysik
- **Chemie**: organische Chemie, Säure-Base, Redox, Kunststoffe
- **Biologie**: Genetik, Evolution, Ökologie, Neurobiologie
- **Deutsch**: Literatur (Goethe, Kafka, Brecht), Sachtexte, Erörterung
- **Englisch**: literature, Shakespeare, mediation, global issues
EOF
);;
               2) SCHOOL_TYPE="Abitur — Sprachen"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Deutsch**: Literatur (Aufklärung bis Moderne), Gedichtanalyse, Dramenanalyse, Erörterung
- **Englisch**: literature, Shakespeare, contemporary novels, mediation
- **Französisch / Latein**: Literatur, Übersetzung, Kultur
- **Geschichte**: Französische Revolution, Nationalsozialismus, DDR, EU
- **Mathematik** (Grundkurs): Analysis, Stochastik
EOF
);;
               3) SCHOOL_TYPE="Abitur — Gesellschaftswissenschaften"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Geschichte**: Antike bis Europäische Integration
- **Politik/Wirtschaft**: politisches System DE, EU, Globalisierung
- **Erdkunde**: Klimawandel, Bevölkerung, Ressourcen
- **Philosophie/Ethik**: Kant, Utilitarismus, Arendt, Bioethik
- **Deutsch, Englisch, Mathematik** (Grundkurse)
EOF
);;
               *) SCHOOL_TYPE="Abitur"
                  SUBJECTS_SECTION="- 4-5 Abiturfächer: 2-3 Leistungskurse + 2 Grundkurse. Deckt Sprachen, Naturwissenschaften, Gesellschaftswissenschaften ab.";;
           esac
           EXAM_NAME="Abitur"
           ;;

        # ── SPAGNA ──
        6) COUNTRY="Spagna"
           echo ""
           echo -e "${BOLD}Scegli la modalidad:${NC}"
           echo "  1) Ciencias (Matemáticas II, Física, Química)"
           echo "  2) Humanidades y CCSS (Latín, Economía, Geografía)"
           echo "  3) Artes"
           echo "  4) Altro"
           read -r -p "$(echo -e "${BLUE}?${NC} Scelta [1-4]: ")" choice
           case "$choice" in
               1) SCHOOL_TYPE="Bachillerato — Ciencias"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Lengua Castellana**: comentario de texto, sintaxis, literatura española e hispanoamericana
- **Historia de España**: desde la Prehistoria hasta la democracia actual
- **Inglés**: reading, writing, listening, speaking
- **Matemáticas II**: análisis, álgebra lineal, geometría, probabilidad
- **Física**: mecánica, electromagnetismo, ondas, óptica, física cuántica
- **Química**: enlace, termoquímica, ácido-base, redox, orgánica
EOF
);;
               2) SCHOOL_TYPE="Bachillerato — Humanidades / CCSS"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Lengua Castellana**: comentario de texto, sintaxis, literatura
- **Historia de España**: completa
- **Inglés**: reading, writing, listening, speaking
- **Matemáticas Aplicadas a las CCSS**: funciones, derivadas, probabilidad, inferencia estadística
- **Economía de la Empresa**: gestión, marketing, finanzas
- **Geografía**: España, Europa, globalización
EOF
);;
               3) SCHOOL_TYPE="Bachillerato — Artes"
                  SUBJECTS_SECTION=$(cat << 'EOF'
- **Lengua Castellana, Historia de España, Inglés** (troncales)
- **Fundamentos del Arte**: historia, teoría, análisis
- **Diseño**: gráfico, producto, interiores
- **Cultura Audiovisual**: cine, fotografía, medios
EOF
);;
               *) SCHOOL_TYPE="Bachillerato"
                  SUBJECTS_SECTION="- Lengua, Historia, Idioma + modalidad (Ciencias/Humanidades/Artes)";;
           esac
           EXAM_NAME="EBAU / Selectividad"
           ;;

        # ── POLONIA ──
        7) COUNTRY="Polonia"
           SCHOOL_TYPE="Liceum / Technikum"
           EXAM_NAME="Matura"
           SUBJECTS_SECTION=$(cat << 'EOF'
- **Język polski**: analiza tekstów literackich, rozprawka — od antyku do współczesności (Mickiewicz, Szymborska, Herbert, Miłosz)
- **Matematyka**: funkcje, ciągi, geometria, kombinatoryka, rachunek prawdopodobieństwa
- **Język angielski**: rozumienie tekstu, gramatyka, wypracowanie
- **Przedmiot dodatkowy** (rozszerzony): biologia, chemia, fizyka, geografia, historia, WOS, informatyka
EOF
)
           ;;

        # ── UNGHERIA ──
        8) COUNTRY="Ungheria"
           SCHOOL_TYPE="Gimnázium / Szakközépiskola"
           EXAM_NAME="Érettségi"
           SUBJECTS_SECTION=$(cat << 'EOF'
- **Magyar nyelv és irodalom**: szövegértés, műelemzés — Petőfi, Arany, Ady, Babits, Kosztolányi, József Attila, Radnóti
- **Matematika**: halmazok, algebra, függvények, trigonometria, valószínűségszámítás
- **Történelem**: ókortól a rendszerváltásig és az EU-ig
- **Angol nyelv**: olvasás, hallás, írás, szóbeli
- **Választható tárgy** (emeltszint): biológia, kémia, fizika, földrajz, informatika
EOF
)
           ;;

        # ── ALTRO ──
        9) COUNTRY="Altro"
           read -r -p "  Specifica il paese: " COUNTRY
           read -r -p "  Nome dell'esame (es. ENEM, Gaokao, Suneung): " EXAM_NAME
           read -r -p "  Tipo di scuola: " SCHOOL_TYPE
           SUBJECTS_SECTION="- **Personalizza**: inserisci qui le materie d'esame per ${COUNTRY}"
           ;;

        *) warn "Scelta non valida, uso 'Altro'"
           COUNTRY="Altro"
           SCHOOL_TYPE="Scuola Secondaria"
           EXAM_NAME="Esame"
           SUBJECTS_SECTION="- **Personalizza**: inserisci qui le tue materie"
           ;;
    esac
    ok "Paese: ${COUNTRY} | Scuola: ${SCHOOL_TYPE} | Esame: ${EXAM_NAME}"
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

ask_llm() {
    echo ""
    echo -e "${BOLD}Scegli il provider LLM:${NC}"
    echo "  1) 🆓  Groq — GRATUITO (Llama 3.3 70B, nessun costo, key gratis)"
    echo "  2) 💰  DeepSeek — economico (~3-5€/mese, miglior rapporto qualità/prezzo)"
    echo "  3) 🔧  Custom — scegli tu provider e modello"
    read -r -p "$(echo -e "${BLUE}?${NC} Scelta [1-3]: ")" choice

    case "$choice" in
        1) LLM_PROVIDER="custom"
           LLM_BASE_URL="https://api.groq.com/openai/v1"
           LLM_MODEL="llama-3.3-70b-versatile"
           LLM_LABEL="Groq (FREE)"
           echo "  Ottieni la API key gratuita: https://console.groq.com/keys"
           read -r -s -p "$(echo -e "${BLUE}?${NC} Groq API key (input nascosto): ")" LLM_API_KEY
           echo ""
           ;;
        2) LLM_PROVIDER="custom"
           LLM_BASE_URL="https://api.deepseek.com/v1"
           LLM_MODEL="deepseek-chat"
           LLM_LABEL="DeepSeek (€3-5/mese)"
           echo "  Ottieni la API key: https://platform.deepseek.com/api_keys"
           read -r -s -p "$(echo -e "${BLUE}?${NC} DeepSeek API key (input nascosto): ")" LLM_API_KEY
           echo ""
           ;;
        3) LLM_PROVIDER="custom"
           read -r -p "  Base URL (es. https://api.openai.com/v1): " LLM_BASE_URL
           read -r -p "  Modello (es. gpt-4o, claude-sonnet-4): " LLM_MODEL
           LLM_LABEL="Custom (${LLM_MODEL})"
           read -r -s -p "$(echo -e "${BLUE}?${NC} API key (input nascosto): ")" LLM_API_KEY
           echo ""
           ;;
        *) warn "Scelta non valida, uso DeepSeek"
           LLM_PROVIDER="custom"
           LLM_BASE_URL="https://api.deepseek.com/v1"
           LLM_MODEL="deepseek-chat"
           LLM_LABEL="DeepSeek"
           read -r -s -p "$(echo -e "${BLUE}?${NC} DeepSeek API key (input nascosto): ")" LLM_API_KEY
           echo ""
           ;;
    esac

    if [ -z "$LLM_API_KEY" ]; then
        err "API key obbligatoria. Riavvia lo script quando ce l'hai."
        exit 1
    fi
    ok "LLM: ${LLM_LABEL}"
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
    sed -i "s|{{LLM_API_KEY}}|${LLM_API_KEY}|" "$PROFILE_DIR/config.yaml"
    sed -i "s|{{LLM_BASE_URL}}|${LLM_BASE_URL}|" "$PROFILE_DIR/config.yaml"
    sed -i "s|{{LLM_MODEL}}|${LLM_MODEL}|" "$PROFILE_DIR/config.yaml"
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
    ask_country_and_school
    ask_channel

    # Variabili derivate
    CONNECTION_EXAMPLE="Leopardi"
    OUT_OF_SCOPE_EXAMPLES="trading, cucina, programmazione"

    ask_llm

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
