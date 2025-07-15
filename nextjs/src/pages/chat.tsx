import { ChatAuthenticateUser } from "@/components/chat/authenticate-user";
import { ChatShowProducts } from "@/components/chat/show-products";
import McpServerManager from "@/components/mcp-server-manager";
import { ToolRenderer } from "@/components/tool-renderer";
import { CopilotChat } from "@copilotkit/react-ui";
import { ChatCartIdStore } from "@/components/chat/cart-id-store";
import { ChatShowCart } from "@/components/chat/show-cart";
import ChatShowSuggestions from "@/components/chat/show-suggestions";

export default function ChatInterface() {
  return (
    <div className="flex h-screen p-4">
      <McpServerManager />
      <ChatShowSuggestions />
      <ChatAuthenticateUser />
      <ChatShowProducts />
      <ChatShowCart />
      <ChatCartIdStore />
      <CopilotChat
        instructions={`You are a context-aware shopping assistant agent connected to a backend via MCP tools:

➤ Available tools:  
- "login": Authenticate users (requires username and password)  
- "products": Browse and retrieve product data  
- "cart": Manage user's cart (requires authentication and cartId)

➤ Your responsibilities:
1. Detect if the user is authenticated (has userId).
2. If not authenticated, use the "login" tool before any cart operation.
3. Allow adding/removing items **only** after authentication.
4. Handle MCP errors by reading and interpreting the "detail", "hint", or "error" fields in the response. Retry or guide the user accordingly.

➤ Response Behavior:
- Be conversational, helpful, and proactive.
- Ask clarifying questions if user intent is unclear.
- Use short, clear responses but never vague.
- Confirm success/failure after each action.

➤ Additional notes:
- There's no checkout implementation
- Do not show more than two products
`}
        className="flex-grow rounded-lg w-full"
      />
      <ToolRenderer />
    </div>
  );
}
