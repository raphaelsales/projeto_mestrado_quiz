"""
gerar_icones.py — Gera os ícones PNG usados no app via Pillow
Execute uma vez: python3 gerar_icones.py
"""
import os
import math
from PIL import Image, ImageDraw

DEST = os.path.join(os.path.dirname(__file__), "assets", "icons")
os.makedirs(DEST, exist_ok=True)

S = 96       # tamanho do ícone em pixels
R = 20       # raio do canto do fundo
W = "#FFFFFF" # branco
T = (0, 0, 0, 0)  # transparente


def base(cor: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGBA", (S, S), T)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=R, fill=cor)
    return img, d


def salvar(img: Image.Image, nome: str):
    caminho = os.path.join(DEST, nome)
    img.save(caminho, "PNG")
    print(f"  ✓  {caminho}")


# ─── 1. Saídas de Emergência — porta + seta ────────────────────────────────────
def icone_saidas():
    img, d = base("#C0392B")

    # Moldura da porta
    d.rounded_rectangle([16, 14, 52, 78], radius=4, outline=W, width=3, fill=None)

    # Maçaneta
    d.ellipse([44, 43, 50, 49], fill=W)

    # Seta para a direita
    ax, ay = 60, 46
    d.line([(ax, ay), (ax + 18, ay)], fill=W, width=4)
    d.polygon([(ax + 14, ay - 7), (ax + 24, ay), (ax + 14, ay + 7)], fill=W)

    # Pezinhos embaixo (pessoa saindo)
    d.ellipse([55, 62, 63, 70], fill=W)   # cabeça
    d.line([(59, 70), (59, 80)], fill=W, width=3)  # corpo
    d.line([(59, 74), (54, 80)], fill=W, width=2)  # perna esq
    d.line([(59, 74), (64, 80)], fill=W, width=2)  # perna dir

    return img


# ─── 2. Extintor de Incêndio — cilindro estilizado ────────────────────────────
def icone_extintor():
    img, d = base("#D35400")

    # Corpo do extintor
    d.rounded_rectangle([30, 34, 58, 76], radius=8, fill=W)

    # Pescoço / cabeça
    d.rectangle([36, 22, 52, 36], fill=W)

    # Válvula (círculo no topo)
    d.ellipse([38, 14, 50, 26], outline=W, width=3, fill=None)

    # Mangueira (curva)
    d.arc([52, 20, 74, 42], start=270, end=90, fill=W, width=3)
    # Bico da mangueira
    d.line([(74, 31), (80, 31)], fill=W, width=4)
    d.polygon([(78, 27), (84, 31), (78, 35)], fill=W)

    # Alça lateral
    d.arc([20, 36, 36, 56], start=180, end=360, fill=W, width=3)

    return img


# ─── 3. Sinalização de Segurança — triângulo de advertência ──────────────────
def icone_sinalizacao():
    img, d = base("#B7950B")

    # Triângulo externo
    pts_ext = [(48, 10), (84, 76), (12, 76)]
    d.polygon(pts_ext, outline=W, width=4, fill=None)

    # Linha de exclamação
    d.line([(48, 30), (48, 56)], fill=W, width=5)

    # Ponto do "!"
    d.ellipse([43, 61, 53, 71], fill=W)

    return img


# ─── 4. Detecção e Alarme — sino ──────────────────────────────────────────────
def icone_alarme():
    img, d = base("#6C3483")

    # Corpo do sino (forma arredondada)
    d.ellipse([22, 24, 74, 68], fill=W)
    # Tampar a parte de baixo plana
    d.rectangle([22, 46, 74, 68], fill=W)

    # Flat bottom do sino
    d.rectangle([18, 62, 78, 70], fill=W)

    # Batoque
    d.ellipse([40, 68, 56, 80], fill=W)

    # Cabo do sino no topo
    d.line([(48, 12), (48, 26)], fill=W, width=4)
    d.line([(38, 14), (58, 14)], fill=W, width=4)

    # Ondas sonoras (arcos)
    for r_off, a_start, a_end in [(10, 300, 420), (18, 300, 420)]:
        d.arc([48 - r_off - 18, 20 - r_off + 10,
               48 + r_off + 18, 20 + r_off + 10 + 30],
              start=a_start % 360, end=a_end % 360, fill=W, width=2)

    return img


# ─── 5. Hidrantes e Mangotinhos — gota d'água ─────────────────────────────────
def icone_hidrante():
    img, d = base("#1A5276")

    # Gota: triângulo (topo) + círculo (base)
    cx = 48
    # Ponta da gota
    d.polygon([(cx, 12), (cx - 22, 54), (cx + 22, 54)], fill=W)
    # Barriga arredondada
    d.ellipse([cx - 22, 36, cx + 22, 78], fill=W)

    # "H" de hidrante em azul sobre a gota
    hc = "#1A5276"
    x0 = cx - 11
    x1 = cx + 11
    yb = 48
    yt = 68
    d.line([(x0, yb), (x0, yt)], fill=hc, width=4)
    d.line([(x1, yb), (x1, yt)], fill=hc, width=4)
    d.line([(x0, (yb + yt) // 2), (x1, (yb + yt) // 2)], fill=hc, width=4)

    return img


# ─── 6. Chama — ícone da tela inicial ────────────────────────────────────────
def icone_chama(tamanho: int = 128):
    img = Image.new("RGBA", (tamanho, tamanho), T)
    d = ImageDraw.Draw(img)

    s = tamanho
    # Chama externa (laranja)
    flame_pts = [
        (s * 0.50, s * 0.04),
        (s * 0.72, s * 0.30),
        (s * 0.80, s * 0.20),
        (s * 0.82, s * 0.55),
        (s * 0.72, s * 0.72),
        (s * 0.78, s * 0.65),
        (s * 0.76, s * 0.82),
        (s * 0.50, s * 0.96),
        (s * 0.24, s * 0.82),
        (s * 0.22, s * 0.65),
        (s * 0.28, s * 0.72),
        (s * 0.18, s * 0.55),
        (s * 0.20, s * 0.20),
        (s * 0.28, s * 0.30),
    ]
    d.polygon([(int(x), int(y)) for x, y in flame_pts], fill="#E74C3C")

    # Chama interna (amarelo)
    inner = [
        (s * 0.50, s * 0.22),
        (s * 0.63, s * 0.44),
        (s * 0.68, s * 0.38),
        (s * 0.70, s * 0.62),
        (s * 0.50, s * 0.84),
        (s * 0.30, s * 0.62),
        (s * 0.32, s * 0.38),
        (s * 0.37, s * 0.44),
    ]
    d.polygon([(int(x), int(y)) for x, y in inner], fill="#F39C12")

    # Núcleo (amarelo claro)
    cx, cy = s // 2, int(s * 0.60)
    d.ellipse([cx - 12, cy - 18, cx + 12, cy + 14], fill="#F9E79F")

    return img


# ─── Gerar todos ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Gerando ícones…")

    salvar(icone_saidas(),      "saidas.png")
    salvar(icone_extintor(),    "extintor.png")
    salvar(icone_sinalizacao(), "sinalizacao.png")
    salvar(icone_alarme(),      "alarme.png")
    salvar(icone_hidrante(),    "hidrante.png")
    salvar(icone_chama(),       "chama.png")
    salvar(icone_chama(64),     "chama_sm.png")

    print("\nPronto! Ícones salvos em assets/icons/")
