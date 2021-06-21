package tasks

import (
    "errors"
    "fmt"
    "log"
    "strings"

    "github.com/earaujoassis/watchman-bot/internal/communicator"
    "github.com/earaujoassis/watchman-bot/internal/utils"
)

// Integration handles tasks performed within a CI environment
func Integration(command string, data utils.H) (utils.H, error) {
    var result utils.H
    var err error = nil

    switch command {
    case GitOpsUpdater:
        managedProject := data["managed_project"].(string)
        commitHash := data["commit_hash"].(string)
        _, err := communicator.ActionCreateRequestor(
            utils.H{
                "type": strings.Replace(GitOpsUpdater, "-", "_", 2),
                "description": fmt.Sprintf("bot: updated %s to %s", managedProject, commitHash),
                "application_id": data["application_id"].(string),
                "managed_realm": data["managed_realm"].(string),
                "managed_project": managedProject,
                "commit_hash": commitHash,
            },
        )
        if err != nil {
            log.Fatal(fmt.Sprintf("Error: %s\n", err))
        }
    default:
        result = utils.H{
            "Message": utils.InvalidCommand,
        }
        err = errors.New(utils.InvalidCommand)
    }
    return result, err
}
