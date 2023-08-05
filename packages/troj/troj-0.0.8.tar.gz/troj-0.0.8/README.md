# TrojAI Integration Package

TrojAI provides the troj Python convenience package to allow users to integrate TrojAI adversarial protections and robustness metrics seamlessly into their AI development pipelines.

## Installation
Run the following to install:
```python
pip install troj
```

## Usage



```python
'''
ImageNet folder style: 
/train
----/class1
----/class2
...
/test
----/class1
----/class2
...etc 

CoCo annotation style:
/images
----image1.jpg
----image2.jpg
...etc
annotation.json

'''



```

## Things we need to upload to aws in test loop
1. Images
2. Labels
3. Embeddings
4. Inferences
5. Perturbations
   
## How to develop locally
these commands add the local package to the wheel
pip install wheel
python setup.py bdist_wheel
pip install -e.[dev]

Build the package under dist folder using this, will create tar.gz and .whl for version id in setup.py:
    python -m build

Upload it to testpypi repo using this (remove --repository flag to go live, make sure dist only has the files you expect):
python -m twine upload --repository testpypi dist/*

python -m twine upload dist/*

When install from testpypi repo you need this format: pip install --extra-index-url https://test.pypi.org/simple/ package_name_here https://stackoverflow.com/questions/51589673/pip-install-producing-could-not-find-a-version-that-satisfies-the-requirement - otherwise dependency packages wont be looked for on live pypi

# Examples
Pytorch Colab Notebook:
https://colab.research.google.com/drive/12F_N4OuO458z_lCF1w3cOHdqDZOc6Nd9#scrollTo=00552zIlGvcD

Tensorflow Colab Notebook:
https://colab.research.google.com/drive/1G9S02HuDH7YsvWZD-RpgWKdIsQct5qBZ#scrollTo=noeHXX2f6_OO