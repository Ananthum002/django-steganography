# 🕵️ Django Steganography Web App

A full-stack web application built with **Django** that allows users to hide secret messages inside images using **steganography** — the practice of concealing information within another medium so that it remains invisible to the naked eye but can be retrieved by anyone with the right tool.

🔗 **Try the live demo:**
- URL: https://django-steganography.onrender.com
- Demo login — Username: `anan@gmail.com`  Password: `123`


---

## 📖 Table of Contents

- [About the Project](#about-the-project)
- [How Steganography Works](#how-steganography-works)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Usage Guide](#usage-guide)
- [Deployment](#deployment)
- [Known Limitations](#known-limitations)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## 📌 About the Project

This project demonstrates **image-based steganography** through a clean, browser-accessible interface. Instead of relying on encryption (which makes data unreadable but obviously suspicious), steganography hides the *existence* of the message itself — the image looks completely normal to anyone who views it.

The app was built as a learning project to explore:
- Image processing using Python's **Pillow** library
- Bitwise manipulation of pixel data (Least Significant Bit encoding)
- Building and deploying a production-ready Django web application
- Handling file uploads, encoding/decoding pipelines, and downloads in a web context

---

## 🔬 How Steganography Works

This project uses the **Least Significant Bit (LSB)** technique:

1. Every pixel in an image is made up of color channels (Red, Green, Blue), each represented by an 8-bit number (0–255).
2. The *least significant bit* of each channel can be changed without causing any visually noticeable difference to the image.
3. The secret message is converted into binary, and each bit of the message is embedded into the least significant bit of consecutive pixel color values.
4. To decode, the app reads the least significant bits back out, in the same order, and reconstructs the original message.

This means the image's appearance is virtually unchanged, while it secretly carries hidden data.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Encode Text** | Type a message and hide it inside an uploaded image |
| **Encode Text File** | Upload a `.txt` file and hide its full contents inside an image |
| **Decode** | Upload an encoded image to extract and reveal the hidden message |
| **Download Encoded Image** | Download the resulting image after encoding |
| **Share** | Share encoded images/messages (if implemented in your app) |
| **Received** | View previously received/decoded messages (if implemented) |
| **Simple Web UI** | No technical knowledge required — just upload, type, and click |
| **User Authentication** | Login system to manage personal encode/decode history (if applicable) |

> ℹ️ Update this table to reflect exactly which features are implemented in your current version.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Django (Python) |
| **Image Processing** | Pillow (PIL) |
| **WSGI Server** | Gunicorn |
| **Static File Serving** | WhiteNoise |
| **Database** | SQLite (default; can be swapped for PostgreSQL in production) |
| **Frontend** | HTML, CSS, JavaScript (Django templates) |
| **Deployment Platform** | Render |
| **Version Control** | Git & GitHub |

---

## 📁 Project Structure

```
django-steganography/
└── site1/                      # Repo root for deployment (Render root directory)
    ├── myapp/                  # Core app: steganography logic
    │   ├── apps.py
    │   ├── filesteg.py         # File-based encoding/decoding logic
    │   ├── models.py
    │   ├── steg.py             # Core LSB encode/decode functions
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── site1/                  # Django project settings
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── staticfiles/             # Collected static assets (CSS, JS, images)
    ├── media/                   # User-uploaded and generated images (ephemeral on free hosting)
    ├── build.sh                 # Build script run on deployment
    ├── manage.py                 # Django management entry point
    ├── Procfile                   # Deployment process declaration
    ├── requirements.txt           # Python dependencies
    ├── runtime.txt                 # Python runtime version
    └── db.sqlite3                   # SQLite database (not committed to GitHub)
```

---

## 🚀 Getting Started (Local Setup)

### Prerequisites

- Python **3.12** or higher
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ananthum002/django-steganography.git
   cd django-steganography/site1
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Collect static files** (optional for local dev, required for production)
   ```bash
   python manage.py collectstatic --no-input
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open the app**
   Visit `http://127.0.0.1:8000` in your browser.

---

## 🔐 Environment Variables

For production deployment, the following environment variables should be set:

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django's cryptographic secret key | A long random string |
| `DEBUG` | Whether debug mode is enabled | `False` in production |
| `ALLOWED_HOSTS` | Comma-separated list of allowed domains | `django-steganography.onrender.com` |
| `PYTHON_VERSION` | Python version for the build environment | `3.12.0` |

Create a `.env` file locally (and ensure it's listed in `.gitignore`) for local development if your `settings.py` is configured to read from environment variables.

---

## 🧭 Usage Guide

### Encoding a Message
1. Navigate to the **Encode** page
2. Choose **Encode Text** or **Encode Text File**
3. Upload a cover image (PNG recommended — lossy formats like JPEG may corrupt hidden data)
4. Enter your secret message (or upload a text file)
5. Click **Encode Message**
6. Download the resulting image

### Decoding a Message
1. Navigate to the **Decode** page
2. Upload the previously encoded image
3. Click **Decode**
4. The hidden message will be revealed

> ⚠️ **Important:** Always use lossless image formats (PNG) for both encoding and decoding. Lossy formats like JPEG compress and alter pixel data, which destroys hidden information.

---

## 🌐 Deployment

This project is deployed on **[Render](https://render.com)**.

**Configuration used:**
- **Root Directory:** `site1`
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn site1.wsgi:application`
- **Runtime:** Python 3.12.0

**`build.sh` contents:**
```bash
#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### Deploying Your Own Copy
1. Fork or clone this repository
2. Create a new Web Service on Render and connect your GitHub repo
3. Set the Root Directory to `site1`
4. Set the Build and Start commands as shown above
5. Add the required environment variables (see above)
6. Deploy

---

## ⚠️ Known Limitations

- **Ephemeral storage on free hosting:** Render's free tier does not persist files written to disk between requests/restarts. Generated images must be served directly in the same request rather than saved and linked to later.
- **Image format sensitivity:** Only lossless formats (PNG) reliably preserve hidden data. JPEG and other compressed formats are not suitable.
- **Free tier sleep:** On Render's free instance type, the app spins down after inactivity. The first request after idling may take 30–50 seconds to respond while the server wakes up.
- **Message size limits:** The amount of data that can be hidden depends on the image's pixel count — larger images can hold larger messages.

---

## 🐛 Troubleshooting

| Issue | Likely Cause | Fix |
|---|---|---|
| Build fails with "No such file or directory: build.sh" | `build.sh` is in the wrong folder relative to Render's Root Directory | Ensure `build.sh` sits next to `manage.py` and `Procfile` |
| `pip install` fails on deploy | Incompatible Python version with package requirements | Check `PYTHON_VERSION` matches your dependencies' requirements |
| Downloaded image link says "File wasn't available on site" | App tried to serve a file that was wiped due to ephemeral storage | Serve the file directly in the HTTP response instead of saving to disk first |
| 500 Internal Server Error on live site | `DEBUG=True` left on, or `ALLOWED_HOSTS` missing the Render domain | Set `DEBUG=False` and add your Render URL to `ALLOWED_HOSTS` |

---

## 🗺️ Roadmap

- [ ] Switch to cloud storage (e.g. AWS S3 / Cloudinary) for persistent file handling
- [ ] Add password-protected message encoding
- [ ] Support for hiding files (not just text) inside images
- [ ] Add image preview before/after encoding
- [ ] Improve mobile responsiveness
- [ ] Add automated tests for encode/decode accuracy

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available for learning and personal use. Add a specific license (e.g. MIT) here if you'd like to formalize usage terms.

---

## 👤 Author

**Ananthu Mohan**
GitHub: [@Ananthum002](https://github.com/Ananthum002)
