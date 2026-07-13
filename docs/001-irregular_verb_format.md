# Irregular Verb Format

Verb data lives in `verben/*.yaml`. Each file has a `title` string and a `verbs` list.

## Schema

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | int | yes | Unique within the file (sequential per file, not global) |
| `infinitiv` | string | yes | Base form of the verb |
| `präteritum` | string | yes | Simple past, 3rd person singular |
| `partizip` | string | yes | Full perfect form including auxiliary (`hat` / `ist`) |
| `person3` | string | yes | 3rd person singular present |
| `translations` | object | yes | Must contain `english` and `ukrainian` |
| `examples` | multiline string | optional | Free-form notes (literal block scalar `|`) |

## Conventions

### `partizip`

Include the auxiliary verb:

- `hat begonnen` (transitive)
- `ist geblieben` (intransitive with movement/state change)
- `hat / ist geschwommen` (when both auxiliaries are possible)

### `präteritum`

Always 3rd person singular form (e.g. `fuhr`, not `fahren wir`).

### `examples`

Free-form literal block scalar. Recommended structure:

1. **Related nouns** — derivatives (e.g. `die Fahrt`, `der Fahrer`)
2. **Prepositional usage** — cases and prepositions (e.g. `zu <Dat>`, `in <Akk>`)
3. **Prefixed verbs** — separable/inseparable compounds (e.g. `anfangen`, `empfangen`)
4. **Idioms / phrases** — fixed expressions
5. **Sentence examples by tense** — bilingual (German / English), grouped under `**Präsens**`, `**Präteritum**`, `**Perfekt**`

## Complete Example

The most complete entry (`fahren`, A1 file, ID 4):

```yaml
- id: 4
  infinitiv: fahren
  präteritum: fuhr
  partizip: ist gefahren
  translations:
    english: to drive, to go, to travel
    ukrainian: їхати
  person3: fährt
  examples: |
    die Fahrt - поїздка
    der Fahrer - водій

    ist - якщо пасажир
    hat - якщо за кермом

    fahre zu <Dat> - я доїхав до ...
    fahre in <Akk> - я в'їхав в ...
    fahre an <Akk> - я в'їхав на ...
    fahre nach - нет артикля
    fahre mit <Dat>

    **Beispiele**:
      Ich fahre zur Arbeit / I drive to work.
      Ich fahre ins Ausland / I drive abroad.
      Ich bin mit dem Bus gefahren. / I drove with the bus.
      Ich bin mit der Bahn gefahren. / I drove with the train.
      Haben Sie Auto gefahren? / Have you driven a car? /
      am Steuer sein; steuern
      Waren Sie am Steuer? / Were you at the wheel?
      vor Schreck in die Höhe fahren / to drive into the sky from fear
      vor Wut auf die Palme fahren / to drive into the sky from anger

    **Präsens**:
      Ich fahre mit dem Auto zur Arbeit. / I drive with the car to work.
      Er fährt gerne Fahrrad in seiner Freizeit. / He likes to ride a bike in his free time.

    **Präteritum**:
      Gestern fuhr ich mit dem Zug nach Hamburg. / I drove with the train to Hamburg yesterday.
      Letzte Woche fuhren wir in den Urlaub ans Meer. / Last week, we went on vacation to the sea.

    **Perfekt**:
      Ich bin heute Morgen mit dem Bus zur Schule gefahren. / I drove with the bus to school this morning.
      Sie hat das Auto zum Supermarkt gefahren, um Lebensmittel einzukaufen. / She drove to the supermarket with the car to buy groceries.
```
