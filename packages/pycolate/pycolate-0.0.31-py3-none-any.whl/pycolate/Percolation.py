#TODO Add comments.

import numpy as np
from pycolate.grid_engine import grid
from colorsys import hsv_to_rgb
from scipy.ndimage import measurements
import scipy.ndimage as ndimage
import PIL


class Percolation:
    def __init__(self, height, width, occupationProb):

        self.config = np.zeros((height, width), dtype=int)

        self.height = height

        self.width = width

        self.clusters = []

        self.foundClusters = False

        self.percolated = False

        prob = occupationProb

        self.config = np.random.choice([0, 1], p=[1 - prob, prob], size=(height, width))

    def cluster_find(self):

        labeledConfig, num = measurements.label(self.config)

        sizes = ndimage.sum(self.config, labeledConfig, range(num + 1))

        self.sizeConfig = sizes[labeledConfig]

        sizes = sizes[sizes != 0]

        self.percolatedSize = 0

        labels = np.unique(labeledConfig)

        labelsToCheck = labels[labels != 0]

        leftColumn = labeledConfig[:, 0]

        rightColumn = labeledConfig[:, -1]

        topRow = labeledConfig[0]

        bottomRow = labeledConfig[-1]

        for label in labelsToCheck:

            left = label in leftColumn

            right = label in rightColumn

            bottom = label in bottomRow

            top = label in topRow

            if (left and right) or (bottom and top):

                self.percolLabel = label

                self.percolated = True

                break

        if self.percolated:

            self.percolatedSize = len(labeledConfig[labeledConfig == self.percolLabel])

            self.sizes = sizes[sizes != self.percolatedSize]

            self.meanClusterSize = np.mean(self.sizes)

        if not self.percolated:

            self.meanClusterSize = np.mean(sizes)

            self.sizes = sizes[sizes != self.percolatedSize]

        self.labeledConfig = labeledConfig

    def generate_graphics(self, site_size=10):

        labelsToCheck = np.unique(self.labeledConfig)

        for label in labelsToCheck:

            if label != 0:

                coordsOfPoints = np.transpose(np.where(self.labeledConfig == label))

                self.clusters.append(coordsOfPoints)

        tmp = np.unique(self.labeledConfig)

        labelsToDraw = np.delete(tmp, np.where(tmp == 0))

        clusterNum = len(self.clusters)

        hues = np.linspace(1, 360, num=clusterNum + 1)

        rulebook = {0: "white"}

        j = 1

        for i in labelsToDraw:

            rulebook[i] = "hsv({},{}%,{}%)".format(
                hues[j], np.random.uniform(50, 70), np.random.uniform(50, 100)
            )

            j += 1

        rulebook[0] = "white"

        self.graphics = grid(self.labeledConfig, rulebook, site_size)

    def display(self):

        self.graphics.display()

    def save(self, path):

        self.graphics.image.save("{}".format(path))


class PercolationExperiment:
    def __init__(self, *args):

        self.data = {}

        self.collect_mean = self.collect_perc_size = self.collect_sizes = False

        if "mean cluster size" in args:

            self.collect_mean = True

            self.data["mean cluster sizes"] = []

        if "percolated cluster size" in args:

            self.collect_perc_size = True

            self.data["percolated cluster sizes"] = []

        if "cluster sizes" in args:

            self.collect_sizes = True

            self.data["cluster sizes"] = []

    def run(self, sample_size: int, width: int, height: int, occupation_prob: float):

        for i in range(sample_size):

            temp_perc = Percolation(
                width=width, height=height, occupationProb=occupation_prob
            )

            temp_perc.cluster_find()

            if self.collect_perc_size:
                self.data["percolated cluster sizes"].append(temp_perc.percolatedSize)
            if self.collect_mean:
                self.data["mean cluster sizes"].append(temp_perc.meanClusterSize)
            if self.collect_sizes:
                self.data["cluster sizes"] += temp_perc.sizes.tolist()

        print(self.data)

if __name__=='__main__':

    perc = Percolation(300, 100, 0.596)

    perc.cluster_find()

    perc.generate_graphics()

    perc.save('./images/cover_image.png')

# experi = PercolationExperiment(10, 'mean cluster size', 'percolated cluster size')

# experi.run(10,30,30,0.6)