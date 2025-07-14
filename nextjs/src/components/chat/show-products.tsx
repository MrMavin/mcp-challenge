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
    name: "showProducts",
    description:
      "Display products from the e-commerce store in a beautiful grid layout. Use this after fetching products from the MCP tool to show them to the user.",
    parameters: [
      {
        name: "products",
        description:
          "List of products to show in JSON format. Should be an array of product objects with id, title, price, description, category, and image fields.",
        type: "string",
        required: true,
      },
    ],
    render: ({ args, status }) => {
      const { products } = args;
      let parsedProducts: Product[] = [];
      let error = "";

      if (status === "inProgress") {
        return (
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4 max-w-xl mx-auto">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">
              Products
            </h2>
            <p className="text-black">Loading products...</p>
          </div>
        );
      }

      try {
        if (typeof products === "string") {
          parsedProducts = JSON.parse(products);
          if (!Array.isArray(parsedProducts)) {
            parsedProducts = [parsedProducts];
          }
        } else if (Array.isArray(products)) {
          parsedProducts = products;
        }
      } catch (e: unknown) {
        if (e instanceof Error) {
          error = `Error parsing products: ${e.message}`;
        } else {
          error = "Error parsing products: Unknown error";
        }
        console.error(error);
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
