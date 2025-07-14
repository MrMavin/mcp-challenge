# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack AI-powered e-commerce application with MCP (Model Context Protocol) integration. The system consists of:

- **FastAPI Backend** (`/fastapi/`): RESTful API server with MCP integration for AI agents
- **Next.js Frontend** (`/nextjs/`): React-based chat interface using CopilotKit
- **External Data**: Uses fakestoreapi.com as the product/cart data source

## Development Commands

### Backend (FastAPI)
```bash
# Setup and dependencies
cp .env.example .env
poetry install

# Database (PostgreSQL 16.3)
just up                    # Start Docker containers
just kill                  # Stop containers

# Development server
just run                   # Start with default config
just run --log-config logging.ini  # With custom logging

# Code quality
just lint                  # Format with ruff and fix issues
just ruff                  # Run linter only

# Docker
docker-compose up -d       # Development environment
docker-compose -f docker-compose.prod.yml up -d --build  # Production
```

### Frontend (Next.js)
```bash
# Setup and development
npm install
npm run dev               # Development server with Turbopack
npm run build            # Production build
npm run start            # Production server
npm run lint             # ESLint
```

## Architecture

### Data Flow
1. User interacts with Next.js chat interface (`/nextjs/src/pages/chat.tsx`)
2. CopilotKit processes AI requests via `/nextjs/src/pages/api/copilotkit.ts`
3. MCP client (`/nextjs/src/lib/mcp-client.ts`) communicates with FastAPI MCP server
4. FastAPI routes (`/fastapi/src/routes/`) call service layer (`/fastapi/src/services/`)
5. Services make HTTP requests to fakestoreapi.com
6. Response flows back through the same chain

### Key Components

**Backend Structure:**
- `src/routes/`: API endpoints with manual validation (no Pydantic models)
- `src/services/`: Business logic layer that proxies to fakestoreapi.com
- `src/mcp/`: MCP server integration for AI tool communication
- `src/main.py`: FastAPI app configuration and MCP setup

**Frontend Structure:**
- `src/pages/chat.tsx`: Main chat interface with CopilotKit integration
- `src/components/chat/`: Chat-specific components including MCP tool renderers
- `src/lib/mcp-client.ts`: Custom MCP client for tool communication
- `src/pages/api/copilotkit.ts`: CopilotKit runtime configuration

### API Patterns

**Cart Management:**
- `POST /carts/manage-cart`: Unified endpoint for create/update operations
  - If `cartId` provided: updates existing cart
  - If no `cartId`: creates new cart
- `POST /carts/get-cart`: Get cart by ID
- `POST /carts/delete-cart`: Delete cart by ID

**Product Management:**
- `GET /products`: Get all products
- `POST /products/single-product`: Get single product by ID

**Validation:**
- **Manual validation** (no Pydantic) with detailed error messages
- **Quantity support** in cart products for proper e-commerce behavior
- **Comprehensive error handling** with specific field-level feedback

### MCP Integration

The system implements Model Context Protocol for AI agent interaction:

**MCP Server** (`/fastapi/src/mcp/`):
- Exposes cart and product operations as tools
- Provides structured responses for AI consumption
- Handles authentication and user context

**MCP Client** (`/nextjs/src/lib/mcp-client.ts`):
- Connects Next.js frontend to FastAPI MCP server
- Manages tool discovery and execution
- Integrates with CopilotKit for seamless AI interaction

**Tool Rendering** (`/nextjs/src/components/chat/`):
- Custom components for displaying MCP tool results
- `show-products.tsx`: Product grid with images
- `authenticate-user.tsx`: User authentication flow

## Important Implementation Details

### Cart Quantity Handling
The fakestoreapi.com doesn't properly handle quantities in cart updates. This system:
- Accepts quantity in product objects during cart operations
- Validates quantity as positive integers
- Passes quantity through to maintain e-commerce semantics

### Authentication
- **Mock authentication** for demo purposes
- User context managed through CopilotKit readable state
- No persistent authentication (uses fakestoreapi.com demo data)

### Error Handling
- **Detailed validation messages** instead of generic Pydantic errors
- **Specific field-level errors** (e.g., "Product quantity at index 2 must be at least 1")
- **HTTP status codes** properly mapped to error types

### Development Environment
- **PostgreSQL 16.3** via Docker (configured but not actively used)
- **Async HTTP clients** for external API calls
- **Structured logging** with different levels for development/production
- **Hot reload** for both frontend and backend development

## Testing

No formal test framework is currently set up. Manual testing available via:
- REST client files in `/fastapi/src/rest/`
- FastAPI automatic OpenAPI documentation
- Frontend chat interface testing

## Production Considerations

- **Docker containers** for both services
- **Gunicorn** with dynamic worker configuration
- **Sentry integration** for error monitoring
- **JSON logging** for production environments
- **Non-root user** in Docker containers for security

## Common Development Patterns

When making changes:

1. **API Changes**: Update routes → services → test via REST files
2. **Frontend Changes**: Components → test via chat interface
3. **MCP Changes**: Update both server tools and client integration
4. **Validation**: Use manual validation functions with detailed error messages
5. **Cart Operations**: Use the unified `/manage-cart` endpoint for all create/update operations

The system is designed to be MCP-first, so all changes should consider how they affect AI agent interaction and tool usability.