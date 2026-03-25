# 🏋️ Fitness Trainer Web Application (Django)

## 🚀 Overview (TL;DR)
**Live Demo:** [Виж сайта]([https://your-demo-link.com](https://trainerappivan-backend2.onrender.com/))

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

**Payments:**

* Integrated with **Stripe (test mode)**
* Designed for future production-ready payment support

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
