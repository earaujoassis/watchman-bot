package utils

import (
    "fmt"
    "log"
    "os"
)

const (
    ClientKeyEnvVar    string = "WATCHMAN_BOT_CLIENT_KEY"
    ClientSecretEnvVar string = "WATCHMAN_BOT_CLIENT_SECRET"
    BaseUrlEnvVar      string = "WATCHMAN_BOT_BASE_URL"
)

func SanityChecker() {
    var errorMessage string = ""

    clientKey := os.Getenv(ClientKeyEnvVar)
    clientSecret := os.Getenv(ClientSecretEnvVar)
    baseUrl := os.Getenv(BaseUrlEnvVar)

    if clientKey == "" {
        errorMessage = fmt.Sprintf("%s env var cannot be empty\n", ClientKeyEnvVar)
    }
    if clientSecret == "" {
        errorMessage = fmt.Sprintf("%s%s env var cannot be empty\n", errorMessage, ClientKeyEnvVar)
    }
    if baseUrl == "" {
        errorMessage = fmt.Sprintf("%s%s env var cannot be empty\n", errorMessage, BaseUrlEnvVar)
    }

    if errorMessage != "" {
        log.Fatal(errorMessage)
    }
}
