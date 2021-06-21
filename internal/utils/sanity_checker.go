package utils

import (
    "fmt"
    "log"
    "os"
)

const (
    // ClientKeyEnvVar is used to authenticate a robot against the watchman server
    ClientKeyEnvVar    string = "WATCHMAN_BOT_CLIENT_KEY"
    // ClientSecretEnvVar is used to authenticate a robot against the watchman server
    ClientSecretEnvVar string = "WATCHMAN_BOT_CLIENT_SECRET"
    // BaseURLEnvVar represents the URL for the watchman server
    BaseURLEnvVar      string = "WATCHMAN_BOT_BASE_URL"
)

// SanityChecker checks if mandatory env vars are available
func SanityChecker() {
    var errorMessage string = ""

    clientKey := os.Getenv(ClientKeyEnvVar)
    clientSecret := os.Getenv(ClientSecretEnvVar)
    baseURL := os.Getenv(BaseURLEnvVar)

    if clientKey == "" {
        errorMessage = fmt.Sprintf("%s env var cannot be empty\n", ClientKeyEnvVar)
    }
    if clientSecret == "" {
        errorMessage = fmt.Sprintf("%s%s env var cannot be empty\n", errorMessage, ClientKeyEnvVar)
    }
    if baseURL == "" {
        errorMessage = fmt.Sprintf("%s%s env var cannot be empty\n", errorMessage, BaseURLEnvVar)
    }

    if errorMessage != "" {
        log.Fatal(errorMessage)
    }
}
