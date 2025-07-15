import { useCopilotAction } from "@copilotkit/react-core";

/**
 * Cart product interface matching the structure returned from fakestoreapi.com
 * This only contains productId and quantity, not full product details
 */
interface CartItem {
  productId: number;
  quantity: number;
}

/**
 * Full product interface for enriched cart items
 */
interface Product {
  id: number;
  title: string;
  price: number;
  description: string;
  category: string;
  image: string;
}

/**
 * Cart interface matching the structure returned from fakestoreapi.com
 */
interface Cart {
  id: number;
  userId: number;
  products: CartItem[];
  date?: string;
}

/**
 * Enriched cart item with full product details
 */
interface EnrichedCartItem extends Product {
  quantity: number;
}

export function ChatShowCart() {
  useCopilotAction({
    name: "showCart",
    description:
      "Display cart contents with items, quantities, and total calculation. Use this after fetching a cart and enriching it with product details.",
    parameters: [
      {
        name: "cart",
        description:
          "Cart object in JSON format. Should contain id, userId, products array with productId and quantity.",
        type: "string",
        required: true,
      },
      {
        name: "products",
        description:
          "Array of full product objects corresponding to the cart items. Each product should have id, title, price, description, category, and image.",
        type: "string",
        required: true,
      },
    ],
    render: ({ args, status }) => {
      const { cart, products } = args;
      let parsedCart: Cart | null = null;
      let parsedProducts: Product[] = [];
      let enrichedItems: EnrichedCartItem[] = [];
      let error = "";

      if (status === "inProgress") {
        return (
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4 max-w-2xl mx-auto">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">
              Shopping Cart
            </h2>
            <p className="text-black">Loading cart...</p>
          </div>
        );
      }

      try {
        // Parse cart
        if (typeof cart === "string") {
          parsedCart = JSON.parse(cart);
        } else if (typeof cart === "object" && cart !== null) {
          parsedCart = cart;
        }

        // Parse products
        if (typeof products === "string") {
          parsedProducts = JSON.parse(products);
          if (!Array.isArray(parsedProducts)) {
            parsedProducts = [parsedProducts];
          }
        } else if (Array.isArray(products)) {
          parsedProducts = products;
        }

        // Enrich cart items with full product details
        if (parsedCart?.products) {
          enrichedItems = parsedCart.products.map((cartItem: CartItem) => {
            const product = parsedProducts.find(
              (p) => p.id === cartItem.productId
            );
            if (product) {
              return {
                ...product,
                quantity: cartItem.quantity,
              };
            }
            // Fallback for missing product details
            return {
              id: cartItem.productId,
              title: `Product ${cartItem.productId}`,
              price: 0,
              description: "Product details not available",
              category: "Unknown",
              image: "",
              quantity: cartItem.quantity,
            };
          });
        }
      } catch (e: unknown) {
        if (e instanceof Error) {
          error = `Error parsing cart or products: ${e.message}`;
        } else {
          error = "Error parsing cart or products: Unknown error";
        }
        console.error(error);
      }

      // Calculate total
      const calculateTotal = (items: EnrichedCartItem[]): number => {
        return items.reduce((total, item) => {
          return total + item.price * item.quantity;
        }, 0);
      };

      const total = calculateTotal(enrichedItems);

      return (
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4 max-w-2xl mx-auto">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">
            Shopping Cart
          </h2>

          {error && (
            <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
              {error}
            </div>
          )}

          {!parsedCart && !error && (
            <p className="text-gray-500 italic">No cart data available</p>
          )}

          {parsedCart && (
            <>
              <div className="mb-4 text-sm text-gray-600">
                Cart ID: {parsedCart.id} | User ID: {parsedCart.userId}
              </div>

              {enrichedItems.length === 0 ? (
                <p className="text-gray-500 italic">Your cart is empty</p>
              ) : (
                <>
                  <div className="space-y-3 mb-4">
                    {enrichedItems.map((item, index) => (
                      <div
                        key={item.id || index}
                        className="border rounded-md p-3 flex gap-4"
                      >
                        {item.image && (
                          <div className="flex-shrink-0">
                            <img
                              src={item.image}
                              alt={item.title}
                              className="h-16 w-16 object-contain"
                              onError={(e) => {
                                e.currentTarget.src =
                                  "https://placehold.co/64x64?text=No+Image";
                                e.currentTarget.alt = "Image not available";
                              }}
                            />
                          </div>
                        )}
                        <div className="flex-1">
                          <h3 className="font-medium text-gray-900">
                            {item.title}
                          </h3>
                          <p className="text-sm text-gray-500 line-clamp-2 mt-1">
                            {item.description}
                          </p>
                          <div className="mt-2 flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className="text-sm text-gray-600">
                                Quantity: {item.quantity}
                              </span>
                              <span className="text-xs px-2 py-1 bg-gray-100 text-black rounded-full">
                                {item.category}
                              </span>
                            </div>
                            <div className="text-right">
                              <div className="text-sm text-gray-600">
                                $
                                {typeof item.price === "number"
                                  ? item.price.toFixed(2)
                                  : item.price}{" "}
                                each
                              </div>
                              <div className="text-lg font-bold text-blue-600">
                                ${(item.price * item.quantity).toFixed(2)}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Cart Total */}
                  <div className="border-t pt-4">
                    <div className="flex justify-between items-center">
                      <span className="text-lg font-semibold text-gray-900">
                        Total (
                        {enrichedItems.reduce(
                          (sum, item) => sum + item.quantity,
                          0
                        )}{" "}
                        items):
                      </span>
                      <span className="text-2xl font-bold text-green-600">
                        ${total.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </>
              )}
            </>
          )}
        </div>
      );
    },
  });

  return null;
}
