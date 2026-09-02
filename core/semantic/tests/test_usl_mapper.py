"""Tests for the Universal Semantic Layer mapper."""

from core.semantic.parser.usl_mapper import (
    UniversalSemanticLayerMapper,
    global_usl_mapper,
)


def test_known_swahili_intent_resolves_and_is_authorized():
    mapper = UniversalSemanticLayerMapper()

    result = mapper.generate_universal_semantic_token(
        {
            "normalized_swahili_target": "pesa",
            "source_variety": "sw-ke",
        }
    )

    assert result == {
        "usl_version": "1.0.0",
        "resolved_intent_token": "INTENT_RESOURCE_VALUE_TRANSACT",
        "origin_variety_source": "sw-ke",
        "governed_execution_authorized": True,
        "safety_status": "VERIFIED",
    }


def test_all_supported_intent_tokens_resolve():
    mapper = UniversalSemanticLayerMapper()

    expected = {
        "hali gani": "INTENT_SYSTEM_DIAGNOSTIC_CHECK",
        "habari gani": "INTENT_SYSTEM_DIAGNOSTIC_CHECK",
        "mipango": "INTENT_PLANNING_ORCHESTRATION_GET",
        "pesa": "INTENT_RESOURCE_VALUE_TRANSACT",
        "kazi": "INTENT_PROCESS_EXECUTION_RUN",
        "viatu": "INTENT_IDENTITY_ASSET_QUERY",
    }

    for text, expected_token in expected.items():
        result = mapper.generate_universal_semantic_token(
            {
                "normalized_swahili_target": text,
                "source_variety": "sw-ke",
            }
        )

        assert result["resolved_intent_token"] == expected_token
        assert result["governed_execution_authorized"] is True
        assert result["safety_status"] == "VERIFIED"


def test_matching_is_case_insensitive_and_whitespace_is_trimmed():
    mapper = UniversalSemanticLayerMapper()

    result = mapper.generate_universal_semantic_token(
        {
            "normalized_swahili_target": "  PeSa  ",
            "source_variety": "sw-ke",
        }
    )

    assert result["resolved_intent_token"] == ("INTENT_RESOURCE_VALUE_TRANSACT")

    assert result["governed_execution_authorized"] is True
    assert result["safety_status"] == "VERIFIED"


def test_unknown_intent_fails_closed():
    mapper = UniversalSemanticLayerMapper()

    result = mapper.generate_universal_semantic_token(
        {
            "normalized_swahili_target": "something unknown",
            "source_variety": "sw-ke",
        }
    )

    assert result["usl_version"] == "1.0.0"

    assert result["resolved_intent_token"] == ("INTENT_UNKNOWN_PASSTHROUGH")

    assert result["origin_variety_source"] == "sw-ke"

    assert result["governed_execution_authorized"] is False
    assert result["safety_status"] == "CLOSED"


def test_empty_target_fails_closed():
    mapper = UniversalSemanticLayerMapper()

    result = mapper.generate_universal_semantic_token(
        {
            "normalized_swahili_target": "",
            "source_variety": "sw-ke",
        }
    )

    assert result["resolved_intent_token"] == ("INTENT_UNKNOWN_PASSTHROUGH")

    assert result["governed_execution_authorized"] is False
    assert result["safety_status"] == "CLOSED"


def test_missing_target_fails_closed():
    mapper = UniversalSemanticLayerMapper()

    result = mapper.generate_universal_semantic_token(
        {
            "source_variety": "sw-ke",
        }
    )

    assert result["resolved_intent_token"] == ("INTENT_UNKNOWN_PASSTHROUGH")

    assert result["governed_execution_authorized"] is False
    assert result["safety_status"] == "CLOSED"


def test_source_variety_defaults_when_missing():
    mapper = UniversalSemanticLayerMapper()

    result = mapper.generate_universal_semantic_token(
        {
            "normalized_swahili_target": "kazi",
        }
    )

    assert result["origin_variety_source"] == "unknown_source"


def test_global_mapper_instance_is_available():
    assert isinstance(
        global_usl_mapper,
        UniversalSemanticLayerMapper,
    )
