#!/usr/bin/env python3
"""Build-time renderer for news-image-20261124 v2.
Draws a 1024x1024 newspaper front page summarising Tuesday 24 Nov 2026.
Runs ONLY here (Pillow available). Never run by the grader.
Deterministic: no timestamps, no randomness, fixed font paths.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 18, 18)
NAVY = (28, 42, 74)
GREY = (90, 86, 76)
LIGHT = (232, 226, 210)
MAPSEA = (205, 224, 222)
MAPLAND = (216, 209, 172)
MAPBORDER = (138, 127, 90)
GOLD = (176, 132, 24)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon(d, kind, cx, cy, s, col):
    u = s / 10.0
    if kind == "chip":
        d.rectangle([cx - 3 * u, cy - 3 * u, cx + 3 * u, cy + 3 * u],
                    outline=col, width=max(2, int(u)))
        d.rectangle([cx - 1.4 * u, cy - 1.4 * u, cx + 1.4 * u, cy + 1.4 * u], fill=col)
        for i in (-2, 0, 2):
            d.line([cx + i * u, cy - 3 * u, cx + i * u, cy - 4.6 * u], fill=col, width=max(1, int(u * 0.7)))
            d.line([cx + i * u, cy + 3 * u, cx + i * u, cy + 4.6 * u], fill=col, width=max(1, int(u * 0.7)))
            d.line([cx - 3 * u, cy + i * u, cx - 4.6 * u, cy + i * u], fill=col, width=max(1, int(u * 0.7)))
            d.line([cx + 3 * u, cy + i * u, cx + 4.6 * u, cy + i * u], fill=col, width=max(1, int(u * 0.7)))
    elif kind == "globe":
        d.ellipse([cx - 4 * u, cy - 4 * u, cx + 4 * u, cy + 4 * u], outline=col, width=max(2, int(u)))
        d.ellipse([cx - 1.6 * u, cy - 4 * u, cx + 1.6 * u, cy + 4 * u], outline=col, width=max(1, int(u * 0.7)))
        d.line([cx - 4 * u, cy, cx + 4 * u, cy], fill=col, width=max(1, int(u * 0.7)))
        d.arc([cx - 4 * u, cy - 2 * u, cx + 4 * u, cy + 2 * u], 200, 340, fill=col, width=max(1, int(u * 0.7)))
        d.arc([cx - 4 * u, cy - 2 * u, cx + 4 * u, cy + 2 * u], 20, 160, fill=col, width=max(1, int(u * 0.7)))
    elif kind == "radar":
        d.ellipse([cx - 4 * u, cy - 4 * u, cx + 4 * u, cy + 4 * u], outline=col, width=max(2, int(u)))
        d.ellipse([cx - 2 * u, cy - 2 * u, cx + 2 * u, cy + 2 * u], outline=col, width=max(1, int(u * 0.7)))
        d.line([cx, cy, cx + 3.4 * u, cy - 3.4 * u], fill=col, width=max(2, int(u)))
        d.ellipse([cx - 0.7 * u, cy - 0.7 * u, cx + 0.7 * u, cy + 0.7 * u], fill=col)
    elif kind == "ship":
        d.polygon([(cx - 4 * u, cy + 1 * u), (cx + 4 * u, cy + 1 * u),
                   (cx + 2.6 * u, cy + 3.6 * u), (cx - 2.6 * u, cy + 3.6 * u)], fill=col)
        d.line([cx, cy + 1 * u, cx, cy - 3.6 * u], fill=col, width=max(2, int(u)))
        d.polygon([(cx, cy - 3.6 * u), (cx, cy - 0.6 * u), (cx + 2.4 * u, cy - 0.6 * u)], fill=col)
        d.line([cx - 4.6 * u, cy + 4.4 * u, cx + 4.6 * u, cy + 4.4 * u], fill=col, width=max(1, int(u * 0.7)))
    elif kind == "oil":
        d.polygon([(cx, cy - 4.4 * u), (cx + 3 * u, cy + 0.4 * u), (cx - 3 * u, cy + 0.4 * u)], fill=col)
        d.ellipse([cx - 3 * u, cy - 0.6 * u, cx + 3 * u, cy + 4.4 * u], fill=col)
    elif kind == "drone":
        d.ellipse([cx - 4.4 * u, cy - 4 * u, cx - 2 * u, cy - 1.6 * u], outline=col, width=max(1, int(u * 0.8)))
        d.ellipse([cx + 2 * u, cy - 4 * u, cx + 4.4 * u, cy - 1.6 * u], outline=col, width=max(1, int(u * 0.8)))
        d.ellipse([cx - 4.4 * u, cy + 1.6 * u, cx - 2 * u, cy + 4 * u], outline=col, width=max(1, int(u * 0.8)))
        d.ellipse([cx + 2 * u, cy + 1.6 * u, cx + 4.4 * u, cy + 4 * u], outline=col, width=max(1, int(u * 0.8)))
        d.rectangle([cx - 1.6 * u, cy - 1.2 * u, cx + 1.6 * u, cy + 1.2 * u], fill=col)
    elif kind == "bus":
        d.rounded_rectangle([cx - 4.2 * u, cy - 3 * u, cx + 4.2 * u, cy + 2.6 * u],
                            radius=int(u), outline=col, width=max(2, int(u)))
        d.rectangle([cx - 3 * u, cy - 1.8 * u, cx + 3 * u, cy + 0.2 * u], outline=col, width=max(1, int(u * 0.7)))
        d.ellipse([cx - 3 * u, cy + 2.6 * u, cx - 1.4 * u, cy + 4.2 * u], fill=col)
        d.ellipse([cx + 1.4 * u, cy + 2.6 * u, cx + 3 * u, cy + 4.2 * u], fill=col)
    elif kind == "scales":
        d.line([cx, cy - 4 * u, cx, cy + 3.6 * u], fill=col, width=max(2, int(u)))
        d.line([cx - 3.6 * u, cy - 2.4 * u, cx + 3.6 * u, cy - 2.4 * u], fill=col, width=max(2, int(u)))
        d.arc([cx - 4.4 * u, cy - 2.4 * u, cx - 1.6 * u, cy + 0.4 * u], 0, 180, fill=col, width=max(1, int(u * 0.8)))
        d.arc([cx + 1.6 * u, cy - 2.4 * u, cx + 4.4 * u, cy + 0.4 * u], 0, 180, fill=col, width=max(1, int(u * 0.8)))
        d.line([cx - 2 * u, cy + 3.6 * u, cx + 2 * u, cy + 3.6 * u], fill=col, width=max(2, int(u)))
    elif kind == "chart":
        d.line([cx - 4 * u, cy + 4 * u, cx + 4.4 * u, cy + 4 * u], fill=col, width=max(1, int(u * 0.8)))
        d.line([cx - 4 * u, cy + 4 * u, cx - 4 * u, cy - 4 * u], fill=col, width=max(1, int(u * 0.8)))
        d.line([cx - 3 * u, cy + 1 * u, cx - 1 * u, cy - 1.4 * u, cx + 1 * u, cy + 0.4 * u, cx + 3.4 * u, cy - 3.4 * u],
               fill=col, width=max(2, int(u)))
        d.polygon([(cx + 3.4 * u, cy - 3.4 * u), (cx + 3.4 * u, cy - 1.8 * u), (cx + 1.8 * u, cy - 3.4 * u)], fill=col)
    elif kind == "shield":
        d.polygon([(cx - 3.4 * u, cy - 3.6 * u), (cx + 3.4 * u, cy - 3.6 * u),
                   (cx + 3.4 * u, cy + 0.4 * u), (cx, cy + 4.4 * u), (cx - 3.4 * u, cy + 0.4 * u)],
                  outline=col, width=max(2, int(u)))
        d.line([cx - 1.4 * u, cy, cx, cy + 1.6 * u, cx + 1.8 * u, cy - 1.8 * u], fill=col, width=max(2, int(u)))
    elif kind == "ball":
        d.ellipse([cx - 3.8 * u, cy - 3.8 * u, cx + 3.8 * u, cy + 3.8 * u], outline=col, width=max(2, int(u)))
        d.polygon([(cx, cy - 1.4 * u), (cx + 1.4 * u, cy - 0.4 * u), (cx + 0.9 * u, cy + 1.2 * u),
                   (cx - 0.9 * u, cy + 1.2 * u), (cx - 1.4 * u, cy - 0.4 * u)], fill=col)
        for dx, dy in ((0, -3.8), (3.6, -1.2), (2.2, 3), (-2.2, 3), (-3.6, -1.2)):
            d.line([cx, cy - 1.4 * u, cx + dx * u, cy + dy * u], fill=col, width=max(1, int(u * 0.7)))
    elif kind == "trophy":
        d.polygon([(cx - 1.8 * u, cy - 3.6 * u), (cx + 1.8 * u, cy - 3.6 * u),
                   (cx + 1.2 * u, cy + 0.6 * u), (cx - 1.2 * u, cy + 0.6 * u)], fill=col)
        d.arc([cx - 3.6 * u, cy - 3.6 * u, cx - 1 * u, cy - 0.6 * u], 90, 270, fill=col, width=max(1, int(u * 0.8)))
        d.arc([cx + 1 * u, cy - 3.6 * u, cx + 3.6 * u, cy - 0.6 * u], 270, 90, fill=col, width=max(1, int(u * 0.8)))
        d.line([cx, cy + 0.6 * u, cx, cy + 2.6 * u], fill=col, width=max(2, int(u)))
        d.line([cx - 2 * u, cy + 3.4 * u, cx + 2 * u, cy + 3.4 * u], fill=col, width=max(2, int(u)))
    elif kind == "lock":
        d.rectangle([cx - 3 * u, cy - 0.4 * u, cx + 3 * u, cy + 4 * u], outline=col, width=max(2, int(u)))
        d.arc([cx - 2 * u, cy - 3.4 * u, cx + 2 * u, cy + 0.6 * u], 180, 360, fill=col, width=max(1, int(u * 0.9)))
        d.ellipse([cx - 0.7 * u, cy + 0.8 * u, cx + 0.7 * u, cy + 2.2 * u], fill=col)
    elif kind == "gavel":
        d.line([cx - 3.4 * u, cy + 3.4 * u, cx + 3.4 * u, cy - 3.4 * u], fill=col, width=max(2, int(u)))
        d.line([cx - 1 * u, cy - 3.8 * u, cx + 1.6 * u, cy - 1.2 * u], fill=col, width=max(3, int(u * 1.4)))
        d.line([cx - 3.8 * u, cy + 3.4 * u, cx + 3.8 * u, cy + 3.4 * u], fill=col, width=max(2, int(u)))
    elif kind == "rocket":
        d.polygon([(cx, cy - 4.4 * u), (cx + 1.8 * u, cy - 0.6 * u), (cx + 1.8 * u, cy + 2 * u),
                   (cx, cy + 3.4 * u), (cx - 1.8 * u, cy + 2 * u), (cx - 1.8 * u, cy - 0.6 * u)], fill=col)
        d.ellipse([cx - 0.8 * u, cy - 1.6 * u, cx + 0.8 * u, cy + 0 * u], fill=PAPER)
        d.polygon([(cx - 1.8 * u, cy + 2 * u), (cx - 3.2 * u, cy + 4.2 * u), (cx - 1.2 * u, cy + 3.4 * u)], fill=col)
        d.polygon([(cx + 1.8 * u, cy + 2 * u), (cx + 3.2 * u, cy + 4.2 * u), (cx + 1.2 * u, cy + 3.4 * u)], fill=col)


# ---------------------------------------------------------------- map data
N_AMERICA = [(-168, 66), (-150, 70), (-140, 70), (-130, 71), (-120, 72), (-110, 73),
             (-100, 73), (-95, 80), (-85, 80), (-80, 73), (-75, 70), (-68, 62),
             (-65, 60), (-58, 55), (-55, 52), (-60, 47), (-65, 44), (-70, 44),
             (-75, 38), (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-89, 30),
             (-90, 21), (-94, 18), (-97, 16), (-92, 15), (-87, 13), (-83, 9),
             (-80, 8), (-77, 7), (-80, 4), (-81, 1), (-80, 4), (-85, 11),
             (-90, 14), (-95, 16), (-97, 16), (-101, 18), (-105, 20), (-108, 23),
             (-112, 29), (-117, 33), (-122, 37), (-124, 42), (-124, 48), (-130, 55),
             (-140, 60), (-150, 59), (-158, 58), (-165, 60), (-168, 66)]
GREENLAND = [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-25, 70),
             (-20, 74), (-30, 78), (-45, 78), (-55, 76), (-60, 74), (-58, 70)]
S_AMERICA = [(-80, 10), (-75, 11), (-72, 12), (-68, 11), (-62, 10), (-58, 8),
             (-54, 6), (-52, 4), (-50, 0), (-48, -2), (-44, -3), (-40, -5),
             (-35, -8), (-37, -13), (-39, -17), (-40, -22), (-45, -24), (-48, -27),
             (-52, -32), (-58, -35), (-62, -39), (-65, -41), (-68, -46), (-70, -50),
             (-69, -53), (-71, -54), (-73, -50), (-73, -44), (-73, -37), (-72, -30),
             (-70, -22), (-70, -18), (-75, -15), (-78, -10), (-81, -6), (-81, -2),
             (-80, 2), (-79, 6), (-77, 8)]
EUROPE = [(-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 47), (-2, 49), (0, 50),
          (2, 51), (4, 53), (7, 54), (8, 57), (10, 58), (12, 56), (18, 56),
          (21, 55), (24, 58), (26, 59), (28, 60), (30, 62), (30, 65), (28, 68),
          (25, 70), (20, 70), (16, 69), (13, 66), (10, 64), (6, 62), (5, 60),
          (5, 58), (2, 57), (-2, 57), (-4, 53), (-5, 50), (-6, 49), (-5, 48),
          (-2, 47), (-4, 44), (-8, 43), (-9, 39), (-9, 37), (-6, 36), (-4, 36),
          (0, 38), (3, 42), (7, 44), (10, 44), (12, 45), (14, 45), (16, 44),
          (18, 41), (19, 42), (21, 40), (23, 40), (25, 39), (26, 38), (27, 41),
          (28, 42), (26, 44), (24, 45), (22, 44), (20, 44), (19, 42), (17, 40),
          (16, 40), (15, 44), (12, 44), (10, 44), (8, 44), (6, 43), (3, 43),
          (0, 39), (-1, 38), (-3, 37), (-6, 36)]
AFRICA = [(-6, 35), (-2, 35), (2, 37), (8, 37), (10, 37), (11, 34), (14, 33),
          (18, 33), (20, 32), (25, 32), (30, 31), (32, 31), (34, 28), (36, 26),
          (37, 22), (38, 20), (39, 18), (41, 15), (43, 12), (46, 11), (48, 11),
          (51, 12), (50, 10), (48, 6), (46, 3), (42, 0), (41, -2), (40, -6),
          (39, -10), (37, -14), (35, -18), (33, -22), (32, -26), (30, -29),
          (28, -33), (25, -34), (20, -35), (18, -33), (17, -29), (15, -27),
          (14, -23), (13, -19), (12, -15), (13, -11), (12, -8), (9, -3), (9, 1),
          (9, 4), (6, 4), (3, 6), (0, 6), (-4, 5), (-8, 5), (-11, 7), (-13, 8),
          (-15, 11), (-17, 13), (-17, 15), (-16, 19), (-16, 22), (-15, 25),
          (-13, 28), (-10, 30), (-8, 32), (-6, 34)]
ASIA = [(28, 68), (32, 68), (36, 66), (40, 66), (44, 68), (50, 69), (55, 68),
        (60, 69), (66, 70), (72, 72), (78, 73), (84, 74), (90, 75), (98, 76),
        (105, 77), (112, 76), (120, 74), (128, 72), (135, 72), (142, 72),
        (150, 70), (158, 69), (165, 66), (170, 66), (178, 65), (178, 62),
        (170, 60), (165, 60), (162, 56), (160, 53), (158, 51), (156, 51),
        (152, 56), (150, 59), (146, 59), (142, 55), (142, 50), (140, 46),
        (138, 44), (135, 43), (132, 43), (130, 42), (128, 38), (126, 38),
        (124, 40), (122, 38), (120, 35), (122, 32), (121, 28), (119, 25),
        (116, 23), (112, 22), (110, 20), (108, 18), (108, 12), (106, 10),
        (104, 9), (101, 8), (99, 8), (98, 12), (96, 14), (94, 16), (92, 19),
        (91, 22), (89, 22), (87, 21), (85, 19), (82, 16), (80, 13), (78, 9),
        (76, 8), (75, 11), (74, 14), (73, 18), (72, 20), (70, 21), (68, 23),
        (66, 25), (63, 25), (61, 25), (58, 25), (56, 27), (54, 27), (52, 28),
        (50, 29), (48, 30), (46, 29), (44, 29), (42, 29), (40, 30), (38, 32),
        (36, 36), (34, 36), (32, 36), (30, 36), (28, 39), (27, 40), (26, 41),
        (27, 42), (28, 44), (30, 46), (32, 48), (34, 50), (36, 52), (38, 55),
        (40, 58), (40, 61), (38, 63), (35, 65), (32, 67), (30, 68)]
AUSTRALIA = [(113, -22), (114, -27), (115, -32), (115, -35), (118, -35), (122, -34),
             (124, -33), (127, -32), (130, -32), (132, -32), (134, -33), (136, -35),
             (138, -35), (140, -38), (143, -39), (146, -39), (149, -37), (150, -37),
             (153, -32), (153, -27), (152, -24), (150, -22), (148, -20), (146, -19),
             (144, -16), (142, -14), (142, -11), (140, -13), (138, -14), (136, -12),
             (134, -12), (132, -12), (130, -13), (128, -14), (126, -14), (124, -15),
             (122, -17), (120, -19), (118, -20), (115, -21), (113, -22)]
UK = [(-5, 50), (-4, 51), (-3, 53), (-4, 55), (-5, 56), (-4, 57), (-3, 58),
      (-2, 57), (-1, 57), (0, 55), (0, 53), (1, 51), (0, 51), (-2, 51), (-4, 50)]
JAPAN = [(130, 31), (131, 32), (132, 33), (133, 34), (135, 34), (136, 35),
         (138, 35), (139, 37), (140, 39), (141, 41), (142, 42), (143, 43),
         (145, 44), (144, 43), (142, 42), (141, 40), (140, 38), (139, 36),
         (137, 35), (135, 34), (133, 34), (131, 33)]
INDONESIA = [(95, 5), (98, 4), (100, 1), (102, -1), (104, -3), (106, -5),
             (108, -6), (110, -7), (112, -7), (114, -8), (116, -9), (118, -9),
             (120, -10), (122, -10), (124, -10), (126, -9), (128, -8), (130, -6),
             (131, -3), (131, -1), (129, 0), (127, 1), (125, 1), (123, 1),
             (121, 0), (119, 0), (117, 0), (115, -1), (113, -2), (111, -3),
             (109, -2), (107, -3), (105, -2), (103, 0), (101, 1), (99, 3), (97, 4)]
NZ = [(167, -45), (168, -44), (170, -43), (172, -42), (174, -41), (176, -39),
      (178, -38), (177, -38), (175, -40), (173, -41), (172, -43), (170, -44),
      (168, -46)]
CONTINENTS = [N_AMERICA, GREENLAND, S_AMERICA, EUROPE, AFRICA, ASIA,
              AUSTRALIA, UK, JAPAN, INDONESIA, NZ]

LAT_TOP, LAT_BOT = 84.0, -58.0


def project(lon, lat, mx, my, mw, mh):
    x = mx + (lon + 180.0) / 360.0 * mw
    y = my + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * mh
    return (x, y)


# ---------------------------------------------------------------- story data
LEADS = [
    (1, "TECH · THE LEAD STORY", "chip",
     "Huang is back: Nvidia board reinstates its CEO",
     "Nvidia reinstated Jensen Huang as chief executive on Monday after "
     "Donald Trump pressed the board, saying he posed no security risk. "
     "Shares leapt 31 percent."),
    (2, "CLIMATE · ANTALYA", "globe",
     "COP31 in ruins as talks end with no deal",
     "The COP31 climate summit collapsed after more than 190 countries "
     "failed to agree a final pact, because the draft never mentioned "
     "fossil fuels. Erdogan promised more talks."),
    (3, "SECURITY · NATO'S EASTERN FLANK", "radar",
     "NATO vows to defend space as satellite fear grows",
     "NATO will defend against threats in space after reports Russia may "
     "launch a nuclear-armed satellite within 60 days. The alliance "
     "counts 25 airspace violations this year."),
]

GRID = [
    (4, "WAR · LIBYA", "ship",
     "Ukraine sinks Russian warship off Libya",
     "Kyiv says its drones sank a Russian corvette at Benghazi. Tripoli "
     "demanded answers from Kyiv."),
    (5, "GULF · SANCTIONS", "oil",
     "Iran vows to fight US naval blockade",
     "Tehran says it will use every tool against a US blockade as the UK "
     "logs record Hormuz attacks."),
    (6, "USA · CRIME", "drone",
     "US drone helps capture 'El Chapo Isidro'",
     "Mexico will try Fausto Isidro Meza Flores at home after a US drone "
     "helped track him in Sinaloa."),
    (7, "DISASTER · UAE", "bus",
     "11 dead in UAE coach crash",
     "Eleven people died when a coach hit a truck in Ras al-Khaimah, the "
     "UAE's deadliest crash this year."),
    (8, "JUSTICE · THE HAGUE", "scales",
     "14 nations back ICJ genocide ruling",
     "Britain, Spain, Canada and Australia are among 14 states backing "
     "the court's Rohingya verdict."),
    (9, "MARKETS · ASIA", "chart",
     "Asian stocks rally as AI panic eases",
     "Seoul jumped over 6 percent and Tokyo 3.9 percent as Jensen "
     "Huang's return revived the AI trade."),
    (10, "USA · POLITICS", "shield",
     "Pentagon rebukes Canada on defence",
     "Washington criticised Ottawa's defence spending and its review of "
     "the F-35 fighter purchase."),
    (11, "SPORT · FOOTBALL", "ball",
     "City host Napoli as De Bruyne returns",
     "Kevin De Bruyne returns to the Etihad as Napoli visit City, who "
     "chase a third straight win."),
    (12, "SPORT · TENNIS", "trophy",
     "Davis Cup Final 8 opens in Bologna",
     "Czechia meet Canada in the opening quarter-final today. Italy "
     "face South Korea on Wednesday."),
    (13, "TECH · CYBER", "lock",
     "CrowdStrike buys Zscaler in $44bn deal",
     "The cybersecurity giants merge in a $43.9 billion all-stock deal as "
     "AI-driven attacks mount."),
    (14, "TECH · LAW", "gavel",
     "States sue SpaceX over Grok images",
     "Oregon and Virginia sued SpaceX, alleging Grok's image tool "
     "generated child abuse material."),
    (15, "SCIENCE · SPACE", "rocket",
     "Pakistani astronaut set for Tiangong",
     "Zeeshan Ali will be the first foreign astronaut aboard China's "
     "space station on Shenzhou-24."),
]

# num: (lon, lat, key label, dx, dy) — dx/dy shift the numbered pin off the
# true spot with a leader line, so close pins stay readable.
PINS = {
    1: (-74, 41, "Huang · USA", 12, 10),
    2: (30.7, 36.9, "COP31 · Turkey", 0, -12),
    3: (4.4, 50.8, "NATO · Brussels", -14, -8),
    4: (20.1, 32.1, "Warship · Libya", 0, 12),
    5: (56.5, 26.5, "Hormuz · Gulf", -13, -9),
    6: (-107, 24.8, "El Chapo · Mexico", -11, 9),
    7: (55.9, 25.8, "Crash · UAE", 13, 10),
    8: (4.3, 52.1, "ICJ · The Hague", 13, -11),
    9: (127, 37.5, "Rally · Seoul", 0, -12),
    10: (-75.7, 45.4, "Rebuke · Canada", 13, -10),
    11: (-2.24, 53.48, "City · Manchester", -16, 10),
    12: (11.34, 44.49, "Davis Cup · Bologna", 15, -6),
    13: (-97.7, 30.3, "Merger · Texas", 11, 8),
    14: (-122.7, 45.5, "Grok · Oregon", -12, -9),
    15: (73.1, 33.7, "Astronaut · Pakistan", 0, -12),
}

ALSO = [
    "China sentences official to death for spying.",
    "US blacklists Megaspeed over the Nvidia scandal.",
    "Zelensky urges talks with Russia, US and Europe.",
    "Russian jets entered South Korea's air zone.",
    "Bukele names three soldiers killed in Haiti.",
    "Gaza strikes kill three, including UNRWA worker.",
    "Houthis say Saudi strike killed 17 in Hodeida.",
    "Somalia, Uganda step up fight against al-Shabaab.",
    "5.6 quake strikes Nepal near the China border.",
    "Pennsylvania records ninth measles death.",
    "Guterres wants an AI-risk framework in a year.",
    "Car bomb hits government offices in Colombia.",
    "Iran gives singer Parastoo Ahmadi 74 lashes.",
    "SpaceX, Tesla directors discuss $3.5tn merger.",
    "Oracle up 13% as OpenAI deal funding confirmed.",
    "Amazon to buy Decart AI chip tech for $7.5bn.",
    "Arm extends CEO Rene Haas's tenure to 2033.",
    "Hernández de Cos tipped to lead the ECB.",
    "Macron wants strategic rare-earth reserves.",
    "Wars choke food aid for 7.3 million, WFP warns.",
    "Floods hit the Galápagos amid El Niño fears.",
]

KPIS = [
    ("+31%", "NVIDIA SHARES"),
    ("+$900BN", "MARKET CAP ADDED IN A DAY"),
    ("25", "AIRSPACE VIOLATIONS IN 2026"),
    ("90+", "NATIONS REJECTED COP31 DRAFT"),
    ("$43.9BN", "CROWDSTRIKE–ZSCALER DEAL"),
    ("7.3M", "PEOPLE'S AID AT RISK"),
]

REGIONS = [
    ("AMERICAS", 14, NAVY),
    ("EUROPE", 8, RED),
    ("ASIA-PACIFIC", 6, GOLD),
    ("MIDDLE EAST", 5, (0, 110, 90)),
    ("AFRICA", 3, (110, 60, 140)),
]

TIMELINE = [
    ("01:06", "Bukele names Haiti dead"),
    ("02:09", "US drone aided El Chapo capture"),
    ("02:15", "NATO vows space defence"),
    ("02:37", "China death sentence for spying"),
    ("03:00", "ICJ ruling backed by 14 nations"),
    ("08:02", "Davis Cup Final 8 opens today"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 10
    CW = (W - 2 * M - 12) // 3

    # ---- masthead (0-128)
    d.text((M, 2), "THE WORLD IN ONE DAY", font=F(SERIF, 58), fill=INK)
    gx, gy, gr = W - M - 28, 30, 26
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=INK, width=3)
    d.ellipse([gx - 10, gy - gr, gx + 10, gy + gr], outline=INK, width=2)
    d.line([gx - gr, gy, gx + gr, gy], fill=INK, width=2)
    d.arc([gx - gr, gy - 12, gx + gr, gy + 12], 200, 340, fill=INK, width=2)
    d.arc([gx - gr, gy - 12, gx + gr, gy + 12], 20, 160, fill=INK, width=2)
    d.line([M, 72, W - M, 72], fill=INK, width=2)
    d.text((M, 78), "TUESDAY, 24 NOVEMBER 2026", font=F(SANS_B, 15), fill=RED)
    t = "No. 24  •  TUESDAY EDITION"
    f_no = F(SANS_B, 13)
    d.text((W - M - d.textlength(t, font=f_no), 80), t, font=f_no, fill=INK)
    d.line([M, 100, W - M, 100], fill=INK, width=1)
    d.rectangle([M, 106, W - M, 128], fill=RED)
    band = "36 STORIES  •  5 REGIONS  •  EVERY ONE DATED  •  TUESDAY 24 NOVEMBER 2026"
    f_band = F(SANS_B, 13)
    d.text(((W - d.textlength(band, font=f_band)) / 2, 111), band, font=f_band, fill=(255, 255, 255))

    # ---- KPI strip (132-170)
    y = 132
    kw = (W - 2 * M - 5 * 6) // 6
    f_kpi_n = F(SANS_B, 20)
    f_kpi_l = F(SANS_B, 8)
    for i, (num, lab) in enumerate(KPIS):
        x = M + i * (kw + 6)
        d.rectangle([x, y, x + kw, y + 38], fill=NAVY)
        d.text((x + 7, y + 3), num, font=f_kpi_n, fill=(255, 255, 255))
        d.text((x + 7, y + 25), lab, font=f_kpi_l, fill=(210, 210, 200))

    # ---- region bar (174-198)
    y = 174
    total = sum(c for _, c, _ in REGIONS)
    bx = M
    for name, cnt, col in REGIONS:
        seg = int((W - 2 * M) * cnt / total)
        d.rectangle([bx, y, bx + seg, y + 10], fill=col)
        bx += seg
    f_reg = F(SANS_B, 10)
    rx = M
    for name, cnt, col in REGIONS:
        d.rectangle([rx, y + 14, rx + 9, y + 23], fill=col)
        lab = "%s %d" % (name, cnt)
        d.text((rx + 12, y + 13), lab, font=f_reg, fill=INK)
        rx += 12 + d.textlength(lab, font=f_reg) + 16
    d.text((rx, y + 13), "— SHARE OF TODAY'S 36 STORIES", font=F(SANS, 10), fill=GREY)

    # ---- timeline (202-256)
    y = 202
    d.text((M, y), "THE DAY IN UTC", font=F(SANS_B, 12), fill=RED)
    d.line([M, y + 15, W - M, y + 15], fill=INK, width=1)
    tw = (W - 2 * M) // 6
    f_tt = F(SANS_B, 11)
    f_td = F(SANS, 9)
    for i, (tm, txt) in enumerate(TIMELINE):
        x = M + i * tw
        d.ellipse([x + 2, y + 20, x + 9, y + 27], fill=RED)
        d.text((x, y + 30), tm, font=f_tt, fill=INK)
        d.text((x, y + 43), txt, font=f_td, fill=INK)

    # ---- lead stories (divider 260, content 266-440)
    y = 260
    d.line([M, y, W - M, y], fill=INK, width=2)
    ly = y + 6
    f_kick = F(SANS_B, 10)
    f_head = F(SERIF, 17)
    f_body = F(SANS, 11)
    for num, tag, kind, head, body in LEADS:
        x = M + (num - 1) * (CW + 6)
        d.text((x, ly), tag, font=f_kick, fill=RED)
        iy = ly + 16
        d.rectangle([x, iy, x + CW, iy + 72], fill=LIGHT, outline=INK, width=1)
        icon(d, kind, x + CW // 2, iy + 36, 44, NAVY if kind != "globe" else (0, 110, 90))
        if kind == "globe":
            d.line([x + CW // 2 - 28, iy + 14, x + CW // 2 + 28, iy + 58], fill=RED, width=3)
        d.text((x + CW - 22, iy + 54), "#%d" % num, font=F(SANS_B, 10), fill=GREY)
        hy = iy + 78
        hl = wrap(d, head, f_head, CW)
        hy = draw_lines(d, hl, x, hy, f_head, INK, 20)
        bl = wrap(d, body, f_body, CW)
        draw_lines(d, bl[:3], x, hy + 4, f_body, INK, 13)

    # ---- grid stories 4-15 (divider 444, cards 450-707)
    gy = 444
    d.line([M, gy, W - M, gy], fill=INK, width=2)
    gh, gap = 62, 3
    f_gtag = F(SANS_B, 9)
    f_ghead = F(SANS_B, 12)
    f_gbody = F(SANS, 10)
    for idx, (num, tag, kind, head, body) in enumerate(GRID):
        row, col = divmod(idx, 3)
        x = M + col * (CW + 6)
        yy = gy + 6 + row * (gh + gap)
        d.rectangle([x, yy, x + CW, yy + gh], fill=(255, 255, 255), outline=(180, 172, 150), width=1)
        icon(d, kind, x + 26, yy + 24, 30, NAVY)
        tx = x + 52
        d.text((tx, yy + 3), "%d  %s" % (num, tag), font=f_gtag, fill=RED)
        hl = wrap(d, head, f_ghead, CW - 58)
        hy = draw_lines(d, hl[:2], tx, yy + 15, f_ghead, INK, 13)
        bl = wrap(d, body, f_gbody, CW - 58)
        draw_lines(d, bl[:2], tx, hy, f_gbody, (60, 58, 50), 11)

    # ---- world map (title 711, map 729-821)
    my = 711
    d.text((M, my), "WHERE IT HAPPENED  —  NUMBERED PINS MARK STORIES 1–15",
           font=F(SANS_B, 12), fill=RED)
    map_y, map_h, map_w = 729, 92, 690
    d.rectangle([M, map_y, M + map_w, map_y + map_h], fill=MAPSEA, outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, M, map_y, map_w, map_h) for lon, lat in poly]
        d.polygon(pts, fill=MAPLAND, outline=MAPBORDER)
    f_pin = F(SANS_B, 8)
    for num, (lon, lat, lab, dx, dy) in PINS.items():
        px, py = project(lon, lat, M, map_y, map_w, map_h)
        qx, qy = px + dx, py + dy
        d.line([px, py, qx, qy], fill=RED, width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.ellipse([qx - 7, qy - 7, qx + 7, qy + 7], fill=RED, outline=(255, 255, 255), width=1)
        twd = d.textlength(str(num), font=f_pin)
        d.text((qx - twd / 2, qy - 6), str(num), font=f_pin, fill=(255, 255, 255))
    # pin key, two columns
    kx = M + map_w + 12
    d.text((kx, map_y), "PIN KEY", font=F(SANS_B, 11), fill=INK)
    f_key = F(SANS, 9)
    for i, (num, (lon, lat, lab, dx, dy)) in enumerate(sorted(PINS.items())):
        col, row = divmod(i, 8)
        xx = kx + col * 158
        yy = map_y + 16 + row * 10
        d.text((xx, yy), "%d  %s" % (num, lab), font=f_key, fill=INK)

    # ---- ALSO list (title 827, rows 848-960)
    ay = 827
    d.text((M, ay), "ALSO ON TUESDAY 24 NOVEMBER  —  21 MORE STORIES",
           font=F(SANS_B, 12), fill=RED)
    d.line([M, ay + 17, W - M, ay + 17], fill=INK, width=1)
    f_also = F(SANS, 10)
    f_also_b = F(SANS_B, 10)
    for i, txt in enumerate(ALSO):
        col, row = divmod(i, 7)
        x = M + col * (CW + 6)
        yy = ay + 21 + row * 16
        d.text((x, yy), "%d." % (16 + i), font=f_also_b, fill=RED)
        d.text((x + 24, yy), txt, font=f_also, fill=INK)

    # ---- bottom (divider 964, content 970-1020)
    by = 964
    d.line([M, by, W - M, by], fill=INK, width=2)
    by += 6
    box_w = 500
    d.rectangle([M, by, M + box_w, by + 50], outline=RED, width=1)
    d.text((M + 6, by + 3), "DATE CHECK — WHAT WAS LEFT OUT AND WHY",
           font=F(SANS_B, 10), fill=RED)
    f_dc = F(SANS, 9)
    dc = ("Huang's reinstatement and the CrowdStrike–Zscaler deal were announced "
          "on Monday 23 Nov — they lead today because markets, lawmakers and "
          "CEOs reacted on Tuesday. The ICJ's Rohingya verdict came last week; "
          "14 nations backed it on Monday. Older stories were left out.")
    dl = wrap(d, dc, f_dc, box_w - 12)
    draw_lines(d, dl[:3], M + 6, by + 17, f_dc, INK, 11)
    kx2 = M + box_w + 12
    f_cert = F(SANS_B, 9)
    d.text((kx2, by + 3), "CERTAINTY: REPORTED = confirmed  •  CLAIM = one side says so",
           font=f_cert, fill=INK)
    d.text((kx2, by + 14), "FORECAST = scheduled or predicted.",
           font=f_cert, fill=INK)
    f_src = F(SANS, 9)
    src = ("Sources: Reuters, Le Monde, AP, BBC, Al Jazeera, The Guardian, WSJ, "
           "FT, Middle East Eye, Grist, The Conversation, UEFA. First reported 22–24 Nov 2026.")
    sl = wrap(d, src, f_src, W - M - kx2)
    draw_lines(d, sl[:2], kx2, by + 28, f_src, GREY, 11)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
