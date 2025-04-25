1.	

class TrieNode:
    def __init__(self):
        self.children, self.is_end = {}, False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        return self._collect(node, prefix)

    def _collect(self, node, prefix):
        res = [prefix] if node.is_end else []
        for ch, child in node.children.items():
            res += self._collect(child, prefix + ch)
        return res

def main():
    trie = Trie()
    while True:
        print("1. Insert word\n2. Autocomplete\n3. Exit")
        match input("Choice: ").strip():
            case '1':
                trie.insert(input("Word: ").strip())
            case '2':
                prefix = input("Prefix: ").strip()
                words = trie.search(prefix)
                print("Suggestions:", words if words else "None")
            case '3':
                break
            case _:
                print("Invalid choice.")

if __name__ == "__main__":
    main()

—--------------------------------

2.	
import heapq
class Graph:
    def __init__(self):
        self.edges = {}

    def add_node(self, node):
        self.edges[node] = []

    def add_edge(self, u, v, w):
        self.edges[u].append((v, w))
        self.edges[v].append((u, w))

def dijkstra(graph, start):
    dist = {n: float('inf') for n in graph.edges}
    prev = {n: None for n in graph.edges}
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue
        for v, w in graph.edges[u]:
            if (alt := d + w) < dist[v]:
                dist[v], prev[v] = alt, u
                heapq.heappush(heap, (alt, v))
    return dist, prev

def shortest_route(graph, start, end):
    dist, prev = dijkstra(graph, start)
    if dist[end] == float('inf'): return [], float('inf')
    path = []
    while end:
        path.append(end)
        end = prev[end]
    return path[::-1], dist[path[0]]

def main():
    g = Graph()
    for _ in range(int(input("No. of locations: "))):
        g.add_node(input().strip())
    for _ in range(int(input("No. of paths: "))):
        u, v, w = input().split()
        g.add_edge(u, v, int(w))
    start, end = input("Start: ").strip(), input("End: ").strip()
    path, time = shortest_route(g, start, end)
    print(f"Shortest route: {' -> '.join(path)}\nTravel time: {time}" if path else f"No route found from {start} to {end}")

if __name__ == "__main__":
    main()

—--------------------
3.
class DisjointSet:
    def __init__(self, verts):
        self.p = {v: v for v in verts}
        self.r = {v: 0 for v in verts}

    def find(self, v):
        if self.p[v] != v:
            self.p[v] = self.find(self.p[v])
        return self.p[v]

    def union(self, u, v):
        ru, rv = self.find(u), self.find(v)
        if ru != rv:
            if self.r[ru] < self.r[rv]:
                self.p[ru] = rv
            else:
                self.p[rv] = ru
                if self.r[ru] == self.r[rv]: self.r[ru] += 1

def kruskal(verts, edges):
    ds, mst = DisjointSet(verts), []
    for u, v, w in sorted(edges, key=lambda x: x[2]):
        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            mst.append((u, v, w))
    return mst

def main():
    verts = input("Cities: ").split()
    edges = [tuple(input().split()) for _ in range(int(input("No. of connections: ")))]
    edges = [(u, v, int(w)) for u, v, w in edges]
    mst = kruskal(verts, edges)
    print("MST Edges:")
    for u, v, w in mst:
        print(f"{u} - {v}: {w}")

if __name__ == "__main__":
    main()

—----------------------------------------------------------
4.

class ChessGame:
    def __init__(self): 
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.white_turn = True

    def print_board(self):
        for row in self.board: print(' '.join(row))

    def make_move(self, source, dest):
        sr, sc = 8 - int(source[1]), ord(source[0]) - ord('a')
        dr, dc = 8 - int(dest[1]), ord(dest[0]) - ord('a')
        self.board[dr][dc], self.board[sr][sc] = self.board[sr][sc], ' '

    def play_game(self):
        while True:
            self.print_board()
            print(f"{'White' if self.white_turn else 'Black'}'s turn")
            self.make_move(input("Source: "), input("Destination: "))
            self.white_turn = not self.white_turn

ChessGame().play_game()


—-------------------------
5.

