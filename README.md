# 📚⚡ Study — Il Tutor Gratuito di HermesBro

**L'unico prodotto gratuito dell'ecosistema HermesBro. Per tutti.**

Study è un tutor AI open source (MIT) che ti prepara all'esame con tre anime: la semplicità radicale di Feynman, il metodo strutturato di Montessori, e le domande scomode di Socrate. Gratuito. Per sempre. Per qualsiasi studente, in qualsiasi paese.

---

## Perché Study

- 🧠 **Spiegazioni che restano**: metodo Feynman — se non lo sai spiegare a un bambino di 8 anni, non l'hai capito
- 📋 **Piani di studio su misura**: spaced repetition, active recall, micro-obiettivi da 25 minuti
- 🎤 **Simulazioni d'esame**: colloquio orale con feedback strutturato su fluidità, collegamenti, precisione
- 🔗 **Collegamenti multidisciplinari**: perchè l'esame premia chi cuce le discipline, non chi le elenca
- 📖 **Revisione discorsi**: carica il PDF del tuo discorso e Study lo analizza, corregge, riscrive le parti deboli

---

## Quick Start (2 minuti)

### Prerequisiti

1. **Hermes Agent** installato → [Guida](https://hermes-agent.nousresearch.com/docs)
2. **DeepSeek API key** → [deepseek.com](https://platform.deepseek.com/api_keys) (gratuita, ~3-5€/mese con uso moderato)
3. Un terminale (o PowerShell su Windows)

### Installazione

```bash
# Clona il repo
git clone https://github.com/hermesbro/study.git
cd study

# Esegui lo script di setup
# Su Linux/Mac/WSL:
bash setup.sh

# Su Windows:
python setup.py
```

Rispondi a 6 domande e Study è vivo.

### Primo utilizzo

```bash
hermes profile use study
hermes chat
```

Poi scrivi: *"Ciao Study, devo preparare l'esame di maturità. Ho 30 giorni."*

---

## Canali

| Canale | Come attivarlo |
|--------|---------------|
| **CLI / Web** | Default — `hermes chat` dal terminale |
| **Telegram** | Crea un bot con @BotFather, inserisci il token durante il setup |

---

## Paesi e indirizzi supportati

| Paese | Esame | Indirizzi |
|-------|-------|-----------|
| 🇮🇹 **Italia** | Maturità | Artistico, Classico, Scientifico, Scienze Umane, Tecnici |
| 🇺🇸 **USA** | SAT / AP | College Prep, AP Sciences, AP Humanities |
| 🇫🇷 **Francia** | Baccalauréat | Scientifique, SES/HGGSP, HLP/LLCER, Arts |
| 🇬🇧 **UK** | A-Levels / GCSE | Sciences, Humanities, Mixed, GCSE |
| 🇩🇪 **Germania** | Abitur | Naturwissenschaften, Sprachen, Gesellschaftswiss. |
| 🇪🇸 **Spagna** | EBAU | Ciencias, Humanidades/CCSS, Artes |
| 🇵🇱 **Polonia** | Matura | Liceum, Technikum |
| 🇭🇺 **Ungheria** | Érettségi | Gimnázium, Szakközépiskola |
| 🌍 **Altri** | — | Austria, Svizzera, Paesi Bassi, Svezia, Brasile, Argentina, Giappone, Corea, India, Cina |

[Programmi completi →](profile/skills/education/study-tutoring/references/subject-syllabi.md)
[Aggiungi il tuo paese →](CONTRIBUTING.md)

---

## Come funziona

Study è un **profilo Hermes** — una configurazione che trasforma l'AI in un tutor con una personalità e un metodo precisi.

```
study/
├── profile/
│   ├── SOUL.md          ← La personalità (Feynman + Montessori + Socrate)
│   ├── GOAL.md          ← Il sistema operativo (inbound, outbound, regole)
│   ├── config.yaml      ← Configurazione tecnica (template)
│   └── skills/
│       └── study-tutoring/
│           ├── SKILL.md              ← Workflow del tutor (8 fasi)
│           └── references/
│               ├── subject-syllabi.md           ← Programmi per indirizzo
│               ├── fisica-feynman-artistico.md  ← Spiegazioni pronte
│               └── collegamenti-multidisciplinari.md
├── setup.sh             ← Script di setup (Linux/Mac)
├── setup.py             ← Script di setup (Windows)
└── docs/
```

### Le tre anime di Study

- **Richard Feynman** — "Se non lo sai spiegare a tua nonna, non l'hai capito." Ogni concetto parte da un'analogia concreta, poi arriva la formula.
- **Maria Montessori** — "Aiutami a fare da solo." Struttura, mappe mentali, micro-obiettivi. Mai la risposta prima che tu ci abbia provato.
- **Socrate** — "Lo so di non sapere." Ti incalza con domande finché non arrivi alla verità. Zero risposte superficiali.

---

## Costi

| Voce | Costo |
|------|-------|
| Hermes Agent | Gratuito (open source) |
| DeepSeek API | ~0.50€ / milione token |
| Uso studente tipico | **3-5€ / mese** |
| Telegram bot | Gratuito |

---

## Contribuire

Study è open source (MIT). Puoi:

- 🏫 **Aggiungere un indirizzo scolastico** → [CONTRIBUTING.md](CONTRIBUTING.md)
- 🎨 **Scrivere spiegazioni Feynman** per nuove materie
- 🐛 **Segnalare bug** o miglioramenti
- 🌍 **Tradurre** in altre lingue

---

## Crediti

Creato da [Tommy](https://github.com/hermesbro) — studente di liceo artistico, cuoco, builder.
Basato su [Hermes Agent](https://github.com/nous-research/hermes-agent) di Nous Research.

---

## Licenza

MIT — usalo, modificalo, condividilo. L'istruzione è di tutti.

---

*📚⚡ Suit up. Si studia.*
