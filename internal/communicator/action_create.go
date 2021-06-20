package communicator

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
    "errors"
    "log"
    "io/ioutil"

    "github.com/earaujoassis/watchman-bot/internal/utils"
)

func ActionCreateRequestor(requestData utils.H) (utils.H, error) {
    payload := ActionPayload{
        ManagedRealm: requestData["managed_realm"].(string),
        ManagedProject: requestData["managed_project"].(string),
        CommitHash: requestData["commit_hash"].(string),
    }
    actionCreate := ActionCreate{
        Type: requestData["type"].(string),
        Description: requestData["description"].(string),
        Payload: payload,
    }
    request := ActionCreateRequest{
        Action: actionCreate,
    }

    jsonData, err := json.Marshal(request)
    if err != nil {
        log.Fatal(fmt.Sprintf("Error: %s", err))
    }

    baseUrl := baseUrl()
    url := fmt.Sprintf("%s/api/applications/%s/actions", baseUrl, requestData["application_id"])

    httpRequest, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
    if err != nil {
        log.Fatal(fmt.Sprintf("Error: %s", err))
    }

    httpRequest.Header.Add("Accept", "application/json")
    httpRequest.Header.Add("Content-Type", "application/json")
    httpRequest.Header.Add("Authorization", fmt.Sprintf("Bearer %s", authorizationBearer()))
    client := &http.Client{}
    httpResponse, err := client.Do(httpRequest)
    if err != nil {
        log.Fatal(fmt.Sprintf("Error: %s", err))
    }
    defer httpResponse.Body.Close()
    bodyBytes, err := ioutil.ReadAll(httpResponse.Body)
    if err != nil {
        log.Fatal(fmt.Sprintf("Error: %s", err))
    }

    if httpResponse.StatusCode != 201 {
        log.Println(httpResponse.Status)
        log.Println(string(bodyBytes))
        return nil, errors.New(utils.UnfulfilledError)
    }

    return nil, nil
}
