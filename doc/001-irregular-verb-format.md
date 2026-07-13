# Irregular Verb YAML Format

## Schema

Each YAML file (e.g. `verben/irregular-verbs-a1.yaml`) has a `title` string and a `verbs` list. Every verb entry contains these fields:

| Field | Type | Description |
|---|---|---|
| `id` | int | Sequential integer ID |
| `infinitiv` | string | Infinitive form |
| `präteritum` | string | Simple past (3rd sg) — **note: key is `präteritum` with ä** |
| `partizip` | string | Full participle phrase with auxiliary (`hat` or `ist`; both with `/` if applicable) |
| `translations` | map | `english` + `ukrainian` keys |
| `person3` | string | 3rd person singular present (er/sie/es) |
| `examples` | string (block scalar `|`) | Free-form multi-line notes, grammar, conjugated examples |

### Minimal YAML structure

```yaml
title: "Unregelmäßige Verben - A1"
verbs:
  - id: 1
    infinitiv: beginnen
    präteritum: begann
    partizip: hat begonnen
    translations:
      english: to begin
      ukrainian: починати
    person3: beginnt
    examples: |
      Grammar notes and examples...
```

## Conventions

- **`präteritum`** — non-ASCII key (with ä), preserve exactly
- **`partizip`** — always includes the auxiliary verb (`hat` or `ist`), e.g. `ist gefallen`
- **`examples`** — YAML block scalar (`|`) for multi-line free text; may include Markdown, HTML case tags (`<Dat>`, `<Akk>`), etc.

## Best-Practice Example (`fallen`, from `irregular-verbs-a2.yaml`)

The most complete entry contains all top-level fields plus a rich `examples` block structured in these optional sections:

1. **Usage/governance** — case/precedent notes at the top (e.g. `fallen - wohin- <Akk>`)
2. **trennbare Verben** — separable prefixed verbs with translation and examples
3. **nicht trennbare Verben** — inseparable prefixed verbs
4. **Substantive** — related nouns with translations
5. **Beispiele** — standalone usage examples (phrases or full sentences)
6. **Präsens** — conjugated example in present tense
7. **Präteritum** — conjugated example in simple past
8. **Perfekt** — conjugated example in perfect tense

```yaml
  - id: 6
    infinitiv: fallen
    präteritum: fiel
    partizip: ist gefallen
    translations:
      english: to fall
      ukrainian: падати
    person3: fällt
    examples: |
      fallen - wohin- <Akk>

      **trennbare Verben**:
        - hinfallen - to fall down (on the ground) / падати на землю
          - Er fällt oft beim Laufen hin. / He often falls when running. / Він часто падає під час бігу.
        - auffallen <Dat> - to stand out, to be noticeable / кидатись в очі, бути помітним
          - Mir fällt auf, dass du heute sehr ruhig bist. / I notice that you are very quiet today. / Я помічаю, що ти сьогодні дуже тихий.
        - einfallen - to come to mind, collapse / спадати / спадати на думку
          - Mir fällt nichts Gutes ein. / Nothing good comes to mind. / Мені нічого не спадає на думку.
        - ausfallen - to fail, be canceled / випадати, скасовуватися
          - Der Unterricht fällt heute aus. / The lesson is canceled today. / Заняття сьогодні скасовуються.
        - abfallen - to fall off / відпадати
          - Die Blätter fallen im Herbst ab. / The leaves fall in autumn. / Листя опадає восени.
        - herunterfallen - to fall down / падати вниз
          - Das Glas ist heruntergefallen. / The glass has fallen. / Склянка впала вниз.
        - durchfallen - to fail (exam) / провалювати
          - Ich bin durch die Prüfung gefallen. / I failed the exam. / Я провалив іспит.

      **Substantive**:
        - der Fall - auf keinen Fall / auf jeden Fall / the case / падіння, випадок
        - der Zufall - the coincidence / збіг, випадковість
        - der Durchfall - the failure / провал

      **Beispiele**:
        - die Temperaturen fallen / the temperatures fall / Температури падають.
        - die Preise fallen / the prices fall / Ціни падають
        - im Krieg fallen / in the war fall / відбувається війна
        - durch die Prüfung fallen / through the test fall / провалився тест
        - einen Baum fallen / a tree fall / впало дерево
        - Die Mathe ist heute ausgefallen. / The math is canceled today. / Математика сьогодні скасовується.

      **Präsens**:
        - Der Apfel fällt vom Baum. / The apple falls from the tree. / Яблуко падає з дерева.

      **Präteritum**:
        - Der Apfel fiel vom Baum. / The apple fell from the tree. / Яблуко впало з дерева.

      **Perfekt**:
        - Der Apfel ist vom Baum gefallen. / The apple has fallen from the tree. / Яблуко впало з дерева.
```

## Completeness Score

A verb entry is scored out of 13 points:

| # | Criterion |
|---|---|
| 1 | `infinitiv` filled |
| 2 | `präteritum` filled |
| 3 | `partizip` filled |
| 4 | `translations` (english + ukrainian) filled |
| 5 | `person3` filled |
| 6 | Präsens examples in `examples` |
| 7 | Präteritum examples in `examples` |
| 8 | Perfekt examples in `examples` |
| 9 | Substantive section |
| 10 | Prefix/prefix-verb section (trennbare / nicht trennbare) |
| 11 | Standalone Beispiele section |
| 12 | Governance/usage notes |
| 13 | Additional notes/extra content |

Best-in-dataset verbs (12/13): `biegen`, `bieten`, `bitten`, `braten`, `fallen`, `gefallen`, `gewinnen`, `laden` (all in `irregular-verbs-a2.yaml`).
