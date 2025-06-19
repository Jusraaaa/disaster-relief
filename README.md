# Disaster Relief – Distributed System Project

This project is a distributed system designed to simulate a real-time disaster relief coordination platform. The system allows multiple clients to send help requests to a distributed network of city-based servers, and provides an admin dashboard for managing incoming requests.

## 🧠 Project Concept

The system demonstrates the following distributed systems principles:
- **Multiple autonomous agents** (users) interacting with the system in real time.
- **Shared state** is distributed between city-based servers and a centralized dashboard.
- **Resilience**: the system can continue to operate even if one server node goes down.
- **Real-time communication** using TCP sockets.
- **Data persistence** using a local JSON file.

## ⚙️ Architecture

```

Client (UI)
│
└───> Socket Communication
│
\[Server - SHKUP]
\[Server - TETOVE]
\[Server - GOSTIVAR]

Admin Dashboard (Flask) ← Reads & displays all requests (JSON file)

````

## 💻 Components

### Client UI (`client_ui/`)
- Users select a city and send categorized help requests.
- Categories: Ambulance, Water, Food, Other
- Requests are sent to the appropriate server using TCP socket communication.

### Admin Dashboard (`admin_ui/`)
- Displays real-time incoming requests on a map.
- Visual + audio alarm for new entries.
- Filtering by city.
- Option to delete all or selected requests.

### City Servers
- Independent server files (`server_shkup.py`, `server_tetove.py`, `server_gostivar.py`)
- Listen on separate ports and accept incoming help requests from the client.

## 📁 Technologies Used
- **Python** (Flask, socket)
- **JavaScript** (Leaflet.js for the map)
- **HTML/CSS**
- **JSON** for storing request data

## 🧪 How to Run
1. Start the servers:
   ```bash
   python server_shkup.py
   python server_tetove.py
   python server_gostivar.py
````

2. Run the admin dashboard:

   ```bash
   cd admin_ui
   python app.py
   ```

3. Run the client UI:

   ```bash
   cd client_ui
   python app.py
   ```

## ✅ Features

* Real-time map and request visualization
* City-based socket routing
* Audio alert on new help request
* Admin panel with request filtering and deletion
* Fully functional distributed architecture

## 👩‍💻 Author

**Jusra Ferati** – Project for Distributed Systems

