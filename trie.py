from typing import List

class TrieNode:
    def __init__(self,label: str = ""):
        self.children = {}
        self.is_end_of_word = False
        self.label = label

class Trie:
    def __init__(self, is_compressed: bool):
        self.root = TrieNode()
        self.is_compressed = is_compressed
        self.is_prefix = True

    def construct_trie_from_text(self, keys: List[str]) -> None:
        self.is_prefix = True
        for key in keys:
            self.insert(key)
            
        if self.is_compressed:
            self.prefix_compress(self.root)
    
    def prefix_compress(self, node: TrieNode, parent=None, char=None) -> None:
        while len(node.children) == 1 and not node.is_end_of_word:
            next_node = next(iter(node.children.values()))
            node.label += next_node.label 
            node.children = next_node.children
            node.is_end_of_word = next_node.is_end_of_word
            if parent:
                parent.children[char] = node
        for char, child in list(node.children.items()):
            self.prefix_compress(child, node, char)

    def insert(self, key: str) -> None:
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode(char)
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, key: str) -> bool:
        node = self.root
        for char in key:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def construct_suffix_tree_from_text(self, keys: List[str]) -> None:
        self.is_prefix = False
        for key in keys:
            for i in range(len(key)):
                self.insert(key[i:])
    
        if self.is_compressed:
            self.suffix_compress(self.root)
    
    def suffix_compress(self, node: TrieNode, parent=None, char=None) -> None:
        while len(node.children) == 1 and not node.is_end_of_word:
            next_node = next(iter(node.children.values()))
            node.label += next_node.label 
            node.children = next_node.children
            node.is_end_of_word = next_node.is_end_of_word
            if parent:
                parent.children[char] = node
        for char, child in list(node.children.items()):
            self.suffix_compress(child, node, char)
    
    def search_and_get_depth(self, key: str) -> int:
        node = self.root
        depth = 0
        i = 0
        while i < len(key):
            found = False
            for _, child in node.children.items():
                if key[i : i + len(child.label)] == child.label:
                    depth += 1
                    node = child
                    i += len(child.label)
                    found = True
                    break
            if not found:
                return -1
        return depth 

        

