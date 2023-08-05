# Beancount Swedbank Importer

beancount-swedbank-importer provides a python import script for beancount to
import CSV exports from swedbank online banking.

## Usage

### Installation

Install `beancountwedbank` from pip like this:

    pip install beancountswedbank

### Configuration

Write a configuration file, eg. `config.py`, (or extend your existing one) to include this:

    import beancountswedbank

    CONFIG = [
        beancountswedbank.CSVImporter({'Nyckelkonto': 'Assets:Your:Nyckelkonto',
                                       'e-sparkonto': 'Assets:Your:ESparKonto'}),
    ]

### Daily use

1. Download the CSV file from your Swedbank online banking,
2. Run `beancount-extract config.py transaction_file.csv`


## License

This package is licensed under the MIT License.

