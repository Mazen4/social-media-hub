# SOCIAL MEDIA CONTENT HUB
#### Video Demo: <[URL HERE](https://youtu.be/kJBXtT3jGHo)>
#### Description:

The Social Media Content Hub is a full-stack, web-based productivity application designed to capture, organize, and track social media content across multiple platforms. Distributing material across networks such as Facebook, Instagram, TikTok, YouTube, and LinkedIn often leads to workflow fragmentation. Ideas strike spontaneously, and drafting, scheduling, and tracking often take place across messy spreadsheets or disparate to-do lists.

This project solves this problem by providing a centralized command post. It pairs a dynamic, interactive web dashboard with an automated backend, allowing users to visually manage their content pipeline from raw concept to published material.

### Project Architecture and Features

The application operates as a three-stage Kanban pipeline, dividing the content lifecycle into three distinct states: Idea, Planned, and Posted. Users can visually track where an asset stands, identify which specific platforms a post is targeted for, and monitor completion progress through dedicated platform checkboxes.

Key features include:
* **Asynchronous Platform Tracking:** Each post contains toggleable checkmarks for Facebook, Instagram, TikTok, YouTube, and LinkedIn. Toggling a checkbox updates the backend SQLite database in real time via asynchronous JavaScript fetch calls, avoiding unnecessary full-page refreshes.
* **Drag-and-Drop Workflow Management:** Content cards can be dragged across Kanban columns (Idea to Planned, Planned to Posted). This utilizes native HTML Drag and Drop API events synchronized with backend state management to ensure the database always reflects the visual board.
* **In-Place Card Deletion:** Users can purge discarded ideas directly from the user interface. Clicking the delete control executes a background request that removes both the DOM element and the corresponding database record instantly, ensuring a clean workspace.
* **REST API Extensibility:** A dedicated API endpoint allows external services to seamlessly push new content ideas into the database, paving the way for future integrations.

### File Structure and Purpose

* **`app.py`**: The core application controller written in Python using the Flask microframework. It defines the routing logic, manages database connection lifecycles via SQLite3 helper functions, and implements the web API routes. The primary routes include:
  * `/`: Serves the primary dashboard, querying the database and organizing entries chronologically.
  * `/add`: Handles standard POST submissions from the desktop web interface to create new ideas.
  * `/api/add_idea`: A REST endpoint designed to accept JSON payloads from external integrations, parsing content and individual platform flags.
  * `/update_platform`: Receives asynchronous JSON requests to toggle individual platform booleans.
  * `/update_status`: Updates a card's status column during drag-and-drop operations.
  * `/delete/<int:post_id>`: Permanently removes a record from the database.

* **`project.db` & `init_db.py`**: The persistent relational database and its setup script. Executing `init_db.py` creates the `posts` table with explicit integer fields for each platform, timestamps, status strings, and content blocks.

* **`templates/layout.html`**: The foundational Jinja2 template establishing the HTML boilerplate, viewport configuration, Bootstrap styling integration, and global navigation headers.

* **`templates/index.html`**: The primary dashboard template extending `layout.html`. It iterates over posts partitioned by status, builds the three Kanban columns, renders individual cards with platform controls, and embeds the desktop quick-capture form.

* **`static/styles.css`**: Custom styling rules augmenting Bootstrap. It establishes board dimensions, column shading, card elevation transitions, cursor modifications for drag events, and responsive card sizing.

* **`static/script.js`**: Contains the client-side JavaScript driving user interactivity. It manages drag events (`drag`, `allowDrop`, `drop`), gathers element identifiers, and issues asynchronous `fetch` requests with JSON payloads to maintain state parity between the user interface and backend database.

* **`requirements.txt`**: Specifies application runtime dependencies.

### Design Decisions

Several technical trade-offs were evaluated during the development of this application:

1. **Relational Schema vs. Flat Boolean Columns:** In traditional relational database design, platforms might be modeled using a separate junction table with a many-to-many relationship (e.g., a `post_platforms` table). However, because the list of target networks is fixed and finite, defining explicit integer columns directly within the `posts` table proved far more performant. It eliminated complex SQL JOIN queries, simplified data serialization, and allowed rapid UI generation without database performance penalties.

2. **Asynchronous Fetch vs. Traditional Form Submissions:** Relying exclusively on standard HTTP POST requests for every checkbox toggle or column move would force full-page reloads. This disrupts the visual flow and resets the user's scroll position, which is highly inefficient for a Kanban board. Using the native JavaScript Fetch API enables a smooth, modern application feel where state changes occur instantly in the background.

3. **API-First Architecture Considerations:** While the primary interface is a web dashboard, the inclusion of the `/api/add_idea` route was a deliberate choice to decouple data ingestion from the frontend UI. This allows for future scalability where automation tools or mobile applications can push records into the SQLite database without requiring HTML form emulation.

### How to Run

1. Clone this repository and open the directory in your terminal.
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize the database schema: `python init_db.py`
4. Run the development server: `flask run` or `python app.py`
5. Access the web dashboard in your browser at `http://127.0.0.1:5000`.
