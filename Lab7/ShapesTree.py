from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import Qt
from Group import Group


class ShapesTree:
    def __init__(self, tree_widget, container):
        self.tree = tree_widget
        self.container = container

        self._ignore_tree_events = False
        self._obj_to_item = {}

        self.tree.setHeaderLabel("Objects")
        self.tree.setSelectionMode(self.tree.ExtendedSelection)

        self.tree.itemSelectionChanged.connect(self._on_tree_selection_changed)
        self.container.subscribe(self)

        self.rebuild()

    def update(self, event):

        if event == "structure":
            self.rebuild()

        elif event == "selection":
            self.sync_from_container()

    def rebuild(self):
        self._ignore_tree_events = True
        self.tree.clear()
        self._obj_to_item.clear()

        for shape in self.container.get_shapes():
            self._process_node(self.tree.invisibleRootItem(), shape)

        self._ignore_tree_events = False

        self.tree.expandAll()
        self.sync_from_container()

    def _process_node(self, parent_item, shape):
        item = QTreeWidgetItem(parent_item)
        item.setText(0, shape.type_shape())
        item.setData(0, Qt.UserRole, shape)

        self._obj_to_item[shape] = item

        if isinstance(shape, Group):
            for child in shape.get_child():
                self._process_node(item, child)

    def _on_tree_selection_changed(self):
        if self._ignore_tree_events:
            return

        selected_shapes = []

        for item in self.tree.selectedItems():
            shape = item.data(0, Qt.UserRole)

            parent = item.parent()
            if parent:
                group = parent.data(0, Qt.UserRole)
                if group:
                    selected_shapes.append(group)
            else:
                selected_shapes.append(shape)

        self.container.set_selection(selected_shapes)

    def sync_from_container(self):

        self._ignore_tree_events = True
        self.tree.clearSelection()

        for shape in self.container.get_selected():
            item = self._obj_to_item.get(shape)
            if item:
                item.setSelected(True)

        self._ignore_tree_events = False
