# PRD: validateNRIC2020

## Overview
A Python Flask web app that validates Singapore NRIC (National Registration Identity Card) numbers using the official checksum algorithm and generates a Code128 barcode for valid NRICs. Supports all current NRIC series: S, T (Citizens/PR), F, G (Foreigners), and M (new FIN series). Intended as a developer tool and security education resource.

## Goals
- Accept an NRIC string via a POST API and validate its format + checksum
- Support S, T, F, G, M prefix series with correct algorithms for each
- Return validation result with expected check digit on failure
- Generate a Code128 barcode image (base64) for valid NRICs
- Serve a web UI with form input

## Non-Goals
- Integration with any government database (NRICs are validated by algorithm only, not against real records)
- Bulk validation
- NRIC generation
- Any form of identity verification beyond checksum math

## User Stories
- As a developer, I want to validate user-entered NRICs in a web form without implementing the algorithm myself.
- As a security researcher, I want to understand how NRIC checksum validation works.
- As a tester, I want to generate barcode images for valid NRICs to test scanning systems.

## Tech Stack
- **Language**: Python 3.x
- **Framework**: Flask
- **Libraries**: `python-barcode` (pip), `Pillow` (pip), `re` (stdlib)
- **Frontend**: Jinja2 HTML templates

## Architecture
```
validateNRIC2020/
├── app.py          # Flask routes
├── utils.py        # validate_nric() + generate_barcode_base64()
├── checksumv1.py   # Original standalone checksum script
├── checksumv2.py   # Alternate/updated standalone version
├── templates/
│   └── index.html  # Web UI
└── static/         # Static assets
```

**Routes:**
- `GET /` → serve `index.html`
- `POST /validate` → accept JSON `{nric: str}`, return validation result + barcode

## Features (detailed)

### NRIC Validation (`validate_nric(nric)`)
1. Check length == 9
2. Match regex `^[STFGM]\d{7}[A-Z]$`
3. Apply weights `[2, 7, 6, 5, 4, 3, 2]` to 7 digits
4. Add offset: T/G prefix → +4, M prefix → +3
5. Compute `remainder = total % 11`
6. Map remainder to check character:
   - S/T → `{0:J, 1:Z, 2:I, 3:H, 4:G, 5:F, 6:E, 7:D, 8:C, 9:B, 10:A}`
   - F/G → `{0:X, 1:W, 2:U, 3:T, 4:R, 5:Q, 6:P, 7:N, 8:M, 9:L, 10:K}`
   - M → compute `check_digit = 11 - (remainder + 1)` then map `{0:K, 1:L, 2:J, 3:N, 4:P, 5:Q, 6:R, 7:T, 8:U, 9:W, 10:X}`
7. Compare computed check char to last char of input
8. Return `{valid: bool, message: str, expected: str|null}`

### Barcode Generation (`generate_barcode_base64(nric)`)
- Generates Code128 barcode via `python-barcode`
- Writes to in-memory `BytesIO` buffer using `ImageWriter`
- Returns base64-encoded PNG string (data URI ready)
- Returns `None` on error (barcode not critical)

### Web UI
- Single-page form with NRIC text input
- AJAX POST to `/validate`
- Shows validation result message
- Shows barcode image if valid

## API Contracts

### POST /validate
**Request:**
```json
{"nric": "S1234567D"}
```
**Response (valid):**
```json
{"valid": true, "message": "Valid S-series NRIC.", "barcode": "data:image/png;base64,..."}
```
**Response (invalid):**
```json
{"valid": false, "message": "Invalid NRIC.", "expected": "D"}
```

## Environment Variables
None — Flask runs on default port 5000 in debug mode.

## Deployment / Run
```bash
pip install flask python-barcode Pillow
python app.py
# open http://localhost:5000
```

## Constraints & Notes
- **Algorithm accuracy**: M-series checksum uses a non-obvious offset formula — double-check with official sources if used in production
- **No real records**: validation is purely algorithmic; a "valid" NRIC may not belong to any real person
- **Barcode format**: Code128 is used but not Code39; scanning systems should be configured for Code128
- **PIL deprecation**: `python-barcode`'s `ImageWriter` requires Pillow; Pillow 10+ may have breaking API changes in write modes
