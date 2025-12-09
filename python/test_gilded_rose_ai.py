import pytest
from gilded_rose_refactored import GildedRose, Item

# Helper to run update_quality for N days
def run_days(items, days):
    gr = GildedRose(items)
    for _ in range(days):
        gr.update_quality()
    return items

# --- General Items ---

def test_general_item_quality_decreases_by_one():
    item = Item("foo", 10, 20)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 19
    assert item.sell_in == 9

def test_general_item_quality_degrades_twice_after_sell_in():
    item = Item("foo", 0, 10)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 8
    assert item.sell_in == -1

def test_general_item_quality_never_negative():
    item = Item("foo", 5, 0)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 0

def test_general_item_quality_degrades_to_zero():
    item = Item("foo", 0, 1)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 0

def test_general_item_sell_in_decreases():
    item = Item("foo", 5, 10)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.sell_in == 4

# --- Aged Brie ---

def test_aged_brie_increases_in_quality():
    item = Item("Aged Brie", 2, 0)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 1
    assert item.sell_in == 1

def test_aged_brie_quality_max_50():
    item = Item("Aged Brie", 2, 50)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 50

def test_aged_brie_increases_twice_after_sell_in():
    item = Item("Aged Brie", 0, 48)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 50

def test_aged_brie_quality_does_not_exceed_50_after_multiple_days():
    item = Item("Aged Brie", 1, 49)
    items = run_days([item], 3)
    assert items[0].quality == 50

def test_aged_brie_sell_in_decreases():
    item = Item("Aged Brie", 5, 10)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.sell_in == 4

# --- Sulfuras ---

def test_sulfuras_never_decreases_in_quality():
    item = Item("Sulfuras, Hand of Ragnaros", 0, 80)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 80

def test_sulfuras_never_decreases_in_sell_in():
    item = Item("Sulfuras, Hand of Ragnaros", 5, 80)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.sell_in == 5

def test_sulfuras_quality_remains_unchanged_after_multiple_days():
    item = Item("Sulfuras, Hand of Ragnaros", 0, 80)
    items = run_days([item], 10)
    assert items[0].quality == 80

def test_sulfuras_sell_in_remains_unchanged_after_multiple_days():
    item = Item("Sulfuras, Hand of Ragnaros", 0, 80)
    items = run_days([item], 10)
    assert items[0].sell_in == 0

# --- Backstage Passes ---

def test_backstage_passes_increase_by_one_above_10_days():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 15, 20)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 21

def test_backstage_passes_increase_by_two_between_10_and_6_days():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 22

def test_backstage_passes_increase_by_three_between_5_and_0_days():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 23

def test_backstage_passes_quality_drops_to_zero_after_concert():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 0

def test_backstage_passes_quality_max_50():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 5, 49)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 50

def test_backstage_passes_quality_does_not_exceed_50():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 5, 50)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 50

def test_backstage_passes_sell_in_decreases():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.sell_in == 4

def test_backstage_passes_quality_increase_multiple_days():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 12, 20)
    items = run_days([item], 2)
    assert items[0].quality == 22

def test_backstage_passes_quality_increase_to_max():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 6, 48)
    items = run_days([item], 2)
    assert items[0].quality == 50

def test_backstage_passes_quality_drop_to_zero_after_multiple_days():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 1, 20)
    items = run_days([item], 2)
    assert items[0].quality == 0

# --- Edge Cases ---

def test_quality_never_negative_for_any_item():
    items = [
        Item("foo", 0, 0),
        Item("Aged Brie", 0, 0),
        Item("Backstage passes to a TAFKAL80ETC concert", 0, 0),
        Item("Sulfuras, Hand of Ragnaros", 0, 80)
    ]
    gr = GildedRose(items)
    gr.update_quality()
    for item in items:
        assert item.quality >= 0

def test_quality_never_exceeds_50_for_non_sulfuras():
    items = [
        Item("Aged Brie", 5, 50),
        Item("Backstage passes to a TAFKAL80ETC concert", 5, 50)
    ]
    gr = GildedRose(items)
    gr.update_quality()
    for item in items:
        assert item.quality <= 50

def test_multiple_items_update_independently():
    items = [
        Item("foo", 1, 10),
        Item("Aged Brie", 1, 10),
        Item("Backstage passes to a TAFKAL80ETC concert", 11, 10),
        Item("Sulfuras, Hand of Ragnaros", 0, 80)
    ]
    gr = GildedRose(items)
    gr.update_quality()
    assert items[0].quality == 9
    assert items[1].quality == 11
    assert items[2].quality == 11
    assert items[3].quality == 80

def test_repr_returns_expected_string():
    item = Item("foo", 1, 2)
    assert repr(item) == "foo, 1, 2"

def test_general_item_quality_degrades_twice_after_multiple_days():
    item = Item("foo", 0, 10)
    items = run_days([item], 2)
    assert items[0].quality == 6

def test_aged_brie_quality_increases_after_sell_in_multiple_days():
    item = Item("Aged Brie", 0, 48)
    items = run_days([item], 2)
    assert items[0].quality == 50

def test_backstage_passes_quality_increase_on_boundaries():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 11, 20)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 21

def test_backstage_passes_quality_increase_on_10_days():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 22

def test_backstage_passes_quality_increase_on_5_days():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 23

def test_backstage_passes_quality_drop_to_zero_on_negative_sell_in():
    item = Item("Backstage passes to a TAFKAL80ETC concert", -1, 20)
    gr = GildedRose([item])
    gr.update_quality()
    assert item.quality == 0