# Prayer Times Scraper for Sri Lanka

A Python application that scrapes prayer times from the ACJU (All Ceylon Jamiyyathul Ulama) website and generates a structured JSON dataset.

## Features

- 🌐 Web scraping of ACJU prayer times website
- 📄 PDF download and parsing
- 🕌 Extraction of prayer times (Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha)
- 🗺️ Zone-to-city mapping for Sri Lankan districts
- 📊 Structured JSON output with timezone information

## Project Structure

```
prayer_times_scraper/
├── config/
│   └── settings.py           # Configuration constants
├── src/
│   ├── scraper/
│   │   ├── web_scraper.py    # Web scraping logic
│   │   └── pdf_downloader.py # PDF download logic
│   ├── extractor/
│   │   ├── pdf_parser.py     # PDF text/table extraction
│   │   ├── time_extractor.py # Prayer time parsing
│   │   └── zone_mapper.py    # City/zone mapping
│   └── utils/
│       ├── file_utils.py     # File operations
│       ├── text_utils.py     # Text cleaning utilities
│       └── date_utils.py     # Date parsing utilities
├── data/      # Temporary PDF storage
├── output/    # Generated JSON files
├── main.py    # Entry point
└── requirements.txt
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd acju_prayer_times
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script:

```bash
python -m main --mode prayer
python -m main --mode calendar

python -m main --month january
python -m main --month jan
python -m main --month 1
```

This will:

1. Scrape the ACJU website for PDF links
2. Download prayer time PDFs
3. Extract prayer times from PDFs
4. Generate a JSON file in the `output/` directory
5. Clean up temporary files

## Output Format

The generated JSON follows this structure:

```json
{
  "version": "1.0",
  "last_updated": "2025-10-23T12:00:00Z",
  "data_source": "acju.lk",
  "cities": [
    {
      "id": "colombo",
      "name": "Colombo",
      "country": "Sri Lanka",
      "timezone": "Asia/Colombo"
    }
  ],
  "prayer_times": {
    "colombo": {
      "timezone": "Asia/Colombo",
      "times": {
        "01-01": {
          "fajr": "5:15 AM",
          "sunrise": "6:30 AM",
          "dhuhr": "12:15 PM",
          "asr": {
            "shafi": "3:30 PM",
            "hanafi": "3:30 PM"
          },
          "maghrib": "6:00 PM",
          "isha": "7:15 PM"
        }
      }
    }
  }
}
```

## Configuration

Modify `config/settings.py` to customize:

- Base URL
- Download/output directories
- City-to-district mappings
- Timezone settings

## Supported Districts

- Colombo, Gampaha, Kalutara
- Hambantota
- Ratnapura, Kegalle
- Galle, Matara
- Badulla, Monaragala
- Trincomalee
- Batticaloa, Ampara
- Kandy, Matale, Nuwara Eliya
- Kurunegala
- Anuradhapura, Polonnaruwa
- Mannar, Puttalam
- Mullaitivu, Kilinochchi, Vavuniya
- Jaffna, Nallur

## Development

### Adding New Features

1. **New scraper**: Add to `src/scraper/`
2. **New extractor**: Add to `src/extractor/`
3. **New utility**: Add to `src/utils/`

### Running Tests

```bash
python -m pytest tests/
```

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Data source: [ACJU (All Ceylon Jamiyyathul Ulama)](https://www.acju.lk/prayer-times/)
