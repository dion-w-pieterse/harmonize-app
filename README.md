# harmonize-app
## Summarized Elements of Project Report

Please contact author if you wish to view the entire project report.
## 3. METHODOLOGY

### Project Objective
Harmonize is a web application that enhances communication, understanding, and trust between patients and providers. The application increases providers' visibility and promotes interaction with patients through two methods of online interaction, a blog, and a forum. Patients have a privacy-focused journal (blog), while a blog is provided to the providers to market their services. The forum will create an environment where patients and providers can interact and evaluate each other in group conversations. The application employs social networking features to enhance effective and direct communication and visibility, including liking/un-liking user entries and mentioning users. The use of NLP will further expedite and enhance the ability of the therapist to analyze large volumes of their patient's monitored data. There will be three user types, patient, provider, and admin. All patients will be identified anonymously for privacy. Providers have a choice of anonymity as well. The admin user has access to a visual back-end data management system, which will make it easier to maintain the application's database information.

### 3.1.1 Application Usage Pattern
The user will be presented with the home page, a general landing page for site visitors. The user will have the option to register a new account or log in as an existing user. The registration form will allow users to make their account a "patient" or "provider" user type. Upon registering as a new user, they are automatically logged into their account and redirected to the home page. Upon creating a new account, the new user will have to navigate to the "Edit Account" page, which allows them to enter critical information that will enhance connectivity with other registered patients and providers. If they are actively seeking a provider, the user can enter their general information, make their account non-searchable, choose their current mental health conditions, choose their insurance company, and write a bio about themselves. Every user has a "Landing Page." The landing page is the primary user page for others to visit when looking for another user. It acts as the launching point for everything concerning that user. Page options include:
- View user's blog
- Choose to monitor a user.
- Grant Privacy Access to a user.
- View if a user is actively seeking a provider or accepting new patients.
- View if the blog is searchable (indicating access status to the entire blog).

The patient or provider has access to their journal and blog, respectively. The users' journals and blogs are the same and have different user types (to signify different usage). Each user can write an entry, which can include an image or not. Each blog entry can be "liked" or "unliked" by other users. The user has complete control to set the privacy control of each blog entry to "public" or "private." The user can edit or remove any blog entry they create. When providers are granted private access to a patient's journal, they will see private and public entries. The provider will also have a color-coded sentiment analysis bar visible on each journal entry for quick visual sentiment interpretation. The provider can click on a "View Analysis" button for each journal entry, which takes them to a new page that details the sentiment analysis and Name Entity Recognition for each journal post. This feature enhances the provider's ability to interpret quickly and single out concerning journal entries of potential clients (since they were granted privacy access).

Every registered user has access to the public forum. The public forum consists of "Rooms," which hold conversations about a specific subject. The author of a room can edit or remove any remove they have made. Upon visiting a room, a user can click on a "Conversation," which contains a dialogue between patient and provider user types in response to a conversation starter question. A starter question is always entered by the author of the conversation upon creation. The user has complete control to edit or remove any response they author. All rooms, conversations, and individual responses have links back to their respective author's landing page. If another user wants to learn more about the author, read their blog and like their entries, monitor or grant privacy access to that user. Every user will have their splashboard. The splashboard is an interface that allows users to quickly access valuable data and connections facilitated by the application's social networking features and data relationships. The splashboard has two sections, "General Data Services” and “Provider Data Services.”

*Options for the "General Data Services" include:*
- Journal and blog feed of all users I am monitoring.
- Journal feed of patients I am monitoring.
- List users that granted the current user privacy access.
- Journal and blog feed(s) where the current user is granted privacy access.
- Manage users I am monitoring.
- Manage private access users.
- Who mentioned the current user within the last week?
- Forum conversations of interest.
- Recommended other patient associations (based on conditions).
- Forum response feed of all users I am monitoring.
- Forum response feed of patients I am monitoring.
- Mental Health Crisis Emergency Services Contact Information.
- User raw search by user alias.

