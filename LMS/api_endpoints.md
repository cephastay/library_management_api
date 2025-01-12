# API ENDPOINTS

Below is the list of endpoints that are available in the Library Management System API:

---

## USER MANAGEMENT ROUTES

| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
|--------|-------|---------------|--------|
| *GET*  | `/api/users/` | _Retrieve Registered Users_ | _All users_ |
| *GET*  | `/api/users/{user_id}/` | _Retrieve User Details_ | _All users_ |
| *POST* | `/api/users/` | _Register new user_ | _Anon-Users or Admin_ |
| *PUT*  | `/api/users/{user_id}/` | _Edit/ Update User Info_ | _Admin or Owner_ |
| *PATCH* | `/api/users/{user_id}/` | _Partial Edit/ Update User Info_ | _Admin or Owner_ |
| *POST* | `/api/users/{user_id}/change_password/` | _Change User Password_ | _Admin or Owner_ |
| *DELETE* | `/api/users/{user_id}/` | _Delete/Remove a user_ | _Admin or Owner_ |

---

## TOKEN ENDPOINTS

| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
|--------|-------|---------------|--------|
| *POST* | `/api/token/jwt/create/` | _Retrieve jwt token_ | _All users_ |
| *POST* | `/api/token/jwt/refresh/` | _Refresh the jwt access token_ | _Authenticated Users_ |
| *POST* | `/api/token/jwt/verify/` | _Verify the validity of a jwt token_ | _Authenticated Users_ |
| *POST* | `/api/token/basic/` | _Retrieve basic rest framework token_ | _Authenticated Users_ |

---

## BOOK MANAGEMENT ROUTES

| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
|--------|-------|---------------|--------|
| *GET*  | `/api/books/` | _Retrieve All Books_ | _All users_ |
| *GET*  | `/api/books/{book_id}/` | _Retrieve Specific Book Details_ | _All Users_ |
| *POST* | `/api/books/` | _Create Book Instance_ | _Admin Users_ |
| *POST* | `/api/books/{book_id}/checkout/` | _Borrow the Book Specified by ID_ | _Authenticated Users_ |
| *POST* | `/api/books/{book_id}/return/` | _Return the Book Borrowed by Book ID_ | _Owner or Admin_ |
| *PUT*  | `/api/books/{book_id}/` | _Edit/ Update Book Details_ | _Admin_ |
| *PATCH* | `/api/books/{book_id}/` | _Partial Edit/ Update Book Details_ | _Admin User_ |
| *DELETE* | `/api/books/{book_id}/` | _Delete Book_ | _Admin User_ |

---

## CHECKOUT ROUTES

| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
|--------|-------|---------------|--------|
| *GET*  | `/api/checkout/` | _Books Checked Out by User (Status Pending)_ | _Owner or Admin_ |
| *GET*  | `/api/checkout/` | _Books Checked Out by All Users (Status Pending)_ | _Admin_ |
| *GET*  | `/api/checkout_history/` | _User CheckOut History_ | _Admin or Owner_ |
| *POST* | `/api/checkout/` | _CheckOut Available Book_ | _Authenticated Users_ |
| *POST* | `/api/checkout/{book_id}/return/` | _Return a checked out Book_ | _Authenticated Users_ |

## OTHER ROUTES

| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
|--------|-------|---------------|--------|
| *GET*  | `/api/docs/` | _View API Documentation SWAGGER UI_ | _All Users_ |
| *GET* | `/api/redoc/` | _View API Documentation Swagger Redoc_ | _All Users_ |
| *GET* | `/api/endpoints/` | _Available API Endpoints in JSON_ | _All Users_ |
| *GET* | `/api/admin/` | _Access Django Admin Page_ | _Admin_ |
---
