# 🥛 DairyDaze – Local Dairy Supply Management System

**DairyDaze** is a web-based platform created to modernize and streamline a city's local dairy supply chain. The system connects customers, sub-branches, and dairy business owners (main branches) through a single interface that simplifies ordering, delivery tracking, inventory management, and secure digital payments.


## 🌟 Features

- 📦 **Real-Time Stock Visibility:** Customers can view live product availability.
- 🛒 **Smart Order Placement:** Customers can place one-time or subscription-based (daily/monthly) orders.
- 📍 **Sub-Branch Allocation:** Customers are auto-assigned to a nearby sub-branch based on location.
- 🚚 **Delivery Tracking:** Sub-branches update order status through the dashboard.
- 💬 **Direct Chat:** Customers can directly message their assigned sub-branch.
- 📅 **Monthly Calendar & Billing:** View past orders and monthly bills; Admin can edit.
- 💳 **QR Code Payment Integration:** Secure UPI or card payment via QR.
- 📊 **Admin Panel:** View analytics, manage products, stock, feedback, and sub-branch activities.


## 🏗️ System Roles

### 👤 Customers:
- Register and login securely
- View products and stock
- Place or schedule orders
- View the delivery calendar and bills
- Chat with sub-branch
- Make QR-based payments

### 🧑‍🏭 Sub-Branches:
- Login via assigned credentials
- Update stock and product status
- View assigned customer orders
- Respond to chats and feedback

### 🧑‍💼 Admin (Main Branch):
- Register products and branches
- Monitor all sub-branches
- Edit billing data and manage subscriptions
- View reports, feedback, and delivery analytics


## 🧑‍💻 Tech Stack

| Layer       | Technology          |
|-------------|---------------------|
| Frontend    | HTML, CSS, JavaScript |
| Backend     | Python (Django)     |
| Database    | SQLite (Django default) |
| Authentication | Django Auth Framework |
| Hosting     | Localhost / Deploy-Ready |
| Payment     | QR Code Integration (Razorpay)
