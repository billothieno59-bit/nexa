from core.applications.api.web_skill_gateway import (
    run_web_skill,
    list_web_reachable_skills,
)


def test_builtin_skill_is_executed():
    result = run_web_skill("knowledge.recall_fact", subject="nexa_web_smoke_test")
    assert result.status == "executed"


def test_privileged_skill_is_denied_before_execution():
    result = run_web_skill("generation.voice", text="hello")
    assert result.status == "denied"
    assert "builtin" in result.message.lower()


def test_system_shutdown_is_denied():
    result = run_web_skill("system.shutdown_nexa", provided_key="anything")
    assert result.status == "denied"


def test_unknown_skill_is_denied():
    result = run_web_skill("nonexistent.skill")
    assert result.status == "denied"


def test_knowledge_write_is_denied_interface_node_lacks_permission():
    # INTERFACE_NODE only has TEXT.PROCESS and KNOWLEDGE.READ per
    # trust_bridge.py's ROLE_PERMISSIONS — not KNOWLEDGE.WRITE. This
    # is expected, correct behavior: the web client cannot write
    # facts, only read them and use TEXT.PROCESS skills.
    result = run_web_skill(
        "knowledge.remember_fact",
        subject="x", predicate="y", value="z",
    )
    assert result.status == "denied"


def test_list_web_reachable_skills_excludes_privileged():
    reachable = list_web_reachable_skills()
    assert "generation.voice" not in reachable
    assert "generation.image" not in reachable
    assert "ai.reason" not in reachable
    assert "system.shutdown_nexa" not in reachable
    assert "agriculture.crop_advisor" in reachable
