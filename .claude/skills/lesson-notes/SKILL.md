---
name: lesson-notes
description: Prepare bilingual (Ukrainian + German) lesson notes ("тези заняття") from a German B1 lesson transcript in ~/My Drive/_Data/DE/b1_v3/<YYYYMMDD>/. Use when the user asks for тези / notes / Stichpunkte of a German lesson or passes a lesson date.
argument-hint: "[YYYYMMDD]"
---

# Lesson notes (тези заняття)

## Locate the transcript

- Lessons live in `/Users/pronin/My Drive/_Data/DE/b1_v3/<YYYYMMDD>/`, transcript `DE-B1-<YYYYMMDD>_transcript.md`.
- Argument: `$ARGUMENTS`. If it is a date (`YYYYMMDD`) or a path, use it. If empty, take the newest date folder that has a transcript and say which one you picked.
- Read the whole transcript. Also list the folder's `HA/` (homework) contents, if present.

## Format

- Language of the notes: Ukrainian. All German words, phrases and examples in *italics*.
- Title: `# Тези заняття B1 від DD.MM.YYYY · Stichpunkte zur Stunde B1 vom DD.MM.YYYY`.
  Below it one sentence: how long the lesson was and which parts it had.
- Each part of the lesson is a numbered section `## N. <Українська назва> · <Deutscher Name>`.
  Sub-headings and vocabulary group labels are bilingual too
  (e.g. `**Куди · Wohin:**`, `**Фрази-кліше · Redemittel:**`, `**Помилки · Typische Fehler:**`).
- Per part:
  - task / topic in one sentence;
  - useful Redemittel, grouped by function (suggest, agree, decline, distribute tasks, conclude…);
  - vocabulary from the lesson: nouns ALWAYS with article (der/die/das), short translation where the word is new;
  - grammar as tables (e.g. Akkusativ | Dativ; case | order | example);
  - typical mistakes the teacher corrected, with the correct form.
- Rektion (verbs with prepositions): a two-column table Akkusativ | Dativ, preposition in **bold**;
  separately the question words (wo(r)- + prep. for things, prep. + wen/wem for persons).
- Teacher's tips set apart: Ukrainian + German (e.g. «Менше думати, більше говорити» · *Weniger denken, mehr sprechen*).
- Final section `## Організаційне · Organisatorisches`: homework (mention `HA/` if it has files), date and time of the next lesson.

## Handling the transcript

- It is noisy speech-to-text (German and Ukrainian mixed, cut-off and garbled words). Reconstruct meaning from context and from the teacher's corrections; give examples grammatically correct, not verbatim.
- Invent nothing beyond what happened in the lesson; skip fragments that are unintelligible.
- End with one sentence warning that the transcript is noisy and the examples were corrected.

## Output

- Answer in chat. Do not create a file unless the user asks for `.md` / PDF (then save next to the transcript; PDF via `md-to-pdf` per global CLAUDE.md).
- After the notes, if the lesson had verbs with prepositions, check which are missing from
  `/Users/pronin/Documents.nosync/Developer/04-pet/de/verben/rektion/verben-mit-prapositionen.yaml`
  and offer (don't do it unasked) to add them.