*Options for Provider Data Services include:*
- Recommended Provider Associations (Based on Conditions)
- Blog Feed of Providers I Am Monitoring.
- Forum Response Feed of Providers I am Monitoring.
- Providers Who Worked as Out-Of-Network Specialists.
- Where Are Monitored Providers Being Mentioned in Journals?
- Where Are Monitored Providers Being Mentioned in Forum?

  Every registered user has a search feature in the navigation, which they can use to search the public forums. The search results will render a paginated list of responses with a breadcrumb link chain of the room, conversation and response. The user can click on any link and access those individual elements. The third type of user, "admin," which is not selectable upon account creation, exists on the system. The admin user has access to the site's administrator section. The admin section is a data management user interface that tabulates the database tables of the website.


### 3.1.2 Activities
1. Create wireframe and OO class diagrams for application.
2. Setup the PostgreSQL server and create the project database.
3. Create the project package, and install all dependencies.
4. Build the back-end logic first, on top of a basic front-end skeleton.
5. Once the back-end is complete and functioning, complete the front-end design.
6. Perform testing on the application.
7. Write the final report documentation for the project.
8. Present and demonstrate the project.

The application is developed using Python. The back end runs on Flask web framework. The front-end uses HTML5, Bootstrap 4 CSS Framework. The database management system is PostgreSQL. The graphics and designs were done using Adobe Photoshop and Illustrator. A minimum RAM requirement of 2GB is suggested to run it efficiently.

### 3.3 Route Functions
  The following section describes the most important route functions and classes that pertain the main features of the application. Mentioned functions do not include required arguments for the sake of brevity. Some route functions will call SQL queries via a parameterized SQL function call via PugSQL. The SQL queries themselves are not explained for the sake of brevity as well. Please note, the word “journal” implies the blog for patients, and “provider blog” implies the blog for providers.

#### Activity: User Visits Home Page
*Action Required:* The user visits the home page (index route) of the application:

*Route URL:* ```/```

*Authentication for Accessing Route:* Unprotected Route Access (Open Access).

*Route Request Methods Allowed:* ```GET, POST```

*Route Function Signature:* ```index()```

*Description:* The index route presents the user with the index.html template which give the user the options to read more about the application features, login, or register as a new user.

#### Activity: User Login
*Action Required:* User clicks the “login” button in the navigation menu.

*Route URL:* ```/login```

*Authentication for Accessing Route:* Unprotected Route Access (Open Access)

*Route Request Methods Allowed:* ```GET, POST```

**Route Function Signature:** ```login()```

*Description:* 
The login route allows registered users to log into the application.

#### Activity: User Registers As A New User
*Action Required:* User clicks the “register” button in the navigation menu.

*Route URL:* ```/register```

*Authentication for Accessing Route:* Unprotected Route Access (Open Access)

*Route Request Methods Allowed:* ```GET, POST```

*Route Function Signature:* ```register()```

*Description:* 
The route allows new users to create an account with the application. All inputs have validation.

#### Activity: User Log Out of Application
*Action Required:* User clicks the “logout” button in the navigation menu.

*Route URL:* ```/logout```

*Authentication for Accessing Route:* Protected Route (Login required)

- *Route protected by:* valid email and hashed SHA256 with 32-bit salted password.

*Route Request Methods Allowed:* ```GET```

*Route Function Signature:* ```logout()```

*Description:* 
The route allows the user to logout of their account.

#### Activity: Edit Account
*Action Required:* User clicks the “Edit Account” button in the “Account / Services” dropdown of the navigation menu.

*Route URL:* ```/user_account/<int:user_id>```

*Authentication for Accessing Route:* ```Protected Route (Login required)```

- *Route protected by:* valid email and hashed SHA256 with 32-bit salted password.

*Route Request Methods Allowed:* ```GET, POST```

*Route Function Signature:* user_account(user_id)

*Description:* 
The route allows the user to edit their account information. Any existing data is prepopulated from the database.

