#!/usr/bin/env python3

import docker


class Dynasty:
    def __init__(self, repo):
        self.client = docker.from_env()
        self.layers = dict()
        self.all = dict()
        for image in self.client.images.list(name=repo):
            self.layers[image.id] = image.attrs['RootFS']['Layers']
            self.all[image.id] = image

    def ancestor(self, name):
        image = self.client.images.get(name)
        l = image.attrs['RootFS']['Layers']
        a = [(len(layers), self.all[id].tags)
             for id, layers in self.layers.items()
             if startswith(layers, l) and id != image.id]
        return [i[1] for i in sorted(a, key=lambda x: x[0])]
        # layers should be indexed as a Trie


def startswith(needle, haystack):
    for a, n in enumerate(needle):
        if n != haystack[a]:
            return False
    return True


if __name__ == '__main__':
    import sys
    image = sys.argv[1]
    d = Dynasty('%s/*' % image.split('/')[0])
    print(d.ancestor(image))
