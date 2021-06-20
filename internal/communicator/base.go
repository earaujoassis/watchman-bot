package communicator

import (
    "os"
    "encoding/base64"

    "github.com/earaujoassis/watchman-bot/internal/utils"
)

func baseUrl() string {
    utils.SanityChecker()
    return os.Getenv(utils.BaseUrlEnvVar)
}

func authorizationBearer() string {
    utils.SanityChecker()
    key := os.Getenv(utils.ClientKeyEnvVar)
    secret := os.Getenv(utils.ClientSecretEnvVar)
    authorization := key + ":" + secret
    encodedAuth := base64.StdEncoding.EncodeToString([]byte(authorization))
    return encodedAuth
}
