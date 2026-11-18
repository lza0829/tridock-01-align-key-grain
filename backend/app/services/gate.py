from __future__ import annotations
import sqlite3

from app.services.daykey import SealedDayError


def is_sealed(conn: sqlite3.Connection, dock_day: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM reconcile_batches WHERE dock_day=? AND status='sealed' LIMIT 1",
        (dock_day,),
    ).fetchone()
    return row is not None


def assert_writable(conn: sqlite3.Connection, dock_day: str) -> None:
    """日闭包封印闸：已封印日的任何一腿写入一律拒绝，不接受折日/改挂旁路。"""
    if is_sealed(conn, dock_day):
        raise SealedDayError(f"到货日 {dock_day} 已结案封印，禁止再写入预报/实收/回执")
