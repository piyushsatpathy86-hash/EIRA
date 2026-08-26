# ============================================================
# EIRA — Doodle / Cartoon Maker
# ============================================================

import sys
sys.path.append("C:/EIRA")

import svgwrite
import os
import subprocess
from datetime import datetime

os.makedirs("C:/EIRA/data/doodles", exist_ok=True)


def stickman(dwg, x, y, label="", color="#7C3AED", size=1.0):
    """Draw a stickman"""
    s = size
    # Head
    dwg.add(dwg.circle(center=(x, y-30*s), r=12*s,
        stroke=color, fill="white", stroke_width=2*s))
    # Eyes
    dwg.add(dwg.circle(center=(x-4*s, y-33*s), r=1.5*s, fill=color))
    dwg.add(dwg.circle(center=(x+4*s, y-33*s), r=1.5*s, fill=color))
    # Smile
    dwg.add(dwg.path(
        d=f"M {x-5*s} {y-26*s} Q {x} {y-21*s} {x+5*s} {y-26*s}",
        stroke=color, fill="none", stroke_width=1.5*s))
    # Body
    dwg.add(dwg.line(start=(x, y-18*s), end=(x, y+20*s),
        stroke=color, stroke_width=2*s))
    # Arms
    dwg.add(dwg.line(start=(x-20*s, y-5*s), end=(x+20*s, y-5*s),
        stroke=color, stroke_width=2*s))
    # Legs
    dwg.add(dwg.line(start=(x, y+20*s), end=(x-15*s, y+45*s),
        stroke=color, stroke_width=2*s))
    dwg.add(dwg.line(start=(x, y+20*s), end=(x+15*s, y+45*s),
        stroke=color, stroke_width=2*s))
    # Label
    if label:
        dwg.add(dwg.text(label, insert=(x, y+62*s),
            text_anchor="middle", font_size=f"{11*s}px",
            font_family="Arial", fill=color, font_weight="bold"))


def speech_bubble(dwg, x, y, text, color="#7C3AED", bg="#F5F3FF"):
    """Speech bubble with wrapped text"""
    words    = text.split()
    lines    = []
    cur_line = []
    for word in words:
        cur_line.append(word)
        if len(" ".join(cur_line)) > 22:
            lines.append(" ".join(cur_line[:-1]))
            cur_line = [word]
    if cur_line:
        lines.append(" ".join(cur_line))

    bw = max(len(l) for l in lines) * 7 + 24
    bh = len(lines) * 20 + 16

    dwg.add(dwg.rect(insert=(x, y), size=(bw, bh),
        rx=10, ry=10, fill=bg, stroke=color, stroke_width=1.5))
    dwg.add(dwg.polygon(
        points=[(x+15, y+bh), (x+5, y+bh+14), (x+28, y+bh)],
        fill=bg, stroke=color, stroke_width=1))
    for i, line in enumerate(lines):
        dwg.add(dwg.text(line, insert=(x+12, y+18+i*20),
            font_size="11px", font_family="Arial", fill=color))
    return bw, bh


