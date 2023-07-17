# Crawl firms from WKO.at das Portal der Wirtschaftskammern

## ⚠️ Disclaimer / Warning!
This repository/project is intended for Educational Purposes ONLY.
The project and corresponding python script should not be used for any purpose other than learning. Please do not use it for any other reason than to learn about webscrapping. Make sure you adhere to the terms and conditions of the site!

This script is designed to streamline the process of extracting B2B leads from registers - specifically the Austrian Wirtschaftskammern portal. It automates the tedious task of manually sorting through over a thousand profiles to determine their relevance and to extract necessary contact information. The script outputs data such as the name, address, email, website, and business type from each profile and neatly organizes it into a structured Excel table for easy use in your marketing initiatives.

## Getting Started

These instructions will guide you on how to run the script on your local machine for development and testing purposes.

### Prerequisites

The script requires the following Python packages:
- requests
- beautifulsoup4
- pandas
- openpyxl

You can install these packages using pip:

```bash
pip install -r requirements.txt
```

### Running the Script

1. Customize the website filters on this [link](https://firmen.wko.at/-/wien/?branche=25376&branchenname=immobilienmakler&page=) according to your needs.
2. Copy the adapted link and replace the `url` variable in the script.
3. Run the script.

For example:
```python
# URL to scrape data from
url = "https://firmen.wko.at/-/wien/?branche=25376&branchenname=immobilienmakler&page=1"
```

Then execute the Python script in your preferred environment.

## Contributing

Contributions are what make the open source community an incredible place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

Feel free to reach out if you have any questions or if there's anything else I can do to help!