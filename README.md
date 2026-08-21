## How The Application Works

The application follows a simple Flask-based request and response structure.

1. The user opens the application.
2. Flask receives the request through a defined route.
3. The corresponding route processes the request.
4. Data is retrieved from or written to the database when required.
5. Flask renders the appropriate Jinja2 template.
6. The browser displays the resulting page.

For example, when a user creates a new entry:

```text
User
  ↓
Writing Form
  ↓
POST Request
  ↓
Flask Route
  ↓
Database
  ↓
Redirect
  ↓
The Writing Shelf
```

---

## Project Structure

```text
the-writing-shelf/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── instance/
│   └── blog.db
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── add.html
│   ├── post.html
│   ├── edit.html
│   ├── search.html
│   └── 404.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── main.js
```

---

## File Structure Explained

### `app.py`

The main Flask application file.

It contains the application's routes, request handling, database operations, and application logic.

### `requirements.txt`

Contains the Python packages required to run the application.

### `README.md`

Project documentation containing information about the application, its structure, setup, and usage.

### `.gitignore`

Specifies files and folders that should not be committed to Git.

### `instance/blog.db`

The local SQLite database used to store application data.

---

## Templates

### `base.html`

Provides the shared HTML structure for the application, including navigation, fonts, stylesheets, and common layout elements.

### `home.html`

Displays the main shelf and the saved entries.

### `add.html`

Provides the form for creating a new entry.

### `post.html`

Displays an individual entry.

### `edit.html`

Provides the interface for editing an existing entry.

### `search.html`

Provides the search interface and displays matching results.

### `404.html`

Custom page displayed when a requested route does not exist.

---

## Static Files

### `static/css/style.css`

Contains the application's styling, responsive layouts, typography, buttons, forms, cards, hover effects, and animations.

### `static/js/main.js`

Contains client-side interactions such as the character counter, flash message handling, and button feedback.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/the-writing-shelf.git
```

Move into the project directory:

```bash
cd the-writing-shelf
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

The application will then be available at:

```text
http://127.0.0.1:5000
```

---

## Application Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Display saved entries |
| `/add` | GET, POST | Create a new entry |
| `/post/<id>` | GET | View an individual entry |
| `/edit/<id>` | GET, POST | Edit an existing entry |
| `/delete/<id>` | POST | Delete an entry |
| `/search` | GET | Search entries |

---

## Responsive Design

The interface is designed to adapt to:

- Desktop
- Laptop
- Tablet
- Mobile devices

Responsive CSS rules adjust the layout, navigation, forms, cards, spacing, and typography for smaller screens.

---

## Project Scope

The project demonstrates the integration of:

- Flask routing
- GET and POST requests
- Jinja2 templates
- Template inheritance
- Form handling
- SQLite
- CRUD operations
- JavaScript interactions
- Responsive CSS