# State-based Puzzle Games in Python
## Simulating a state-based sliding puzzle and comparing two solving algorithms

This  project was inspired by [*Professor Layton and the Curious Village*](https://en.wikipedia.org/wiki/Professor_Layton_and_the_Curious_Village "Wikipedia"), a puzzle solving adventure game for the Nintendo DS. [One particular puzzle](https://layton.fandom.com/wiki/Puzzle:A_Worm%27s_Dream "Layton Wiki") involves completing a rather difficult sliding-puzzle, and makes for an intersting python excercise. For my python code, I decided to represent it in the form of a list (in a class, with other things such as width, previous state and the index of the whole) such that:

![Starting Puzzle](/wormpuzzlegraphic.png)

Here, each number represents a different tile, with zeros in place of the two identical tiles, and an asterisk in place of the hole. The puzzle is numbered such that the solution looks like this:

![Puzzle Solution](/wormsolutiongraphic.png)

In order to find the shortest possible path from the first list to the second, I use a breadth-first search. This is done using a function in the class (apply_moves), which is combined with get_legal_moves to find which moves can be performed then putting these states on a kind of to-do list. States are then popped of the left of the list to be investigated for their legal moves.

When a state which has already been investigated is reached, it and its next possible moves are ignored. This avoids repeatedly checking the same states multiple times.

When a state is found which matches the desired final state, we find and print the path which led us to said state. This provides a set of moves which result in the final state from the original starting state of the puzzle, hence giving a solution. This solution is always of optimal (minimal) length.

## Solving algorithm comparison

While the search algorithm I have described works consistently and provides an optimal solution, it can be done faster. One possibility for a faster algorithm could be approaching the solution from both ends, with the algorithm searching from start to finish and finish to start simultaneously. In order to verify any enhancement in speed, I defined functions "search" and "double_ended_search". 

Upon implementation, it is shown that the double-ended search is indeed faster. A typical set of results is as follows:

**Double ended search:**
Number of moves: 23
Time taken: 25.903564453125ms

**Regular search:**
Number of moves: 23
Time taken: 1091.1025390625ms

As the regular search provides a perfect solution, no improvement can be made in terms of moves, but there is a clear time difference.
