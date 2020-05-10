from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene
from PyQt5.QtGui import QColor

class BlockDiagram():
    def __init__(self, blocks, block_labels, title):
        self.blocks = blocks
        self.block_labels = block_labels
        self.title = title

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 750, 700)

    def add_tree_items(self, block_type): # switch colour depending on type (expeneses / income)
        for it in self.blocks: # loop through dict list
            # Construct a square object
            rect = QGraphicsRectItem(it["x"], it["y"], it["dx"], it["dy"])

            if block_type == "income":
                rect.setBrush(QColor.fromRgb(97, 247, 255))

            elif block_type == "expenses":
                rect.setBrush(QColor.fromRgb(255, 105, 97))

            self.scene.addItem(rect)

        return self.scene
        