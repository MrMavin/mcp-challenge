import { useCopilotAction } from "@copilotkit/react-core";

/**
 * Product interface matching the structure returned from the API
 * We define a strict interface rather than using any/unknown types
 * to ensure type safety and better code completion
 */
interface Product {
  id: number;
  title: string;
  price: number;
  description: string;
  category: string;
  image: string;
}

export function ChatShowProducts() {
  useCopilotAction({
    name: "displayProductResults",
    description: "Show products after MCP call, then stop.",
    parameters: [
      {
        name: "products",
        description: "List of products to show",
        type: "string",
        required: true,
      },
    ],
    render: (props) => {
      // We use ActionRenderProps type from CopilotKit for proper typing
      // This approach avoids TypeScript errors while still maintaining type checking
      // We didn't use a generic parameter since the parameters are already defined in the args array

      // Extract products from arguments
      const { products } = props.args;
      let parsedProducts: Product[] = [];
      let error = ""; // Track any parsing errors to display to user

      // Parse the products string which should be JSON
      try {
        if (typeof products === "string") {
          parsedProducts = JSON.parse(products);
          if (!Array.isArray(parsedProducts)) {
            parsedProducts = [parsedProducts]; // Handle single product case
          }
        } else if (Array.isArray(products)) {
          // If it's already an array, use it directly
          parsedProducts = products;
        }
      } catch (e: unknown) {
        // Handle the error with proper type checking
        if (e instanceof Error) {
          error = `Error parsing products: ${e.message}`;
        } else {
          error = "Error parsing products: Unknown error";
        }
        console.error(error);
      }

      if (props.status === "inProgress" || props.status === "executing") {
        return (
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4 max-w-xl mx-auto">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">
              Products
            </h2>
            <p className="text-black">Loading products...</p>
          </div>
        );
      }

      return (
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4 max-w-xl mx-auto">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Products</h2>

          {error && (
            <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
              {error}
            </div>
          )}

          {parsedProducts.length === 0 && !error && (
            <p className="text-gray-500 italic">No products available</p>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {parsedProducts.map((product, index) => (
              <div
                key={product.id || index}
                className="border rounded-md p-3 flex flex-col"
              >
                {product.image && (
                  <div className="mb-3 flex justify-center">
                    <img
                      src={product.image}
                      alt={product.title}
                      className="h-32 object-contain"
                      onError={(e) => {
                        // Replace broken image with a placeholder
                        e.currentTarget.src =
                          "https://placehold.co/200x150?text=No+Image";
                        e.currentTarget.alt = "Image not available";
                      }}
                    />
                  </div>
                )}
                <h3 className="font-medium text-gray-900">{product.title}</h3>
                <p className="text-sm text-gray-500 line-clamp-2 mt-1">
                  {product.description}
                </p>
                <div className="mt-2 flex items-center justify-between">
                  <span className="text-lg font-bold text-blue-600">
                    $
                    {typeof product.price === "number"
                      ? product.price.toFixed(2)
                      : product.price}
                  </span>
                  <span className="text-xs px-2 py-1 bg-gray-100 text-black rounded-full">
                    {product.category}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    },
  });

  return null;
}
