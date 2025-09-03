# Overview

A web-based scratch card game application built with Flask that allows users to scratch virtual cards to win prizes. Users interact with an HTML5 canvas-based scratch card interface, reveal prizes, and complete a redemption process by providing their details. The application manages products, generates unique redemption links, and tracks user redemptions through a complete prize fulfillment workflow.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 for responsive design and styling
- **Interactive Elements**: HTML5 Canvas for scratch card functionality with pointer events
- **Client-side Logic**: Vanilla JavaScript for scratch detection, canvas manipulation, and user interactions
- **Visual Effects**: CSS animations, SVG filters for scratch effects, and Canvas Confetti for celebrations

## Backend Architecture
- **Web Framework**: Flask with SQLAlchemy ORM for database operations
- **Application Structure**: Modular design with separate files for models, routes, and application configuration
- **Session Management**: Flask sessions for maintaining user state during the scratch-to-redeem workflow
- **Security**: Secure token generation using Python's secrets module for unique redemption links

## Data Storage Solutions
- **Database**: SQLAlchemy with support for both SQLite (development) and PostgreSQL (production)
- **Schema Design**: Three main entities - Products (prizes), RedemptionLinks (unique redemption tokens), and UserDetails (customer information)
- **Connection Management**: Database connection pooling with automatic reconnection handling

## Authentication and Authorization
- **Token-based Access**: Unique redemption tokens for prize claiming without traditional user accounts
- **Session Security**: Environment-based secret keys with development fallbacks
- **Link Security**: One-time use redemption links with timestamp tracking

## External Dependencies

### Third-party Services
- **CDN Resources**: Bootstrap 5, Font Awesome icons, Canvas Confetti library served via CDN
- **Image Hosting**: Via.assets.so for dynamic product image generation with customizable text and colors

### Database Integration
- **SQLAlchemy ORM**: Database abstraction layer supporting multiple database backends
- **Migration Support**: Built-in table creation and schema management through Flask-SQLAlchemy

### Production Considerations
- **Proxy Support**: Werkzeug ProxyFix middleware for deployment behind reverse proxies
- **Environment Configuration**: Database URLs and session secrets configurable via environment variables
- **Logging**: Comprehensive logging setup for debugging and monitoring