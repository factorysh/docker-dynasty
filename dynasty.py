#!/usr/bin/env python3

import docker


class Layers:
    def __init__(self):
        self._data = dict()

    def layer(self, layer):
        if layer not in self._data:
            self._data[layer] = encode(len(self._data))
        return self._data[layer]


def encode(n: int):
    return ("".join(chr(a +97) for a in num(n)) + "___")[:3]


def num(n: int, r=None):
    if r is None:
        assert type(n) == int, type(n)
        r = []
    d = n // 26
    r.append(n % 26)
    if d > 0:
        return num(d, r)
    return r


class Dynasty:
    def __init__(self, repo):
        self.client = docker.from_env()
        self.layers = dict()
        self.all = dict()
        self._layers = Layers()
        for image in self.client.images.list(name=repo):
            self.layers[image.id] = " ".join(self._layers.layer(a)
                                            for a
                                            in image.attrs['RootFS']['Layers'])
            self.all[image.id] = image
        #print(self.layers)

    def tree(self):
        for id, layers in sorted(self.layers.items(), key=lambda a: a[1]):
            print(layers, " ".join(self.all[id].tags))

    def ancestor(self, name):
        image = self.client.images.get(name)
        l = image.attrs['RootFS']['Layers']
        a = [(len(layers), self.all[id].tags)
             for id, layers in self.layers.items()
             if startswith(layers, l) and id != image.id]
        return [i[1] for i in sorted(a, key=lambda x: x[0])]
        # layers should be indexed as a Trie

    def descendant(self, name):
        image = self.client.images.get(name)
        l = image.attrs['RootFS']['Layers']
        return [self.all[id].tags
                for id, layers in self.layers.items()
                if startswith(l, layers) and id != image.id]


def startswith(needle, haystack):
    if len(needle) > len(haystack):
        return False
    for a, n in enumerate(needle):
        if n != haystack[a]:
            return False
    return True


if __name__ == '__main__':
    import sys
    image = sys.argv[1]
    d = Dynasty('%s/*' % image.split('/')[0])
    d.tree()
    #print("Ancestor : ", d.ancestor(image))
    #print("Descendant : ", d.descendant(image))
