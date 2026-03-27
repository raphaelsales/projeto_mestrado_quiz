"""
main.py — Quiz Educacional: Normas Técnicas do Corpo de Bombeiros
Desenvolvido com Python 3.12 + CustomTkinter + SQLite

Projeto de Mestrado — PPGECA / IFTO
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import time
import random
import os
from datetime import datetime
from PIL import Image

from database import DatabaseManager
from questoes import QUESTOES_SEED

# ─── Carregamento de ícones ───────────────────────────────────────────────────
_ICONS_DIR = os.path.join(os.path.dirname(__file__), "assets", "icons")

def _load(nome: str, size: int = 48) -> ctk.CTkImage | None:
    """Carrega um PNG como CTkImage (suporte HiDPI/Retina)."""
    path = os.path.join(_ICONS_DIR, nome)
    if not os.path.exists(path):
        return None
    img = Image.open(path).convert("RGBA")
    return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

ICONES: dict = {}

def _carregar_icones():
    ICONES["chama"]       = _load("chama.png",       96)
    ICONES["chama_sm"]    = _load("chama_sm.png",     48)
    ICONES["saidas"]      = _load("saidas.png",       48)
    ICONES["extintor"]    = _load("extintor.png",     48)
    ICONES["sinalizacao"] = _load("sinalizacao.png",  48)
    ICONES["alarme"]      = _load("alarme.png",       48)
    ICONES["hidrante"]    = _load("hidrante.png",     48)

# ─── Configurações globais ────────────────────────────────────────────────────

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

TIMER_SEGUNDOS = 30
QUESTOES_POR_SESSAO = 10

# Metadados de cada módulo
MODULO_META: dict = {
    "Saídas de Emergência": {
        "icone_key": "saidas",
        "norma": "NBR 9077",
        "desc": "Rotas de fuga, dimensionamento e tipos de escadas",
        "cor": "#C0392B",
    },
    "Extintores de Incêndio": {
        "icone_key": "extintor",
        "norma": "NBR 12693",
        "desc": "Classes de fogo, agentes extintores e distribuição",
        "cor": "#D35400",
    },
    "Sinalização de Segurança": {
        "icone_key": "sinalizacao",
        "norma": "NBR 13434",
        "desc": "Símbolos, cores e requisitos de sinalização",
        "cor": "#B7950B",
    },
    "Detecção e Alarme": {
        "icone_key": "alarme",
        "norma": "NBR 17240",
        "desc": "Detectores, acionadores e centrais de alarme",
        "cor": "#6C3483",
    },
    "Hidrantes e Mangotinhos": {
        "icone_key": "hidrante",
        "norma": "NBR 13714",
        "desc": "Sistemas de combate por água sob pressão",
        "cor": "#1A5276",
    },
}

DIFIC_LABEL = ["Todos", "Básico", "Intermediário", "Avançado"]
DIFIC_VALOR = {"Todos": "todos", "Básico": "basico",
               "Intermediário": "intermediario", "Avançado": "avancado"}


def calcular_pontuacao(correta: bool, tempo_gasto: float) -> int:
    if not correta:
        return 0
    restante = max(0, TIMER_SEGUNDOS - tempo_gasto)
    bonus = int((restante / TIMER_SEGUNDOS) * 50)
    return 100 + bonus


def pct(acertos: int, total: int) -> float:
    return (acertos / total * 100) if total else 0.0


def estrelas(percentual: float) -> str:
    if percentual >= 90:
        return "★★★★★"
    elif percentual >= 75:
        return "★★★★☆"
    elif percentual >= 60:
        return "★★★☆☆"
    elif percentual >= 40:
        return "★★☆☆☆"
    else:
        return "★☆☆☆☆"


# ─── Aplicação Principal ──────────────────────────────────────────────────────

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Quiz Normas — Corpo de Bombeiros  |  PPGECA · IFTO")
        self.geometry("1920x1080")
        self.minsize(840, 620)

        _carregar_icones()
        self.db = DatabaseManager()
        self.db.seed_questions(QUESTOES_SEED)

        # Estado compartilhado entre telas
        self.player_name = ctk.StringVar(value="")
        self.modulo_sel: str | None = None
        self.dific_sel = ctk.StringVar(value="Todos")
        self.session_id: int | None = None
        self.quiz_resultado: dict = {}

        # Container principal
        self._cont = ctk.CTkFrame(self, fg_color="transparent")
        self._cont.pack(fill="both", expand=True)
        self._cont.grid_rowconfigure(0, weight=1)
        self._cont.grid_columnconfigure(0, weight=1)

        # Instanciar telas
        self._telas: dict[str, ctk.CTkFrame] = {}
        for Cls in (TelaHome, TelaModulos, TelaQuiz, TelaRelatorio, TelaHistorico):
            t = Cls(self._cont, self)
            self._telas[Cls.__name__] = t
            t.grid(row=0, column=0, sticky="nsew")

        self.mostrar("TelaHome")

    def mostrar(self, nome: str, **kw):
        tela = self._telas[nome]
        if hasattr(tela, "ao_mostrar"):
            tela.ao_mostrar(**kw)
        tela.tkraise()


# ─── Tela 1: Home ─────────────────────────────────────────────────────────────

class TelaHome(ctk.CTkFrame):
    def __init__(self, parent, app: App):
        super().__init__(parent, fg_color="#121212")
        self.app = app
        self._construir()

    def _construir(self):
        # Faixa superior decorativa
        faixa = ctk.CTkFrame(self, height=6, fg_color="#C0392B", corner_radius=0)
        faixa.pack(fill="x")

        # Conteúdo central
        centro = ctk.CTkFrame(self, fg_color="transparent")
        centro.pack(expand=True)

        icone_chama = ICONES.get("chama")
        if icone_chama:
            ctk.CTkLabel(centro, text="", image=icone_chama).pack(pady=(0, 8))
        else:
            ctk.CTkLabel(centro, text="🔥", font=("Segoe UI Emoji", 72)).pack(pady=(0, 8))

        ctk.CTkLabel(
            centro,
            text="Quiz Normas Técnicas",
            font=ctk.CTkFont("Segoe UI", 34, "bold"),
            text_color="#FFFFFF",
        ).pack()

        ctk.CTkLabel(
            centro,
            text="Corpo de Bombeiros — PPGECA · IFTO",
            font=ctk.CTkFont("Segoe UI", 14),
            text_color="#AAB7B8",
        ).pack(pady=(2, 30))

        # Card de acesso
        card = ctk.CTkFrame(centro, fg_color="#1E1E1E", corner_radius=16,
                            border_width=1, border_color="#2C2C2C")
        card.pack(ipadx=40, ipady=30)

        ctk.CTkLabel(
            card,
            text="Digite seu nome para começar",
            font=ctk.CTkFont("Segoe UI", 14),
            text_color="#BDC3C7",
        ).pack(pady=(0, 8))

        self._entry_nome = ctk.CTkEntry(
            card,
            textvariable=self.app.player_name,
            placeholder_text="Ex.: João Silva",
            font=ctk.CTkFont("Segoe UI", 15),
            width=320,
            height=44,
            corner_radius=10,
            border_color="#C0392B",
        )
        self._entry_nome.pack()
        self._entry_nome.bind("<Return>", lambda _: self._iniciar())

        ctk.CTkButton(
            card,
            text="  Jogar  →",
            font=ctk.CTkFont("Segoe UI", 15, "bold"),
            height=46,
            width=320,
            corner_radius=10,
            fg_color="#C0392B",
            hover_color="#A93226",
            command=self._iniciar,
        ).pack(pady=(14, 0))

        ctk.CTkButton(
            card,
            text="Ver Histórico",
            font=ctk.CTkFont("Segoe UI", 13),
            height=38,
            width=320,
            corner_radius=38,
            fg_color="transparent",
            border_width=1,
            border_color="#5D6D7E",
            text_color="#AAB7B8",
            hover_color="#1C1C1C",
            command=self._historico,
        ).pack(pady=(8, 0))

        # Rodapé
        ctk.CTkLabel(
            self,
            text="Pesquisa de Mestrado · PPGECA / IFTO  ·  2025",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color="#4D5656",
        ).pack(side="bottom", pady=12)

    def _iniciar(self):
        nome = self.app.player_name.get().strip()
        if not nome:
            self._entry_nome.configure(border_color="#E74C3C")
            messagebox.showwarning("Nome obrigatório",
                                   "Por favor, informe seu nome antes de jogar.")
            return
        self._entry_nome.configure(border_color="#C0392B")
        self.app.mostrar("TelaModulos")

    def _historico(self):
        nome = self.app.player_name.get().strip()
        if not nome:
            self._entry_nome.configure(border_color="#E74C3C")
            messagebox.showwarning("Nome obrigatório",
                                   "Informe seu nome para ver o histórico.")
            return
        self.app.mostrar("TelaHistorico")


# ─── Tela 2: Seleção de Módulo ────────────────────────────────────────────────

class TelaModulos(ctk.CTkFrame):
    def __init__(self, parent, app: App):
        super().__init__(parent, fg_color="#121212")
        self.app = app
        self._construir()

    def ao_mostrar(self):
        self._label_nome.configure(
            text=f"Olá, {self.app.player_name.get()}! Escolha um módulo:"
        )
        self._atualizar_contadores()

    def _construir(self):
        # Barra de topo
        topo = ctk.CTkFrame(self, fg_color="#1A1A1A", height=60, corner_radius=0)
        topo.pack(fill="x")
        topo.pack_propagate(False)

        ctk.CTkButton(
            topo, text="← Voltar", width=90, height=34,
            fg_color="transparent", border_width=1, border_color="#5D6D7E",
            text_color="#AAB7B8", hover_color="#1C1C1C",
            font=ctk.CTkFont("Segoe UI", 12),
            command=lambda: self.app.mostrar("TelaHome"),
        ).place(x=16, rely=0.5, anchor="w")

        self._label_nome = ctk.CTkLabel(
            topo, text="",
            font=ctk.CTkFont("Segoe UI", 17, "bold"), text_color="#FFFFFF"
        )
        self._label_nome.place(relx=0.5, rely=0.5, anchor="center")

        # Configuração
        cfg = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=0, height=52)
        cfg.pack(fill="x")
        cfg.pack_propagate(False)

        ctk.CTkLabel(
            cfg, text="Questões por sessão:",
            font=ctk.CTkFont("Segoe UI", 13), text_color="#BDC3C7"
        ).place(x=20, rely=0.5, anchor="w")

        self._qtd_var = ctk.StringVar(value="10")
        ctk.CTkOptionMenu(
            cfg, variable=self._qtd_var,
            values=["5", "10", "15"],
            font=ctk.CTkFont("Segoe UI", 13),
            fg_color="#2C2C2C", button_color="#C0392B",
            button_hover_color="#A93226", width=80,
        ).place(x=170, rely=0.5, anchor="w")

        # Grid de módulos
        self._scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._scroll.pack(fill="both", expand=True, padx=16, pady=12)
        self._scroll.grid_columnconfigure((0, 1), weight=1)

        self._cards: dict = {}
        self._sel_modulo: str | None = None

        for i, (nome, meta) in enumerate(MODULO_META.items()):
            card = self._criar_card(self._scroll, nome, meta, i)
            card.grid(row=i // 2, column=i % 2, padx=8, pady=8, sticky="nsew")
            self._cards[nome] = card

        # Botão iniciar
        self._btn_iniciar = ctk.CTkButton(
            self, text="▶  Iniciar Quiz",
            font=ctk.CTkFont("Segoe UI", 15, "bold"),
            height=50, corner_radius=10,
            fg_color="#C0392B", hover_color="#A93226",
            state="disabled",
            command=self._iniciar_quiz,
        )
        self._btn_iniciar.pack(fill="x", padx=20, pady=(4, 16))

    def _criar_card(self, parent, nome: str, meta: dict, idx: int) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            parent, fg_color="#1E1E1E", corner_radius=14,
            border_width=2, border_color="#2C2C2C", cursor="hand2",
        )
        card.grid_columnconfigure(0, weight=1)

        # Faixa colorida topo
        faixa = ctk.CTkFrame(card, height=5, fg_color=meta["cor"], corner_radius=0)
        faixa.pack(fill="x")

        corpo = ctk.CTkFrame(card, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=16, pady=12)

        # Ícone + norma
        linha1 = ctk.CTkFrame(corpo, fg_color="transparent")
        linha1.pack(fill="x")

        icone_img = ICONES.get(meta.get("icone_key", ""))
        if icone_img:
            ctk.CTkLabel(linha1, text="", image=icone_img).pack(side="left", padx=(0, 6))
        else:
            ctk.CTkLabel(linha1, text="●", font=("Segoe UI", 26),
                         text_color=meta["cor"]).pack(side="left")

        ctk.CTkLabel(
            linha1, text=meta["norma"],
            font=ctk.CTkFont("Segoe UI", 11, "bold"),
            text_color=meta["cor"],
        ).pack(side="right", pady=(6, 0))

        ctk.CTkLabel(
            corpo, text=nome,
            font=ctk.CTkFont("Segoe UI", 15, "bold"),
            text_color="#FFFFFF", anchor="w",
        ).pack(fill="x", pady=(4, 2))

        ctk.CTkLabel(
            corpo, text=meta["desc"],
            font=ctk.CTkFont("Segoe UI", 12),
            text_color="#7F8C8D", anchor="w", wraplength=340,
        ).pack(fill="x")

        self._label_cont = ctk.CTkLabel(
            corpo, text="… questões",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color="#5D6D7E", anchor="w",
        )
        self._label_cont.pack(fill="x", pady=(6, 0))
        card._lbl_cont = self._label_cont

        # Bind cliques
        for w in [card, corpo, linha1]:
            w.bind("<Button-1>", lambda e, n=nome: self._selecionar(n))

        return card

    def _atualizar_contadores(self):
        contadores = self.app.db.count_questoes_por_modulo()
        for nome, card in self._cards.items():
            n = contadores.get(nome, 0)
            card._lbl_cont.configure(text=f"{n} questões disponíveis")

    def _selecionar(self, nome: str):
        # Desmarcar anterior
        if self._sel_modulo and self._sel_modulo in self._cards:
            self._cards[self._sel_modulo].configure(border_color="#2C2C2C")

        self._sel_modulo = nome
        self.app.modulo_sel = nome
        cor = MODULO_META[nome]["cor"]
        self._cards[nome].configure(border_color=cor)
        self._btn_iniciar.configure(state="normal")

    def _iniciar_quiz(self):
        if not self._sel_modulo:
            return
        qtd = int(self._qtd_var.get())
        questoes = self.app.db.get_questoes(self._sel_modulo, "todos", qtd)

        if not questoes:
            messagebox.showinfo(
                "Sem questões",
                f"Nenhuma questão encontrada para o módulo '{self._sel_modulo}'."
            )
            return

        self.app.session_id = self.app.db.criar_sessao(
            self.app.player_name.get(),
            self._sel_modulo,
            "todos",
        )
        self.app.mostrar("TelaQuiz", questoes=questoes, modulo=self._sel_modulo)


# ─── Tela 3: Quiz ─────────────────────────────────────────────────────────────

class TelaQuiz(ctk.CTkFrame):
    def __init__(self, parent, app: App):
        super().__init__(parent, fg_color="#0F0F0F")
        self.app = app

        self._questoes: list = []
        self._idx: int = 0
        self._modulo: str = ""
        self._inicio_q: float = 0.0
        self._timer_job = None
        self._respondeu: bool = False

        # Totalizadores da sessão
        self._acertos: int = 0
        self._pontuacao: int = 0
        self._tempo_total: float = 0.0
        self._detalhes: list = []

        self._construir()

    def ao_mostrar(self, questoes: list, modulo: str):
        self._questoes = questoes
        self._modulo = modulo
        self._idx = 0
        self._acertos = 0
        self._pontuacao = 0
        self._tempo_total = 0.0
        self._detalhes = []
        self._exibir_questao()

    # ── Construção da interface ────────────────────────────────────────────────

    def _construir(self):
        # ── Barra superior ────────────────────────────────────────────────────
        self._topo = ctk.CTkFrame(self, fg_color="#1A1A1A", height=64, corner_radius=0)
        self._topo.pack(fill="x")
        self._topo.pack_propagate(False)

        self._lbl_modulo = ctk.CTkLabel(
            self._topo, text="",
            font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color="#FFFFFF"
        )
        self._lbl_modulo.place(relx=0.5, rely=0.3, anchor="center")

        self._lbl_progresso = ctk.CTkLabel(
            self._topo, text="",
            font=ctk.CTkFont("Segoe UI", 12), text_color="#7F8C8D"
        )
        self._lbl_progresso.place(relx=0.5, rely=0.72, anchor="center")

        self._lbl_score = ctk.CTkLabel(
            self._topo, text="Pontos: 0",
            font=ctk.CTkFont("Segoe UI", 13, "bold"), text_color="#E67E22"
        )
        self._lbl_score.place(relx=0.98, rely=0.5, anchor="e")

        # Barra de progresso
        self._barra_prog = ctk.CTkProgressBar(self, height=5, corner_radius=0,
                                               fg_color="#1A1A1A",
                                               progress_color="#C0392B")
        self._barra_prog.pack(fill="x")
        self._barra_prog.set(0)

        # ── Timer ─────────────────────────────────────────────────────────────
        timer_frame = ctk.CTkFrame(self, fg_color="transparent")
        timer_frame.pack(fill="x", padx=24, pady=(12, 0))

        self._lbl_timer = ctk.CTkLabel(
            timer_frame, text="⏱ 30s",
            font=ctk.CTkFont("Segoe UI", 13, "bold"), text_color="#27AE60"
        )
        self._lbl_timer.pack(side="left")

        self._barra_timer = ctk.CTkProgressBar(
            timer_frame, height=10, corner_radius=6,
            fg_color="#2C2C2C", progress_color="#27AE60"
        )
        self._barra_timer.pack(side="left", fill="x", expand=True, padx=(10, 0))
        self._barra_timer.set(1.0)

        # ── Enunciado ─────────────────────────────────────────────────────────
        self._frame_enunciado = ctk.CTkFrame(self, fg_color="#1A1A1A",
                                              corner_radius=12)
        self._frame_enunciado.pack(fill="x", padx=24, pady=(12, 0))

        self._lbl_enunciado = ctk.CTkLabel(
            self._frame_enunciado, text="",
            font=ctk.CTkFont("Segoe UI", 15),
            text_color="#ECEFF1", wraplength=880, justify="left", anchor="w"
        )
        self._lbl_enunciado.pack(padx=20, pady=16, fill="x")

        # ── Opções ────────────────────────────────────────────────────────────
        self._frame_opcoes = ctk.CTkFrame(self, fg_color="transparent")
        self._frame_opcoes.pack(fill="both", expand=True, padx=24, pady=10)
        self._frame_opcoes.grid_columnconfigure((0, 1), weight=1)
        self._frame_opcoes.grid_rowconfigure((0, 1), weight=1)

        self._btns: list[ctk.CTkButton] = []
        rotulos = ["A", "B", "C", "D"]
        posicoes = [(0, 0), (0, 1), (1, 0), (1, 1)]

        for i, (letra, pos) in enumerate(zip(rotulos, posicoes)):
            btn = ctk.CTkButton(
                self._frame_opcoes, text="",
                font=ctk.CTkFont("Segoe UI", 13),
                height=72, corner_radius=10,
                fg_color="#1E1E1E", hover_color="#2C2C2C",
                border_width=1, border_color="#2C2C2C",
                text_color="#ECEFF1", anchor="w",
                command=lambda idx=i: self._responder(idx),
            )
            btn.grid(row=pos[0], column=pos[1], padx=6, pady=6, sticky="nsew")
            self._btns.append(btn)

        # ── Feedback ──────────────────────────────────────────────────────────
        self._frame_feedback = ctk.CTkFrame(self, fg_color="#1A1A1A",
                                             corner_radius=12)
        self._frame_feedback.pack(fill="x", padx=24, pady=(0, 4))

        self._lbl_resultado = ctk.CTkLabel(
            self._frame_feedback, text="",
            font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color="#27AE60"
        )
        self._lbl_resultado.pack(anchor="w", padx=16, pady=(10, 2))

        self._lbl_explicacao = ctk.CTkLabel(
            self._frame_feedback, text="",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color="#BDC3C7", wraplength=880,
            justify="left", anchor="w"
        )
        self._lbl_explicacao.pack(anchor="w", padx=16, pady=(0, 10), fill="x")

        self._frame_feedback.pack_forget()

        # ── Botão próxima ─────────────────────────────────────────────────────
        self._btn_proxima = ctk.CTkButton(
            self, text="Próxima  →",
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            height=46, corner_radius=10,
            fg_color="#C0392B", hover_color="#A93226",
            command=self._proxima,
        )
        self._btn_proxima.pack(fill="x", padx=24, pady=(0, 14))
        self._btn_proxima.pack_forget()

    # ── Lógica do quiz ────────────────────────────────────────────────────────

    def _exibir_questao(self):
        self._respondeu = False
        self._frame_feedback.pack_forget()
        self._btn_proxima.pack_forget()

        q = self._questoes[self._idx]
        total = len(self._questoes)

        # Topo
        meta = MODULO_META.get(self._modulo, {})
        self._lbl_modulo.configure(text=f"  {self._modulo}")
        icone_img = ICONES.get(meta.get("icone_key", ""))
        if icone_img:
            self._lbl_modulo.configure(image=icone_img, compound="left")
        self._lbl_progresso.configure(
            text=f"Questão {self._idx + 1} de {total}"
        )
        self._lbl_score.configure(text=f"Pontos: {self._pontuacao}")
        self._barra_prog.set((self._idx) / total)

        # Enunciado
        self._lbl_enunciado.configure(text=q["enunciado"])

        # Opções
        letras = ["A", "B", "C", "D"]
        opcoes = [q["opcao_a"], q["opcao_b"], q["opcao_c"], q["opcao_d"]]
        for i, (btn, letra, txt) in enumerate(zip(self._btns, letras, opcoes)):
            btn.configure(
                text=f"  {letra})  {txt}",
                fg_color="#1E1E1E", border_color="#2C2C2C",
                text_color="#ECEFF1", state="normal",
            )

        # Iniciar timer
        self._inicio_q = time.time()
        self._timer_restante = TIMER_SEGUNDOS
        self._tick_timer()

    def _tick_timer(self):
        if self._respondeu:
            return
        elapsed = time.time() - self._inicio_q
        restante = max(0, TIMER_SEGUNDOS - elapsed)
        self._timer_restante = restante
        ratio = restante / TIMER_SEGUNDOS

        self._lbl_timer.configure(text=f"⏱ {int(restante)}s")
        self._barra_timer.set(ratio)

        # Mudar cor conforme urgência
        if ratio > 0.5:
            cor = "#27AE60"
        elif ratio > 0.25:
            cor = "#F39C12"
        else:
            cor = "#E74C3C"
        self._barra_timer.configure(progress_color=cor)
        self._lbl_timer.configure(text_color=cor)

        if restante <= 0:
            self._responder(None)  # Tempo esgotado
        else:
            self._timer_job = self.after(100, self._tick_timer)

    def _cancelar_timer(self):
        if self._timer_job:
            self.after_cancel(self._timer_job)
            self._timer_job = None

    def _responder(self, idx_escolha):
        if self._respondeu:
            return
        self._respondeu = True
        self._cancelar_timer()

        tempo_gasto = time.time() - self._inicio_q
        q = self._questoes[self._idx]
        gabarito = q["correta"]  # 'A', 'B', 'C', 'D'

        letras = ["A", "B", "C", "D"]
        opcoes_btn = self._btns

        if idx_escolha is not None:
            letra_escolhida = letras[idx_escolha]
            acertou = letra_escolhida == gabarito
            resposta_str = letra_escolhida
        else:
            acertou = False
            resposta_str = None  # Tempo esgotado

        pts = calcular_pontuacao(acertou, tempo_gasto)
        self._pontuacao += pts
        if acertou:
            self._acertos += 1
        self._tempo_total += tempo_gasto

        # Registrar no DB
        self.app.db.registrar_resposta(
            self.app.session_id, q["id"],
            resposta_str, acertou, tempo_gasto
        )

        # Guardar detalhe
        self._detalhes.append({
            "enunciado": q["enunciado"][:80] + "…" if len(q["enunciado"]) > 80 else q["enunciado"],
            "acertou": acertou,
            "resposta": resposta_str or "—",
            "gabarito": gabarito,
            "pts": pts,
            "tempo": round(tempo_gasto, 1),
        })

        # Desabilitar botões e colorir
        for i, btn in enumerate(opcoes_btn):
            btn.configure(state="disabled")
            l = letras[i]
            if l == gabarito:
                btn.configure(fg_color="#1E8449", border_color="#27AE60",
                              text_color="#FFFFFF")
            elif idx_escolha is not None and i == idx_escolha and not acertou:
                btn.configure(fg_color="#922B21", border_color="#E74C3C",
                              text_color="#FFFFFF")

        # Feedback
        if idx_escolha is None:
            resultado_txt = "⏰  Tempo esgotado!"
            resultado_cor = "#F39C12"
        elif acertou:
            resultado_txt = f"✅  Correto! +{pts} pontos"
            resultado_cor = "#27AE60"
        else:
            resultado_txt = f"❌  Incorreto. A resposta correta era a alternativa {gabarito}."
            resultado_cor = "#E74C3C"

        self._lbl_resultado.configure(text=resultado_txt, text_color=resultado_cor)
        self._lbl_explicacao.configure(text=q["explicacao"])

        self._frame_feedback.pack(fill="x", padx=24, pady=(0, 4))
        self._btn_proxima.pack(fill="x", padx=24, pady=(0, 14))
        self._lbl_score.configure(text=f"Pontos: {self._pontuacao}")

    def _proxima(self):
        self._idx += 1
        if self._idx >= len(self._questoes):
            self._finalizar()
        else:
            self._exibir_questao()

    def _finalizar(self):
        self._cancelar_timer()
        total = len(self._questoes)
        self.app.db.finalizar_sessao(
            self.app.session_id, total,
            self._acertos, self._pontuacao, self._tempo_total
        )
        self.app.quiz_resultado = {
            "modulo": self._modulo,
            "total": total,
            "acertos": self._acertos,
            "pontuacao": self._pontuacao,
            "tempo_total": self._tempo_total,
            "detalhes": self._detalhes,
        }
        self.app.mostrar("TelaRelatorio")


# ─── Tela 4: Relatório Final ──────────────────────────────────────────────────

class TelaRelatorio(ctk.CTkFrame):
    def __init__(self, parent, app: App):
        super().__init__(parent, fg_color="#0F0F0F")
        self.app = app
        self._construir()

    def ao_mostrar(self):
        r = self.app.quiz_resultado
        total = r.get("total", 0)
        acertos = r.get("acertos", 0)
        pts = r.get("pontuacao", 0)
        tempo = r.get("tempo_total", 0.0)
        modulo = r.get("modulo", "")
        detalhes = r.get("detalhes", [])
        percentual = pct(acertos, total)

        meta = MODULO_META.get(modulo, {})

        self._lbl_titulo.configure(text=f"  Resultado — {modulo}")
        icone_img = ICONES.get(meta.get("icone_key", ""))
        if icone_img:
            self._lbl_titulo.configure(image=icone_img, compound="left")
        self._lbl_pts.configure(text=str(pts))
        self._lbl_acertos.configure(
            text=f"{acertos}/{total} acertos  ({percentual:.0f}%)"
        )
        self._lbl_estrelas.configure(text=estrelas(percentual))
        self._lbl_tempo.configure(
            text=f"Tempo médio por questão: {tempo / max(total, 1):.1f}s"
        )
        self._lbl_player.configure(text=self.app.player_name.get())

        # Preencher tabela de detalhes
        for w in self._frame_tabela.winfo_children():
            w.destroy()

        cores = {"True": "#1E8449", "False": "#922B21"}
        for i, d in enumerate(detalhes):
            bg = "#1A1A1A" if i % 2 == 0 else "#141414"
            linha = ctk.CTkFrame(self._frame_tabela, fg_color=bg, corner_radius=0)
            linha.pack(fill="x")

            icone = "✅" if d["acertou"] else "❌"
            ctk.CTkLabel(
                linha, text=icone, font=("Segoe UI Emoji", 13), width=28
            ).pack(side="left", padx=(8, 4), pady=5)

            ctk.CTkLabel(
                linha, text=d["enunciado"],
                font=ctk.CTkFont("Segoe UI", 11),
                text_color="#BDC3C7", anchor="w", wraplength=580
            ).pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                linha,
                text=f"{d['tempo']}s  |  {d['pts']}pts",
                font=ctk.CTkFont("Segoe UI", 11),
                text_color="#7F8C8D", width=90
            ).pack(side="right", padx=8)

    def _construir(self):
        # Topo
        topo = ctk.CTkFrame(self, fg_color="#1A1A1A", height=56, corner_radius=0)
        topo.pack(fill="x")
        topo.pack_propagate(False)

        self._lbl_titulo = ctk.CTkLabel(
            topo, text="",
            font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color="#FFFFFF"
        )
        self._lbl_titulo.place(relx=0.5, rely=0.5, anchor="center")

        # Painel de pontuação
        painel = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=14,
                              border_width=1, border_color="#2C2C2C")
        painel.pack(fill="x", padx=20, pady=(14, 6))

        col_pts = ctk.CTkFrame(painel, fg_color="transparent")
        col_pts.pack(side="left", expand=True, pady=14)

        self._lbl_pts = ctk.CTkLabel(
            col_pts, text="0",
            font=ctk.CTkFont("Segoe UI", 52, "bold"), text_color="#E67E22"
        )
        self._lbl_pts.pack()

        ctk.CTkLabel(
            col_pts, text="PONTOS",
            font=ctk.CTkFont("Segoe UI", 11), text_color="#7F8C8D"
        ).pack()

        sep = ctk.CTkFrame(painel, width=1, fg_color="#2C2C2C")
        sep.pack(side="left", fill="y", pady=10)

        col_info = ctk.CTkFrame(painel, fg_color="transparent")
        col_info.pack(side="left", expand=True, pady=14, padx=20)

        self._lbl_player = ctk.CTkLabel(
            col_info, text="",
            font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color="#FFFFFF"
        )
        self._lbl_player.pack(anchor="w")

        self._lbl_acertos = ctk.CTkLabel(
            col_info, text="",
            font=ctk.CTkFont("Segoe UI", 13), text_color="#BDC3C7"
        )
        self._lbl_acertos.pack(anchor="w", pady=2)

        self._lbl_estrelas = ctk.CTkLabel(
            col_info, text="",
            font=("Segoe UI Emoji", 22), text_color="#F1C40F"
        )
        self._lbl_estrelas.pack(anchor="w")

        self._lbl_tempo = ctk.CTkLabel(
            col_info, text="",
            font=ctk.CTkFont("Segoe UI", 11), text_color="#7F8C8D"
        )
        self._lbl_tempo.pack(anchor="w", pady=(4, 0))

        # Tabela de detalhes
        ctk.CTkLabel(
            self, text="Detalhes por questão",
            font=ctk.CTkFont("Segoe UI", 13, "bold"), text_color="#AAB7B8"
        ).pack(anchor="w", padx=22, pady=(8, 4))

        self._frame_tabela = ctk.CTkScrollableFrame(
            self, fg_color="#141414", corner_radius=10, height=200
        )
        self._frame_tabela.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        # Botões de ação
        acoes = ctk.CTkFrame(self, fg_color="transparent")
        acoes.pack(fill="x", padx=20, pady=(0, 16))
        acoes.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(
            acoes, text="▶  Jogar Novamente",
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            height=44, corner_radius=10,
            fg_color="#C0392B", hover_color="#A93226",
            command=lambda: self.app.mostrar("TelaModulos"),
        ).grid(row=0, column=0, padx=4, sticky="ew")

        ctk.CTkButton(
            acoes, text="📊  Histórico",
            font=ctk.CTkFont("Segoe UI", 13),
            height=44, corner_radius=10,
            fg_color="#1A5276", hover_color="#154360",
            command=lambda: self.app.mostrar("TelaHistorico"),
        ).grid(row=0, column=1, padx=4, sticky="ew")

        ctk.CTkButton(
            acoes, text="🏠  Menu Principal",
            font=ctk.CTkFont("Segoe UI", 13),
            height=44, corner_radius=10,
            fg_color="transparent", border_width=1, border_color="#5D6D7E",
            text_color="#AAB7B8", hover_color="#1C1C1C",
            command=lambda: self.app.mostrar("TelaHome"),
        ).grid(row=0, column=2, padx=4, sticky="ew")


# ─── Tela 5: Histórico e Ranking ──────────────────────────────────────────────

class TelaHistorico(ctk.CTkFrame):
    def __init__(self, parent, app: App):
        super().__init__(parent, fg_color="#0F0F0F")
        self.app = app
        self._construir()

    def ao_mostrar(self):
        self._atualizar()

    def _construir(self):
        # Barra topo
        topo = ctk.CTkFrame(self, fg_color="#1A1A1A", height=56, corner_radius=0)
        topo.pack(fill="x")
        topo.pack_propagate(False)

        ctk.CTkButton(
            topo, text="← Voltar", width=90, height=34,
            fg_color="transparent", border_width=1, border_color="#5D6D7E",
            text_color="#AAB7B8", hover_color="#1C1C1C",
            font=ctk.CTkFont("Segoe UI", 12),
            command=lambda: self.app.mostrar("TelaHome"),
        ).place(x=16, rely=0.5, anchor="w")

        ctk.CTkLabel(
            topo, text="📊  Histórico e Ranking",
            font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Tabs
        self._tab = ctk.CTkTabview(
            self, fg_color="#141414",
            segmented_button_fg_color="#1A1A1A",
            segmented_button_selected_color="#C0392B",
            segmented_button_unselected_color="#1A1A1A",
            text_color="#BDC3C7",
            segmented_button_selected_hover_color="#A93226",
        )
        self._tab.pack(fill="both", expand=True, padx=16, pady=12)

        self._tab.add("Minhas Sessões")
        self._tab.add("Ranking Geral")
        self._tab.add("Exportar Dados")

        self._build_tab_sessoes()
        self._build_tab_ranking()
        self._build_tab_exportar()

    def _build_tab_sessoes(self):
        tab = self._tab.tab("Minhas Sessões")

        self._lbl_stats = ctk.CTkLabel(
            tab, text="",
            font=ctk.CTkFont("Segoe UI", 13), text_color="#BDC3C7"
        )
        self._lbl_stats.pack(anchor="w", padx=8, pady=(8, 4))

        # Cabeçalho
        cab = ctk.CTkFrame(tab, fg_color="#1A1A1A", corner_radius=6)
        cab.pack(fill="x", padx=4, pady=(0, 2))
        for txt, w in [("Módulo", 200), ("Acertos", 90),
                       ("Pontos", 90), ("T.Médio", 80), ("Data", 140)]:
            ctk.CTkLabel(
                cab, text=txt, width=w,
                font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color="#7F8C8D"
            ).pack(side="left", padx=4, pady=6)

        self._frame_sessoes = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        self._frame_sessoes.pack(fill="both", expand=True, padx=4)

    def _build_tab_ranking(self):
        tab = self._tab.tab("Ranking Geral")

        cab = ctk.CTkFrame(tab, fg_color="#1A1A1A", corner_radius=6)
        cab.pack(fill="x", padx=4, pady=(8, 2))
        for txt, w in [("#", 40), ("Participante", 200), ("Total Pts", 110),
                       ("Acertos", 100), ("Questões", 100), ("Sessões", 80)]:
            ctk.CTkLabel(
                cab, text=txt, width=w,
                font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color="#7F8C8D"
            ).pack(side="left", padx=4, pady=6)

        self._frame_ranking = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        self._frame_ranking.pack(fill="both", expand=True, padx=4, pady=4)

    def _build_tab_exportar(self):
        tab = self._tab.tab("Exportar Dados")

        ctk.CTkFrame(tab, height=20, fg_color="transparent").pack()

        card = ctk.CTkFrame(tab, fg_color="#1A1A1A", corner_radius=14,
                            border_width=1, border_color="#2C2C2C")
        card.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(
            card,
            text="📤  Exportar dados de pesquisa",
            font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color="#FFFFFF"
        ).pack(pady=(16, 4))

        ctk.CTkLabel(
            card,
            text="Gera um arquivo CSV com todas as sessões e respostas registradas,\n"
                 "incluindo participante, módulo, questão, resposta, gabarito e tempo.",
            font=ctk.CTkFont("Segoe UI", 13), text_color="#BDC3C7",
            justify="center"
        ).pack(pady=(0, 16))

        ctk.CTkButton(
            card,
            text="💾  Exportar CSV",
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            height=46, width=260, corner_radius=10,
            fg_color="#1A5276", hover_color="#154360",
            command=self._exportar,
        ).pack(pady=(0, 20))

    def _atualizar(self):
        self._atualizar_sessoes()
        self._atualizar_ranking()

    def _atualizar_sessoes(self):
        for w in self._frame_sessoes.winfo_children():
            w.destroy()

        participante = self.app.player_name.get()
        sessoes = self.app.db.historico_participante(participante)
        stats = self.app.db.estatisticas_participante(participante)

        n = stats.get("sessoes") or 0
        pts = stats.get("total_pts") or 0
        self._lbl_stats.configure(
            text=f"{participante}  •  {n} sessões realizadas  •  {pts} pontos acumulados"
        )

        if not sessoes:
            ctk.CTkLabel(
                self._frame_sessoes,
                text="Nenhuma sessão registrada ainda.",
                font=ctk.CTkFont("Segoe UI", 13), text_color="#5D6D7E"
            ).pack(pady=20)
            return

        for i, s in enumerate(sessoes):
            bg = "#1A1A1A" if i % 2 == 0 else "#141414"
            linha = ctk.CTkFrame(self._frame_sessoes, fg_color=bg, corner_radius=4)
            linha.pack(fill="x", pady=1)

            total = s["total_questoes"] or 1
            pct_val = pct(s["acertos"], total)
            t_medio = (s["tempo_total_segundos"] / total) if total else 0
            data_str = s["data_inicio"][:16].replace("T", " ")

            for txt, w in [
                (s["modulo"][:25], 200),
                (f"{s['acertos']}/{total} ({pct_val:.0f}%)", 90),
                (str(s["pontuacao"]), 90),
                (f"{t_medio:.1f}s", 80),
                (data_str, 140),
            ]:
                ctk.CTkLabel(
                    linha, text=txt, width=w,
                    font=ctk.CTkFont("Segoe UI", 12), text_color="#BDC3C7"
                ).pack(side="left", padx=4, pady=5)

    def _atualizar_ranking(self):
        for w in self._frame_ranking.winfo_children():
            w.destroy()

        ranking = self.app.db.ranking_geral()
        if not ranking:
            ctk.CTkLabel(
                self._frame_ranking,
                text="Nenhuma pontuação registrada ainda.",
                font=ctk.CTkFont("Segoe UI", 13), text_color="#5D6D7E"
            ).pack(pady=20)
            return

        player = self.app.player_name.get()

        for i, r in enumerate(ranking):
            destaque = r["participante"] == player
            bg = "#1E2D1A" if destaque else ("#1A1A1A" if i % 2 == 0 else "#141414")
            linha = ctk.CTkFrame(self._frame_ranking, fg_color=bg, corner_radius=4)
            linha.pack(fill="x", pady=1)

            medalha = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i + 1}."
            for txt, w in [
                (medalha, 40),
                (r["participante"][:22], 200),
                (str(r["total_pts"] or 0), 110),
                (str(r["total_acertos"] or 0), 100),
                (str(r["total_q"] or 0), 100),
                (str(r["n_sessoes"]), 80),
            ]:
                cor = "#F1C40F" if destaque else "#BDC3C7"
                ctk.CTkLabel(
                    linha, text=txt, width=w,
                    font=ctk.CTkFont("Segoe UI", 12, "bold" if destaque else "normal"),
                    text_color=cor
                ).pack(side="left", padx=4, pady=5)

    def _exportar(self):
        caminho = filedialog.asksaveasfilename(
            title="Salvar dados da pesquisa",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Todos os arquivos", "*.*")],
            initialfile=f"dados_pesquisa_{datetime.now().strftime('%Y%m%d')}.csv",
        )
        if not caminho:
            return
        try:
            arquivo = self.app.db.exportar_csv(caminho)
            messagebox.showinfo(
                "Exportação concluída",
                f"Dados exportados com sucesso!\n\nArquivo salvo em:\n{arquivo}"
            )
        except Exception as exc:
            messagebox.showerror("Erro na exportação", str(exc))


# ─── Ponto de entrada ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
