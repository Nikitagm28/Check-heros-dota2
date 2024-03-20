import pytest
from scraper import get_hero_info, get_hero_counters

@pytest.mark.parametrize("hero_name", ["Invoker", "Anti-Mage", "NotAValidHero"])
def test_get_hero_info(hero_name):
    result = get_hero_info(hero_name)
    if result.get("error"):
        assert "Герой не найден" in result["error"]
    else:
        assert "hero_name" in result
        assert "popular_lanes" in result
        assert isinstance(result["hero_name"], str)
        assert isinstance(result["popular_lanes"], list)
        assert len(result["popular_lanes"]) > 0

@pytest.mark.parametrize("hero_name", ["Invoker", "Anti-Mage", "NotAValidHero"])
def test_get_hero_counters(hero_name):
    result = get_hero_counters(hero_name)
    if result.get("error"):
        assert "Герой не найден" in result["error"]
    else:
        assert "counters" in result
        assert isinstance(result["counters"], list)
        assert len(result["counters"]) > 0
