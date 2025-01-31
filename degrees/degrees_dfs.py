import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")

    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    s_person_id = source
    t_person_id = target

    # Create Frontier
    BFS = StackFrontier()

    # Create a Node with initial state (movie_id, person_id)
    state = (None, s_person_id)
    parent = None
    action = (None, s_person_id)
    path = []
    first_node = Node(state, parent, action, path)

    # Add initial state to frontier
    BFS.add(node=first_node)

    # Repeat
    while(True):
        # if frontier is empty break loop return None
        if BFS.empty():
            #print('Frontier is empty, escape loop')
            path = None
            break

        # remove a node from the frontier
        node = BFS.remove()
        if node.state in BFS.explored_states:
            continue

        n_movie_id, n_person_id = node.state
        #print(f'Checking node {node.state}')
        #print("\n")

        # if node containes solution return solution
        if n_person_id == t_person_id:
            # return solution
            #print(f'Find solution, escape loop with {node.state}')
            #print("\n")
            path = node.path
            break

        # add current node state to explored
        BFS.explored_states.add(node.state)

        # expand node
        pairs = neighbors_for_person(n_person_id)
        #print(f'Expanding {n_person_id} to: {pairs}')
        #print("\n")

        # add resulting nodes to frontier (movie, person) pairs
        for pair in pairs:
            # create node
            current_path = node.path[:]
            current_path.append(pair)
            expanded_node = Node(state=pair, parent=node, action=pair, path=current_path)

            #check if frontier already have this state
            if BFS.contains_state(expanded_node.state):
                #print(f'Find pair  {expanded_node.state} in frontier, skip it, > check next')
                #print("\n")
                continue

            # check for explored solutions
            if expanded_node.state in BFS.explored_states:
                #print(f'Find pair {expanded_node.state} in explored state, skip it, > check next')
                #print("\n")
                continue

            # Pass all checks, adding to frontier
            BFS.add(node=expanded_node)

    return path


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
