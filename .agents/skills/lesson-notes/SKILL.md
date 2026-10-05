---
name: lesson-notes
description: Prepare bilingual (Ukrainian + German) lesson notes ("тези заняття") and a Wörterbuch from a German B1 lesson transcript in ~/My Drive/_Data/DE/b1_v3/<YYYYMMDD>/ and save them to lessons/ in this repo. Use when the user asks for тези / notes / Stichpunkte or a Wörterbuch of a German lesson or passes a lesson date.
---

# Lesson notes (тези заняття)

## Locate the transcript

- Lessons live in `/Users/pronin/My Drive/_Data/DE/b1_v3/<YYYYMMDD>/`, transcript `DE-B1-<YYYYMMDD>_transcript.md`.
- If the user gave a date (`YYYYMMDD`) or a path, use it. If no date was given, take the newest date folder that has a transcript and say which one you picked.
- Read the whole transcript. Also list the folder's `HA/` (homework) contents, if present.

## Format

- Language of the notes: Ukrainian. All German words, phrases and examples in *italics*.
- Title: `# DE-<Course> - <YYYYMMDD>, <lesson title>`. `<Course>` is the Drive course folder without the
  underscore (`b1_v3` → `B1v3`); `<lesson title>` names the lesson's main topics in German, short
  (e.g. `# DE-B1v3 - 20261003, Wetter, Umweltschutz, Briefe, Buch und Film`).
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

## Wörterbuch

- Separate file, title `# DE-<Course> - <YYYYMMDD>, Wörterbuch`, below it a link back to `notes.md`.
- Grouped by the lesson's topics, each group a bilingual `## <Українська> · <Deutsch>` heading and a two-column table `Deutsch | Українська`.
- German in *italics*; nouns with article and plural (*das Gewitter, -*, *die Wolke, -n*); prepositions and case where they belong (*abhängig von + Dat*).
- Only words that came up in the lesson, no padding.

## Handling the transcript

- It is noisy speech-to-text (German and Ukrainian mixed, cut-off and garbled words). Reconstruct meaning from context and from the teacher's corrections; give examples grammatically correct, not verbatim.
- Invent nothing beyond what happened in the lesson; skip fragments that are unintelligible.
- End with one sentence warning that the transcript is noisy and the examples were corrected.

## Output

- Save both files to `/Users/pronin/Documents.nosync/Developer/04-pet/de/lessons/<course>/<YYYYMMDD>/`,
  mirroring the Drive path (`b1_v3/20261003` → `lessons/b1_v3/20261003/`):
  `notes.md` (тези) and `woerterbuch.md`. `notes.md` links to `woerterbuch.md` under the title line.
  If the files already exist, read them first and ask before overwriting.
- In chat: the paths and a short overview of the lesson parts, not the full notes.
- PDF only on request, beside the `.md` (PDF via `md-to-pdf <file>.md`, run in that folder).
- Don't commit unless asked.
- After the notes, if the lesson had verbs with prepositions, check which are missing from
  `/Users/pronin/Documents.nosync/Developer/04-pet/de/verben/rektion/verben-mit-prapositionen.yaml`
  and offer (don't do it unasked) to add them.
