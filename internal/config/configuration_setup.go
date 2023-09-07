package config

import (
	"github.com/caarlos0/env/v9"
	"gopkg.in/ini.v1"
)

type Http struct {
	VerifySsl       bool   `ini:"verify_ssl" default:"true" envDefault:"true"`
	CertificatePath string `ini:"certificate_path" envDefault:""`
}

type Config struct {
	Http         Http   `ini:"http"`
	BaseUrl      string `ini:"base_url"      env:"WATCHMAN_BOT_BASE_URL"`
	ClientKey    string `ini:"client_key"    env:"WATCHMAN_BOT_CLIENT_KEY"`
	ClientSecret string `ini:"client_secret" env:"WATCHMAN_BOT_CLIENT_SECRET"`
}

var globalConfig *Config

func GetConfig() *Config {
	return globalConfig
}

func LoadConfig() {
	var cfg Config = Config{Http: Http{}}

	// 1. attempt to load configuration from .watchmanbotrc
	inidata, err := ini.Load(".watchmanbotrc")
	if err == nil {
		err = inidata.MapTo(&cfg)
	}

	// 2. attempt to load configuration from environment variables
	if err != nil {
		opts := env.Options{RequiredIfNoDef: true}
		if err = env.ParseWithOptions(&cfg, opts); err != nil {
			panic("No configuration option available")
		}
	}

	globalConfig = &cfg
}
