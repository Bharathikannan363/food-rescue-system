## project structure Frontend

── 📁 frontend/                         # React + Vite + Tailwind CSS App
    ├── package.json                     # Node.js dependencies
    ├── vite.config.js                   # Vite configuration & proxy routes
    ├── tailwind.config.js               # Tailwind CSS theme configuration
    ├── postcss.config.js                # PostCSS configuration
    ├── index.html                       # Base HTML file (includes Leaflet CSS)
    └── 📁 src/                          # React Source Code
        ├── main.jsx                     # React DOM root entry point
        ├── App.jsx                      # App root layout with Providers
        ├── index.css                    # Tailwind directives & map CSS
        ├── 📁 components/               # Reusable UI Components
        │   ├── Navbar.jsx               # Top navigation bar
        │   ├── Sidebar.jsx              # Role-specific collapsible sidebar
        │   ├── Footer.jsx               # Page footer
        │   ├── Button.jsx               # Variant button component
        │   ├── Card.jsx                 # Card container
        │   ├── Modal.jsx                # Accessible modal dialog
        │   ├── ConfirmDialog.jsx        # Confirmation prompt dialog
        │   ├── StatusBadge.jsx          # Styled status badge
        │   ├── Loading.jsx              # Loading spinner
        │   ├── ErrorMessage.jsx         # Alert message banner
        │   ├── DataTable.jsx            # Reusable tabular data viewer
        │   ├── DashboardCard.jsx        # Metric summary widget card
        │   ├── ChartCard.jsx            # Chart container card
        │   ├── NotificationBell.jsx     # Dropdown notification bell
        │   ├── SearchBar.jsx            # Search filter input
        │   ├── FilterBar.jsx            # Status dropdown selector
        │   ├── ImageUpload.jsx          # Camera capture / upload input
        │   ├── LocationPicker.jsx       # Address & GPS picker
        │   ├── Map.jsx                  # Single marker Leaflet map
        │   ├── LiveMap.jsx              # Multi-marker live tracking map
        │   └── ProtectedRoute.jsx       # Role access route guard
        ├── 📁 pages/                    # Portal Page Views
        │   ├── 📁 auth/                 # Login, Register, Captcha, ForgotPassword
        │   ├── 📁 admin/                # Admin Dashboard, NGOs, Donors, Volunteers, Donations, Requests, Assignments, LiveTracking, Reports..
        │   ├── 📁 donor/                # Donor Dashboard, PostFood, MyDonations, Requests, Tracking, Notifications, History
        │   ├── 📁 ngo/                  # NGO Dashboard, AvailableFood, Requests, Deliveries, Tracking, Beneficiaries, FoodVerification.
        │   └── 📁 volunteer/            # Volunteer Dashboard, MyAssignments, AvailableAssignments, Tracking, Notifications, History
        ├── 📁 services/                 # Axios Service Layer (api.js, authService, adminService, donorService, ngoService, volunteerService, etc.)
        ├── 📁 context/                  # AuthContext, NotificationContext, AppContext
        ├── 📁 hooks/                    # useAuth, useGeolocation, useNotifications
        ├── 📁 routes/                   # AppRoutes (URL mapping & role guards)
        └── 📁 mock/                     # mockData.js (Fallback mock data)
