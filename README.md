# ValidateNRIC2020

A Python-based tool to validate and generate Singapore NRIC (National Registration Identity Card) checksum letters.

## Description

This project provides two Python scripts for working with Singapore NRIC numbers. It can validate whether a given NRIC is valid by checking its checksum letter, and can also calculate the correct checksum letter for an NRIC. The tool supports both Singaporean citizens (S/T prefix) and Foreigners (F/G prefix).

## Features

- Validate complete NRIC numbers by verifying the checksum letter
- Calculate the correct checksum letter for NRIC numbers
- Support for Singaporean citizens (S/T prefix) and Foreigners (F/G prefix)
- Simple command-line interface

## Technologies Used

- Python 3

## Installation

```bash
# Clone the repository
git clone https://github.com/theprawnorganisation/validateNRIC2020.git

# Navigate to project directory
cd validateNRIC2020
```

## Usage

### Validate a complete NRIC (checksumv1.py)

```bash
python checksumv1.py
```

Enter the full NRIC when prompted to check if it's valid.

### Calculate the checksum letter (checksumv2.py)

```bash
python checksumv2.py
```

Enter the first 8 characters of the NRIC (prefix + 7 digits) to calculate the correct last letter.

## Web API and regression checks

The Flask app in `app.py` serves the web interface and `POST /validate`.
Send a JSON object with a text `nric` field. Malformed JSON, non-object bodies,
and non-text identifiers return HTTP 400 with a JSON error, including
`valid: false` and `barcode: null`. Ordinary checksum-validation results,
including empty or invalid text, continue to return HTTP 200. A matching
checksum returns the generated barcode in memory; this does not verify an
identifier against an identity registry.

Install `requirements.txt`, then run the API regression checks:

```bash
python -B -m unittest discover -s tests -v
```

The checks use synthetic input and cover malformed requests, existing
validation responses and barcode generation.

### Static delivery and privacy

`python build_assets.py` copies the existing assets into `public/static/`
for Vercel's CDN. The generated copies are committed so Vercel discovers them
when it plans the deployment. Regenerate and commit them when changing assets;
CI rejects copies that differ from their source. Vercel also runs this command
before deployment. Flask development continues to use `static/`. The same
asset URLs work in both environments, and the source images remain unchanged.

The script URL is stable across page loads. Default conditional cache
revalidation lets a browser reuse unchanged bytes and receive changed scripts
after a deployment; these URLs are not marked immutable. Validation responses
are not included in the static cache. Browser debug logs no longer print
entered identifiers or individual input characters. Manual entry, wheel input,
checksum validation and barcode generation keep their existing behavior.

## Disclaimer

1. FOR EDUCATIONAL PURPOSES ONLY
2. USE AT YOUR OWN DISCRETION

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
