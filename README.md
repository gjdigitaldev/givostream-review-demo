# GiVo Stream — App Review demo playlist + EPG

Public, license-clear demo content used **only** to let an App Store reviewer
exercise GiVo Stream's generic player during review. GiVo Stream is a
media player and **bundles no content of its own** — these
files are not shipped in the app, are not visible to end users, and are
referenced only from the **App Review Information** notes.

## Raw URLs (paste into the App Review notes)

- **M3U playlist:**
  `https://raw.githubusercontent.com/gjdigitaldev/givostream-review-demo/main/givostream-review-demo.m3u`
- **EPG (XMLTV):**
  `https://raw.githubusercontent.com/gjdigitaldev/givostream-review-demo/main/givostream-demo-epg.xml`

In the app: add a playlist of type **M3U & EPG**, paste the M3U URL into the
playlist field and the EPG URL into the guide field, then load it. Turn on the playlist's "Include Movies & Series" switch to see the two VOD titles in VOD.

## What's in the playlist

All streams are public, license-clear test assets — nothing rights-encumbered:

| Channel | Source |
|---|---|
| Big Buck Bunny (VOD) | Mux public test stream (Blender, CC-BY) |
| Tears of Steel (VOD) | Mux public test stream (Blender, CC-BY) |
| Apple BipBop (Multi-Bitrate) | Apple HLS example stream (devstreaming-cdn.apple.com) |
| Apple BipBop (fMP4) | Apple HLS example stream (devstreaming-cdn.apple.com) |
| Live Test Channel | GiVo Stream review live channel: Big Buck Bunny (Blender, CC-BY 3.0) looped as a live HLS stream (givo-review-live.givostream.workers.dev) |
| Live Test Channel 2 | GiVo Stream review live channel 2: Tears of Steel (Blender, CC-BY 3.0) looped as a live HLS stream |

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
