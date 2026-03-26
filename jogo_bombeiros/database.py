# database.py — Gerenciador do banco de dados SQLite
import sqlite3
import csv
import os
from datetime import datetime


class DatabaseManager:
    """Gerencia todas as operações de banco de dados da aplicação."""

    SCHEMA_VERSION = 1

    def __init__(self, db_path: str = "bombeiros_quiz.db"):
        self.db_path = db_path
        self._init_db()

    # ─── Conexão ──────────────────────────────────────────────────────────────

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ─── Inicialização ────────────────────────────────────────────────────────

    def _init_db(self):
        with self._connect() as conn:
            c = conn.cursor()

            c.execute("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY
                )
            """)

            c.execute("""
                CREATE TABLE IF NOT EXISTS questoes (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    modulo      TEXT    NOT NULL,
                    dificuldade TEXT    NOT NULL CHECK(dificuldade IN ('basico','intermediario','avancado')),
                    enunciado   TEXT    NOT NULL,
                    opcao_a     TEXT    NOT NULL,
                    opcao_b     TEXT    NOT NULL,
                    opcao_c     TEXT    NOT NULL,
                    opcao_d     TEXT    NOT NULL,
                    correta     TEXT    NOT NULL CHECK(correta IN ('A','B','C','D')),
                    explicacao  TEXT    NOT NULL,
                    ativa       INTEGER NOT NULL DEFAULT 1
                )
            """)

            c.execute("""
                CREATE TABLE IF NOT EXISTS sessoes (
                    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
                    participante          TEXT    NOT NULL,
                    modulo                TEXT    NOT NULL,
                    dificuldade           TEXT    NOT NULL,
                    data_inicio           TEXT    NOT NULL,
                    data_fim              TEXT,
                    total_questoes        INTEGER NOT NULL DEFAULT 0,
                    acertos               INTEGER NOT NULL DEFAULT 0,
                    pontuacao             INTEGER NOT NULL DEFAULT 0,
                    tempo_total_segundos  REAL    NOT NULL DEFAULT 0
                )
            """)

            c.execute("""
                CREATE TABLE IF NOT EXISTS respostas (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    sessao_id      INTEGER NOT NULL,
                    questao_id     INTEGER NOT NULL,
                    resposta_dada  TEXT,
                    correta        INTEGER NOT NULL,
                    tempo_resposta REAL    NOT NULL,
                    FOREIGN KEY (sessao_id)  REFERENCES sessoes(id),
                    FOREIGN KEY (questao_id) REFERENCES questoes(id)
                )
            """)

            c.execute("INSERT OR IGNORE INTO schema_version VALUES (?)", (self.SCHEMA_VERSION,))
            conn.commit()

    # ─── Questões ─────────────────────────────────────────────────────────────

    def seed_questions(self, questions: list):
        """Insere questões iniciais apenas se a tabela estiver vazia."""
        with self._connect() as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM questoes")
            if c.fetchone()[0] == 0:
                c.executemany("""
                    INSERT INTO questoes
                        (modulo, dificuldade, enunciado, opcao_a, opcao_b, opcao_c, opcao_d, correta, explicacao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, questions)
                conn.commit()

    def get_modulos(self) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT DISTINCT modulo FROM questoes WHERE ativa=1 ORDER BY modulo"
            ).fetchall()
            return [r[0] for r in rows]

    def count_questoes_por_modulo(self) -> dict:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT modulo, COUNT(*) FROM questoes WHERE ativa=1 GROUP BY modulo"
            ).fetchall()
            return {r[0]: r[1] for r in rows}

    def get_questoes(self, modulo: str, dificuldade: str = "todos", quantidade: int = 10) -> list:
        with self._connect() as conn:
            if dificuldade and dificuldade != "todos":
                rows = conn.execute("""
                    SELECT id, enunciado, opcao_a, opcao_b, opcao_c, opcao_d, correta, explicacao
                    FROM questoes
                    WHERE modulo=? AND dificuldade=? AND ativa=1
                    ORDER BY RANDOM() LIMIT ?
                """, (modulo, dificuldade, quantidade)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT id, enunciado, opcao_a, opcao_b, opcao_c, opcao_d, correta, explicacao
                    FROM questoes
                    WHERE modulo=? AND ativa=1
                    ORDER BY RANDOM() LIMIT ?
                """, (modulo, quantidade)).fetchall()
            return [dict(r) for r in rows]

    # ─── Sessões ──────────────────────────────────────────────────────────────

    def criar_sessao(self, participante: str, modulo: str, dificuldade: str) -> int:
        with self._connect() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO sessoes (participante, modulo, dificuldade, data_inicio)
                VALUES (?, ?, ?, ?)
            """, (participante, modulo, dificuldade, datetime.now().isoformat()))
            conn.commit()
            return c.lastrowid

    def registrar_resposta(self, sessao_id: int, questao_id: int,
                           resposta_dada: str, correta: bool, tempo: float):
        with self._connect() as conn:
            conn.execute("""
                INSERT INTO respostas (sessao_id, questao_id, resposta_dada, correta, tempo_resposta)
                VALUES (?, ?, ?, ?, ?)
            """, (sessao_id, questao_id, resposta_dada, 1 if correta else 0, round(tempo, 2)))
            conn.commit()

    def finalizar_sessao(self, sessao_id: int, total: int, acertos: int,
                         pontuacao: int, tempo_total: float):
        with self._connect() as conn:
            conn.execute("""
                UPDATE sessoes
                SET data_fim=?, total_questoes=?, acertos=?, pontuacao=?, tempo_total_segundos=?
                WHERE id=?
            """, (datetime.now().isoformat(), total, acertos, pontuacao,
                  round(tempo_total, 2), sessao_id))
            conn.commit()

    # ─── Histórico e Ranking ──────────────────────────────────────────────────

    def historico_participante(self, participante: str) -> list:
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT modulo, dificuldade, total_questoes, acertos, pontuacao,
                       data_inicio, tempo_total_segundos
                FROM sessoes
                WHERE participante=? AND data_fim IS NOT NULL
                ORDER BY data_inicio DESC LIMIT 30
            """, (participante,)).fetchall()
            return [dict(r) for r in rows]

    def ranking_geral(self) -> list:
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT participante,
                       SUM(pontuacao)      AS total_pts,
                       SUM(acertos)        AS total_acertos,
                       SUM(total_questoes) AS total_q,
                       COUNT(*)            AS n_sessoes
                FROM sessoes
                WHERE data_fim IS NOT NULL
                GROUP BY participante
                ORDER BY total_pts DESC
                LIMIT 15
            """).fetchall()
            return [dict(r) for r in rows]

    def ranking_modulo(self, modulo: str) -> list:
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT participante,
                       MAX(pontuacao) AS melhor_pts,
                       COUNT(*)       AS n_sessoes
                FROM sessoes
                WHERE modulo=? AND data_fim IS NOT NULL
                GROUP BY participante
                ORDER BY melhor_pts DESC
                LIMIT 15
            """, (modulo,)).fetchall()
            return [dict(r) for r in rows]

    def estatisticas_participante(self, participante: str) -> dict:
        with self._connect() as conn:
            row = conn.execute("""
                SELECT COUNT(*)            AS sessoes,
                       SUM(pontuacao)      AS total_pts,
                       SUM(acertos)        AS total_acertos,
                       SUM(total_questoes) AS total_q,
                       MAX(pontuacao)      AS melhor_pts
                FROM sessoes
                WHERE participante=? AND data_fim IS NOT NULL
            """, (participante,)).fetchone()
            return dict(row) if row else {}

    # ─── Exportação ───────────────────────────────────────────────────────────

    def exportar_csv(self, caminho: str | None = None) -> str:
        if not caminho:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho = f"dados_pesquisa_{ts}.csv"

        with self._connect() as conn:
            rows = conn.execute("""
                SELECT s.participante, s.modulo, s.dificuldade,
                       s.data_inicio, s.data_fim,
                       s.total_questoes, s.acertos, s.pontuacao, s.tempo_total_segundos,
                       r.questao_id, r.resposta_dada, r.correta, r.tempo_resposta,
                       q.enunciado, q.correta AS gabarito
                FROM sessoes s
                JOIN respostas r ON r.sessao_id = s.id
                JOIN questoes  q ON q.id = r.questao_id
                ORDER BY s.id, r.id
            """).fetchall()

        with open(caminho, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "participante", "modulo", "dificuldade",
                "data_inicio", "data_fim",
                "total_questoes", "acertos", "pontuacao", "tempo_total_segundos",
                "questao_id", "resposta_dada", "correta", "tempo_resposta",
                "enunciado", "gabarito"
            ])
            writer.writerows(rows)

        return caminho
