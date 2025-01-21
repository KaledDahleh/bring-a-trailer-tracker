# Car Sales Tracker

A web application that tracks and visualizes car auction prices from Bring a Trailer. The application allows users to search for specific car models and displays historical auction data in an interactive chart.

## Features

- Search for any car model to view its auction history
- Pre-configured buttons for popular luxury and sports cars
- Interactive line chart showing price trends over time
- Responsive design that works on both desktop and mobile devices
- Real-time data scraping from Bring a Trailer
- Support for handling large datasets

## Technology Stack

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript
  - Chart.js for data visualization
  - Google Fonts (Roboto)

- **Backend:**
  - Python 3.x
  - Flask web framework
  - Selenium for web scraping
  - Chrome WebDriver

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd car-sales-tracker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Install Chrome WebDriver:
   - The application uses webdriver-manager which will automatically handle ChromeDriver installation

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Use the application by:
   - Entering a car model in the search box and clicking "Fetch Data"
   - Or clicking one of the preset car model buttons
   - View the resulting price trend chart

## Project Structure

```
car-sales-tracker/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Main webpage template
└── README.md          # Project documentation
```

## Error Handling

The application includes robust error handling for:
- Invalid car model inputs
- Network connection issues
- Data scraping failures
- Missing or invalid data formats

## Development Notes

- The application uses headless Chrome for scraping
- Rate limiting is implemented to respect the website's terms of service
- Chart.js is configured for optimal visualization of price trends
- Responsive design breakpoints are set for various screen sizes

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
