Project Title: Custom Google Social Login Integration with Django Authentication System

Detailed Project Description

This Django project offers a **custom Google Social Login integration** designed to work seamlessly with `dj-rest-auth` and `allauth`. The system is built using Django REST Framework (DRF) and enables a flexible, API-based authentication flow suitable for various frontend applications, such as React or others. 

Key Features and Custom Authentication Logic

1. Custom Google Social Login Integration**:
   - **API-Driven Flow**: Google login is handled entirely through a custom API, making the frontend completely decoupled and adaptable. This API design allows any frontend that can communicate via REST to work with the system.
   - **Account Creation or Existing Login**: The backend checks the user’s email upon Google login:
     - **If the email is new**, it creates a new account, bypassing email verification, as Google already handles it.
     - **If the email exists**, it authenticates the user to the existing account, preventing duplicates.
   - **Automatic Password Handling**: Google-created accounts are assigned a secure, generated password, unknown to the user, and managed by Django.

2. Standard Email and Password Login:
   - Flexible Option: For traditional login, `dj-rest-auth` manages email and password authentication, and users can switch easily between Google login and standard login.
   - Password Reset for Google Accounts: Users who initially logged in with Google may reset their password if they wish to log in traditionally. This flow includes:
     - An email-based reset link, allowing them to set a new password for standard login.
  
3. Centralized Data and Account Flexibility:
   - Both Google and traditional login methods point to the same user data, so users can switch between them seamlessly without data fragmentation.

4. Decoupled Frontend Integration:
   - The system works smoothly with React, using `axios` for API requests and `@react-oauth/google` for OAuth, but is designed to be frontend-agnostic, allowing easy integration with any frontend framework or mobile app.

Advantages of the Project:
- Custom Google Social Login ensures compatibility with `dj-rest-auth` and `allauth`, providing seamless Google integration.
- High Security with Google’s verification and Django’s password reset process.
- Flexibility and Scalability due to a decoupled backend, modular packages, and fully API-driven authentication.

This setup delivers a powerful, extensible authentication system suited for modern applications that require Google login along with traditional login support, all while keeping account data centralized.
