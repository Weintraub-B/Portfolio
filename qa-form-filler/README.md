# QA Form Filler

QA Form Filler is a Python-based automation tool designed for quality assurance professionals and developers who need to rapidly test form input fields on websites. It uses either Playwright or Selenium to simulate realistic user input using the Faker library.

## Features

- Cross-browser automation with Playwright (Chromium) and Selenium (Chrome).
- Randomized realistic input for text, emails, dates, numbers, etc.
- Dropdown, checkbox, radio, and color field interaction.
- Automatic screenshot capture of filled forms.
- Field-by-field logging of successes and failures in structured CSVs.
- Support for multiple URLs defined in a JSON list.
- Optional headless mode for silent background execution.
- Command-line interface (CLI) for flexible control.
- Modular structure suitable for extension and testing.

## Project Structure

```
qa-form-filler/
├── main.py
├── cli.py
├── save_auth.py
├── auth.json
├── url_list.json
├── form_data_log.csv
├── requirements.txt
├── logging_config.py
├── screenshots/
└── logs/
```

## Usage

### 1. Install Dependencies

Create a virtual environment and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
playwright install  # Only if using Playwright
```

### 2. Prepare Your URL List

Update `url_list.json` with a list of forms to test:

```json
[
  { "url": "https://www.selenium.dev/selenium/web/web-form.html" },
  { "url": "https://www.techlistic.com/p/selenium-practice-form.html" }
]
```

### 3. Run the Filler

Using Playwright (default):

```bash
python main.py --urls url_list.json --headless --submit
```

Using Selenium:

```bash
python main.py --urls url_list.json --headless --submit --selenium
```

## Command Line Options

| Option      | Description                                    |
|-------------|------------------------------------------------|
| --urls      | Path to JSON file with URLs to test            |
| --headless  | Run browser in headless mode (no GUI)          |
| --submit    | Automatically submits forms after filling      |
| --selenium  | Use Selenium instead of Playwright             |
| --login     | Optionally run login logic if enabled          |
| --auth      | Path to authentication file (optional)         |

## Output

- Screenshots are saved to the `screenshots/` directory.
- Field-level logs are saved in `logs/{domain}/{date}/form_data_log.csv`.

## Technologies Used

- Python 3.10+
- Playwright (default)
- Selenium (optional fallback)
- Faker (for generating realistic data)
- Webdriver Manager
- CSV and logging modules

## Limitations and Notes

While QA Form Filler handles a wide range of field types, some advanced input types (such as file uploads or custom JavaScript widgets like date pickers or color selectors) may not be fully supported or might require manual interaction or extension. Date fields, in particular, may behave inconsistently depending on browser implementation or client-side validation. Contributions or improvements to expand this functionality are welcome.

## Disclaimer

This tool is for development, QA, and demonstration purposes only. Ensure you have permission before automating any third-party website.

## License

This project is released under the MIT License.
