import { useCopilotAction } from "@copilotkit/react-core";
import { useCopilotReadable } from "@copilotkit/react-core";
import { useCallback, useState } from "react";
import { useChatStore } from "./state";

export function ChatAuthenticateUser() {
  const { userId, username, setUsername, setUserId } = useChatStore();

  const [formUsername, setFormUsername] = useState("");
  const [formPassword, setFormPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const setUserData = useCallback((userId: string, username: string) => {
    setUserId(userId);
    setUsername(username);
  }, []);

  useCopilotReadable({
    description:
      "The current user's id. This is null if the user is not authenticated.",
    value: userId,
  });

  useCopilotReadable({
    description:
      "The current user's username. This is null if the user is not authenticated.",
    value: username,
  });

  useCopilotAction({
    name: "authenticateUser",
    description:
      "Authenticates the user. Show this when the user needs to log in or asks to log in.",
    renderAndWaitForResponse: ({ respond, status }) => {
      // Handle successful authentication
      const handleAuthentication = () => {
        setIsLoading(true);

        // Mock authentication delay
        setTimeout(() => {
          setUserData("1", formUsername);

          // Send response back to the action
          respond?.({
            username: formUsername,
            userId: "1",
          });

          setIsLoading(false);
        }, 1000);
      };

      if (status === "inProgress") {
        return (
          <div className="p-4 max-w-sm mx-auto rounded-lg border border-gray-200 shadow-sm bg-white">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Loading...
            </h3>
          </div>
        );
      }

      if (status === "executing") {
        return (
          <div className="p-4 max-w-sm mx-auto rounded-lg border border-gray-200 shadow-sm bg-white">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Login Required
            </h3>

            {isLoading ? (
              <div className="flex items-center justify-center py-4">
                <div className="animate-spin rounded-full h-6 w-6 border-2 border-blue-500 border-t-transparent"></div>
                <span className="ml-2 text-sm text-gray-600">
                  Authenticating...
                </span>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="space-y-2">
                  <label
                    htmlFor="username"
                    className="text-sm font-medium text-gray-700"
                  >
                    Username
                  </label>
                  <input
                    id="username"
                    type="text"
                    value={formUsername}
                    onChange={(e) => setFormUsername(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm text-black"
                    placeholder="Enter your username"
                  />
                </div>

                <div className="space-y-2">
                  <label
                    htmlFor="password"
                    className="text-sm font-medium text-gray-700"
                  >
                    Password
                  </label>
                  <input
                    id="password"
                    type="password"
                    value={formPassword}
                    onChange={(e) => setFormPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm text-black"
                    placeholder="Enter your password"
                  />
                </div>

                <button
                  onClick={handleAuthentication}
                  disabled={!formUsername || !formPassword}
                  className={`w-full py-2 px-4 rounded-md text-white font-medium text-sm 
                    ${
                      !formUsername || !formPassword
                        ? "bg-blue-300 cursor-not-allowed"
                        : "bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    }
                  `}
                >
                  Login
                </button>

                <div className="text-xs text-gray-500 text-center mt-2">
                  Enter any username/password for demo
                </div>
              </div>
            )}
          </div>
        );
      }

      return (
        <div className="p-4 max-w-sm mx-auto rounded-lg border border-green-200 shadow-sm bg-green-50">
          <div className="flex items-center">
            <svg
              className="w-5 h-5 text-green-600"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            <span className="ml-2 text-sm font-medium text-green-800">
              Logged in as <span className="font-semibold">{username}</span>
            </span>
          </div>
        </div>
      );
    },
  });

  return null;
}
