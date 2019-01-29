### TODO:

Rewrite main function to give the actor (robot) a 'current action'.
Keyboard (and by extension, the computer algorithm) gives an input that changes the current action.
The current action of the actor calls the collision methods, etc.


control loop:
initialize field
initialize robots
for each robot, call run (starting each subthread - tentative!)
if robot is in 'wait' mode, ask for command until timeout
    receiving command, change state and begin moving
        moving an individual robot calls collision and in turn updates collided objects. object list referenced from a global list of objects (need to figure out how to make sure no race conditions appear).
    else no command, don't change state.
    special command to exit game.

robotFrame::loop()
    looks at current state, moves based on it, calls collision, etc.
