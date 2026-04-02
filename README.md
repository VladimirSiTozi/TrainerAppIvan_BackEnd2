# 🏋️ Fitness Trainer Web Application (Django)

## 🚀 Overview (TL;DR)

**A full-stack fitness trainer web application built with Django, designed to help users manage workouts, track progress, and stay consistent with their fitness goals. The platform provides an intuitive interface and responsive design for a smooth experience across all devices.**

<p align="center">
  <a href="https://trainerappivan-backend2.onrender.com/"><strong><ion-icon name="enter-outline"></ion-icon>Live Demo</strong></a>
</p>

> ⚠️ Note: The initial load of the site may take 1–2 minutes because it’s hosted on Render’s free plan.

--- 

## 🖼️ Application Preview (Homepage)
<img width="1547" height="975" alt="image" src="https://github.com/user-attachments/assets/6fcb92f8-6434-423c-836c-f74fef517983" />

A full-stack **Python/Django web application** built for **fitness trainers and their clients**.

It enables trainers to create and manage personalized workout programs, while clients can access them through their own profiles.

**Key highlights:**

* 👥 Role-based system (**Trainer / Client**)
* 🔐 Authentication (email + Google login)
* 🧑‍🏫 Trainers create and manage workout programs directly from the UI
* 📋 Clients access personalized training plans
* 🛒 Online store with Stripe (test payments)
* 📚 Articles/blog system
* 📩 Contact form for direct communication
* ☁️ Deployed on Render with a live database

---

## 📌 Core Features

### 👥 User Roles

The system supports two types of users:

* **Client**

  * Can register/login (email or Google)
  * Has access to a personal **Profile page**
  * Can view assigned workout plans and trainer advice
  * Can purchase programs/products

* Logged client view with created training plan
  <img width="1300" height="985" alt="image" src="https://github.com/user-attachments/assets/6d0cf0df-02f0-4b0b-9bed-597347f7c9ef" />

* **Trainer**

  * Has extended permissions
  * Can create and manage:

    * Workout programs
    * Exercises
    * Training content
  * Works entirely through the application UI (no need for Django admin)

---

### 🧑‍🏫 Trainer Dashboard

Trainers can:

* Create **custom workout plans**
* Add exercises to each plan
* Include:

  * Descriptions
  * YouTube videos or images
* Manage content dynamically from the website interface

* Trainer (Admin) Dashboard
<img width="1416" height="899" alt="image" src="https://github.com/user-attachments/assets/a58da9bb-0d12-46a2-9574-189eade6ad4f" />

* Client training plan with editing capabilities
<img width="1240" height="985" alt="image" src="https://github.com/user-attachments/assets/df8af1bb-7e21-4e96-9a23-d75c2c6a0c4a" />

---

### 🏋️ Workout Plans

Each workout plan contains:

* A structured list of exercises
* For every exercise:

  * 📄 Description
  * 🎥 YouTube video **or**
  * 🖼️ Image illustration

Plans are assigned to clients and visible in their **Profile section**.

---

### 👤 Profile System

After logging in, users gain access to a **Profile page**, where they can:

* View their assigned workout program
* Read trainer instructions and recommendations

---

### 🛒 Online Store (PROGRAMS Page)

Users can:

* Browse available programs
* Purchase training plans or products

* Shoping cart
<img width="918" height="682" alt="image" src="https://github.com/user-attachments/assets/5dd39293-551e-4129-911c-8c40c372acb1" />

**Payments:**

* Integrated with **Stripe (test mode)**
* Designed for future production-ready payment support

* Stripe payment method
<img width="933" height="687" alt="image" src="https://github.com/user-attachments/assets/abaf7785-0999-44b0-9a2d-946996e4b690" />

---

### 📚 Content System

* **Articles/Blog**

  * Users can read fitness-related articles

* **Programs Page**

  * Displays purchasable training programs

---

### 📩 Contact System

* Users can contact the trainer directly via a **Contact form**
* Messages are sent via email

---

## 🧭 User Flow

1. User visits the website
2. Browses programs, articles, and content
3. Registers or logs in (email or Google)
4. Accesses **Profile page**
5. Views assigned workout plan
6. Purchases additional programs (optional)
7. Contacts trainer if needed

---

## 🛠️ Tech Stack

### Backend

* Python
* Django

### Frontend

* Django Templates
* JavaScript (basic scripts)

### Authentication

* Django Authentication System
* Google OAuth

* User registration page with email and Google authentication
<img width="720" height="675" alt="image" src="https://github.com/user-attachments/assets/b01a595e-4905-4481-942e-e966b99e233a" />

### Payments

* Stripe (test environment)

### Deployment

* Render (free hosting)
* Hosted database (via Render)

---

## 🗂️ System Architecture (High-Level)

* Users (Clients & Trainers)
* Workout Programs
* Exercises
* Store / Products
* Articles
* Contact System
* Payment Integration (Stripe)

---

## 🔐 Authentication

* Email & password registration
* Google login integration

---

## 💳 Payments

* Stripe test payments implemented
* Ready to be switched to live mode

---

## ☁️ Deployment

* Hosted on **Render**
* Includes:

  * Web service
  * Database

---

## ⚙️ Admin & Content Management

* Trainers manage everything via the frontend UI
* Django Admin can still be used (optional, not required)

---

## 📈 Future Improvements

* Live Stripe payments
* Progress tracking for clients
* Messaging system (trainer ↔ client)
* Mobile optimization
* Notifications system

---

## 📱 Responsive Design

The application is fully responsive and optimized for:

- 📱 Mobile devices
- 📲 Tablets
- 💻 Desktop screens

The layout adapts dynamically to provide a smooth user experience across all devices.

* Mobile View (Responsive Design)
<img width="320" height="600" alt="image" src="https://github.com/user-attachments/assets/e30a3daf-701d-4a99-a076-e2e7a20d2134" />

---
