from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from datetime import date
from threading import Lock
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .evaluator import evaluate_submission
from .questions import QUESTION_BANK, Question

app = FastAPI(title="Code Arena")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@dataclass
class PlayerState:
    client_id: str
    ip: str
    nickname: str
    score: int
    current_index: int
    assigned_qids: list[str]


class SubmitPayload(BaseModel):
    code: str


class NicknamePayload(BaseModel):
    nickname: str


_players: dict[str, PlayerState] = {}
_lock = Lock()
_question_map: dict[str, Question] = {q.qid: q for q in QUESTION_BANK}


def _extract_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
    if forwarded:
        return forwarded
    if request.client:
        return request.client.host
    return "unknown"


def _build_seed(ip: str, client_id: str) -> int:
    material = f"{ip}|{client_id}|{date.today().isoformat()}".encode("utf-8")
    digest = hashlib.sha256(material).hexdigest()
    return int(digest[:16], 16)


def _assign_questions(ip: str, client_id: str, count: int = 5) -> list[str]:
    qids = [q.qid for q in QUESTION_BANK]
    rng = random.Random(_build_seed(ip, client_id))
    rng.shuffle(qids)
    return qids[: min(count, len(qids))]


def _get_or_create_player(request: Request) -> tuple[PlayerState, bool]:
    client_id = request.cookies.get("client_id")
    ip = _extract_ip(request)

    with _lock:
        if client_id and client_id in _players:
            player = _players[client_id]
            if player.ip != ip:
                player.ip = ip
                player.assigned_qids = _assign_questions(ip, client_id)
                player.current_index = 0
            return player, False

        client_id = str(uuid4())
        player = PlayerState(
            client_id=client_id,
            ip=ip,
            nickname=f"Player-{client_id[:6]}",
            score=0,
            current_index=0,
            assigned_qids=_assign_questions(ip, client_id),
        )
        _players[client_id] = player
        return player, True


def _public_question(question: Question) -> dict[str, Any]:
    return {
        "qid": question.qid,
        "title": question.title,
        "description": question.description,
        "starter_code": question.starter_code,
        "function_name": question.function_name,
        "tags": list(question.tags),
    }


def _current_question(player: PlayerState) -> Question | None:
    if player.current_index >= len(player.assigned_qids):
        return None
    qid = player.assigned_qids[player.current_index]
    return _question_map[qid]


@app.get("/")
def home() -> FileResponse:
    return FileResponse("app/static/index.html")


@app.get("/api/me")
def get_me(request: Request) -> JSONResponse:
    player, is_new = _get_or_create_player(request)
    question = _current_question(player)

    response = JSONResponse(
        {
            "client_id": player.client_id,
            "ip": player.ip,
            "nickname": player.nickname,
            "score": player.score,
            "progress": {
                "current": player.current_index,
                "total": len(player.assigned_qids),
                "done": player.current_index >= len(player.assigned_qids),
            },
            "question": _public_question(question) if question else None,
        }
    )
    if is_new:
        response.set_cookie("client_id", player.client_id, max_age=60 * 60 * 24 * 30, httponly=True)
    return response


@app.post("/api/nickname")
def set_nickname(payload: NicknamePayload, request: Request) -> dict[str, Any]:
    player, _ = _get_or_create_player(request)
    nickname = payload.nickname.strip()
    if not nickname:
        return {"ok": False, "message": "暱稱不能是空白"}
    with _lock:
        player.nickname = nickname[:24]
    return {"ok": True, "nickname": player.nickname}


@app.post("/api/submit")
def submit(payload: SubmitPayload, request: Request) -> dict[str, Any]:
    player, _ = _get_or_create_player(request)
    question = _current_question(player)
    if not question:
        return {"ok": False, "message": "你已完成全部題目"}

    result = evaluate_submission(payload.code, question)

    if result.ok:
        with _lock:
            player.score += 10
            player.current_index += 1
        next_question = _current_question(player)
        return {
            "ok": True,
            "message": f"答對了！+10 分 ({result.passed}/{result.total})",
            "score": player.score,
            "next_question": _public_question(next_question) if next_question else None,
            "done": next_question is None,
        }

    return {
        "ok": False,
        "message": result.message,
        "passed": result.passed,
        "total": result.total,
        "score": player.score,
    }


@app.get("/api/leaderboard")
def leaderboard() -> dict[str, Any]:
    with _lock:
        rows = sorted(_players.values(), key=lambda p: p.score, reverse=True)[:20]
        data = [
            {
                "nickname": p.nickname,
                "score": p.score,
                "solved": p.current_index,
                "ip": p.ip,
            }
            for p in rows
        ]
    return {"items": data}
