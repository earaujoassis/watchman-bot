package main

import (
	"os"

	"github.com/urfave/cli/v2"

	"github.com/earaujoassis/watchman-bot/internal/tasks"
	"github.com/earaujoassis/watchman-bot/internal/utils"
	"github.com/earaujoassis/watchman-bot/internal/config"
)

func main() {
	config.LoadConfig()
	app := cli.NewApp()
	app.Name = "bot"
	app.Usage = "Watchman helps to keep track of automating services; a tiny bot"
	app.EnableBashCompletion = true
	app.Commands = []*cli.Command{
		{
			Name:  "ci",
			Usage: "Tasks to perform from a CI environment",
			Subcommands: []*cli.Command{
				{
					Name:  "git-ops-updater",
					Usage: "Create a new client application",
					Flags: []cli.Flag{
						&cli.StringFlag{
							Name:     "application",
							Usage:    "Application UUID to perform action",
							Required: true,
						},
						&cli.StringFlag{
							Name:     "realm",
							Usage:    "Project's top-level realm/folder name",
							Required: true,
						},
						&cli.StringFlag{
							Name:     "project",
							Usage:    "Project's folder name",
							Required: true,
						},
						&cli.StringFlag{
							Name:     "commit",
							Usage:    "Git commit-hash to update",
							Required: true,
						},
					},
					Action: func(c *cli.Context) error {
						config.LoadConfig()
						tasks.Integration(
							tasks.GitOpsUpdater,
							utils.H{
								"application_id":  c.String("application"),
								"managed_realm":   c.String("realm"),
								"managed_project": c.String("project"),
								"commit_hash":     c.String("commit"),
							},
						)
						return nil
					},
				},
			},
		},
	}

	app.Run(os.Args)
}
