---
name: lesson-notes
description: Prepare German lesson notes (Stichpunkte, "тези заняття") with Ukrainian glosses and a Wörterbuch from a German B1 lesson transcript in ~/My Drive/_Data/DE/b1_v3/<YYYYMMDD>/ and save them to lessons/ in this repo. Use when the user asks for тези / notes / Stichpunkte or a Wörterbuch of a German lesson or passes a lesson date.
argument-hint: "[YYYYMMDD]"
---

# Lesson notes (тези заняття)

## Locate the transcript

- Lessons live in `/Users/pronin/My Drive/_Data/DE/b1_v3/<YYYYMMDD>/`, transcript `DE-B1-<YYYYMMDD>_transcript.md`.
- Argument: `$ARGUMENTS`. If it is a date (`YYYYMMDD`) or a path, use it. If empty, take the newest date folder that has a transcript and say which one you picked.
- Read the whole transcript. Also list the folder's `HA/` (homework) contents, if present.

## Format

- Language of the notes: German, simple and at B1 level, so the notes are reading practice too.
  Ukrainian only in: the second half of headings and sub-labels, short glosses of new words in
  parentheses (*glatt* … „rutschig“ (слизько)), and the translation of the teacher's tips.
  Example sentences and the German words being taught in *italics*; explanatory prose not.
  Address the learner as *du*; call the teacher *die Lehrkraft*.
- Title: `# DE-<Course> - <YYYYMMDD>: <lesson title>`. `<Course>` is the Drive course folder without the
  underscore (`b1_v3` → `B1v3`); `<lesson title>` names the lesson's main topics in German, short
  (e.g. `# DE-B1v3 - 20261003: Wetter, Umweltschutz, Briefe, Buch und Film`).
  Below it one sentence naming the parts of the lesson («Teile der Stunde: …»). No duration, breaks, technical problems
  or other session logistics.
- Each part of the lesson is a numbered section `## N. <Deutscher Titel> / <Українська назва>`
  (e.g. `## 1. Das Wetter / Погода`). Unnumbered sections follow the same German / Ukrainian order.
  Sub-headings and vocabulary group labels are bilingual too
  in the same German / Ukrainian order (e.g. `**Wohin / Куди:**`, `**Redemittel / Фрази-кліше:**`, `**Typische Fehler / Помилки:**`).
- Per part:
  - task / topic in one sentence;
  - useful Redemittel, grouped by function (suggest, agree, decline, distribute tasks, conclude…);
  - vocabulary from the lesson: nouns ALWAYS with article (der/die/das), short translation where the word is new;
  - grammar as tables (e.g. Akkusativ | Dativ; case | order | example);
  - typical mistakes the teacher corrected, with the correct form.
- Rektion (verbs with prepositions): a two-column table Akkusativ | Dativ, preposition in **bold**;
  separately the question words (wo(r)- + prep. for things, prep. + wen/wem for persons).
  Under the table one line linking to the full list, relative from the notes file:
  `[verben-mit-prapositionen.md](../../../verben/verben-mit-prapositionen.md)`.
  Name the lesson's verbs that the list doesn't have yet; once they are added to the YAML,
  change that part of the line to «Neu aus dieser Stunde: …».
- Teacher's tips in `## 💡 Tipps / Поради`: German first, Ukrainian translation after
  (e.g. *Weniger denken, mehr sprechen.* · «Менше думати, більше говорити»).
- Final section `## Organisatorisches / Організаційне`: homework (mention `HA/` if it has files), date and time of the next lesson.

## Wörterbuch

- Separate file `worterbuch.md`, title `# DE-<Course> - <YYYYMMDD>: Wörterbuch`, below it a link back to
  `notes.md` («Notizen zur Stunde: …»), then the legend lines (copy them from the latest `lessons/*/*/worterbuch.md`): nouns
  (gender circles, `/` = plural per verbformen.de, `–`, usage markers), verbs (`(r)`, `(u)`, `|`, the
  forms line), and «In jeder Tabelle: Nomen → Verben → Adjektive → Sonstiges». All in German.
- Grouped by the lesson's topics, each group a `## <Deutsch> / <Українська>` heading and a four-column
  table with German headers `Deutsch | Beispiele | Englisch | Ukrainisch`, plain text (no italics).
