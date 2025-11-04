Smart QR-Based Inventory and Order Tracking System

A modern QR-powered inventory & order management system designed to enable seamless item tracking, order verification, and real-time status updates across multiple devices. Built using Flask, WebSockets, and QR code technology, this application provides a reliable, scalable, and network-accessible solution for diverse operational environments.

Note: This system is not limited to food ordering. It is adaptable for retail inventory, token-based systems, library management, warehouse tracking, and event entry validation.

✨ Key Features
Core Capabilities

🔐 Unique QR generation for each order/item

📲 Instant scanning through mobile devices

⚡ Real-time tracking & live updates via WebSockets

🌐 Multi-device support over local network

🧾 Automatic order log storage

🖥️ Simple, clean, professional UI

🗃️ Light-weight SQLite backend (extendable to MySQL/PostgreSQL)

Suitable For
Application Area	Use Case
Canteens / Cafes	Order pickup & live queue tracking
Retail & Stores	QR-based item & transaction validation
Warehouses	Stock tracking & receiving/dispatch scanning
Libraries	Book issue/return & inventory
Events & Registration	QR-based attendee validation
Hostels / Offices	Token & coupon management
🧠 Technology Stack
Layer	Technology
Backend Framework	Python (Flask)
Frontend	HTML, Bootstrap
Realtime Communication	Flask-SocketIO
Database	SQLite
QR Code Engine	Python qrcode library

📂 Project Structure
qr-tracking-system/
│── app.py
│── requirements.txt
│── README.md
│
├── templates/
│   ├── index.html
│   ├── generate.html
│   └── track.html
└── static/
    └── qrcodes/

⚙️ Installation & Setup
Prerequisites

Python 3.8+

Pip installed

Install Dependencies
pip install -r requirements.txt

Run Server
python app.py

Access the Application

Open in browser:

http://<your-local-ip>:5000


Ensure both mobile devices and host system are on the same Wi-Fi network.

🚀 Usage Guide

Open Generate QR

Enter order/item ID → Generate QR

Scan QR using phone camera

Order appears in Real-Time Dashboard

Track live status updates instantly

🛣️ Roadmap

The following enhancements are planned:

✅ Role-based authentication (Admin / Staff / User)

✅ Cloud/database integration (PostgreSQL, Firebase option)

✅ Analytics & reporting dashboard

✅ Push notifications (Web & Mobile)

✅ Dedicated mobile app (Flutter / React Native)

✅ RFID + QR hybrid model

✅ Multi-branch network support

📄 License

This project is released under the MIT License.
You are free to use, modify, and distribute this application.

🤝 Contribution

Contributions are welcome!
Please raise issues or submit pull requests to collaborate.

⭐ Support

If you find this project useful, please give it a star ⭐ on GitHub — it encourages more improvements and open-source work.
