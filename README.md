# Seminary Management System

A desktop application for managing seminary operations built with PySide6 (Qt for Python).

## Features

- User authentication system with login interface
- Modern Qt-based user interface
- Cross-platform compatibility (Windows, macOS, Linux)

## Screenshots

![Login Screen](images/login-screenshot.png)

## Requirements

- Python 3.12 or higher
- PySide6
- Qt 6.x

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/nguyendan07/seminary-management-system.git
cd seminary-management-system
```

### 2. Create and activate virtual environment

```bash
python -m venv .qtcreator/Python_3_12_7venv
# Windows
.qtcreator\Python_3_12_7venv\Scripts\activate
# macOS/Linux
source .qtcreator/Python_3_12_7venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the application

```bash
python mainwindow.py
```

### Building the project (using PySide6 tools)

```bash
pyside6-project build
```

### Running via project tools

```bash
pyside6-project run mainwindow.py
```

## Project Structure

```
seminary-management-system/
├── mainwindow.py          # Main application entry point
├── form.ui               # Qt Designer UI file
├── ui_form.py            # Generated UI Python file
├── form_ui.py            # Alternative UI Python file
├── pyproject.toml        # Project configuration
├── requirements.txt      # Python dependencies
├── images/              # Application assets
│   ├── logo.png
│   └── logo.ico
├── .qtcreator/          # Qt Creator project files
└── __pycache__/         # Python cache files
```

## Development

### Prerequisites for development

- Qt Creator (optional, for UI design)
- PySide6 development tools

### Building UI files

If you modify the `.ui` files, regenerate the Python UI files:

```bash
pyside6-uic form.ui -o ui_form.py
```

### Code formatting

This project uses:

- `ruff` for linting and formatting
- `isort` for import sorting

```bash
ruff check .
ruff format .
isort .
```

### Testing the login system

Default test credentials:

- Email: `admin@seminary.edu`
- Password: `admin123`

Or:

- Email: `user@seminary.edu`  
- Password: `user123`

## Configuration

The application can be configured through:

- [`pyproject.toml`](pyproject.toml) - Project settings
- Environment variables for database connections
- Configuration files (to be implemented)

## Building for Distribution

### Using PySide6 Deploy

```bash
pyside6-deploy mainwindow.py
```

### Manual build with Nuitka

```bash
python -m nuitka --onefile --windows-icon-from-ico=images/logo.ico mainwindow.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write docstrings for all functions and classes
- Add type hints where possible
- Test your changes thoroughly

## Dependencies

Main dependencies:

- `PySide6` - Qt for Python framework
- `shiboken6` - Python bindings generator

Development dependencies:

- `ruff` - Fast Python linter and formatter
- `isort` - Import sorting utility

See [`requirements.txt`](requirements.txt) for complete list.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [PySide6](https://doc.qt.io/qtforpython/) (Qt for Python)
- UI designed with Qt Designer
- Icons and assets from [source to be credited]

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/nguyendan07/seminary-management-system/issues) page
2. Create a new issue with detailed description
3. Contact: [your-email@example.com]

## Roadmap

- [ ] Database integration
- [ ] Student management module
- [ ] Course management system
- [ ] Attendance tracking
- [ ] Grade management
- [ ] Report generation
- [ ] Multi-language support
- [ ] Dark theme support

---

**Seminary Management System** - Making seminary administration easier and more efficient.
