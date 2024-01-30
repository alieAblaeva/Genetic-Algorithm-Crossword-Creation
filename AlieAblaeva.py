import random
import copy
from collections import deque
import os
def is_non_zero(num):
    if num == 0:
        return 0
    else:
        return 1


class Word:
    def __init__(self, word, x=None, y=None, orientation=None):
        self.word = word
        self.x = x
        self.y = y
        self.orientation = orientation  #where 0 is horizontal and 1 is vertical


class Crossword:
    size = 20

    def __init__(self, words=None):
        self.words = words
        self.grid = []
        self.fitness = 0

    def generate_initial(self, words):
        self.words = []
        for string in words:
            new_word = Word(string)
            new_word.orientation = random.randint(0,1)
            new_word.x = random.randint(0, 19)
            new_word.y = random.randint(0, 19)
            self.words.append(new_word)


    def place_on_grid(self):
        self.grid = []
        for i in range(20):
            line = []
            for j in range(20):
                line.append(".")
            self.grid.append(line)
        for string in self.words:
            symbol = 0
            if string.orientation == 0:
                for i in range(string.y, string.y+len(string.word)):
                    if i<20:
                        if self.grid[string.x][i] == string.word[symbol] or self.grid[string.x][i] == ".":
                            self.grid[string.x][i] = string.word[symbol]
                        else:
                            self.grid[string.x][i]+=string.word[symbol]
                        symbol += 1
            else:
                for i in range(string.x, string.x+len(string.word)):
                    if i<20:
                        if self.grid[i][string.y] == string.word[symbol] or self.grid[i][string.y] == ".":
                            self.grid[i][string.y] = string.word[symbol]
                        else:
                            self.grid[i][string.y] += string.word[symbol]
                        symbol += 1

    def isFit(self, word):
        if word.orientation == 0:
            if word.y + len(word.word) < self.size:
                return True
        else:
            if word.x + len(word.word) < self.size:
                return True
        return False

    def print_crossword(self):
        self.place_on_grid()
        for row in self.grid:
            for element in row:
                print(f'{element:>{2}}', end=' ')
            print()
        print()

    def mutation(self, probability):
        mutated_crossword = copy.deepcopy(self)
        word_number = random.randint(0, len(self.words)-1)
        if random.randint(0,1000) < probability*10:
            mutated_crossword.words[word_number].orientation = random.randint(0,1)
            mutated_crossword.words[word_number].x = random.randint(0, self.size-1)
            mutated_crossword.words[word_number].y = random.randint(0, self.size-1)
        return mutated_crossword

    def crossover(self, other_crossword):

        crossover_point = random.randint(1, len(self.words) - 1)

        offspring_words = self.words[:crossover_point] + other_crossword.words[crossover_point:]
        offspring_words2 = other_crossword.words[:crossover_point] + self.words[crossover_point:]

        offspring1 = Crossword(offspring_words)
        offspring2 = Crossword(offspring_words2)
        return offspring1, offspring2

    def find_connected_groups(self):
        # function to find connected groups of words using BFS
        visited = set()
        groups = []
        max_group = -10000000
        total_length = 0
        index = 0
        max_index = 0
        for word in self.words:
            if word not in visited:
                group = set()
                queue = deque([word])
                while queue:
                    current_word = queue.popleft()
                    if current_word not in group:
                        group.add(current_word)
                        visited.add(current_word)
                        neighbors = [w for w in self.words if self.relation(current_word, w) in [1, -3]]
                        queue.extend(neighbors)
                if max_group < len(group):
                    max_group = len(group)
                    max_index = index
                groups.append(group)
                index += 1
        for i in range(len(groups)):
            if i != max_index:
                for word in groups[i]:
                    total_length+= len(word.word)
        outsiders = len(self.words) - max_group
        return total_length, outsiders

