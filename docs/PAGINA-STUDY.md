# Pagina /study — hermesbro.cloud

> **Contenuto per la landing page.** Da integrare nel sito HermesBro.

---

## Hero

**📚⚡ Study — Il Tutor Gratuito di HermesBro**

L'unico prodotto open source dell'ecosistema HermesBro. Feynman + Montessori + Socrate in un assistente AI che ti prepara all'esame. Gratuito. Per sempre. Per qualsiasi studente, in qualsiasi paese.

[Scarica Study](#download) [Guarda la demo →](#demo)

---

## Come funziona

Study è un profilo Hermes — un "cervello" AI preconfigurato con una personalità precisa e un metodo didattico collaudato.

1. **Scarica Study** — è open source, gratuito
2. **Esegui lo script di setup** — 6 domande e sei pronto
3. **Studia** — via chat (terminale) o Telegram

Zero pubblicità. Zero costi nascosti. Solo studio.

---

## Le tre anime di Study

|  |  |  |
|---|---|---|
| 🧠 **Feynman** | "Se non lo sai spiegare a tua nonna, non l'hai capito" | Ogni concetto parte da un'analogia concreta. La formula arriva dopo. |
| 📋 **Montessori** | "Aiutami a fare da solo" | Struttura, mappe, micro-obiettivi. Mai la risposta prima che tu ci abbia provato. |
| ❓ **Socrate** | "Lo so di non sapere" | Ti incalza con domande finché non arrivi alla verità da solo. |

---

## Cosa fa Study

- 📖 **Spiega** — qualsiasi argomento, dal teorema di Pitagora a Nietzsche, con analogie quotidiane
- 🎤 **Interroga** — simulazioni d'esame con feedback su fluidità, precisione, collegamenti
- 📅 **Pianifica** — piani di studio personalizzati con spaced repetition e micro-obiettivi
- 🔗 **Collega** — percorsi multidisciplinari tra materie che sembrano distanti
- 📝 **Revisiona** — carica il PDF del tuo discorso e Study lo analizza, corregge, riscrive

---

## Download e installazione (2 minuti)

### Prerequisiti

1. **Hermes Agent** — [Scarica gratis](https://hermes-agent.nousresearch.com/docs)
2. **DeepSeek API key** — [Registrati gratis](https://platform.deepseek.com/api_keys) (~3-5€/mese di token)

### Installazione

```bash
# Scarica Study
git clone https://github.com/bonaventuratommasosam-bot/study.git
cd study

# Su Linux/Mac:
bash setup.sh

# Su Windows:
python setup.py
```

Rispondi alle domande (nome, paese, scuola, canale) — Study si configura da solo.

```bash
# Avvia Study
hermes profile use study
hermes chat
```

Poi scrivi: *"Ciao Study, devo preparare l'esame. Ho 30 giorni."*

---

## Canali

| Canale | Come funziona |
|--------|---------------|
| 💻 **Terminale / Web** | `hermes chat` dal tuo computer. Semplice, privato. |
| 📱 **Telegram** | Crea un bot con @BotFather, inserisci il token nel setup. Study ti manda anche i reminder. |

---

## Paesi supportati

Study copre i programmi scolastici di **9+ paesi** con syllabi dettagliati:

🇮🇹 Italia (Maturità) · 🇺🇸 USA (SAT/AP) · 🇫🇷 Francia (Bac) · 🇬🇧 UK (A-Levels) · 🇩🇪 Germania (Abitur) · 🇪🇸 Spagna (EBAU) · 🇵🇱 Polonia (Matura) · 🇭🇺 Ungheria (Érettségi) · 🌍 e altri in arrivo

[Vedi tutti i programmi →](https://github.com/bonaventuratommasosam-bot/study/blob/main/profile/skills/education/study-tutoring/references/subject-syllabi.md)

---

## Perché gratuito?

Study è **l'unico prodotto gratuito di HermesBro**. 

Perché? Perché l'istruzione è un diritto. Tommy l'ha costruito per sé stesso mentre preparava la maturità — ora è di tutti.

Gli altri prodotti HermesBro (contabilità AI, trading bot, marketing automation) sono servizi professionali a pagamento. Study è il nostro contributo open source alla comunità.

---

## Chi l'ha creato

Study è stato creato da **Tommy** — studente di liceo artistico, cuoco, e founder di HermesBro. Preparandosi per l'esame di maturità, ha costruito il tutor che avrebbe voluto avere. Poi l'ha reso open source.

Basato su [Hermes Agent](https://github.com/nous-research/hermes-agent) di Nous Research.

---

## Open Source (MIT)

Study è completamente open source. Puoi:

- Usarlo gratis, per sempre
- Modificarlo per adattarlo al tuo paese
- Contribuire con nuovi programmi scolastici
- Installarlo sul tuo server

[GitHub →](https://github.com/bonaventuratommasosam-bot/study)
[Come contribuire →](https://github.com/bonaventuratommasosam-bot/study/blob/main/CONTRIBUTING.md)

---

## FAQ

**Quanto costa?**
Zero. Study è gratuito. Paghi solo i token LLM (DeepSeek: ~3-5€/mese con uso intensivo).

**Devo saper programmare?**
No. Lo script di setup fa tutto da solo. Se sai usare il terminale, sai installare Study.

**Posso usarlo per qualsiasi esame?**
Sì. Study si adatta al programma del tuo paese e della tua scuola. Se manca, puoi aggiungerlo.

**Funziona su Windows?**
Sì. C'è uno script Python apposta (`python setup.py`).

**È sicuro?**
Sì. Study gira sul tuo computer, non su server esterni. La tua API key resta privata.

---

*📚⚡ Study — perché la risposta che trovi da solo è l'unica che non dimenticherai.*
