# Matrix Regression

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CodeFactor](https://www.codefactor.io/repository/github/nicoloverardo/matrix_regression/badge/main)](https://www.codefactor.io/repository/github/nicoloverardo/matrix_regression/overview/main)
![PyPI](https://img.shields.io/pypi/v/matrixreg)
[![codecov](https://codecov.io/gh/nicoloverardo/matrix_regression/branch/main/graph/badge.svg)](https://codecov.io/gh/nicoloverardo/matrix_regression)
![Lines of code](https://img.shields.io/tokei/lines/github/nicoloverardo/matrix_regression)

Table of contents:

00. [Description](#description)
01. [Installation](#installation)
02. [Usage](#usage)

## Description
Implementation of the MatrixRegression (MR) algorithm for multi-label text classification that can be used in an online learning context. It is presented in the following paper:

[Popa, I. & Zeitouni, Karine & Gardarin, Georges & Nakache, Didier & Métais, Elisabeth. (2007). Text Categorization for Multi-label Documents and Many Categories. 421 - 426. 10.1109/CBMS.2007.108.](https://www.researchgate.net/publication/4257876_Text_Categorization_for_Multi-label_Documents_and_Many_Categories)

Abstract:
> In this paper, we propose a new classification method that addresses classification in multiple categories of textual documents. We call it Matrix Regression (MR) due to its resemblance to regression in a high dimensional space. Experiences on a medical corpus of hospital records to be classified by ICD (International Classification of Diseases) code demonstrate the validity of the MR approach. We compared MR with three frequently used algorithms in text categorization that are k-Nearest Neighbors, Centroide and Support Vector Machine. The experimental results show that our method outperforms them in both precision and time of classification.


## Installation
```bash
pip install matrixreg
```

## Usage
```python
from matrixregr.matrixregression import MatrixRegression

mr = MatrixRegression()

# Fit
mr.fit(X_train, y_train)

# Predict
mr.predict(X_test)

# Partial fit
mr.partial_fit(new_X, new_y)
```

### Parameters optimization
This implementation is scikit-friendly; thus, it supports GridSearchCV

```python
# Parameter to optimize
param_grid = [{"threshold": [0.3, 0.6, 0.9]}]

# Initialization
mr = MatrixRegression()
clf = GridSearchCV(mr, param_grid, cv = 5, verbose=10, n_jobs=-1, scoring='f1_micro')

# Fit
clf.fit(X_train, y_train)

# Results
clf.best_params_, clf.best_score_
```