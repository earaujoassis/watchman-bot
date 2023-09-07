package communicator

import (
	"encoding/base64"

	"github.com/earaujoassis/watchman-bot/internal/config"
)

func authorizationBearer() string {
	cfg := config.GetConfig()
	key := cfg.ClientKey
	secret := cfg.ClientSecret
	authorization := key + ":" + secret
	encodedAuth := base64.StdEncoding.EncodeToString([]byte(authorization))
	return encodedAuth
}
