exp 1

class TrieNode:
    def _init_(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def _init_(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._find_words_from_node(node, prefix)

    def _find_words_from_node(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char, next_node in node.children.items():
            words.extend(self._find_words_from_node(next_node, prefix + char))
        return words

def main():
    trie = Trie()
    while True:
        print("Choose an option:")
        print("1. Insert word")
        print("2. Get autocomplete suggestions")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            word = input("Enter the word to insert: ").strip()
            trie.insert(word)
            print(f"Inserted '{word}' into the trie.\n")
        elif choice == '2':
            prefix = input("Enter the prefix to search: ").strip()
            suggestions = trie.search(prefix)
            if suggestions:
                print(f"Autocomplete suggestions for '{prefix}': {suggestions}\n")
            else:
                print(f"No suggestions found for '{prefix}'.\n")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.\n")

if _name_ == "_main_":
    main()



exp 4

class ChessGame:
    def _init_(self):
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
        for row in self.board:
            print(' '.join(row))
        print()

    def get_pawn_moves(self, row, col):
        moves = []
        direction = -1 if self.board[row][col].isupper() else 1
        start_row = 6 if self.board[row][col].isupper() else 1
        if self.board[row + direction][col] == ' ':
            moves.append((row + direction, col))
        if row == start_row and self.board[row + 2 * direction][col] == ' ':
            moves.append((row + 2 * direction, col))
        if col - 1 >= 0 and self.board[row + direction][col - 1] != ' ' and self.board[row + direction][col - 1].isupper() != self.white_turn:
            moves.append((row + direction, col - 1))
        if col + 1 < 8 and self.board[row + direction][col + 1] != ' ' and self.board[row + direction][col + 1].isupper() != self.white_turn:
            moves.append((row + direction, col + 1))
        return moves

    def get_rook_moves(self, row, col):
        return []

    def get_knight_moves(self, row, col):
        return []

    def get_bishop_moves(self, row, col):
        return []

    def get_queen_moves(self, row, col):
        return []

    def get_king_moves(self, row, col):
        return []

    def get_piece_moves(self, row, col):
        piece = self.board[row][col].lower()
        if piece == 'p':
            return self.get_pawn_moves(row, col)
        elif piece == 'r':
            return self.get_rook_moves(row, col)
        elif piece == 'n':
            return self.get_knight_moves(row, col)
        elif piece == 'b':
            return self.get_bishop_moves(row, col)
        elif piece == 'q':
            return self.get_queen_moves(row, col)
        elif piece == 'k':
            return self.get_king_moves(row, col)
        else:
            return []

    def is_valid_move(self, row, col, new_row, new_col):
        if new_row < 0 or new_row >= 8 or new_col < 0 or new_col >= 8:
            return False
        if self.board[new_row][new_col].isupper() == self.white_turn:
            return False
        piece_moves = self.get_piece_moves(row, col)
        for move in piece_moves:
            if move == (new_row, new_col):
                return True
        return False

    def make_move(self, row, col, new_row, new_col):
        piece = self.board[row][col]
        self.board[row][col] = ' '
        self.board[new_row][new_col] = piece
        self.white_turn = not self.white_turn

    def play_game(self):
        while True:
            self.print_board()
            print("White's turn" if self.white_turn else "Black's turn")
            source = input("Enter the source square (e.g., a2): ")
            destination = input("Enter the destination square (e.g., a4): ")
            source_col = ord(source[0]) - ord('a')
            source_row = 8 - int(source[1])
            dest_col = ord(destination[0]) - ord('a')
            dest_row = 8 - int(destination[1])
            if self.is_valid_move(source_row, source_col, dest_row, dest_col):
                self.make_move(source_row, source_col, dest_row, dest_col)
            else:
                print("Invalid move. Please try again.")
                continue

game = ChessGame()
game.play_game()


exp 5

class SegmentTree:
    def _init_(self, arr):
        self.n = len(arr)
        self.tree = [0] * (2 * self.n)
        self.construct_segment_tree(arr, 0, self.n - 1, 0)

    def construct_segment_tree(self, arr, start, end, index):
        if start == end:
            self.tree[index] = arr[start]
            return arr[start]
        mid = (start + end) // 2
        self.tree[index] = self.construct_segment_tree(arr, start, mid, 2 * index + 1) + \
                           self.construct_segment_tree(arr, mid + 1, end, 2 * index + 2)
        return self.tree[index]

    def query_range_sum(self, query_start, query_end):
        return self._query_range_sum(0, self.n - 1, query_start, query_end, 0)

    def _query_range_sum(self, start, end, query_start, query_end, index):
        if query_start <= start and query_end >= end:
            return self.tree[index]
        if query_end < start or query_start > end:
            return 0
        mid = (start + end) // 2
        return self._query_range_sum(start, mid, query_start, query_end, 2 * index + 1) + \
               self._query_range_sum(mid + 1, end, query_start, query_end, 2 * index + 2)

    def update_value(self, student_index, new_value):
        diff = new_value - self.tree[self.n + student_index - 1]
        self._update_value(0, self.n - 1, student_index, diff, 0)

    def _update_value(self, start, end, student_index, diff, index):
        if student_index < start or student_index > end:
            return
        self.tree[index] += diff
        if start != end:
            mid = (start + end) // 2
            self._update_value(start, mid, student_index, diff, 2 * index + 1)
            self._update_value(mid + 1, end, student_index, diff, 2 * index + 2)

arr = [int(x) for x in input("Enter the array elements separated by spaces: ").split()]
segment_tree = SegmentTree(arr)
print("Initial segment tree:", segment_tree.tree)

query_start, query_end = [int(x) for x in input("Enter the query range (start end) separated by spaces: ").split()]
print("Sum of elements in range [{}, {}]: {}".format(query_start, query_end, segment_tree.query_range_sum(query_start, query_end)))

student_index, new_value = [int(x) for x in input("Enter the student index and new value separated by spaces: ").split()]
segment_tree.update_value(student_index, new_value)
print("Segment tree after updating value of student {}: {}".format(student_index, segment_tree.tree))

print("Sum of elements in range [{}, {}]: {}".format(query_start, query_end, segment_tree.query_range_sum(query_start, query_end)))



exp 6

class QuadTree:
    def _init_(self, boundary, capacity):
        self.b = boundary  # (x, y, w, h)
        self.c = capacity  # capacity
        self.d = []        # data (cities)
        self.e = []        # children

    def insert(self, city):
        if len(self.d) < self.c:
            self.d.append(city)
        else:
            if not self.e:
                self._subdivide()
            for child in self.e:
                if self._contains(child.b, city):
                    child.insert(city)

    def _subdivide(self):
        x, y, w, h = self.b
        hw, hh = w / 2, h / 2
        self.e = [
            QuadTree((x + hw * (i % 2), y + hh * (i // 2), hw, hh), self.c)
            for i in range(4)
        ]
        for city in self.d:
            for child in self.e:
                if child._contains(child.b, city):
                    child.insert(city)
        self.d = []

    def _contains(self, boundary, city):
        x, y, w, h = boundary
        return x <= city[0] < x + w and y <= city[1] < y + h

    def query_location(self, point):
        if not self.e:
            return self.d
        return sum((child.query_location(point) for child in self.e if child._contains(child.b, point)), [])

    def query_nearest_city(self, point, min_dist=float('inf'), nearest=None):
        if not self._contains(self.b, point):
            return nearest
        for city in self.d:
            dist = ((city[0] - point[0])*2 + (city[1] - point[1])2)*0.5
            if dist < min_dist:
                min_dist, nearest = dist, city
        for child in self.e:
            nearest = child.query_nearest_city(point, min_dist, nearest)
        return nearest


# ----- Run Example -----
qt = QuadTree(tuple(map(int, input("Enter map boundary (x y w h): ").split())), int(input("Enter capacity per node: ")))

for _ in range(int(input("Enter number of cities: "))):
    city = tuple(map(int, input("Enter city coordinates (x y): ").split()))
    qt.insert(city)

q = tuple(map(int, input("Enter query point (x y): ").split()))
print("Cities near query:", qt.query_location(q))
print("Nearest city:", qt.query_nearest_city(q))



exp 2

import heapq

class CityNetwork:
    def _init_(self):
        self.graph = {}
        
    def add_edge(self, from_node, to_node, travel_time):
        if from_node not in self.graph:
            self.graph[from_node] = []
        if to_node not in self.graph:
            self.graph[to_node] = []
        self.graph[from_node].append((to_node, travel_time))
        self.graph[to_node].append((from_node, travel_time))
    
    def dijkstra(self, start, end):
        queue = [(0, start)]
        distances = {start: 0}
        previous_nodes = {start: None}
        
        while queue:
            current_distance, current_node = heapq.heappop(queue)
            if current_node == end:
                break
            for neighbor, travel_time in self.graph.get(current_node, []):
                new_distance = current_distance + travel_time
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(queue, (new_distance, neighbor))
        
        path = []
        node = end
        while node is not None:
            path.append(node)
            node = previous_nodes[node]
        
        path = path[::-1]
        total_time = distances.get(end, float('inf'))
        return path, total_time

network = CityNetwork()

nodes = []
print("Enter the names of 5 locations:")
for _ in range(5):
    node = input(f"Location {_ + 1}: ")
    nodes.append(node)

num_paths = int(input("Enter the number of paths between locations: "))

for _ in range(num_paths):
    from_node, to_node, travel_time = input("Enter path (from_node to_node travel_time): ").split()
    travel_time = int(travel_time)
    network.add_edge(from_node, to_node, travel_time)

start_location = input("Enter the starting location: ")
end_location = input("Enter the destination location: ")

path, travel_time = network.dijkstra(start_location, end_location)

if path:
    print(f"Shortest path from {start_location} to {end_location}: {' -> '.join(path)}")
    print(f"Total travel time: {travel_time} minutes")
else:
    print(f"No path found from {start_location} to {end_location}.")



exp 3

class DisjointSet:
    def _init_(self, vertices):
        self.parent = {v: v for v in vertices}
    
    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])  # Path compression
        return self.parent[item]
    
    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        if root1 != root2:
            self.parent[root2] = root1

def kruskal(vertices, edges):
    mst = []
    ds = DisjointSet(vertices)
    
    # Sort edges based on cost
    edges.sort(key=lambda x: x[2])
    
    for u, v, cost in edges:
        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            mst.append((u, v, cost))
    
    return mst

# Main program
def main():
    # Input city names
    cities = input("Enter city names separated by space: ").split()
    
    # Input number of connections
    n = int(input("Enter number of possible connections: "))
    
    edges = []
    print("Enter each connection in the format: City1 City2 Cost")
    for _ in range(n):
        data = input().split()
        city1, city2, cost = data[0], data[1], int(data[2])
        edges.append((city1, city2, cost))
    
    mst = kruskal(cities, edges)
    
    print("\nEdges in the Minimum Spanning Tree (MST):")
    for u, v, cost in mst:
        print(f"{u} - {v} : {cost}")

if _name_ == "_main_":
    main()