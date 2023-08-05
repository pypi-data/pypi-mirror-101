#TODO Add comments.

import numpy as np
from pycolate.grid_engine import grid
from colorsys import hsv_to_rgb
from scipy.ndimage import measurements
import scipy.ndimage as ndimage
from random import shuffle
import PIL


class Percolation:
    def __init__(self, width, height, occupationProb):

        self.height = height

        self.width = width

        self._site_size = 10

        self.clusters = []

        self.found_clusters = False

        self.generated_graphics = False

        prob = occupationProb

        self.config = np.random.choice([0, 1], p=[1 - prob, prob], size=(width, height))

    def cluster_find(self):
        
        self.percolated = False

        self.percolated_size = 0

        labeledConfig, num = measurements.label(self.config)

        sizes = ndimage.sum(self.config, labeledConfig, range(num + 1))

        self.sizeConfig = sizes[labeledConfig]

        sizes = sizes[sizes != 0]

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

            self.percolated_size = len(labeledConfig[labeledConfig == self.percolLabel])

            self.sizes = sizes[sizes != self.percolated_size]

            self.mean_cluster_size = np.mean(self.sizes)

        if not self.percolated:

            self.mean_cluster_size = np.mean(sizes)

            self.sizes = sizes[sizes != self.percolated_size]

        self.labeledConfig = labeledConfig

        self.found_clusters = True

    def generate_graphics(self):

        labelsToCheck = np.unique(self.labeledConfig)

        for label in labelsToCheck:

            if label != 0:

                coordsOfPoints = np.transpose(np.where(self.labeledConfig == label))

                self.clusters.append(coordsOfPoints)

        tmp = np.unique(self.labeledConfig)

        labelsToDraw = np.delete(tmp, np.where(tmp == 0))

        clusterNum = len(self.clusters)

        hues = np.linspace(1, 350, num=clusterNum + 1)

        shuffle(hues)

        rulebook = {0: "white"}

        j = 1

        for i in labelsToDraw:

            rulebook[i] = "hsv({},{}%,{}%)".format(
                hues[j], np.random.uniform(20, 60), np.random.uniform(50, 100)
            )

            j += 1

        rulebook[0] = "white"

        self.graphics = grid(self.labeledConfig, rulebook, self.site_size)

        self.generated_graphics = True

    def display(self):

        if not self.found_clusters: 
            self.cluster_find()

        if not self.generated_graphics:
            self.generate_graphics()

        self.graphics.display()

    def save(self, path):

        if not self.found_clusters: 
            self.cluster_find()

        if not self.generated_graphics:
            self.generate_graphics()

        self.graphics.image.save("{}".format(path))

    @property
    def site_size(self):
        return self._site_size

    @site_size.setter
    def site_size(self,new_size):
        if type(new_size) != int:
            raise TypeError('The site_site must be a postive integer.')
        if not new_size >= 1:
            raise ValueError('The site_site must be a positive integer.')
        self._site_size = new_size
    

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
                self.data["percolated cluster sizes"].append(temp_perc.percolated_size)
            if self.collect_mean:
                self.data["mean cluster sizes"].append(temp_perc.mean_cluster_size)
            if self.collect_sizes:
                self.data["cluster sizes"] += temp_perc.sizes.tolist()

        print(self.data)

if __name__=='__main__':

    perc = Percolation(100, 100, 0.596)

    perc.site_size = 3
 
    perc.display()