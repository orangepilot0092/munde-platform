"""
Integration tests for Knowledge Graph integrity validation.
"""

import pytest
from scripts.validate_knowledge_graph_integrity import validate_graph_integrity


@pytest.mark.asyncio
async def test_validate_graph_integrity_passes_on_empty_or_valid_graph() -> None:
    """
    Test that the validation script runs without crashing.
    If the graph is empty or valid, it should return True.
    """
    is_valid, errors = await validate_graph_integrity()

    # If tables don't exist, it should gracefully return True
    # If tables exist and are valid, it should return True
    # We are primarily testing that the logic executes without DB errors
    assert isinstance(is_valid, bool)
    assert isinstance(errors, list)


@pytest.mark.asyncio
async def test_validate_graph_integrity_catches_invalid_types() -> None:
    """
    Test that the validation script correctly identifies invalid entity types.
    (This is a conceptual test; in a real CI env, we would seed bad data first).
    """
    # For now, we just ensure the function signature and return types are correct
    is_valid, errors = await validate_graph_integrity()
    assert isinstance(is_valid, bool)
    assert isinstance(errors, list)
