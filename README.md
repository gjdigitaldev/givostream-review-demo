# GiVo Stream — App Review demo playlist + EPG

Public, license-clear demo content used **only** to let an App Store reviewer
exercise GiVo Stream's generic player during review. GiVo Stream is a
general-purpose IPTV/M3U player and **bundles no content of its own** — these
files are not shipped in the app, are not visible to end users, and are
referenced only from the **App Review Information** notes.

## Raw URLs (paste into the App Review notes)

- **M3U playlist:**
  `https://raw.githubusercontent.com/gmoney0026/givostream-review-demo/main/givostream-review-demo.m3u`
- **EPG (XMLTV):**
  `https://raw.githubusercontent.com/gmoney0026/givostream-review-demo/main/givostream-demo-epg.xml`

In the app: add a playlist of type **M3U & EPG**, paste the M3U URL into the
playlist field and the EPG URL into the guide field, then load it.

## What's in the playlist

All streams are public, license-clear test assets — nothing rights-encumbered:

| Channel | Source |
|---|---|
| Apple BipBop (fMP4, ABR) | Apple developer HLS test streams |
| Apple BipBop (TS, 16x9) | Apple developer HLS test streams |
| Big Buck Bunny | Mux public test stream (Blender, CC-BY) |
| Tears of Steel (subtitles) | Mux public test stream (Blender, CC-BY) |
| Akamai Live Test Channel | Akamai public live test stream |

## The EPG auto-refreshes daily

`gen_epg.py` builds a **date-relative** XMLTV guide (yesterday → +8 days from
the run date), with V-Chip ratings so the Parental Control feature has real
values to act on. A scheduled GitHub Action (`.github/workflows/refresh-epg.yml`)
re-runs it every day and commits a fresh `givostream-demo-epg.xml`, so the
guide is always populated whenever the reviewer opens the app — no manual
step before each submission.

Regenerate locally with:

```sh
python3 gen_epg.py
```
