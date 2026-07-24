"""
LangGraph wrapper around the existing RAG pipeline. Adds two things plain
LangChain wasn't doing on its own:
1. Conversation memory — pulls recent chat history for this session so
   follow-up questions ("tell me more about that") have context.
2. A retry branch — if retrieval finds nothing relevant, the graph
   reformulates the question once and retries before giving up.
"""
from typing import TypedDict

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.chatbot import ChatLog
from app.schemas.chatbot import ChatAction
from app.services.chatbot import (
    _build_always_context,
    _retrieve_context,
    _detect_actions,
    FEW_SHOT_EXAMPLES,
    FALLBACK_MESSAGE,
)


class ChatState(TypedDict):
    db: Session
    session_id: str
    user_message: str
    history: str
    always_context: str
    always_values: dict
    retrieved_context: str
    reply: str
    was_fallback: bool
    actions: list[ChatAction]
    retried: bool


def _get_history(db: Session, session_id: str, limit: int = 3) -> str:
    """Last few exchanges for this session, oldest first."""
    logs = (
        db.query(ChatLog)
        .filter(ChatLog.session_id == session_id)
        .order_by(ChatLog.created_at.desc())
        .limit(limit)
        .all()
    )
    logs.reverse()
    if not logs:
        return ""
    lines = [f"Visitor: {l.user_message}\nAssistant: {l.bot_response}" for l in logs]
    return "PREVIOUS CONVERSATION (for follow-up context only):\n" + "\n\n".join(lines)


def _node_retrieve(state: ChatState) -> ChatState:
    retrieved = _retrieve_context(state["db"], state["user_message"])
    state["retrieved_context"] = retrieved
    return state


def _node_reformulate_and_retry(state: ChatState) -> ChatState:
    """Only reached if the first retrieval came back empty. Asks the LLM to
    rephrase the question in a way more likely to match portfolio content,
    then retrieves again with the reformulated version."""
    llm = ChatGroq(model=settings.GROQ_MODEL, api_key=settings.GROQ_API_KEY, temperature=0.2, max_tokens=60)
    prompt = (
        "Rewrite the following visitor question as a short, specific search "
        "query about a person's professional background (skills, work, "
        "education, projects). Return ONLY the rewritten query, nothing else.\n\n"
        f"Question: {state['user_message']}"
    )
    result = llm.invoke([HumanMessage(content=prompt)])
    reformulated = result.content.strip()

    retrieved = _retrieve_context(state["db"], reformulated)
    state["retrieved_context"] = retrieved
    state["retried"] = True
    return state


def _node_generate(state: ChatState) -> ChatState:
    full_context = f"{state['always_context']}\n\n{state['retrieved_context']}".strip()

    if not full_context:
        state["reply"] = FALLBACK_MESSAGE
        state["was_fallback"] = True
        state["actions"] = []
        return state

    system_prompt = (
        "You are a strict Q&A assistant on a personal portfolio website. You ONLY "
        "answer questions about the portfolio owner's background, skills, experience, "
        "education, projects, resume, and contact details — using ONLY the CONTEXT below.\n\n"
        "Rules, no exceptions:\n"
        "1. If the question is not about the portfolio owner, respond with exactly: "
        f'"{FALLBACK_MESSAGE}"\n'
        "2. If the question IS about the portfolio owner but CONTEXT doesn't contain the "
        f'answer, also respond with exactly: "{FALLBACK_MESSAGE}"\n'
        "3. Never use outside knowledge, even if you know the answer — only the CONTEXT.\n"
        "4. NEVER invent specific facts not explicitly present in the CONTEXT.\n"
        "5. Keep answers to 1-3 sentences. Be direct, no filler.\n"
        "6. NEVER include raw URLs, email addresses, or markdown links — the UI shows "
        "those separately as buttons.\n"
        "7. If PREVIOUS CONVERSATION is provided below, use it only to resolve "
        "follow-up references like 'that one' or 'the second project' — never let it "
        "override rule 1-4.\n\n"
        f"{FEW_SHOT_EXAMPLES}\n"
        f"{state['history']}\n\n"
        f"CONTEXT:\n{full_context}"
    )

    llm = ChatGroq(model=settings.GROQ_MODEL, api_key=settings.GROQ_API_KEY, temperature=0.1, max_tokens=300)
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=state["user_message"])])
    reply = response.content.strip()
    was_fallback = FALLBACK_MESSAGE in reply

    state["reply"] = reply
    state["was_fallback"] = was_fallback
    state["actions"] = [] if was_fallback else _detect_actions(state["user_message"], state["always_values"])
    return state


def _should_retry(state: ChatState) -> str:
    if not state["retrieved_context"] and not state["retried"]:
        return "reformulate"
    return "generate"


_graph = StateGraph(ChatState)
_graph.add_node("retrieve", _node_retrieve)
_graph.add_node("reformulate", _node_reformulate_and_retry)
_graph.add_node("generate", _node_generate)
_graph.set_entry_point("retrieve")
_graph.add_conditional_edges("retrieve", _should_retry, {"reformulate": "reformulate", "generate": "generate"})
_graph.add_edge("reformulate", "generate")
_graph.add_edge("generate", END)
_compiled_graph = _graph.compile()


def get_chat_reply_graph(db: Session, session_id: str, user_message: str) -> tuple[str, bool, list[ChatAction]]:
    if not settings.GROQ_API_KEY:
        return ("The chatbot isn't configured yet — the site owner needs to add a Groq API key.", True, [])

    ctx = _build_always_context(db)

    initial_state: ChatState = {
        "db": db,
        "session_id": session_id,
        "user_message": user_message,
        "history": _get_history(db, session_id),
        "always_context": ctx["text"],
        "always_values": ctx["values"],
        "retrieved_context": "",
        "reply": "",
        "was_fallback": False,
        "actions": [],
        "retried": False,
    }

    final_state = _compiled_graph.invoke(initial_state)
    return final_state["reply"], final_state["was_fallback"], final_state["actions"]