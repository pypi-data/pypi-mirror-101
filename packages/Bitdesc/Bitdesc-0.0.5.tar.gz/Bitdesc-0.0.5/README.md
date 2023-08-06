# BiT

BiT is a novel approach capable of quantifying a complex system of diverse patterns through 
species diversity and richness, and taxonomic distinctiveness. 
It considers an image as a species ecosystem and computes species diversity and richness measures, 
and taxonomic indices to describe the texture. 
BiT takes advantage of ecological patterns' invariance characteristics to build a permutation, rotation, and translation invariant descriptor. 
Experiments on different datasets have shown that BiT texture descriptor has advantages over several texture descriptors and deep methods. 

More details can be found in our paper available at https://arxiv.org/abs/2102.06997

# Installation

Run the following to install:
```python
pip install Bitdesc
```

# Developing BiT

To install BiT, along with the tools you need to develop and run tests, run the following in your virtualenv:
```bash
$ pip install -e .[dev]
```
# How to use BiT 

After the installation, the library should be used following the example underneath:

```python
import ClassBit
path = './resources/test.png'
bit = ClassBit.BiT(path, bfeat=False, tfeat=True, unsharpfilter=False, crimminsfilter=False, normalization=False)
features = bit.features()
```
The class BiT accepts the following parameters:
```python
path: the path to the image file
bfeat= biodiversity indices (True, False). It returns 28 features (7 for R, 7 for G, 7 for B, and 7 for RGB)  
tfeat= taxonomic indices (True, False) It returns 28 features (7 for R, 7 for G, 7 for B, and 7 for RGB)
unsharpfilter= applies UnsharpMask onto R, G, B channels (True, False) 
crimminsfilter= applies crimmins filter onto RGB - original image - (True, False) 
normalization= normalize the array (divide the array by its algebraic norm)
``` 
Not that at least one type of features should be true, that is, (bfeat=False, tfeat=True) or (bfeat=True, tfeat=False) or (bfeat=True, tfeat=True).
It may be recommended to not normalize should you use need to standardize the dataset before training. 
# Contributors
Steve Ataky & Alessandro Koerich
