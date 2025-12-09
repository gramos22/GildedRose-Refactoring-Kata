# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class Item:
    """
    Represents an item in the inventory.
    """
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class ItemUpdater(ABC):
    """
    Abstract base class for item update strategies.
    """
    @abstractmethod
    def update(self, item: Item):
        pass

class NormalItemUpdater(ItemUpdater):
    """
    Updates normal items.
    """
    def update(self, item: Item):
        if item.quality > 0:
            item.quality -= 1
        item.sell_in -= 1
        if item.sell_in < 0 and item.quality > 0:
            item.quality -= 1

class AgedBrieUpdater(ItemUpdater):
    """
    Updates 'Aged Brie' items.
    """
    def update(self, item: Item):
        if item.quality < 50:
            item.quality += 1
        item.sell_in -= 1
        if item.sell_in < 0 and item.quality < 50:
            item.quality += 1

class SulfurasUpdater(ItemUpdater):
    """
    'Sulfuras' is a legendary item, never has to be sold or decreases in quality.
    """
    def update(self, item: Item):
        # Sulfuras does not change
        pass

class BackstagePassUpdater(ItemUpdater):
    """
    Updates 'Backstage passes' items.
    """
    def update(self, item: Item):
        if item.quality < 50:
            item.quality += 1
            if item.sell_in < 11 and item.quality < 50:
                item.quality += 1
            if item.sell_in < 6 and item.quality < 50:
                item.quality += 1
        item.sell_in -= 1
        if item.sell_in < 0:
            item.quality = 0

class ItemUpdaterFactory:
    """
    Factory to get the correct updater for an item.
    """
    @staticmethod
    def get_updater(item: Item) -> ItemUpdater:
        if item.name == "Aged Brie":
            return AgedBrieUpdater()
        elif item.name == "Sulfuras, Hand of Ragnaros":
            return SulfurasUpdater()
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            return BackstagePassUpdater()
        else:
            return NormalItemUpdater()

class GildedRose:
    """
    Main class to update inventory items.
    """
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        """
        Updates quality and sell_in for all items in inventory.
        """
        for item in self.items:
            updater = ItemUpdaterFactory.get_updater(item)
            updater.update(item)