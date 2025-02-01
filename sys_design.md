## 1. Functional & Non-Functional Requirements

### **Functional Requirements**
- **User Management:**  
  - User registration, authentication, and profile management.
- **Timetable Management:**  
  - CRUD (Create, Read, Update, Delete) operations for the weekly timetable (e.g., subjects on Monday–Saturday).
- **Academic Calendar & Holidays:**  
  - Input of academic year start/end dates.
  - Ability to add and manage holiday dates.
- **Attendance Rules:**  
  - Define minimum attendance percentages for each subject.
- **Calculation Engine:**  
  - Compute total classes per subject over the academic period.
  - Calculate the minimum number of classes to attend.
  - Determine maximum classes that can be skipped.
  - Identify specific days or sessions that are “skippable” while still meeting the requirements.
- **Visualization:**  
  - Calendar or dashboard view to show skippable days and subject-wise attendance data.
- **Notifications:**  
  - Alert the user if their planned skips could cause attendance to fall below the threshold.

### **Non-Functional Requirements**
- **Scalability:**  
  - The system should support many users concurrently.
- **Responsiveness:**  
  - Near real-time recalculation and UI updates when users change their schedule or parameters.
- **Security:**  
  - Secure storage of user data and safe API communications.
- **Portability:**  
  - Support for both web and mobile clients.
- **Maintainability:**  
  - Clear separation of concerns and modular design for ease of updates.

---

## 2. High-Level System Architecture Overview

The system is divided into client applications, backend/API services, a calculation engine, a data persistence layer, and external services. Here’s a high-level diagram followed by detailed component descriptions:

```
          +-------------------------+
          |       Client App        |
          | (Web/Mobile Interface)  |
          +-----------+-------------+
                      |
                      V
           +---------------------+
           |    API Gateway      |
           +-----------+---------+
                       |
                       V
          +----------------------------+
          |   Backend Application      |
          |    (Business Logic)        |
          +-------------+--------------+
                        |
          +-------------+--------------+
          |  Calculation Engine Module |
          +-------------+--------------+
                        |
          +-------------+--------------+
          |        Database            |
          | (Users, Timetable, etc.)   |
          +-------------+--------------+
                        |
          +-------------+--------------+
          | External Services (Auth,   |
          |   Notification, etc.)      |
          +----------------------------+
```

---

## 3. Detailed Component Architecture

### **3.1 Client Applications**

- **User Interfaces:**  
  - **Web Application:** A responsive web interface built with frameworks like React, Angular, or Vue.js.
  - **Mobile Application:** Native (Swift/Kotlin) or cross-platform (Flutter, React Native) apps.
- **Responsibilities:**
  - Collect user inputs for timetables, academic calendars, holidays, and attendance rules.
  - Display computed results, such as a calendar view marking skippable days.
  - Handle user interactions (e.g., adjustments to planned skips) and notify users of attendance warnings.
- **Communication:**  
  - Interact with the backend using RESTful APIs or GraphQL.

---

### **3.2 API Gateway / Load Balancer**

- **Purpose:**
  - Route incoming requests to appropriate backend services.
  - Implement basic rate limiting and security checks.
- **Technology Options:**
  - NGINX, AWS API Gateway, or any cloud-provider-specific solution.

---

### **3.3 Backend Application & Business Logic**

- **Core Responsibilities:**
  - **User Management:**  
    - Endpoints for user registration, login, and profile management.
  - **Timetable & Calendar Management:**  
    - CRUD endpoints for timetable, academic calendar, and holidays.
  - **Attendance Calculation Trigger:**  
    - When user data is updated, trigger recalculation of attendance and skippable sessions.
  - **Result Serving:**  
    - Provide computed results to the client on request.
- **Technology Options:**
  - Frameworks like Express.js (Node.js), Django/Flask (Python), or Spring Boot (Java).
- **Security:**  
  - Use JWT or OAuth2 for authentication/authorization.
- **Deployment:**  
  - Containerized (using Docker) and managed via orchestration (Kubernetes, ECS, etc.) if needed.

---

### **3.4 Calculation Engine / Scheduling Module**

- **Core Functions:**
  - **Data Aggregation:**  
    - Iterate over the academic calendar (from start to end date), filtering out holidays and non-class days.
    - Map each valid day to the corresponding timetable details.
  - **Computation:**  
    - Calculate the total number of classes per subject.
    - Determine the minimum number of classes that need to be attended (e.g., `ceil(total * minimum_percentage)`).
    - Compute the maximum number of classes that can be skipped per subject.
    - Identify which days or sessions can be skipped while respecting per-subject constraints.
  - **Flexibility:**  
    - Support both whole-day skipping and partial-day (subject-by-subject) skipping.
- **Design Options:**
  - **Monolithic Module:**  
    - Integrate the calculation logic within the main backend if the load is light.
  - **Microservice:**  
    - If calculations become computationally heavy or require scaling independently, deploy as a separate microservice.
- **Implementation Considerations:**  
  - Use an event-driven or message queue approach (e.g., RabbitMQ, Kafka) to decouple heavy computations from user interactions.

---

### **3.5 Data Persistence Layer**

