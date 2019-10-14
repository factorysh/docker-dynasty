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
        a = []
        for id, layers in self.layers.items():
            if startswith(layers, l):
                a.append((len(layers), self.all[id].tags))
        return [i[1] for i in sorted(a, key=lambda x: x[0])]
        # layers should be indexed as a Trie


def startswith(needle, haystack):
    for a, n in enumerate(needle):
        if n != haystack[a]:
            return False
    return True


def dynasty(image):
    client = docker.from_env()
    image = client.images.get(image)
    for k,v  in image.attrs.items():
        print("\t", k, v)
    d = []
    for h in image.history():
        if h['Tags'] is not None:
            d.append(h['Tags'])
    return d


if __name__ == '__main__':
    import sys
    #print(dynasty(sys.argv[1]))
    d = Dynasty('bearstech/*')
    print(d.ancestor(sys.argv[1]))
