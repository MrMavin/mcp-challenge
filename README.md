# Interview Challenge - MCP Server Assignment

## Project Overview

This project is an AI shop assistant application PoC. The application integrates with CopilotKit to provide AI-powered suggestions and interactions (MCP client) and FastAPI-MCP to provide backend services (MCP server).

## Running the project

### FastAPI

```bash
cd fastapi
cp .env.example .env
poetry install --no-root
just run
```

### Next.js

```bash
cd nextjs
cp .env.example .env
# set OPENAI_API_KEY
yarn install
yarn dev
```

### MCP Client

```
http://localhost:3000/chat
```

## Project Structure

### Backend (FastAPI) - `./fastapi`

The backend is built with FastAPI and implements an MCP server with FastAPI-MCP for AI-backend communication.

#### Files & Structure

- `./fastapi/src/main.py` - Main application file
- `./fastapi/routes` - Project routes
- `./fastapi/services` - Project services
- `./fastapi/validation` - Custom LLM friendly validation
- `./fastapi/middleware` - Middleware for authentication
- `./fastapi/data` - FakeStore API reference JSON
- `./fastapi/utils` - LLM friendly exception management
- `./fastapi/rest` - REST testing

#### Key Features

##### FakeStoreAPI wrapper with smart endpoints

As FakeStoreAPI has misalignments between request expectations and actual requirements, which make the LLM to send invalid requests and going crazy, we implemented a wrapper with smart endpoints to manage the cart.

##### Custom validation for routes

By default pydantic validation is not LLM friendly, so we implemented custom validation for routes. The package `fastapi-mcp` considers pydantic as the main source for validation, which actually makes the package to be reconsidered for future projects.

##### REST testing

We implemented a REST testing module to manually test the API endpoints with validation and successful requests, speeding up the development.


### Frontend (Next.js) - `./nextjs`

The frontend is built with Next.js, React, and TypeScript, featuring a conversational AI interface powered by CopilotKit.

#### Files & Structure

- `./nextjs/src/pages/chat.tsx` - Main chat page implementing CopilotKit's conversational interface
- `./nextjs/src/lib/mcp-client.ts` - Custom MCP client implementation for communicating with FastAPI backend
- `./nextjs/src/components/chat/` - Chat components (state management, UI elements, suggestions)


#### Key Features

##### Pages router vs App router

The project uses Next.JS Pages Router which is considered to be a more lightweight routing system suitable for this project's scope. The App Router requires more maintenance and abstractions to be maintained.

##### CopilotKit

CopilotKit has been chosen for its simplicity in creating a chatbot interface.

After some tests and going deeper into the documentation, I wouldn't consider CopilotKit for future projects at this stage of development.

As of today there isn't a way to implement an observability system out of the box, which means that we can't track the LLM's usage and costs.

There's also a [bug in the suggestions system](https://github.com/CopilotKit/CopilotKit/issues/2157) that makes it break the user experience.

Additionally, a great part of the documentation is broken and makes it difficult to find what we need.

Finally, they push really hard into their SaaS, making CopilotKit being really hard to use when you decide to self-host, resulting in a huge vendor lock-in that should be carefully considered.

##### OpenAI Model

When choosing the model, I considered that going with `gpt-4.1` was a good balance between cost and performance.

I didn't want to get a higher performing model (e.g. Claude Opus) to be forced into paying more attention on prompt, make sure that a "dumber" solution would do the job anyway and that it would be more cost-effective.

## Known limitations

1. **Mocked Authentication**: Frontend authentication is mocked for demo purposes only.
2. **FakeStore API**: External API limitations led to internal "smart" capability implementation
3. **Cost Tracking**: No built-in token usage monitoring
4. **Vendor Lock-in**: Heavy dependency on CopilotKit ecosystem
5. **CopilotKit Suggestions Bug**: User experience is broken due to this.
6. **Prompt Engineering**: Extensive and long-term prompt engineering with observability is required to iterate on user experiences and to improve them.
7. **MCP Server**: MCP itself is a great framework, but I wouldn't consider it for critical applications that needs write endpoints. I would consider a full agentic backend approach which will have a better routing and different agents for each operation. Reducing the amount of context needed and increasing precision.