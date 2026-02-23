import sys
from collections import defaultdict


def normalize_word(word):
    return ''.join(ch.lower() for ch in word if ch.isalpha() or ch == "'")


def are_similar(w1, w2):
    if len(w1) <= 1 or len(w2) <= 1:
        return False
    len1, len2 = len(w1), len(w2)
    if len1 == len2:
        diff = 0
        for i in range(len1):
            if w1[i] != w2[i]:
                diff += 1
                if diff > 1:
                    return False
        return diff == 1
    if abs(len1 - len2) != 1:
        return False
    if len1 > len2:
        longer, shorter = w1, w2
    else:
        longer, shorter = w2, w1
    return longer[-1] in ('e', 's') and longer[:-1] == shorter


class DSU:


    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n


    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]


    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1


def main():
    first_line = sys.stdin.readline().strip()
    if not first_line:
        return
    K = int(first_line)
    text_words = []
    for line in sys.stdin:
        line = line.rstrip()
        if line == "":
            break
        text_words.extend(line.split())
    normalized = [normalize_word(word) for word in text_words]
    unique_words = []
    word_to_idx = {}
    for word in normalized:
        if word not in word_to_idx:
            word_to_idx[word] = len(unique_words)
            unique_words.append(word)
    n = len(unique_words)
    dsu = DSU(n)
    words_by_len = defaultdict(list)
    for idx, word in enumerate(unique_words):
        words_by_len[len(word)].append((word, idx))
    for length, words in words_by_len.items():
        if length <= 1:
            continue
        m = len(words)
        for i in range(m):
            w1, i1 = words[i]
            for j in range(i + 1, m):
                w2, i2 = words[j]
                if are_similar(w1, w2):
                    dsu.union(i1, i2)
    lengths = sorted(words_by_len.keys())
    for i in range(len(lengths)):
        l1 = lengths[i]
        if l1 <= 1:
            continue
        for j in range(i + 1, len(lengths)):
            l2 = lengths[j]
            if abs(l1 - l2) == 1:
                for w1, i1 in words_by_len[l1]:
                    for w2, i2 in words_by_len[l2]:
                        if are_similar(w1, w2):
                            dsu.union(i1, i2)
    groups = defaultdict(list)
    for idx, word in enumerate(unique_words):
        root = dsu.find(idx)
        groups[root].append(word)
    group_repr = {}
    group_words = {}
    word_to_group = {}
    for root, words in groups.items():
        repr_word = min(words)
        group_repr[root] = repr_word
        group_words[root] = set(words)
        for w in words:
            word_to_group[w] = root
    freq = defaultdict(int)
    for i, word in enumerate(normalized):
        if word not in word_to_group:
            continue
        group = word_to_group[word]
        has_neighbor = False
        start = max(0, i - K)
        for j in range(start, i):
            neighbor = normalized[j]
            if neighbor in word_to_group and word_to_group[neighbor] == group:
                has_neighbor = True
                break
        if not has_neighbor:
            end = min(len(normalized), i + K + 1)
            for j in range(i + 1, end):
                neighbor = normalized[j]
                if neighbor in word_to_group and word_to_group[neighbor] == group:
                    has_neighbor = True
                    break
        if has_neighbor:
            freq[group] += 1
    result = [(group_repr[group], count) for group, count in freq.items() if count > 0]
    result.sort(key=lambda x: (-x[1], x[0]))
    for repr_word, count in result:
        print(f"{repr_word}: {count}")


if __name__ == "__main__":
    main()