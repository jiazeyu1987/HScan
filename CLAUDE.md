# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**全国医院官网扫描与招投标监控系统** (National Hospital Website Scanning and Bidding Monitoring System) - A full-stack hospital information monitoring and bidding tracking system.

- **Frontend**: React 18.3 + TypeScript + Ant Design + Tailwind CSS
- **Backend**: Flask 2.3.3 + SQLAlchemy + APScheduler
- **Database**: SQLite (development) with PostgreSQL upgrade path
- **Status**: Production-ready, complete system

## Development Commands

### Backend Development (Flask)

```bash
cd backend

# Start development server
python run.py                    # Starts Flask app on http://127.0.0.1:5000

# Database operations
python run.py --init-db         # Initialize database with seed data
pip install -r requirements.txt # Install Python dependencies

# Testing
pytest                           # Run unit tests
pytest --cov                     # Run tests with coverage
```

### Frontend Development (React + Vite)

```bash
cd hospital-monitor-antd

# Start development server (installs dependencies automatically)
pnpm dev                        # Starts Vite dev server on http://localhost:5174

# Build commands
pnpm build                      # Standard build
pnpm build:prod                 # Production build with optimizations
pnpm preview                    # Preview production build

# Code quality
pnpm lint                       # Run ESLint
pnpm install-deps              # Install dependencies only
pnpm clean                     # Clean node_modules and cache
```

### System Operations

```bash
# Complete system restart (kills existing processes and restarts both services)
./restart_system.sh

# API testing and validation
python api_test.py              # Test API connectivity and data integrity
```

## Architecture Overview

### High-Level System Architecture

```
Frontend (React + TypeScript + Ant Design)
         ↕ REST API (http://localhost:5000/api/v1)
Backend (Flask + SQLAlchemy + APScheduler)
         ↕ SQLAlchemy ORM
Database (SQLite → PostgreSQL upgrade path)
         ↕ External APIs
External Data Sources (Search Engines, Government Data, Hospital Websites)
```

### Backend Architecture

**Core Structure**:
- **API Layer** (`app/api/`): 8 modules with 34 REST endpoints
  - `hospitals.py` - Hospital management API (10,724 lines)
  - `regions.py` - Administrative regions API (10,987 lines)
  - `tenders.py` - Bidding records API (8,192 lines)
  - `crawler.py` - Web crawler control API (4,675 lines)
  - `settings.py` - System configuration API (9,661 lines)
  - `exports.py` - Data export API (611 lines)
  - `health.py` - Health check API (781 lines)

- **Services Layer** (`app/services/`): Business logic separation
  - `hospital_search.py` - Multi-channel hospital search
  - `tender_extractor.py` - Bidding information extraction
  - `content_deduplicator.py` - Content deduplication (SHA256 + Bloom filters)
  - `crawler_service.py` - Web crawler engine
  - `task_scheduler.py` - APScheduler-based task orchestration
  - `crawler_manager.py` - Crawler orchestration and management

- **Data Models** (`app/models/`): SQLAlchemy models
  - 6 core tables: `regions`, `hospitals`, `tender_records`, `scan_history`, `settings`, `crawler_logs`
  - 3 auxiliary tables: `hospital_alias`, `tender_raw_html`, `crawler_errors`
  - Comprehensive indexing strategy

### Frontend Architecture

**Core Structure**:
- **Pages** (`src/pages/`): 11 feature-rich pages
  - `Dashboard.tsx` - Main analytics dashboard
  - `HospitalsPage.tsx` - Hospital management interface
  - `TendersPage.tsx` - Bidding records management
  - `CrawlerDashboard.tsx` - Web crawler control panel
  - `Settings.tsx` - System configuration interface

- **State Management**: Zustand store (lightweight alternative to Redux)
- **API Client**: Axios with interceptors for error handling and authentication
- **Component Library**: Reusable components including `MainLayout`, `RegionTree`, `ErrorBoundary`

### Key Business Features

1. **Administrative Region Hierarchy**: 4-level system (Province → City → County → Township)
2. **Multi-Channel Hospital Discovery**: DuckDuckGo, Baidu, Google search integration
3. **Automated Web Scraping**: Playwright-based crawler with configurable intervals
4. **Content Deduplication**: SHA256 hashing + Bloom filters for efficiency
5. **Real-time Monitoring**: APScheduler for automated scanning (6 hours for tenders, 24 hours for hospitals)
6. **Excel Export**: Advanced formatting with openpyxl and xlsxwriter

## Configuration Management

### Environment Configuration
- **Development**: SQLite database, debug mode enabled
- **Production**: PostgreSQL support, Redis caching, structured logging
- **Testing**: Separate test database configuration

### Key Configuration Files
- `backend/config.py` - Flask configuration with environment-based settings
- `hospital-monitor-antd/vite.config.ts` - Vite build configuration with React plugin
- `hospital-monitor-antd/tailwind.config.js` - Tailwind CSS configuration

### Database Setup
```bash
# Initialize database with seed data
cd backend && python run.py --init-db

# Database upgrade path (production)
# Set DATABASE_URL=postgresql://username:password@localhost:5432/hospital_monitor
```

## Testing Strategy

### Backend Testing
- **Framework**: Pytest with Flask-Testing extension
- **Coverage**: pytest-cov for code coverage reporting
- **API Testing**: Comprehensive test suite in `api_test.py`

### Frontend Testing
- **Linting**: ESLint with React-specific rules
- **Type Checking**: TypeScript strict mode enabled
- **Build Validation**: Vite build process validation

## Development Workflow

### Getting Started

1. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python run.py --init-db  # First time only
   python run.py            # Start development server
   ```

2. **Frontend Setup**:
   ```bash
   cd hospital-monitor-antd
   pnpm dev  # Automatically installs dependencies and starts dev server
   ```

3. **System Validation**:
   ```bash
   python api_test.py  # Verify API connectivity and data integrity
   ```

### Common Development Patterns

- **API Endpoints**: Follow RESTful conventions with `/api/v1/` prefix
- **Error Handling**: Structured logging with rotating file handlers
- **Database Operations**: Use SQLAlchemy models with proper session management
- **Frontend State**: Zustand stores for global state, local state for component-specific data
- **Styling**: Ant Design components with Tailwind CSS for custom styles

### Security Considerations

- CORS configuration for cross-origin requests
- SQL injection prevention through SQLAlchemy ORM
- Input validation on all API endpoints
- Secure configuration management with environment variables

## Performance Optimizations

- **Caching**: Redis integration for frequently accessed data
- **Database Indexing**: Comprehensive indexing strategy on all tables
- **Async Processing**: Background task scheduling with APScheduler
- **Frontend Optimization**: Vite build with code splitting and tree shaking

## Deployment Notes

- **Production Ready**: Comprehensive error handling and logging
- **Scalability**: Modular architecture supports horizontal scaling
- **Monitoring**: Structured logging with prometheus metrics
- **Database**: SQLite for development, PostgreSQL upgrade path for production