- `Beispiele`: one short, correct German sentence per row that uses the word in the meaning it had in
  the lesson. Prefer a sentence from the lesson (corrected, as in the notes); otherwise write a simple
  B1 sentence on the lesson's topic. Verbs and nouns in the form the row shows (`ab | hängen von` →
  `… hängt vom Zuschauer ab.`).
- Inside each table sort by part of speech: nouns, then verbs, then adjectives (incl. participles used
  as adjectives, `gesetzlich geregelt`), then everything else (adverbs, prepositions, set phrases).
  Within a group keep the order of the lesson.
- Nouns: gender circle, article, singular, `/`, plural ending: `🔴 die Wolke / -n`, `🔵 der Frost / ¨-e`,
  `🟢 das Gewitter / -`. Take every plural from verbformen.de
  (`https://www.verbformen.de/deklination/substantive/<Wort>.htm`; for a compound missing there, its last
  part), never from memory. `–` only when the dictionary gives no plural (`🔵 der Müll / –`). Keep its
  usage notes after the ending: `(selten)` (selten/unüblich), `(fachspr.)` (nur fachsprachlich),
  `(je nach Bedeutung)` (bedeutungsabhängig), e.g. `🔴 die Hitze / -n (fachspr.)`. One noun per row; a
  phrase built on a noun goes after it (`🔴 die Regel / -n – strenge Regeln`). GitHub strips HTML colour,
  hence the emoji.
- Verbs: two lines in the Deutsch cell, joined by `<br>`:
  1. infinitive, `(r)` regelmäßig or `(u)` unregelmäßig (strong and mixed), preposition with case;
     a separable prefix split off with `\|` (an escaped pipe inside the table);
  2. `Infinitiv; Präteritum (er); Perfekt (er, with hat/ist)`.

  ```
  verzichten (r) auf \<Akk\><br>verzichten; verzichtete; hat verzichtet
  an \| bieten (u)<br>anbieten; bot an; hat angeboten
  wenden (u) an \<Akk\><br>wenden; wandte; hat gewandt
  ```
  An optional third line `z. B. <phrase from the lesson>` (`z. B. den Müll trennen`). Take the forms
  from verbformen.de (`https://www.verbformen.de/konjugation/<verb>.htm`, «Die Stammformen …»). It
  shows only one reading: when strong and weak forms depend on meaning, check de.wiktionary.org and
  use the lesson's meaning (*abhängen von*: *hing ab; hat abgehangen*, not *hängte ab*).
- Prepositions with case as `\<Akk\>` / `\<Dat\>` / `\<Gen\>`, escaped so GitHub keeps them
  (`abhängig von \<Dat\>`, `die Sorge / -n um \<Akk\>`). No circle on anything but nouns.
- Only words that came up in the lesson, no padding.
- verbformen.de rate-limits (HTTP 429): pause a few seconds between requests.

## Handling the transcript

- It is noisy speech-to-text (German and Ukrainian mixed, cut-off and garbled words). Reconstruct meaning from context and from the teacher's corrections; give examples grammatically correct, not verbatim.
- Invent nothing beyond what happened in the lesson; skip fragments that are unintelligible.
- End with one sentence (German, italics) warning that the transcript is noisy and the examples were corrected.

## Output

- Save both files to `/Users/pronin/Documents.nosync/Developer/04-pet/de/lessons/<course>/<YYYYMMDD>/`,
  mirroring the Drive path (`b1_v3/20261003` → `lessons/b1_v3/20261003/`):
  `notes.md` (тези) and `worterbuch.md`. `notes.md` links to `worterbuch.md` under the title line.
  If the files already exist, read them first and ask before overwriting.
- In chat: the paths and a short overview of the lesson parts, not the full notes.
- PDF only on request, beside the `.md` (PDF via `md-to-pdf` per global CLAUDE.md).
- Don't commit unless asked.
- After the notes, if the lesson had verbs with prepositions, check which are missing from
  `/Users/pronin/Documents.nosync/Developer/04-pet/de/verben/rektion/verben-mit-prapositionen.yaml`
  and offer (don't do it unasked) to add them.
