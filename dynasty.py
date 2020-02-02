#!/usr/bin/env python3

import docker


class Layers:
    "Encode layers a sortable string"

    def __init__(self):
        self._data = dict()

    def layer(self, layer):
        if layer not in self._data:
            self._data[layer] = encode(len(self._data))
        return self._data[layer]


def encode(n: int, size: int = 3):
    "Convert an int to a readable string, with a fixed size"
    return ("".join(chr(a + 97) for a in num(n)) + size * "_")[:size]


def num(n: int, r=None):
    "Convert an int to base 26, with latin alphabet"
    if r is None:
        assert type(n) == int, type(n)
        r = []
    d = n // 26
    r.append(n % 26)
    if d > 0:
        return num(d, r)  # recusivity rulez
    return r


class Dynasty:
    def __init__(self, client=None):
        if client is None:
            self.client = docker.from_env()
        else:
            self.client = client
        self.layers = dict()
        self.all = dict()
        self._layers = Layers()
        for image in self.client.images.list():  # all available images
            self.layers[image.id] = self.encode_layers(image.attrs["RootFS"]["Layers"])
            self.all[image.id] = image

    def encode_layers(self, layers):
        return " ".join(self._layers.layer(a) for a in layers)

    def tree(self):
        for id, layers in sorted(self.layers.items(), key=lambda a: a[1]):
            print(layers, " ".join(self.all[id].tags))

    def ancestor(self, name):
        image = self.client.images.get(name)
        l = self.encode_layers(image.attrs["RootFS"]["Layers"])
        a = [
            (len(layers), self.all[id].tags)
            for id, layers in self.layers.items()
            if l.startswith(layers) and id != image.id
        ]
        return [i[1] for i in sorted(a, key=lambda x: x[0])]

    def descendant(self, name):
        image = self.client.images.get(name)
        l = self.encode_layers(image.attrs["RootFS"]["Layers"])
        return [
            self.all[id].tags
            for id, layers in self.layers.items()
            if layers.startswith(l) and id != image.id
        ]


if __name__ == "__main__":
    import sys

    d = Dynasty()
    if len(sys.argv) == 1:
        d.tree()
    else:
        image = sys.argv[1]
        print("Ancestor")
        for a in d.ancestor(image):
            print("\t", a)
        print("Descendant")
        for a in d.descendant(image):
            print("\t", a)
