class Node:
    def __init__(self, max_children):
        self.keys = [None for i in range(max_children-1)]
        self.children = [None for i in range(max_children)]
        self.size = 0
        self.is_leaf = True

    def insert(self, key, child_to_add):
        if self.keys[-1] is None:
            for i in range(len(self.keys)):
                if self.keys[i] is None:
                    idx = i
                    break
                if key < self.keys[i]:
                    idx = i
                    break
            self.keys.insert(idx, key)
            self.keys = self.keys[:-1]
            self.size+=1
            for i in range(len(self.children)-1, idx+1, -1):
                self.children[i] = self.children[i-1]
            self.children[idx+1]=child_to_add
            return None

        center_id = len(self.keys) // 2
        center_elem = self.keys.pop(center_id)

        idx = None
        for i in range(len(self.keys)):
            if key < self.keys[i]:
                idx = i
                break

        if idx is None:
            idx = len(self.keys)

        self.keys.insert(idx, key)

        if key > center_elem:
            id_to_split = center_id
        else:
            id_to_split = center_id+1

        new_key_list = self.keys[id_to_split:]

        new_node = Node(len(self.keys)+1)

        if child_to_add is not None:
            new_node.is_leaf = False

        for i in range(len(new_key_list)):
            new_node.keys[i] = new_key_list[i]
            if new_key_list[i] is not None:
                new_node.size+=1

        for i in range(id_to_split+1, len(self.keys)+1):
            if self.children[i] is not None:
                new_node.children[i-id_to_split-1] = self.children[i]

        for i in range(id_to_split, len(self.keys)):
            if self.keys[i] is not None:
                self.size -= 1
            self.keys[i] = None
        for i in range(id_to_split+1, len(self.children)):
            self.children[i] = None

        if child_to_add is not None:
            if key < center_elem:
                self.children[id_to_split+1] = child_to_add
            else:
                for k in range(len(new_node.keys)):
                    if new_node.keys[k] == key:
                        new_node.children.insert(k+1, child_to_add)
                        break

        return center_elem, new_node


class BTree:
    def __init__(self, max_children_):
        self.root = None
        self.max_children = max_children_

    def insert(self, key):
        if self.root is None:
            self.root = Node(self.max_children)
            self.root.keys[0] = key
            self.root.size += 1
            self.root.is_leaf = False
            return None
        else:
            tuple = self.insert_rec(key, self.root)
            if tuple is not None:
                center_elem, new_node = tuple
                new_root = Node(self.max_children)
                new_root.keys[0] = center_elem
                new_root.children[0] = self.root
                new_root.children[1] = new_node
                new_root.is_leaf = False
                new_root.size = 1
                self.root = new_root
            return None

    def insert_rec(self, key, node, child_to_add=None):

        if node is None:
            node = Node(self.max_children)
            node.keys[0] = key
            node.size += 1
            return None

        parent_idx = None
        parent_key = None
        for i in range(len(node.keys)):
            if node.keys[i] is None:
                parent_idx = i
                break
            if key < node.keys[i]:
                parent_key = node.keys[i]
                parent_idx = i
                break

        if parent_idx is None:
            parent_idx = len(node.keys)

        if node.keys[-1] is None and node.children[parent_idx] is None:
            for i in range(len(node.keys) - 1, parent_idx, -1):
                node.keys[i] = node.keys[i - 1]
            node.keys[parent_idx] = key
            for i in range(len(node.keys), parent_idx-1, -1):
                node.children[i] = node.children[i - 1]
            node.size += 1
            return None

        #jesli nie jest lisciem
        if node.is_leaf is False:
            if node.children[parent_idx] is None:
                node.children[parent_idx] = Node(self.max_children)
            tuple = self.insert_rec(key, node.children[parent_idx])

            if tuple is None:
                return None
            #jesli potomek zostal podzielony
            else:
                center_elem, new_node = tuple
                node.is_leaf = True
                tuple = self.insert_rec(center_elem, node, new_node)
                node.is_leaf = False
                return tuple

        else:
            tuple = node.insert(key, child_to_add)
            return tuple


    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            for i in range(node.size+1):
                self._print_tree(node.children[i], lvl+1)
                if i<node.size:
                    print(lvl*'  ', node.keys[i])


lst = [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18, 15, 10, 19]

b_tree = BTree(4)

for i in range(len(lst)):
    b_tree.insert(lst[i])

# print tree
b_tree.print_tree()

second_tree = BTree(4)

for i in range(20):
    second_tree.insert(i)

second_tree.print_tree()

for i in range(20, 200):
    second_tree.insert(i)

second_tree.print_tree()

third_tree = BTree(6)

for i in range(200):
    third_tree.insert(i)

third_tree.print_tree()

