package communicator

/*
{
    "action": {
        "type": "git_ops_updater",
        "description": "robot: watchman new release 749afbf",
        "payload": {
            "managed_realm": "charts",
            "managed_project": "watchman",
            "commit_hash": "749afbf"
        }
    }
}
*/

// ActionPayload represents the payload for Actions
type ActionPayload struct {
    ManagedRealm   string `json:"managed_realm"`
    ManagedProject string `json:"managed_project"`
    CommitHash     string `json:"commit_hash"`
}

// ActionCreate represents data for creating a new Action
type ActionCreate struct {
    Type        string `json:"type"`
    Description string `json:"description"`
    Payload     ActionPayload `json:"payload"`
}

// ActionCreateRequest represents a request to create a new Action
type ActionCreateRequest struct {
    Action ActionCreate `json:"action"`
}
