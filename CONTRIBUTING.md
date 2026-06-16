# Contribuire a Study

Grazie! Study esiste per democratizzare il tutoring di qualità. Ecco come puoi aiutare.

---

## Aggiungere un indirizzo scolastico

Il 90% del lavoro è compilare il programma in `profile/skills/education/study-tutoring/references/subject-syllabi.md`.

### Template

```markdown
## [Nome Indirizzo] — [Esame] [Anno]

**Materie orali:**
- Materia 1 — commissario [interno/esterno]
- Materia 2 — commissario [interno/esterno]
- Materia 3 — commissario [interno/esterno]
- Materia 4 — commissario [interno/esterno]

### Materia 1 — programma standard
1. **Argomento**: dettagli chiave, autori, date
2. ...

### Materia 2 — programma standard
...
```

### Passi

1. Fai fork del repo
2. Aggiungi il programma in `subject-syllabi.md`
3. (Opzionale) Aggiungi spiegazioni Feynman in un nuovo file `references/fisica-feynman-[indirizzo].md`
4. Aggiungi l'indirizzo alla tabella in `README.md`
5. Apri una Pull Request

---

## Scrivere spiegazioni Feynman

Ogni spiegazione Feynman segue questo formato:

```markdown
### Nome del concetto

| Mossa | Cosa dire |
|-------|-----------|
| 👶 Versione 8 anni | [Analogia concreta dalla vita quotidiana. Massimo 2 frasi.] |
| 🎨 Collegamento alla materia | [Come si applica nella pratica / nella materia dello studente] |
| 📐 Formula / Teoria | [La formula o definizione formale, solo DOPO l'intuizione] |
```

### Regole

- Prima il senso fisico, poi la formula. Mai il contrario.
- Usa oggetti quotidiani (pentole, palloncini, matite, acqua)
- Collega sempre alla materia d'indirizzo dello studente
- Una spiegazione = massimo 150 parole

Vedi `fisica-feynman-artistico.md` per esempi completi.

---

## Modificare SOUL.md o GOAL.md

SOUL e GOAL sono file template con variabili `{{LI_KE_THIS}}`. Lo script `setup.sh`/`setup.py` le sostituisce.

Quando modifichi:
- Usa `{{STUDENT_NAME}}` invece di nomi specifici
- Usa `{{SCHOOL_TYPE}}` e `{{EXAM_NAME}}` per riferimenti alla scuola
- Non rimuovere le variabili esistenti senza aggiornare anche lo script di setup

---

## Standard del codice

- **Python (setup.py)**: compatibile Python 3.8+, zero dipendenze esterne
- **Bash (setup.sh)**: POSIX-compatibile, testato su bash e zsh
- **Markdown**: tutti i file .md usano tabelle quando possibile, emoji per priorità

---

## Segnalare bug

Apri una issue su GitHub con:
- Sistema operativo
- Versione Hermes Agent (`hermes --version`)
- Messaggio di errore completo
- Cosa stavi facendo

---

## Domande?

Apri una Discussion su GitHub o scrivi a [hermesbro.cloud](https://hermesbro.cloud).

---

*📚⚡ Ogni contributo è un esame in meno senza tutor.*