#### Activity: Choose Out-Of-Network Specialist Services
*Action Required:* User clicks the “Choose Out-Of-Network Specialist Services” button in the navigation menu.

*Route URL:* ```/insurance_provider_out_net_svces```

*Authentication for Accessing Route:* Protected Route (Login required & user_type = ‘provider’)
- Route protected by: valid email and hashed SHA256 with 32-bit salted password.

*Route Request Methods Allowed:* ```GET, POST```

*Route Function Signature:* ```insurance_provider_out_net_svces()```

*Description:* 
The route allows a logged in provider user to choose the insurance companies that they have worked for as out-of-network specialists.

#### Activity: Full-Text Search:
*Action Required:* User clicks the “Search” button in the navigation menu after typing their query in the “Find Something…” input field in the navigation menu.

*Route URL:* ```/search_site```

*Authentication for Accessing Route:* Protected Route (Login required & user_type = ‘provider’)

- *Route protected by:* valid email and hashed SHA256 with 32-bit salted password.

*Route Request Methods Allowed:* ```GET, POST```

*Route Function Signature:* ```search_site()```

*Description:* 
The Full-Text Search feature was manually implemented for the application using PostgreSQL. All database table field data for all fields that are to be searched are tokenized. Tokens are turned into a vectorized, weighted index field for fast access. The weights are determined based on word relevance in accordance to predefined PostgreSQL English dictionary. Words that are irrelevant to the meaning of the data are removed. The search results deliver responses with links to their pertaining conversation based on relevance to the search query terms.

#### Activity: Access Patient Journal / Provider Blog

Action Required: User clicks the “View My Journal Blog” or “View My Blog” button in the navigation menu.
Route URL: /blog/<int:user_id>
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’ , ‘patient’))
- Route protected by: valid email and hashed SHA256 with 32-bit salted password.
Route Request Methods Allowed: GET, POST
Route Function Signature: blog()
Description:
Every patient and provider has access to their journal and blog, respectively. All blog entries are listed chronologically. This example uses a provider account to showcase the provider’s blog.

#### Activity: View Individual Patient Journal / Provider Blog Entry Page
Action Required: User clicks the title of a journal / blog entry.
Route URL: /blog/<int:user_id>/entry/<int:blog_entry_id>
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’ , ‘patient’)
- Route protected by: valid email and hashed SHA256 with 32-bit salted password.
Route Request Methods Allowed: GET, POST
Route Function Signature: view_blog_entry(user_id, blog_entry_id)
Description:
Every patient and provider can view a journal entry or blog entry on its own separate page.

#### Activity: Write A Patient Journal / Provider Blog Entry
Action Required: User clicks the “Write an Entry” button on the user’s journal / blog landing page.
Route URL: /blog/<int:user_id>/write
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’ , ‘patient’)
- Route protected by: valid email and hashed SHA256 with 32-bit salted password.
Route Request Methods Allowed: GET, POST
Route Function Signature: write_blog_entry(user_id)
Description:
Every patient and provider can write an new journal or blog entry, respectively.

#### Activity: View Journal Blog Entry Analysis Page (Available To Provider If Granted Privacy Access)
Action Required: Provider clicks the “View Analysis” button on a patient journal entry.
Route URL: /blog/<int:user_id>/entry/<int:blog_entry_id>/analysis
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’)
- Route protected by: valid email and hashed SHA256 with 32-bit salted password.
- Only a provider who is granted privacy access by a patient user type can view this page.
Route Request Methods Allowed: GET, POST
Route Function Signature: view_journal_entry_analysis(user_id, blog_entry_id)
Description:
Providers who are granted privacy access by a patient will have access to this route, which enables them to see sentiment analysis and Name Entity Recognition for the specific journal entry.

#### Activity: Edit A Patient Journal / Provider Blog Entry
Action Required: User clicks the “Edit” button on the user’s individual journal / blog entry page.
Route URL: /blog/<int:user_id>/entry/<int:blog_entry_id>/edit
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’ , ‘patient’)
•	Route protected by: valid email and hashed SHA256 with 32-bit salted password.
•	Only the author of the blog entry can edit the blog entry.
Route Request Methods Allowed: GET, POST
Route Function Signature: edit_blog_entry(user_id, blog_entry_id)
Description:
Every patient and provider can edit any entry they create.

