# Contributing to Study

Thank you! Study exists to democratize quality tutoring. Here's how you can help.

---

## Adding a Country or School System

90% of the work is filling in the curriculum in `profile/skills/education/study-tutoring/references/subject-syllabi.md`.

### Template

```markdown
## [Country] — [Exam Name] [Year]

**Exam subjects:**
- Subject 1 — [internal/external] examiner
- Subject 2 — [internal/external] examiner
- Subject 3 — [internal/external] examiner
- Subject 4 — [internal/external] examiner

### Subject 1 — standard curriculum
1. **Topic**: key details, authors, dates
2. ...

### Subject 2 — standard curriculum
...
```

### Steps

1. Fork the repo
2. Add the curriculum to `subject-syllabi.md`
3. (Optional) Add Feynman-style explanations in a new file `references/feynman-[subject]-[country].md`
4. Add the country to the table in `README.md`
5. Open a Pull Request

---

## Writing Feynman Explanations

Every Feynman explanation follows this format:

```markdown
### Concept Name

| Move | What to say |
|------|-------------|
| 👶 8-year-old version | [Concrete analogy from everyday life. 2 sentences max.] |
| 🎨 Connection to the subject | [How this applies in practice / in the student's field] |
| 📐 Formula / Theory | [The formula or formal definition, only AFTER the intuition] |
```

### Rules

- Physical intuition first, formula second. Never the other way around.
- Use everyday objects (pots, balloons, pencils, water)
- Always connect to the student's field of study
- One explanation = 150 words max

See `fisica-feynman-artistico.md` for complete examples.

---

## Modifying SOUL.md or GOAL.md

SOUL and GOAL are template files with `{{LI_KE_THIS}}` variables. The `setup.sh`/`setup.py` scripts replace them.

When editing:
- Use `{{STUDENT_NAME}}` instead of specific names
- Use `{{SCHOOL_TYPE}}` and `{{EXAM_NAME}}` for school references
- Don't remove existing variables without updating the setup scripts too

---

## Code Standards

- **Python (setup.py)**: Python 3.8+ compatible, zero external dependencies
- **Bash (setup.sh)**: POSIX-compatible, tested on bash and zsh
- **Markdown**: all .md files use tables where possible, emoji for priority

---

## Reporting Bugs

Open a GitHub issue with:
- Operating system
- Hermes Agent version (`hermes --version`)
- Full error message
- What you were doing

---

## Questions?

Open a GitHub Discussion or reach out at [hermesbro.cloud](https://hermesbro.cloud).

---

*📚⚡ Every contribution is one less exam without a tutor.*
