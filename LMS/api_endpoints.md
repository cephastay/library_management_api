# API ENDPOINTS

Below are the list of endpoints that are available in the Library Management System API:

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

# How To Interact EndPoints
```
The Swagger API documentation is still under development, 
so I’ll provide guidance on interacting with some key endpoints here. 
To keep this concise, I’ll focus on the most important ones.
```
---

### User Endpoints
- #### How to Create/ Register User Instances
    You can create new user accounts by sending a **POST** request to 
    the ``api/users`` endpoint. This endpoint is accessible to Anonymous 
    users and Admins (__is_staff: true__) but not to users with an active 
    authenticated session. The request must include the user's email 
    and password in the JSON body, as these are required for successful 
    account creation. Full details on the allowed request format can be 
    found in the Swagger documentation at ``api/docs``.

    
    **example body**
    ```json
    {
        "email":"user@example.com",
        "password": "secretpassword"
    }
    ```
    A successfull **POST** request should return a status code of **201_Created** with a response body containing the user information.

    ```json
    {
        "username": null,
        "email": "user@example.com",
        "joined": "2025-01-13",
        "status": "member",
        "url": "https://hostingaddress/api/users/{user_id}/",
        "bio": null
    } 
    ```
    Bad requests will return a status code of __400_Bad_Request__ with an indication of the errors.

#
### Token EndPoints
- #### How to Create/ Retrieve User Tokens
    The API supports **Basic Authentication**, **REST Framework Tokens**, 
    and **Django Simple JWT Tokens**. The endpoints for retrieving tokens 
    are: `api/token/basic` for **Basic Authentication** 
    `api/token/jwt/create` for **JWT Tokens**

    To access your user account token, you must provide your email and 
    password. However, for the **REST Framework Token** endpoint 
    (`api/token/basic`), the key in the JSON body is labeled as 
    **username** but actually requires the **email** instead. This 
    inconsistency will be corrected soon.

    **example body**

    ```json
    {
        "username": "user@example.com", #should be your email not username
        "password": "secretpassword"
    }
    ```

    This will return a **200_OK** response if you have an active account
    with a response body of your Token. Currently the basic Tokens do not
    expire so keep them safe for accessing protected views.
    
    ```json
    {
        "token": "randomlygeneratedsecuretoken"
    }
    ```
    This will return a **200_OK** response if you have an active account, 
    along with a response body containing your token. 
    Note that **Basic Tokens** currently do not expire, so ensure they 
    are kept secure for accessing protected views.
#
### Book EndPoints
- #### How to view Books in the Library
    The API endpoint `api/books/` is the core of the 
    **Library Management System API**. This endpoint allows for creating 
    new books in the database and viewing all available books. The 
    **POST**, **PUT**, **PATCH**, and **DELETE** methods are 
    restricted to **Admin Users** or specially designated users.  **GET** 
    requests return a list of books currently available for checkout 
    (i.e., books with copies greater than 0 at the time of the request). 
    
    The books are ordered by their publication dates and can be:  **Filtered** by author and **Searched** by title, author, or unique 
    ISBN number (ISBN-13 or ISBN-10)  Books with no available copies will 
    not appear in the response to a **GET** request, even if they exist 
    in the database.

- #### How to Create Books 
    Admin users can create a book entry using the following recommended 
    fields in the request body. The **copies** field is not mandatory, 
    but it helps in managing related models that store additional details 
    about the book.

    **example body**

    ```json
    {
        "title": "Things Fall Apart", #string must be unique
        "author": "Chinua Achebe", #string
        "ISBN": "9780435272463", #13 or 10 characters must be valid and Unique
        "published_date": "1992-04-02", #datetimefield in YYYY-MM-DD
        "book_copies": 5 #integerfield not-required
    }
    ``` 

    A successful **POST** request will return a **201_Created** status 
    code with a response body with the book detail. If the request is 
    unsuccessful or contains errors, a **400_Bad_Request** status code 
    will be returned.

    The **can_checkout** field is automatically updated based on the 
    **copies** provided earlier. If no copies are provided, it is set to 
    **false**. If the number of copies is greater than 0, it will be set 
    to **true**.

    The **url** and **book_info** fields are hyperlinks that provide 
    extra information about the book.

    **example json response body**
    ```json
    {
        "url": "https://hostaddress/api/books/1/",
        "title": "Things Fall Apart",
        "author": "Chinua Achebe",
        "ISBN": "9780435272463",
        "published_date": "1992-04-02",
        "book_copies": 5,
        "can_checkout": true,
        "book_info": "https://hostaddress/api/booksinfo/1/"
    }
    ```