- **Database Types & Structure:**
  - **Relational Database (SQL):**
    - Recommended for structured data.
    - **Tables / Collections:**
      - **Users:** User credentials, preferences, and settings.
      - **Timetable:** Records with day-of-week, subject details, timings, and associated user ID.
      - **Academic Calendar:** User-specific start and end dates.
      - **Holidays:** List of holidays for each user.
      - **Attendance Rules:** Minimum percentages for each subject.
      - **Calculation Results:** Cached computed values such as total classes, minimum required, and skippable session lists.
  - **NoSQL Option:**  
    - Use MongoDB if you expect schema flexibility or document-based storage needs.
- **Performance Enhancements:**
  - Use caching (e.g., Redis) for frequently accessed calculation results.
  - Indexing on common query fields (e.g., user_id, dates).

---

### **3.6 External Services and Integrations**

- **Authentication Service:**
  - Utilize services like Auth0, Firebase Auth, or in-house JWT-based authentication.
- **Notification Services:**
  - For push notifications (mobile) or email alerts regarding attendance status, integrate with services like Firebase Cloud Messaging (FCM) or SendGrid.
- **Calendar Integration (Optional):**
  - If you want to sync with external calendars (Google Calendar, Outlook), integrate using their APIs.

---

## 4. Data Flow & Interaction

### **4.1 User Interaction Flow**

1. **User Onboarding:**
   - **Registration/Login:**  
     The client app sends credentials to the authentication service via the API Gateway.
2. **Input and Management:**
   - **Timetable Input:**  
     User inputs or updates their weekly schedule.
   - **Calendar & Holiday Input:**  
     User sets academic year dates and adds any holidays.
   - **Attendance Rules:**  
     User defines minimum attendance percentages for each subject.
3. **Calculation Trigger:**
   - **Backend Processing:**  
     Once the user updates any relevant data, the backend either immediately triggers or schedules a calculation run.
   - **Calculation Engine:**  
     The engine processes the inputs to compute:
     - Total classes per subject.
     - Minimum classes required.
     - Maximum skippable classes.
     - Which days/sessions can be skipped.
4. **Result Delivery:**
   - **API Response:**  
     The computed schedule is stored and returned via an API endpoint.
   - **UI Update:**  
     The client app displays a calendar view, highlighting skippable days and providing subject-wise details.
5. **User Adjustments:**
   - If users manually modify or “lock in” skip decisions, the backend recalculates to ensure attendance thresholds remain satisfied.
6. **Notifications:**
   - Alerts are sent if the user’s adjustments jeopardize required attendance (via email or in-app notifications).

### **4.2 API Endpoints Example**

- **User & Authentication:**
  - `POST /api/users/register` – Create a new user.
  - `POST /api/users/login` – Authenticate and obtain JWT.
- **Timetable Management:**
  - `GET /api/timetable` – Retrieve user’s timetable.
  - `POST /api/timetable` – Create or update timetable entries.
- **Academic Calendar & Holidays:**
  - `GET /api/academic-calendar` – Retrieve current academic period.
  - `POST /api/academic-calendar` – Set or update academic period.
  - `GET /api/holidays` – List holidays.
  - `POST /api/holidays` – Add new holiday.
- **Attendance Calculation:**
  - `GET /api/attendance-calculation` – Retrieve computed attendance metrics and skippable days.
  - _Optionally_ `POST /api/attendance-calculation` – Trigger a recalculation (if not automatically triggered).
- **Notifications:**
  - `GET /api/notifications` – Retrieve attendance-related alerts.

---

## 5. Infrastructure & Deployment Considerations

### **5.1 Cloud & Containerization**
- **Cloud Providers:**  
  - AWS, Google Cloud, or Azure can host your application.
- **Containerization:**  
  - Use Docker to containerize backend services.  
  - For scaling, orchestration via Kubernetes or managed container services (e.g., AWS ECS/EKS).

### **5.2 CI/CD Pipeline**
- **Continuous Integration:**  
  - Tools such as GitHub Actions, Jenkins, or GitLab CI/CD for automated testing and deployment.
- **Continuous Deployment:**  
  - Automated deployment to staging/production environments.

### **5.3 Logging, Monitoring & Security**
- **Logging & Monitoring:**  
  - Implement centralized logging (ELK Stack, CloudWatch, or similar) and application performance monitoring (APM) tools.
- **Security:**  
  - Enforce HTTPS, encrypt sensitive data, regularly update dependencies, and perform routine security audits.

---

## 6. Scalability, Maintainability & Future Enhancements

- **Modular Architecture:**  
  - Begin with a monolithic design for rapid development.  
  - As the user base grows, refactor into microservices:
    - **User Service**
    - **Timetable Service**
    - **Calendar & Holiday Service**
    - **Calculation Engine Service**
    - **Notification Service**
- **Event-Driven Architecture:**  
  - Use message queues (e.g., Kafka or RabbitMQ) to decouple timetable updates from the calculation engine.
- **API Gateway & Service Discovery:**  
  - As you split into microservices, implement an API Gateway to route requests and a service registry for service discovery.
- **Data Analytics:**  
  - In the future, you could integrate data analytics to offer insights on attendance trends or predictive alerts.

---