#### Activity: Remove Patient Journal / Provider Blog Entry
Action Required: User clicks the “Remove” button on the user’s individual journal / blog entry page.
Route URL: /blog/<int:user_id>/entry/<int:blog_entry_id>/remove
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’ , ‘patient’)
•	Route protected by: valid email and hashed SHA256 with 32-bit salted password.
•	Only the author of the blog entry can remove the entry.
Route Request Methods Allowed: GET, POST
Route Function Signature: remove_blog_entry(user_id, blog_entry_id)
Description:
Every patient and provider can remove any entry they create.

#### Activity: Like A Journal Or Blog Entry
Action Required: User clicks the “Like” button on the card of a specific patient journal or provider blog entry. The ‘Like’ button will be visible through various feeds as well.
Route URL: /blog/like_blog_entry/<int:blog_entry_id>
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’ , ‘patient’)
•	Route protected by: valid email and hashed SHA256 with 32-bit salted password.
Route Request Methods Allowed: GET, POST
Route Function Signature: like_blog_entry(blog_entry_id)
Description:
Every patient and provider can choose to like a patient journal or provider blog entry.

#### Activity: Un-Like A Journal Or Blog Entry
Action Required: User clicks the “Un-Like” button on the card of a specific patient journal or provider blog entry (only if they have first liked the entry). The “Un-Like” button will be visible through various feeds as well.
Route URL: /blog/unlike_blog_entry/<int:blog_entry_id>
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’ , ‘patient’)
•	Route protected by: valid email and hashed SHA256 with 32-bit salted password.
Route Request Methods Allowed: GET, POST
Route Function Signature: like_blog_entry(blog_entry_id)
Description:
Every patient and provider can choose to like a patient journal or provider blog entry.

#### Activity: Like A Forum Response
Action Required: User clicks the “Like” button on the card of a specific forum response. The “Like” button will be visible through various feeds as well.
Route URL: /forum/like_forum_response/<int:convo_response_id>
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’ , ‘patient’)
•	Route protected by: valid email and hashed SHA256 with 32-bit salted password.
Route Request Methods Allowed: GET, POST
Route Function Signature: like_forum_response(convo_response_id)
Description:
Every patient and provider can choose to like a forum response.

#### Activity: Un-Like A Forum Response
Action Required: User clicks the “Un-Like” button on the card of a specific forum response. The “Un-Like” button will be visible through various feeds as well.
Route URL: /forum/unlike_forum_response/<int:convo_response_id>
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’ , ‘patient’)
•	Route protected by: valid email and hashed SHA256 with 32-bit salted password.
Route Request Methods Allowed: GET, POST
Route Function Signature: unlike_forum_response(convo_response_id)
Description:
Every patient and provider can choose to un-like a forum response.

#### Activity: View User’s Landing Page
Action Required: User clicks the “<username>’s Landing Page” button on the user’s journal / blog landing page.
Route URL: /landing_page/<int:user_id>
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’ , ‘patient’)
•	Route protected by: valid email and hashed SHA256 with 32-bit salted password.
Route Request Methods Allowed: GET, POST
Route Function Signature: landing_page(user_id)
Description:
Every patient and provider can access their account landing page.
  
#### Activity: View Forum
Action Required: User clicks the View Main Public Forum” button under “Account / Services” dropdown menu in navigation bar.
Route URL: /forum_rooms
Authentication for Accessing Route: Protected Route (Login required & (user_type = ‘provider’ , ‘patient’)
•	Route protected by: valid email and hashed SHA256 with 32-bit salted password.
Route Request Methods Allowed: GET, POST
Route Function Signature: forum_rooms()
Description:
Every patient and provider can access application’s forum.






























## Documentation is incomplete, please check back.