# in the comments below 'touches' means 'is neighbor of'
# the method returns a number indicating the type of relation

    def relation(self, word1, word2):
        # horizontal and vertical words:
        if word1.orientation == 0 and word2.orientation == 1:
            # the horizontal word lies withing one of the vertical one's rows
            if word2.x <= word1.x < word2.x + len(word2.word):
                # the horizontal word touches the vertical one with its first or last letter
                if word2.y == word1.y - 1 or word2.y == word1.y + len(word1.word):
                    return -9
                # two words intersect
                elif word1.y <= word2.y < word1.y + len(word1.word):
                    x = word1.x
                    y = word2.y
                    # the letter on the intersection is the same
                    if word1.word[y - word1.y] == word2.word[x - word2.x]:
                        return 1
                    # different letters on the intersection
                    else:
                        return -3
            # the vertical word lies within one of the horizontal one's columns
            elif word1.y <= word2.y < word1.y + len(word1.word):
                # the vertical word touches the horizontal one with its first or last letter
                if word1.x == word2.x - 1 or word1.x == word2.x + len(word2.word):
                    return -9

        # same as before where word1 is vertical and word2 is horizontal
        elif word2.orientation == 0 and word1.orientation == 1:
            if word1.x <= word2.x < word1.x + len(word1.word):
                if word1.y == word2.y - 1 or word1.y == word2.y + len(word2.word):
                    return -9
                elif word2.y <= word1.y < word2.y + len(word2.word):
                    x = word2.x
                    y = word1.y
                    # the letter on the intersection is the same
                    if word2.word[y - word2.y] == word1.word[x - word1.x]:
                        return 1
                    # different letters on the intersection
                    else:
                        return -3
            elif word2.y <= word1.y < word2.y + len(word2.word):
                if word2.x == word1.x - 1 or word2.x == word1.x + len(word1.word):
                    return -9

        # both words are horizontal
        elif word1.orientation == 0 and word2.orientation == 0:
            # both words are on the same row
            if word1.x == word2.x:
                # words touch each other
                if word1.y == word2.y + len(word2.word) or word2.y == word1.y + len(word1.word):
                    return -9
                elif word2.y <= word1.y < word2.y + len(word2.word):
                    return -3 * min(len(word1.word), word2.y + len(word2.word) - word1.y)
                if word1.y <= word2.y < word1.y + len(word1.word):
                    return -3 * min(len(word2.word), word1.y + len(word1.word) - word2.y)
            # words touch from neighbour rows
            elif word1.x == word2.x + 1 or word1.x == word2.x - 1:
                if word2.y <= word1.y < word2.y + len(word2.word):
                    return -9
                elif word1.y <= word2.y < word1.y + len(word1.word):
                    return -9

        elif word1.orientation == 1 and word2.orientation == 1:
            if word1.y == word2.y:
                if word1.x == word2.x + len(word2.word) or word2.x == word1.x + len(word1.word):
                    return -9
                elif word2.x <= word1.x < word2.x + len(word2.word):
                    return -3 * min(len(word1.word), word2.x + len(word2.word) - word1.x)
                elif word1.x <= word2.x < word1.x + len(word1.word):
                    return -3 * min(len(word2.word), word1.x + len(word1.word) - word2.x)
            elif word1.y == word2.y + 1 or word1.y == word2.y - 1:
                if word2.x <= word1.x < word2.x + len(word2.word):
                    return -9
                elif word1.x <= word2.x < word1.x + len(word1.word):
                    return -9
        return 0

    #@lru_cache(maxsize=None)
    def calculate_fitness(self):
        self.fitness = 0
        for line in self.words:
            if not self.isFit(line):
                self.fitness -= 10000000
                return
        intersections = [0] * len(self.words)
        for i in range(len(self.words)-1):
            for j in range(i+1, len(self.words)):
                relation = self.relation(self.words[i], self.words[j])
                if is_non_zero(relation):
                    self.fitness += (relation-1)*100000
        length, outsiders = self.find_connected_groups()
        self.fitness -= length
        self.fitness -= outsiders*1000


def main():
    words = []
    #output = open(f"outputs/output{path+1}.txt", "w")
    with open(f"input.txt", 'r') as file:
        line = file.readline()
        while line:
            wrd = line.replace("\n", "")
            words.append(wrd)
            line = file.readline()
    for word in words:
        print(word)
    population = []
    pop_size = 2000
    go_next = 800
    for _ in range(pop_size):
        crossword = Crossword()
        crossword.generate_initial(words)
        crossword.calculate_fitness()
        population.append(crossword)
    population[0].print_crossword()
    print(population[0].fitness)

    weight = []

    overall_fitness = 0
    max_fit = 0

    for i in range(0, pop_size):
        weight.append((i+1))
    weight.sort(reverse=True)
    epoch = 0
    while True:
        population.sort(key=lambda x: x.fitness, reverse=True)

        new_population = []

        min_fitness = min(individual.fitness for individual in population)
        # normalized_fitness = [(individual.fitness - min_fitness)**10 for individual in population]
        normalized_fitness = [(individual.fitness - min_fitness) for individual in population]

        fitness_sum = sum(normalized_fitness)
        # probabilities = [fit / fitness_sum for fit in normalized_fitness]
        probabilities = [fit for fit in normalized_fitness]
        p = sorted(set(probabilities))
        # print(p)
        probabilities = [int(1.3 ** (1 + p.index(fit))) for fit in normalized_fitness]
        selected_indices = random.choices(list(range(pop_size)), k=go_next, weights=probabilities)

        new_population.extend(population[k] for k in selected_indices)

        #print("crossover")
        for crsvr in range(go_next, pop_size, 2):
            parents = random.choices(population, weights=probabilities, k=2)
            offspring1, offspring2 = parents[0].crossover(parents[1])
            new_population.extend([offspring1, offspring2])
        new_population.sort(key=lambda x: x.fitness, reverse=True)
        #print("mutation")
        for crossword in range(10, len(new_population)):
            new_population[crossword] = new_population[crossword].mutation(65)
        population = copy.deepcopy(new_population)
        for i in range(len(population)):
            population[i].calculate_fitness()
        population.sort(key=lambda x: x.fitness, reverse=True)
        # max_fit = max(max_fit, max(population, key=lambda x: x.fitness).fitness)
        max_fit = max(max_fit, population[0].fitness)
        if epoch % 10 == 0:
            print()
            print("\n\n============================")
            print(population[0].fitness)
            population[0].print_crossword()
            population[0].calculate_fitness()
            print(population[0].fitness)

        if(population[0].fitness == 0):
            for individual in population:
                overall_fitness += individual.fitness

            # for wrd in population[0].words:
            #     output.write(str(wrd.x)+" " + str(wrd.y) + " " + str(wrd.orientation) + "\n")


            print()
            population[0].print_crossword()
            print(population[0].fitness)
            break

        print('\r', population[0].fitness, "    ", epoch, end="     ")
        epoch+=1
    # output.close()


if __name__ == '__main__':
        main()
