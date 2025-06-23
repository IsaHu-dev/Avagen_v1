# Avagen - Digitally Crafted Avatar Collection


[**Avagen – Live Site**](https://avagen-502553ff2610.herokuapp.com/) 

## About

**Avagen** is a digital concept store for the next generation of online creators, gamers and explorers. It lets you **browse, purchase and immediately download** high‑quality, digitally crafted avatars to represent your online identity across games, social platforms and virtual worlds.

The platform is built with **Django 5**, **PostgreSQL** and **Stripe** to provide a secure, scalable and fully‑featured e‑commerce experience while keeping content‑creators and end‑users front‑of‑mind.

### Why Avagen?

* **Creators first** – Upon purchase and download, both creators and metaverse users can immediately assign their selected avatar to their profile for use across supported platforms.
* **Instant delivery** – every purchase is a digital download as a ready‑to‑use PNGs in a zipped file, plus the original layered source file PSD so buyers can re‑skin as they wish.
* **Cross‑platform licensing** – a single licence grants customers the right to reuse the avatar across games, socials and the open metaverse.

---

### Target Users

| Persona                   | Needs                                                 |
| ------------------------- | ----------------------------------------------------- |
| **Gamers & streamers**    | Original in‑game skins & digital profile                                          |
| **All users**             | Anyone aged 16 or older, of any gender, who loves social media and gaming.        |
| **Influencers & VTubers** | A recognizable digital persona that travels with them        |
| **Everyday web users**    | Anonymity & security without sacrificing style               |
| **Hobbyists**             | Users using avatars to add to their profiles for recreation  |
---

## Key Features

### Features

Avagen is a full-stack Django web application designed for selling digital products. Built with Python, Django, HTML, CSS, and JavaScript, it emphasizes responsive design, secure digital delivery, and user-friendly interfaces. The platform includes admin tools, SEO optimization, and Stripe integration for a seamless checkout experiences.

- **Catalogue**
  - Responsive product grid layout optimized for all screen sizes.
  - Displays high-quality product thumbnails.
  - Filter products by theme or price range.

- **Product Detail**
  - High-resolution image gallery on each product page.
  - License drop down selector - License terms displayed clearly: Personal, Indie, or Professional.
  - Detailed product descriptions before checkout.
  - Detailed product specifications and price breakdown before purchase.
  - Average star rating and customer reviews displayed beneath the product descriptions.

  **Reviews & Ratings**
   - Authenticated users can leave 1–5 star reviews with optional comments.
   - Average rating is calculated on‑the‑fly and displayed for performance.
   - Catalogue can be sorted by rating to surface the most popular avatars.

- **Cart & Checkout**
  - Add products (with chosen licence) to cart and adjust quantities inline.
  - Encrypted payment processing ensures security.
  - Optimized for mobile and desktop devices.
  - Verified Stripe webhooks finalise orders.
  - Fully responsive checkout pages optimised for mobile and desktop.

- **Digital Delivery**
  - Download links shown immediately after successful payment.
  - Order history includes access to previously purchased downloads.
  - Instant and secure delivery of digital products.
  - Purchased digital products are downloadable from the registered user's account. The downloads are resumable. Lifetime access to them is granted.

- **User Accounts**
  - Built using the django-allauth third-party package for robust user authentication.
  - Users can register, log in, and manage their orders easily.
  - Users can update their profile information, i.e Phone number, Address, Postcode and County and Country.
  - Includes a "Download Again" page for users to re-download past purchases.

- **Newsletter Signup**
  - Users can subscribe using their first name, last name, and email.
  - Supports email marketing integrations (e.g., Mailchimp or SMTP).

- **Admin / Superuser Dashboard**
  - Django Admin interface for product and category management.
  - Full CRUD functionality for superusers.
  - Restricted content visibility by user tier. 
  - Superusers and administrators have access to the Django Interface. They can delete and edit products on the products & products detail page.
  
  **Search Bar**
   - Instant, keyword-based search.
   - Helps users quickly find products by name, model, or relevant terms.

- **SEO Optimization**
  - Custom, SEO-optimized meta tags implemented on essential pages.
  - Clean, readable URLs.
  - Custom 404 error page for better user experience and site crawlability.
  - Optimized meta tags applied to key pages for enhanced search engine indexing.
  
  **Performance** 
  - WhiteNoise serves compressed static assets; Cloudinary transforms images on‑the‑fly for smaller payloads.


## How to Use Avagen

1. **Register** – click *Sign‑up*, enter your email address username and password.
2. **Login** - Login with your username or email and input your password.
2. **Explore avatars** – filter by theme (Personalized, Artistic, Seasonal or Special Events, etc.) or sort by price / rating.
3. **Add to cart** – adjust quantity or remove items directly from the mini‑cart.
4. **Checkout** – fill in billing info and pay securely via Stripe. A confirmation email is sent instantly.
5. **Download** – use the *Download* button on the success page or from *My Orders* at any time.
6. **Manage account** – change personal info, view order history, re‑download files or delete your account.


## UX & Design

| Asset              | Preview |
| ------------------ | ------- |
| **Wireframes**     |   tbc   |
| **Colour palette** |   tbc   |


### Logo 

[![Avagen Logo](media/avagen_logo_text.png)](media/avagen_logo_text.png)


The interface uses soft, neutral colors with a single eye-catching gradient ( #7F00FF → #17A2B8 → #E100FF) for buttons and key actions. This keeps the focus on the products page while still guiding users where to click. For typography, it uses Inter for body text and Space Grotesk for headings, creating a modern and readable design.

## Agile Process

Project tasks were tracked in **GitHub Projects** (Kanban). Each card contained a *user story* with acceptance criteria and links to the relevant pull request.

### User Stories

| Role            | Story                                     | Acceptance criteria                                                     |
| --------------- | ----------------------------------------- | ----------------------------------------------------------------------- |
| Visitor         | *I want to preview avatars before buying* | Index page loads within <3 s, shows 12 avatars, click opens detail page |

## Models (simplified)



## Technologies Used

* **Backend** – Python 3.13, Django 5, Django‑Allauth, Stripe SDK
* **Database** – PostgreSQL 16, AWS RDS (production)
* **Frontend** – HTML5, CSS3, Bootstrap 5, JavaScript, jQuery for some DOM manipulation
* **Dev‑Ops** – GitHub and Heroku
* **Testing** – `pytest`, Lighthouse, W3C validators, Black.

## Database Schema 



## Deployment

 The application was deployed with Heroku. The following preparatory steps are as follows:
  1. Set Debug Mode to False. In settings.py, the DEBUG setting was set to False to ensure a production-ready environment.
  2. A Procfile document is defined. web: gunicorn avagen_main.wsgi.
  3. Store Dependencies - All required dependencies were documented in requirements.txt using: pip3 freeze --local > requirements.txt.
  4. Create a New Heroku App. 
    - Log in to the Heroku dashboard.
    - Click New > Create New App.
    - Enter a unique app name.
    - Click Create App.
  5.  Configure Application Settings
    - Navigate to the Settings tab.
    - In the Config Vars section, add the required environment variables:
      - Database_URL
      - DJANGO_SECRET_KEY
      - Cloudinary_Cloud_Name
      - Cloundinary_API_Key
      - GCS_KEY_BASE64 - Import the text file (Taken from the gcs-service-key.json from Google Storage)
      - Stripe_Public_key, Stripe Secret Key and the Stripe Webhook Secret key. 

    - Add the Heroku/Python buildpack.
  6.  Install Whitenoise for Heroku to serve static files / images on Heroku.
      - Setting Up Whitenoise for Static Files in Heroku

    - pip install whitenoise

    Add to settings.py: 

    MIDDLEWARE = [
         "whitenoise.middleware.WhiteNoiseMiddleware",
    ]

    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"  # Heroku serves from this folder
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

  7. Connect to GitHub Repository.
      -  In the Deploy tab, under Deployment Method, select GitHub.
      -  Follow the steps to authorize and connect your GitHub account.
      -  Search for the repository and click Connect.
  8.  Deploy the Application.   
      -  Select manual deployment
      -  In the Manual Deploys section, select a branch and click Deploy Branch.
  9.  Access the Live Application.
      -  Once the deployment is complete, an app link is generated. The live application can be accessed at <a href="https://avagen-502553ff2610.herokuapp.com/" target="_blank">Avagen App</a>
   ```
4. Upload media files to Google Cloud Storage 3.1.0


## Local Installation

```bash
git clone https://github.com/IsaHu-dev/Avagen_v1.git
cd Avagen_v1
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # add your Stripe keys, etc.
python manage.py migrate
python manage.py runserver
```

### Browse to [http://127.0.0.1:8000](http://127.0.0.1:8000).
---

## 🧪 Detailed User Testing

### ✅ Manual Testing

| Area              | Action                            | Expected Result                                  | Status |
| ----------------- | --------------------------------- | ------------------------------------------------ | ------ |
| **Registration**  | Submit form with valid input      | Redirect to Dashboard, confirmation email sent   | ✅      |
|                   | Submit mismatched passwords       | Form errors shown, account not created           | ✅      |
| **Login**         | Valid credentials                 | Redirect to dashboard, session starts            | ✅      |
|                   | Invalid credentials               | Error message shown                              | ✅      |
| **Catalogue**     | Visit home page                   | 12+ products visible, filter sidebar available   | ✅      |
|                   | Use search or filters             | Grid updates with matching items                 | ✅      |
| **Product Page**  | Click on product card             | Redirect to detail page, preview gallery visible | ✅      |
|                   | Click "Add to Cart"               | Item added to cart, page redirects with success message | ✅      |
| **Cart**          | Adjust quantity                   | Cart subtotal updates without page reload        | ✅      |
|                   | Remove item                       | Item removed, cart total recalculates            | ✅      |
| **Checkout**      | Fill form with Stripe test card   | Payment succeeds, redirect to success page       | ✅      |
|                   | Cancel checkout                   | Return to cart, no order created                 | ✅      |
| **Delivery**      | Download from success page        | ZIP or file download starts                      | ✅      |
|                   | Download from past orders         | File re-downloads without issues                 | ✅      |
|                   | Attempt expired link (>24h)       | 403 Forbidden shown                              | ✅      |
| **Profile**       | Edit account info                 | Name/email updates persist                       | ✅      |
|                   | Delete account                    | Data removed, user logged out                    | ✅      |
| **Mobile**        | Navigate on iPhone SE / Galaxy S8 | Layout responsive, navbar collapses correctly    | ✅      |
| **Accessibility** | Navigate with keyboard            | All interactive elements are reachable           | ✅      |

### 🧪 Testing Status

* **Manual Testing**: ✅ Comprehensive manual testing completed
* **Performance**: Lighthouse scores -- across all categories
* **HTML/CSS**: Passes W3C validators

---

## Known Issues / Future Work

* **Avatar builder** – client‑side compositor using Three.js & Fabric.js
* **Marketplace payouts** – migrate to Stripe Connect Express for automated royalties

---
## Resources

| **Real Python / Django docs / Stack Overflow**   | Reference for the code in the Avagen app |


## Credits

| Resource                      | Usage                                   |
| ----------------------------- | --------------------------------------- |
| **Envato**                            | Base png elements for some avatar packs   |
| **Stylized semi-3D character images** | Created by the owner of Avagen - Isa Hu      |                  
| **Stripe Docs & Samples**             | Checkout & stripe credit card implementation   |
| **Code Institute**                    | Webhooks implementation


---

## Licence

All code is released under the **MIT Licence**. Avatars and artwork are released under the **Avagen Digital Asset Licence** (see `LICENCE.md`).

---

## Acknowledgements
















