- #### __How to Borrow a Book__
    To borrow a book from the library, you must be an authenticated user 
    with a registered account. The book must be available for checkout, 
    which can be confirmed by accessing its detail endpoint at 
    `api/books/{book_id}/` using the book's ID.   
    
    Future versions of the API will support query parameters 
    (e.g., book title, ISBN, or author) to simplify retrieving book 
    information. 
    
    The endpoint to borrow books is `api/books/{book_id}/checkout/`.
    It supports: a **GET** which returns the book's details if it exists 
    in the database.   A **POST** request allows borrowing the book. 
    Currently, a **POST** request must include a request body. However, 
    future updates will allow borrowing a book without a request body, as 
    the `{book_id}` is already specified in the endpoint. 

    **example request body to borrow book**
    ```json
    {
        "book" : 1 # {book_id} integer
    }
    ```

    A successful post request should return a 201_Created with this
    response body. Other status codes will apply based on general guides
    Also note that the copies of the book in the database will be reduced
    by one and the **checkout_status** will also be updated automatically.
    So in the case where a book has only once copy, upon checkout that
    book becomes unavailable until returned or a new copy added.

    **example response body for successful checkout**

    ```json
    {
        "book": 1,
        "book_title": "Things Fall Apart",
        "user": "user@example.com",
        "checkout_date": "2025-01-13",
        "due_date": "2025-01-28",
        "return_date": null,
        "status": "pending",
        "id": 1
    }
    ```

    The response body contains the following details,  **checkout_date** 
    which is when the book was borrowed, **due_date** by which the book 
    should be returned, **status** current status of the checkout (e.g., 
    _pending_, _overdue_, etc), **id** a unique identifier for the 
    checkout record.   

    The **return_date** for the book is set when the book is returned 
    (covered in the next section). 
    
    If a user fails to return a book by the due date, a penalty will be 
    applied to their account. However, the current API implementation 
    does not yet enforce this penalty. Future versions of the API will 
    also consider adding email notification systems to remind users about 
    due dates and overdue books. 

    **Note:** Users are only allowed to borrow a particular book at a time
    so attempting to checkout a book again will return a bad request 
    status code with a message detailing the user has borrowed the book 
    already.

- #### __How to Return a Book__

    To return a book, an authenticated user will navigate to 
    ``api/books/{book_id}/return/``. A **GET** request to this address
    should return details of the book to be returned, however this 
    operation first queries the database to find existing checkouts for 
    that authenticated user with an active status (i.e with 
    __"status":"pending"__ or any of the statuses) for that user
    if it exists in the database.
    
    A __404_Not_Found__ is returned if no such instance exists in the 
    database however a successful request returns a 200_OK. Currently 
    contemplating on wether to return the checkout instance details 
    instead of the book detail. 

    Send a **POST** request with body containing the {book_id} under the 
    key __"book"__ as illustrated bellow to return the book. As with the
    previous section. I am working on not requiring to supply a request
    body to this address as the {book_id} is apparent in the url.

    **example request body**
    ```json
    {
        "book":1
    }
    ```

    A successfull request will return a 200_OK response and a 
    message body indicated below. The __copies__ of the book in the 
    database is also updated accordingly and as is their __checkout_status__

    **example response body**
    ```json
    {
        "detail": "Borrowed Book returned successfully."
    }
    ```
#
### CheckOut EndPoints

- #### __How to Access Active CheckOuts__
    Authenticated users can retrieve their active checkouts by sending a 
    **GET** request to the endpoint:   ``api/checkout/`` No unique 
    identifier is required in the URL. The backend automatically filters 
    and returns only the active checkouts associated with the 
    authenticated user. Admin users can view all active checkouts in the 
    library by default. This allows them to monitor the activity of all 
    registered users in the system. If no active checkouts are present 
    for the user, or in the system the response body will be an empty set. 

- #### __How to Access CheckOut History__
    As with the previous section authenticated users can send a **GET**
    request to the endpoint ``api/checkout_history/`` to access their 
    checkout history. Admin users can access the history of everyone in 
    the system.Here is a response body of what a successful request will detail.

    **example response body**
    ```json
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
                {
                    "id": 1,
                    "user": "someuser@email.com",
                    "book": "Things Fall Apart",
                    "checkout_date": "2025-01-13",
                    "return_date": "2025-01-13"
                }
                    ]
    }
    ```