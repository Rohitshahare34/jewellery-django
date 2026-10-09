MOST IMPORTANT: DO NOT BREAK OR CHANGE ANY EXISTING WEBSITE FEATURE OR WORKING BEHAVIOR. THIS IS AN EXISTING PRODUCTION JEWELLERY WEBSITE. THE NEW CAMPAIGN SYSTEM MUST BE ADDITIVE ONLY AND MUST NOT ALTER EXISTING BUSINESS LOGIC, DATA, UI, URLs, PRICING, PRODUCTS, CART, WISHLIST, AUTHENTICATION, OR ADMIN FUNCTIONALITY.

==================================================
CRITICAL: PRESERVE ALL EXISTING WEBSITE FEATURES
==================================================

THIS IS AN EXISTING PRODUCTION WEBSITE.

The existing website functionality is already working and MUST NOT
change, break, disappear, or behave differently because of this new
Festival & Promotion Campaign System.

The new feature must be ADDITIVE ONLY.

DO NOT redesign or rewrite existing functionality unless absolutely
required for integration.

The following existing functionality must continue working exactly as
before:

- Homepage
- Navbar/header
- Footer
- Hero section
- Product categories
- Subcategories
- Product listing
- Product detail pages
- Product images/gallery
- Product pricing
- Gold/Silver/Platinum rates
- Automatic product price calculation
- Manual pricing where applicable
- Wishlist
- Quick View
- Cart
- Checkout/order functionality
- User registration/login/logout
- User profile
- Search
- Filters
- Product sorting
- Pagination
- Testimonials
- Existing banners/images
- Existing static files
- Media/uploads
- Django Admin
- Existing admin functionality
- Existing database records
- Existing PostgreSQL database
- Existing URLs/routes
- Existing API/AJAX functionality
- Existing JavaScript functionality
- Existing CSS/design
- Existing responsive behavior
- Existing authentication/permissions
- Existing email functionality if present
- Existing SEO/meta functionality if present

IMPORTANT:

DO NOT modify existing Product, Order, User, Wishlist, Cart,
MetalRate or other business logic unless there is a genuine,
necessary integration requirement.

The promotion system should use its OWN models and logic as much
as possible.

Do NOT replace existing templates unnecessarily.

Do NOT rewrite the homepage.

Do NOT remove existing HTML sections.

Do NOT change existing URLs.

Do NOT rename existing models or fields.

Do NOT change existing database data.

Do NOT change existing pricing calculations.

Do NOT change existing product behavior.

Do NOT change existing login/signup behavior.

Do NOT change existing admin behavior.

If an existing template needs a small integration point for the
promotion component, make the SMALLEST possible change and preserve
the surrounding code exactly.

==================================================
NO REGRESSION REQUIREMENT
==================================================

Before implementation, inspect and understand how every relevant
existing feature works.

After implementation, verify that existing functionality still works.

At minimum test:

1. Homepage loads correctly.
2. Product listing works.
3. Product detail works.
4. Product image/gallery works.
5. Search works.
6. Category/subcategory navigation works.
7. Wishlist works.
8. Quick View works.
9. Cart works.
10. Authentication works.
11. Existing pricing works.
12. Metal rate functionality works.
13. Admin works.
14. Existing media loads.
15. Mobile responsive layout still works.
16. Existing JavaScript has no new console errors.

The new promotion system must not negatively affect page loading,
database queries, existing UI, or existing business logic.

==================================================
DATABASE SAFETY
==================================================

Before production deployment:

- Take a verified database backup.
- Do not delete existing data.
- Do not reset the database.
- Do not modify existing migration files.
- Create new migrations only for the new promotion feature.
- Do not change existing production records unnecessarily.

If migration changes could affect existing tables or data,
STOP and explain the risk before proceeding.

==================================================
PRODUCTION SAFETY
==================================================

DO NOT deploy directly to production.

First:

1. Inspect.
2. Plan.
3. Implement.
4. Test.
5. Run Django checks.
6. Run automated tests.
7. Test existing functionality.
8. Review changed files.
9. Review migrations.
10. Prepare rollback plan.

Only after all checks pass should production deployment be considered.

If you find that an implementation may affect existing functionality,
STOP and clearly explain the issue before making the change.

==================================================
GOLDEN RULE
==================================================

The final website must behave exactly like the old website when the
promotion system is disabled.

If:

Promotion System = OFF

then:

Existing website = EXACTLY AS BEFORE

No banner.
No popup.
No countdown.
No floating video.
No layout disruption.
No pricing changes.
No product behavior changes.

When a campaign is enabled, it should simply ADD the promotional
content to the existing website.

The new system must be completely removable/disableable without
breaking the original website.
