# Beancount Triodos Importer

beancount-triodos-importer provides a python import script for beancount to
import CSV exports from triodos online banking.

## Usage

### Installation

Install `beancounttriodos` from pip like this:

    pip install beancounttriodos

### Configuration

Write a configuration file, eg. `config.py`, (or extend your existing one) to include this:

    import beancounttriodos

    CONFIG = [
        beancounttriodos.CSVImporter('Assets:Your:Account')
    ]

### Daily use

1. Download the CSV file from your triodos online banking,
2. Run `beancount-extract config.py transaction_file.csv`


## License

This package is licensed under the MIT License.

