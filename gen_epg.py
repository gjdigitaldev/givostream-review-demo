#!/usr/bin/env python3
"""Generate a demo XMLTV EPG for GiVo Stream App Store review testing.

Channel ids match the tvg-id values in givostream-review-demo.m3u so the
player can associate guide data with each channel. Ratings are included so
the Parental Control feature has real values to act on:
    06:00-09:00  TV-Y
    09:00-18:00  TV-PG
    18:00-22:00  TV-14
    22:00-05:00  TV-MA   (post-watershed; a clear target for parental lock)
The guide window spans yesterday through +8 days so it stays populated
regardless of exactly when the app is reviewed.

Output path is repo-relative so the daily GitHub Action (and local runs)
write the EPG into the repo root for hosting via raw.githubusercontent.com.
"""
import datetime as dt
from xml.sax.saxutils import escape

UTC = dt.timezone.utc
OUT = "givostream-demo-epg.xml"

N_DAYS = 9            # yesterday + today + 7 ahead
SLOT_HOURS = 2        # 12 programmes per channel per day

channels = [
    ("test.apple.fmp4", ["Apple BipBop (fMP4, ABR)", "Apple BipBop fMP4"]),
    ("test.apple.ts",   ["Apple BipBop (TS, 16x9)", "Apple BipBop TS"]),
    ("test.bbb",        ["Big Buck Bunny", "BBB Test"]),
    ("test.tos.subs",   ["Tears of Steel (Subtitles)", "ToS Test"]),
    ("test.live",       ["Akamai Live Test Channel", "Live Test"]),
]

# (title, sub_title|None, desc, category)
pools = {
    "test.apple.fmp4": [
        ("BipBop Adaptive Stream", None,
         "Apple's reference fMP4 HLS test stream, used to verify adaptive-bitrate switching across renditions.", "Technology"),
        ("Variant Ladder Demo", None,
         "Demonstrates multiple quality renditions within a single master playlist.", "Technology"),
        ("fMP4 Segment Loop", None,
         "Fragmented-MP4 segmented playback sample for HLS player testing.", "Technology"),
    ],
    "test.apple.ts": [
        ("BipBop Transport Stream", None,
         "MPEG-TS segmented HLS reference sample from Apple's developer streams.", "Technology"),
        ("16x9 Variant Demo", None,
         "Widescreen variant ladder for adaptive-bitrate testing.", "Technology"),
    ],
    "test.bbb": [
        ("Big Buck Bunny", "Open Movie",
         "Creative Commons (CC-BY) animated short produced by the Blender Foundation.", "Movie"),
        ("Blender Open Movie Showcase", None,
         "A selection of short films released by the Blender Foundation under Creative Commons.", "Animation"),
    ],
    "test.tos.subs": [
        ("Tears of Steel", "Project Mango",
         "Creative Commons (CC-BY) science-fiction short by the Blender Foundation, carrying multiple subtitle tracks.", "Movie"),
        ("Subtitle Track Demo", None,
         "License-clear sample with several caption tracks for verifying subtitle rendering and selection.", "Technology"),
    ],
    "test.live": [
        ("Live Test Channel", None,
         "Continuous public HLS live test stream for verifying live playback.", "Technology"),
        ("Live Reference Loop", None,
         "24/7 reference live playout used for player and buffering tests.", "Technology"),
    ],
}


def rating_for_hour(h):
    if h >= 22 or h < 5:
        return "TV-MA"
    if 18 <= h < 22:
        return "TV-14"
    if 6 <= h < 9:
        return "TV-Y"
    return "TV-PG"


def xfmt(d):
    # XMLTV timestamp: YYYYMMDDHHMMSS +ZZZZ
    return d.strftime("%Y%m%d%H%M%S %z")


def el(tag, text, **attrs):
    a = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f"<{tag}{a}>{escape(text)}</{tag}>"


midnight_today = dt.datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
start_window = midnight_today - dt.timedelta(days=1)
slots_per_day = 24 // SLOT_HOURS

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<!DOCTYPE tv SYSTEM "xmltv.dtd">')
lines.append('<!-- GiVo Stream demo EPG. Test/review use only. Channel ids match '
             'givostream-review-demo.m3u tvg-ids. -->')
lines.append('<tv generator-info-name="GiVo Stream demo EPG">')

# channels
for cid, names in channels:
    lines.append(f'  <channel id="{cid}">')
    for n in names:
        lines.append("    " + el("display-name", n, lang="en"))
    lines.append("  </channel>")

# programmes, grouped by channel
total = 0
for cid, _ in channels:
    pool = pools[cid]
    idx = 0
    for day in range(N_DAYS):
        for slot in range(slots_per_day):
            start = start_window + dt.timedelta(days=day, hours=slot * SLOT_HOURS)
            stop = start + dt.timedelta(hours=SLOT_HOURS)
            title, sub, desc, cat = pool[idx % len(pool)]
            idx += 1
            rating = rating_for_hour(start.hour)
            lines.append(f'  <programme start="{xfmt(start)}" stop="{xfmt(stop)}" channel="{cid}">')
            lines.append("    " + el("title", title, lang="en"))
            if sub:
                lines.append("    " + el("sub-title", sub, lang="en"))
            lines.append("    " + el("desc", desc, lang="en"))
            lines.append("    " + el("category", cat, lang="en"))
            lines.append(f'    <rating system="VCHIP"><value>{rating}</value></rating>')
            lines.append("  </programme>")
            total += 1

lines.append("</tv>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {OUT}")
print(f"Channels: {len(channels)}  Programmes: {total}")
print(f"Window: {start_window.date()} -> {(start_window + dt.timedelta(days=N_DAYS)).date()} (UTC)")
