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

type ActionPayload struct {
    ManagedRealm   string `json:"managed_realm"`
    ManagedProject string `json:"managed_project"`
    CommitHash     string `json:"commit_hash"`
}

type ActionCreate struct {
    Type        string `json:"type"`
    Description string `json:"description"`
    Payload     ActionPayload `json:"payload"`
}

type ActionCreateRequest struct {
    Action ActionCreate `json:"action"`
}
