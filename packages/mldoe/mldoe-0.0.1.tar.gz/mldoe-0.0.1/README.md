# MLDOE

This package provides the tools to enumerate and characterize regular mixed-level designs (with four and two-level factors).

## Installation

Run the following to install:

```python
pip install mldoe
```

## Usage

```python
from mldoe import design

# Generate a two-level design by columns
D = TLdesign(16,[1,2,4,8,6])

# Print the design matrix
print(D.array)

# Compute its word-length pattern
print(D.wlp())

```

## Developing mldoe

To install mldoe, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
pip install -e .[dev]
```
