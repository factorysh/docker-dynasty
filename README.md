# Docker Dynasty

Guess docker image history.

`docker image history` was fun, but *buildkit* smash it.

Lets use brute force.

The rule are simple :
 - if a image (something with a tag) layers are the begining of another image, it's an ancestor.
 - lets sort ancestors by number of layers
