"""Draw the hero diagram: the Opera Game after 6...Nf6, White to move.

    python3 tools/board.py        (needs python-chess, for the pieces)

Dark squares are hatched, as in a nineteenth-century chess book. The solid
arrow is the move Teresa's Pawn played here, and the dashed arrows are the
next three it ranked and passed over (a run of 24 October 2026, after play
by end: it now plays Qb3, as Morphy did).

Pieces: Colin M.L. Burnett (Cburnett), BSD licence; see pieces-LICENSE.txt.
"""
import math
import chess
import chess.svg

S = 45
MOVES = "e4 e5 Nf3 d6 d4 Bg4 dxe5 Bxf3 Qxf3 dxe5 Bc4 Nf6"
PLAYED = ("f3", "b3")
PASSED = [("e1", "g1"), ("c4", "b5"), ("b1", "c3")]


def centre(sq):
    f, r = ord(sq[0]) - 97, int(sq[1]) - 1
    return (f * S + S / 2, (7 - r) * S + S / 2)


def arrow(a, b, cls, width, head):
    (x1, y1), (x2, y2) = centre(a), centre(b)
    ang = math.atan2(y2 - y1, x2 - x1)
    x2s, y2s = x2 - math.cos(ang) * head * 0.9, y2 - math.sin(ang) * head * 0.9
    x1s, y1s = x1 + math.cos(ang) * 8, y1 + math.sin(ang) * 8
    hx, hy = x2 - math.cos(ang) * head, y2 - math.sin(ang) * head
    px, py = -math.sin(ang) * head * 0.55, math.cos(ang) * head * 0.55
    return (f'<line class="{cls}" x1="{x1s:.1f}" y1="{y1s:.1f}" x2="{x2s:.1f}" y2="{y2s:.1f}" stroke-width="{width}"/>'
            f'<polygon class="{cls}-head" points="{x2:.1f},{y2:.1f} {hx + px:.1f},{hy + py:.1f} {hx - px:.1f},{hy - py:.1f}"/>')


def svg():
    b = chess.Board()
    for m in MOVES.split():
        b.push_san(m)
    out = ['<svg class="diagram" viewBox="-26 -8 412 400" role="img" aria-labelledby="diagram-title">',
           '<title id="diagram-title">The Opera Game, Paris 1858, after 6...Nf6 with White to move. '
           'A solid arrow shows the bot castling; dashed arrows show Bd5, Nc3 and Bb5+, the moves it passed over.</title>',
           '<defs><pattern id="hatch" width="4.2" height="4.2" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           '<line x1="0" y1="0" x2="0" y2="4.2" class="hatchline"/></pattern>']
    for sym, g in chess.svg.PIECES.items():
        out.append(g.replace('id="', 'id="p-'))
    out.append('</defs>')
    out.append(f'<rect x="-4" y="-4" width="{8 * S + 8}" height="{8 * S + 8}" class="frame"/>')
    for r in range(8):
        for f in range(8):
            x, y = f * S, (7 - r) * S
            out.append(f'<rect x="{x}" y="{y}" width="{S}" height="{S}" class="light"/>')
            if (f + r) % 2 == 0:
                out.append(f'<rect x="{x}" y="{y}" width="{S}" height="{S}" class="dark"/>')
    for sq, piece in b.piece_map().items():
        f, r = chess.square_file(sq), chess.square_rank(sq)
        name = ("white-" if piece.color else "black-") + chess.piece_name(piece.piece_type)
        out.append(f'<use href="#p-{name}" x="{f * S}" y="{(7 - r) * S}"/>')
    for a, c in PASSED:
        out.append(arrow(a, c, "passed", 3.2, 11))
    out.append(arrow(*PLAYED, "played", 7, 17))
    for i, ch in enumerate("abcdefgh"):
        out.append(f'<text class="coord" x="{i * S + S / 2}" y="{8 * S + 21}" text-anchor="middle">{ch}</text>')
    for r in range(8):
        out.append(f'<text class="coord" x="-14" y="{(7 - r) * S + S / 2 + 5}" text-anchor="middle">{r + 1}</text>')
    out.append('</svg>')
    return "".join(out)


if __name__ == "__main__":
    import pathlib, re
    page = pathlib.Path(__file__).parent.parent / "index.html"
    html = page.read_text()
    page.write_text(re.sub(r"(<!-- diagram:start -->).*?(<!-- diagram:end -->)",
                           lambda m: m.group(1) + "\n      " + svg() + "\n      " + m.group(2), html, flags=re.S))
    print("wrote", page.name)
