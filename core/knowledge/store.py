"""
NEXA Africa Operating System
File: core/knowledge/store.py
Constitutional Owner: Bill Odhiambo Othieno
Description: FactStore — persists Facts to their own SQLite database,
             separate from core/cognition/memory/ (session state), per
             core/contracts/knowledge/ukl_contract_v1.md. Supports
             superseding an existing fact (subject+predicate) with a
             newer value rather than accumulating contradictory rows.
             Also supports relationship queries that fall out of the
             existing subject-predicate-value schema — no separate
             graph engine or table.
"""

from __future__ import annotations

import os
import sqlite3
from typing import List, Optional

from core.knowledge.facts import Fact
from core.services.logging.logger import get_logger

logger = get_logger(__name__)

DEFAULT_DB_PATH = os.path.join("data", "knowledge_facts.db")


class FactStore:
    """
    Stores and retrieves Facts in their own SQLite database.

    add_fact() supersedes any existing fact with the same
    (subject, predicate) pair rather than accumulating contradictory
    rows — the newest value for a given subject+predicate wins.
    """

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._shared_conn: Optional[sqlite3.Connection] = None

        if self.db_path == ":memory:":
            self._shared_conn = sqlite3.connect(":memory:")
            self._shared_conn.row_factory = sqlite3.Row
        else:
            directory = os.path.dirname(self.db_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

        self._init_db()
        logger.info("FactStore initialized at db_path=%s", self.db_path)

    def _get_connection(self) -> sqlite3.Connection:
        if self._shared_conn:
            return self._shared_conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        conn = self._get_connection()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS facts (
                subject TEXT NOT NULL,
                predicate TEXT NOT NULL,
                value TEXT NOT NULL,
                provenance TEXT NOT NULL,
                timestamp REAL NOT NULL,
                PRIMARY KEY (subject, predicate)
            )
            """
        )
        conn.commit()

    def add_fact(self, fact: Fact) -> bool:
        """
        Insert a fact, superseding any existing fact with the same
        (subject, predicate) pair.
        """
        if not isinstance(fact, Fact):
            raise TypeError("FactStore.add_fact() requires a Fact.")

        conn = self._get_connection()
        conn.execute(
            """
            INSERT INTO facts (subject, predicate, value, provenance, timestamp)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(subject, predicate) DO UPDATE SET
                value=excluded.value,
                provenance=excluded.provenance,
                timestamp=excluded.timestamp
            """,
            (fact.subject, fact.predicate, fact.value, fact.provenance, fact.timestamp),
        )
        conn.commit()
        return True

    def get_facts_about(self, subject: str) -> List[Fact]:
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT subject, predicate, value, provenance, timestamp FROM facts WHERE subject = ?",
            (subject,),
        )
        rows = cursor.fetchall()
        return [
            Fact(
                subject=row["subject"],
                predicate=row["predicate"],
                value=row["value"],
                provenance=row["provenance"],
                timestamp=row["timestamp"],
            )
            for row in rows
        ]

    def get_fact(self, subject: str, predicate: str) -> Optional[Fact]:
        """
        Retrieve the single current fact for a specific subject+predicate,
        or None if no such fact exists.
        """
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT subject, predicate, value, provenance, timestamp FROM facts WHERE subject = ? AND predicate = ?",
            (subject, predicate),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Fact(
            subject=row["subject"],
            predicate=row["predicate"],
            value=row["value"],
            provenance=row["provenance"],
            timestamp=row["timestamp"],
        )

    def get_facts_by_predicate(self, predicate: str) -> List[Fact]:
        """
        Retrieve every fact across all subjects that uses this predicate.
        E.g. get_facts_by_predicate("owns_farm") -> every subject with
        that relationship, regardless of which subject.
        """
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT subject, predicate, value, provenance, timestamp FROM facts WHERE predicate = ?",
            (predicate,),
        )
        rows = cursor.fetchall()
        return [
            Fact(
                subject=row["subject"],
                predicate=row["predicate"],
                value=row["value"],
                provenance=row["provenance"],
                timestamp=row["timestamp"],
            )
            for row in rows
        ]

    def get_facts_with_value(self, value: str) -> List[Fact]:
        """
        Retrieve every fact across all subjects/predicates whose value
        matches exactly. E.g. get_facts_with_value("Nairobi") -> every
        fact that points at "Nairobi", regardless of subject or predicate.
        """
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT subject, predicate, value, provenance, timestamp FROM facts WHERE value = ?",
            (value,),
        )
        rows = cursor.fetchall()
        return [
            Fact(
                subject=row["subject"],
                predicate=row["predicate"],
                value=row["value"],
                provenance=row["provenance"],
                timestamp=row["timestamp"],
            )
            for row in rows
        ]

    def get_related(self, subject: str, max_depth: int = 1) -> List[Fact]:
        """
        Cycle-safe breadth-first walk: starting from `subject`, follow
        each fact's value into another subject's facts (treating the
        value as if it might itself be a subject), up to max_depth hops.

        No separate graph table — this walks the existing
        subject-predicate-value rows.
        """
        if max_depth < 0:
            raise ValueError("FactStore.get_related() requires max_depth >= 0.")

        visited_subjects = {subject}
        collected: List[Fact] = []
        frontier = [subject]
        depth = 0

        while frontier and depth < max_depth:
            next_frontier: List[str] = []
            for current_subject in frontier:
                facts = self.get_facts_about(current_subject)
                for fact in facts:
                    collected.append(fact)
                    if fact.value not in visited_subjects:
                        visited_subjects.add(fact.value)
                        next_frontier.append(fact.value)
            frontier = next_frontier
            depth += 1

        return collected


__all__ = [
    "FactStore",
    "DEFAULT_DB_PATH",
]