class SegmentTree:
    def __init__(self, scores):
        self.n, self.scores = len(scores), scores
        self.tree = [0] * (4 * self.n)
        self._build(0, 0, self.n - 1)

    def _build(self, node, start, end):
        if start == end:
            self.tree[node] = self.scores[start]
        else:
            mid = (start + end) // 2
            self._build(2*node+1, start, mid)
            self._build(2*node+2, mid+1, end)
            self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]

    def update_score(self, idx, val):
        self.scores[idx] = val
        def _update(node, start, end):
            if start == end:
                self.tree[node] = val
            else:
                mid = (start + end) // 2
                if idx <= mid: _update(2*node+1, start, mid)
                else: _update(2*node+2, mid+1, end)
                self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]
        _update(0, 0, self.n-1)

    def get_range_sum(self, l, r):
        def _query(node, start, end):
            if r < start or l > end: return 0
            if l <= start and end <= r: return self.tree[node]
            mid = (start + end) // 2
            return _query(2*node+1, start, mid) + _query(2*node+2, mid+1, end)
        return _query(0, 0, self.n-1)

def main():
    scores = [int(input(f"Score for student {i+1}: ")) for i in range(int(input("Number of students: ")))]
    st = SegmentTree(scores)

    while True:
        choice = int(input("\n1. Range Sum\n2. Update Score\n3. View All Scores\n4. Exit\nChoice: "))
        if choice == 4: break
        if choice == 1:
            l, r = map(int, input("Range (start end): ").split())
            print(f"Sum: {st.get_range_sum(l-1, r-1)}")
        elif choice == 2:
            idx, score = map(int, input("Update (index new_score): ").split())
            st.update_score(idx-1, score)
        elif choice == 3:
            print("All Student Scores:", st.scores)

if __name__ == "__main__":
    main()

—--------------------------------------------------------------------------
6. 
import numpy as np
class QuadTreeNode:
    def __init__(self, boundary):
        self.boundary, self.cities, self.children = boundary, [], [None] * 4

class QuadTree:
    def __init__(self, boundary, capacity):
        self.root, self.capacity = QuadTreeNode(boundary), capacity

    def insert(self, city):
        self._insert(self.root, city)

    def _insert(self, node, city):
        if len(node.cities) < self.capacity:
            node.cities.append(city)
        else:
            if not node.children[0]: self._subdivide(node)
            for child in node.children:
                if self._contains(child.boundary, city): self._insert(child, city)

    def _subdivide(self, node):
        x, y, w, h = node.boundary
        half_w, half_h = w / 2, h / 2
        node.children = [QuadTreeNode((x + i * half_w, y + j * half_h, half_w, half_h)) for i in range(2) for j in range(2)]
        for city in node.cities:
            for child in node.children:
                if self._contains(child.boundary, city): self._insert(child, city)
        node.cities.clear()

    def _contains(self, boundary, city):
        x, y, w, h = boundary
        return x <= city[0] < x + w and y <= city[1] < y + h

    def query_location(self, point):
        return self._query_location(self.root, point)

    def _query_location(self, node, point):
        if not node or not self._contains(node.boundary, point): return []
        if not node.children[0]: return node.cities
        return [city for child in node.children for city in self._query_location(child, point)]

    def query_nearest_city(self, point):
        return self._query_nearest(self.root, point, float('inf'), None)

    def _query_nearest(self, node, point, min_dist, nearest_city):
        if not node or not self._contains(node.boundary, point): return nearest_city
        for city in node.cities:
            dist = np.linalg.norm(np.array(city) - np.array(point))
            if dist < min_dist: min_dist, nearest_city = dist, city
        for child in node.children:
            nearest_city = self._query_nearest(child, point, min_dist, nearest_city)
        return nearest_city

boundary = tuple(map(int, input("Enter the map boundary (x, y, width, height): ").split()))
capacity = int(input("Enter the capacity of each quadtree node: "))
quadtree = QuadTree(boundary, capacity)

for _ in range(int(input("Enter the number of cities to insert: "))):
    quadtree.insert(tuple(map(int, input("Enter city coordinates (x, y): ").split())))

query_point = tuple(map(int, input("Enter the query point (x, y): ").split()))
print("Cities near query point:", quadtree.query_location(query_point))
print("Nearest city to query point:", quadtree.query_nearest_city(query_point))