def draw_box(dwg, x, y, w, h, label,
             bg="#F5F3FF", border="#7C3AED", tc="#1E1B4B"):
    dwg.add(dwg.rect(insert=(x, y), size=(w, h),
        rx=8, ry=8, fill=bg, stroke=border, stroke_width=2))
    dwg.add(dwg.text(label, insert=(x+w//2, y+h//2+5),
        text_anchor="middle", font_size="12px",
        font_family="Arial", fill=tc, font_weight="bold"))


def add_arrow_marker(dwg, color="#7C3AED"):
    marker = dwg.marker(id="arr", markerWidth="10",
        markerHeight="7", refX="9", refY="3.5", orient="auto")
    marker.add(dwg.polygon(points="0 0, 10 3.5, 0 7", fill=color))
    dwg.defs.add(marker)


def open_svg(path: str):
    subprocess.Popen(["start", path], shell=True)


# ── Diagram functions ────────────────────────────────────────

def make_array_diagram(values: list, title: str = "Array") -> str:
    """Visual array diagram"""
    fname = (f"C:/EIRA/data/doodles/"
             f"array_{datetime.now().strftime('%H%M%S')}.svg")
    w   = max(500, len(values)*60+80)
    dwg = svgwrite.Drawing(fname, size=(w, 170))
    dwg.add(dwg.rect(insert=(0,0), size=(w,170), fill="white"))

    dwg.add(dwg.text(title, insert=(w//2, 30),
        text_anchor="middle", font_size="16px",
        font_family="Arial", fill="#1E1B4B", font_weight="bold"))

    colors = ["#7C3AED","#2563EB","#059669","#D97706","#DC2626"]
    for i, val in enumerate(values):
        x   = 40+i*60
        col = colors[i % len(colors)]
        dwg.add(dwg.rect(insert=(x,50), size=(50,50),
            fill=col, rx=6, opacity=0.9))
        dwg.add(dwg.text(str(val), insert=(x+25,82),
            text_anchor="middle", font_size="16px",
            font_family="Arial", fill="white", font_weight="bold"))
        dwg.add(dwg.text(f"[{i}]", insert=(x+25,122),
            text_anchor="middle", font_size="11px",
            font_family="Arial", fill="#6B7280"))

    dwg.save()
    return fname


def make_flowchart(steps: list, title: str = "Flowchart") -> str:
    """Step by step flowchart with stickman"""
    fname = (f"C:/EIRA/data/doodles/"
             f"flow_{datetime.now().strftime('%H%M%S')}.svg")
    h   = 100 + len(steps)*85 + 80
    dwg = svgwrite.Drawing(fname, size=(520, h))
    dwg.add(dwg.rect(insert=(0,0), size=(520,h), fill="white"))
    add_arrow_marker(dwg)

    dwg.add(dwg.text(title, insert=(260,35),
        text_anchor="middle", font_size="18px",
        font_family="Arial", fill="#1E1B4B", font_weight="bold"))

    stickman(dwg, 460, 110, "EIRA", color="#7C3AED", size=0.85)
    speech_bubble(dwg, 290, 55,
        "Let me explain!", color="#7C3AED", bg="#F5F3FF")

    colors = ["#7C3AED","#2563EB","#059669","#D97706","#DC2626"]
    y = 80
    for i, step in enumerate(steps):
        col = colors[i % len(colors)]
        bg  = "#F5F3FF" if i % 2 == 0 else "#EFF6FF"
        draw_box(dwg, 130, y, 220, 46, step, bg=bg, border=col)
        if i < len(steps)-1:
            dwg.add(dwg.line(
                start=(240, y+46), end=(240, y+83),
                stroke=col, stroke_width=2,
                marker_end="url(#arr)"))
        y += 85

    dwg.save()
    return fname


def make_concept_cartoon(concept: str, explanation: str) -> str:
    """EIRA stickman explaining a concept"""
    fname = (f"C:/EIRA/data/doodles/"
             f"concept_{datetime.now().strftime('%H%M%S')}.svg")
    dwg = svgwrite.Drawing(fname, size=(620, 320))
    dwg.add(dwg.rect(insert=(0,0), size=(620,320),
        fill="#FAFAFA", rx=12))
    dwg.add(dwg.rect(insert=(2,2), size=(616,316),
        fill="none", stroke="#7C3AED", stroke_width=2, rx=12))

    # Title
    dwg.add(dwg.text(concept, insert=(310,38),
        text_anchor="middle", font_size="20px",
        font_family="Arial", fill="#1E1B4B", font_weight="bold"))

    # EIRA stickman
    stickman(dwg, 90, 200, "EIRA", color="#7C3AED")

    # Speech bubble
    short = (explanation[:80]+"...") if len(explanation)>80 else explanation
    speech_bubble(dwg, 155, 90, short, color="#7C3AED", bg="#F5F3FF")

    # Lightbulb
    dwg.add(dwg.circle(center=(530,130), r=32,
        fill="#FEF3C7", stroke="#D97706", stroke_width=2))
    dwg.add(dwg.text("💡", insert=(516,140), font_size="26px"))
    dwg.add(dwg.text("Idea!", insert=(530,175),
        text_anchor="middle", font_size="11px",
        font_family="Arial", fill="#D97706", font_weight="bold"))

    # Student stickman
    stickman(dwg, 530, 240, "You", color="#2563EB")

    dwg.save()
    return fname


def make_vs_diagram(item1: str, item2: str,
                    pts1: list, pts2: list) -> str:
    """VS comparison cartoon"""
    fname = (f"C:/EIRA/data/doodles/"
             f"vs_{datetime.now().strftime('%H%M%S')}.svg")
    h   = max(len(pts1), len(pts2))*30 + 200
    dwg = svgwrite.Drawing(fname, size=(620, h))
    dwg.add(dwg.rect(insert=(0,0), size=(620,h), fill="white"))

    # Title
    dwg.add(dwg.text(f"{item1}  VS  {item2}", insert=(310,36),
        text_anchor="middle", font_size="18px",
        font_family="Arial", fill="#1E1B4B", font_weight="bold"))

    # Left header
    draw_box(dwg, 20, 55, 260, 42, item1,
             bg="#EFF6FF", border="#2563EB", tc="#2563EB")
    # Right header
    draw_box(dwg, 340, 55, 260, 42, item2,
             bg="#ECFDF5", border="#059669", tc="#059669")
    # VS circle
    dwg.add(dwg.circle(center=(310,76), r=20, fill="#1E1B4B"))
    dwg.add(dwg.text("VS", insert=(310,81),
        text_anchor="middle", font_size="11px",
        font_family="Arial", fill="white", font_weight="bold"))

    # Divider
    dwg.add(dwg.line(start=(310,110), end=(310,h-20),
        stroke="#E5E7EB", stroke_width=1.5))

    # Points
    for i, p in enumerate(pts1):
        dwg.add(dwg.text(f"✓  {p}", insert=(30, 120+i*30),
            font_size="11px", font_family="Arial", fill="#2563EB"))
    for i, p in enumerate(pts2):
        dwg.add(dwg.text(f"✓  {p}", insert=(350, 120+i*30),
            font_size="11px", font_family="Arial", fill="#059669"))

    dwg.save()
    return fname


def make_timeline(events: list, title: str = "Timeline") -> str:
    """Timeline diagram"""
    fname = (f"C:/EIRA/data/doodles/"
             f"timeline_{datetime.now().strftime('%H%M%S')}.svg")
    w   = max(600, len(events)*120+80)
    dwg = svgwrite.Drawing(fname, size=(w, 200))
    dwg.add(dwg.rect(insert=(0,0), size=(w,200), fill="white"))

    dwg.add(dwg.text(title, insert=(w//2,30),
        text_anchor="middle", font_size="16px",
        font_family="Arial", fill="#1E1B4B", font_weight="bold"))

    # Main line
    dwg.add(dwg.line(start=(60,100), end=(w-60,100),
        stroke="#7C3AED", stroke_width=2))

    colors = ["#7C3AED","#2563EB","#059669","#D97706","#DC2626"]
    gap = (w-120)//(len(events))

    for i, ev in enumerate(events):
        x   = 60 + i*gap + gap//2
        col = colors[i % len(colors)]
        dwg.add(dwg.circle(center=(x,100), r=8,
            fill=col, stroke="white", stroke_width=2))
        if i % 2 == 0:
            dwg.add(dwg.line(start=(x,92), end=(x,65),
                stroke=col, stroke_width=1.5))
            dwg.add(dwg.text(ev, insert=(x,58),
                text_anchor="middle", font_size="10px",
                font_family="Arial", fill=col, font_weight="bold"))
        else:
            dwg.add(dwg.line(start=(x,108), end=(x,135),
                stroke=col, stroke_width=1.5))
            dwg.add(dwg.text(ev, insert=(x,148),
                text_anchor="middle", font_size="10px",
                font_family="Arial", fill=col, font_weight="bold"))

    dwg.save()
    return fname


# ── Test ────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing EIRA Doodle Maker...")

    f1 = make_array_diagram([10,25,7,3,18], "My Array")
    print(f"Array SVG: {f1}")
    open_svg(f1)

    f2 = make_flowchart(
        ["Start","Read Input","Process","Show Output","End"],
        "Basic Program Flow"
    )
    print(f"Flowchart: {f2}")
    open_svg(f2)

    f3 = make_concept_cartoon(
        "Binary Search",
        "Find middle, compare target, go left or right. Repeat!"
    )
    print(f"Concept: {f3}")
    open_svg(f3)

    f4 = make_vs_diagram(
        "Array","Linked List",
        ["Fast access O(1)","Fixed size","Less memory"],
        ["Dynamic size","Easy insert","No wasted space"]
    )
    print(f"VS: {f4}")
    open_svg(f4)

    f5 = make_timeline(
        ["Phase 1","Phase 2","Phase 3","Phase 4","Phase 5"],
        "EIRA Build Timeline"
    )
    print(f"Timeline: {f5}")
    open_svg(f5)

    print("\nAll doodles done!")