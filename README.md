# Nexus PDF Engine 🚀

Nexus PDF Engine is a professional desktop automation tool designed to convert image sequences into high-quality PDF documents. Built with a **Clean Architecture** approach, it separates business logic from the UI, ensuring scalability and performance.



## ✨ Features
- **Multi-Selection:** Choose specific images manually using a native file explorer.
- **Real-time Previews:** High-tech UI with dynamic thumbnails and "card-style" list.
- **Smart Formatting:** Automatically converts images to RGB and scales them proportionally to A4 size.
- **Asynchronous Processing:** Multi-threaded engine that prevents UI freezing during PDF generation.
- **Dark Tech UI:** Modern interface built with `CustomTkinter`.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **UI Framework:** CustomTkinter
- **Image Processing:** Pillow (PIL)
- **PDF Generation:** ReportLab
- **Concurrency:** Threading

## 📂 Project Structure
```text
image_to_pdf_automa/
├── core/               # Business Logic (PDF Engine)
├── ui/                 # GUI Components and Layout
├── main.py             # Application Entry Point
├── requirements.txt    # Project Dependencies
└── README.md           # Documentation