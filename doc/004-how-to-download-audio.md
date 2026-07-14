# How to Download Audio for German Verbs

## Goal

Download pronunciation audio files (`.mp3` / `.ogg`) for all German verbs from the YAML data files, organized by level (a1/a2/b).

## Source: Wikimedia Commons

Wikimedia Commons hosts **crowdsourced native-speaker audio** for thousands of German words. Each file follows a naming convention:

```
File:LL-Q188 (deu)-{username}-{word}.{ext}
```

- `LL-Q188` = Wiktionary Language List, German (deu)
- `username` = the contributor who uploaded it (e.g., Natschoba, Jeuwre)
- Extension: `.ogg` (preferred), `.mp3`, or `.wav`

Example: `File:LL-Q188 (deu)-Natschoba-beginnen.wav`

## Steps

### 1. Extract infinitives from YAML files

Parse each `verben/*.yaml` file to collect all `infinitiv` values:

```python
# From irregular-verbs-a1.yaml (50 verbs)
infinitives = ['beginnen', 'bleiben', 'essen', ..., 'verstehen']
```

### 2. Search Wikimedia Commons for audio files

Use the Commons API to search for audio files matching each verb:

```
GET https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch="LL-Q188"+"{word}"&format=json&srnamespace=6&srlimit=5
```

Key parameters:
- `srsearch="LL-Q188"+"{word}"` — searches for German pronunciation audio of the specific word
- `srnamespace=6` — limits results to file namespace (audio/video/images)
- Returns titles like `File:LL-Q188 (deu)-Natschoba-beginnen.wav`

### 3. Resolve file URL via API

Convert the filename to a direct download URL:

```
GET https://commons.wikimedia.org/w/api.php?action=query&titles={filename}&prop=imageinfo&iiprop=url&format=json
```

Returns the direct URL to `upload.wikimedia.org/...`.

### 4. Download and save

Download the file and save it to `audio/{folder}/{word}.{ext}`:

```
audio/
├── irregular-verbs-a1/
│   ├── beginnen.mp3
│   ├── bleiben.wav
│   └── ... (50 files)
├── irregular-verbs-a2/
│   ├── backen.mp3
│   └── ... (9 files)
└── irregular-verbs-b/
    ├── brennen.wav
    └── ... (3 files)
```

### 5. Handle rate limiting

Wikimedia Commons enforces **HTTP 429 (Too Many Requests)** on rapid requests. Mitigation:

- Add `time.sleep(2)` between requests
- Retry failed downloads (3 attempts, 10s delay)
- Prefer `.ogg` files (smaller, faster to download)

## Current Status (as of 2026-07-14)

| Level | Verbs | Downloaded | Missing |
|---|---:|---:|---:|
| **a1** | 50 | 50 ✅ | 0 |
| **a2** | 27 | 9 | 18 |
| **b** | 16 | 3 | 13 |

**Total: 62/93 verbs have audio.**

### Missing a2 verbs (18)
aufgeben, aufwachen, befehlen, bemerken, empfehlen, empfangen, ergreifen, erziehen, fangen, fliehen, genieren, gelingen, geschehen, gewähren, hegen, kauen, leihen, reiben, scheiden, schmeißen, schwören, verzeihen, zergehen, zeichnen, ziehen

### Missing b verbs (13)
beißen, dulden, einladen, entzweien, flüstern, gähnen, hassen, küssen, lügen, mögen, rätseln, schämen

## Alternative Sources (if Commons is unavailable)

| Source | Notes |
|---|---|
| **Forvo API** (`api.forvo.com`) | 6M pronunciations, requires API key, rate-limited |
| **Wiktionary bulk audio** (`kaikki.org/dictionary/rawdata.html`) | 20.4GB tar with ~942K audio files — filter by our verb list |
| **gTTS** (`gtts` Python library) | Google Text-to-Speech, free but synthetic voice (not native speaker) |

## Notes

- `.ogg` files are preferred (smallest, good quality for speech)
- `.mp3` is the fallback (widely supported by web players)
- `.wav` files are larger but highest quality — acceptable for learning purposes
- Files are saved with the infinitive as filename (e.g., `verstehen.mp3`)
- The folder structure mirrors the YAML file naming: `audio/irregular-verbs-a1/`
