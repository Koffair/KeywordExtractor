from src.hu_keywords import _remove_article, _remove_overlappings

def test__remove_overlappings_empty():
    assert _remove_overlappings([]) == []


def test__remove_overlappings_no_overlap():
    assert _remove_overlappings(["a", "b", "c"]) == ["a", "b", "c"]


def test__remove_overlappings_overlaps():
    assert _remove_overlappings(["Angela Merkel", "Merkel", "Biden", "Joe Biden"]) == [
        "Angela Merkel",
        "Joe Biden",
    ]


def test__remove_article_no_article():
    assert _remove_article("World Health Organization") == "World Health Organization"


def test__remove_article_false_start():
    assert _remove_article("Theodor Altmann") == "Theodor Altmann"


def test__remove_article_lower():
    assert _remove_article("az Országház") == "Országház"


def test__remove_indefinite_article_lower():
    assert _remove_article("egy Edda album") == "Edda album"
