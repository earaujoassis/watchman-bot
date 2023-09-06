package communicator

import (
	"bytes"
	"crypto/tls"
	"crypto/x509"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/earaujoassis/watchman-bot/internal/utils"
)

// ActionCreateRequestor make a request to the watchman server to create new actions
func ActionCreateRequestor(requestData utils.H) (utils.H, error) {
	var client *http.Client
	var tlsConfig *tls.Config
	var tr *http.Transport

	payload := ActionPayload{
		ManagedRealm:   requestData["managed_realm"].(string),
		ManagedProject: requestData["managed_project"].(string),
		CommitHash:     requestData["commit_hash"].(string),
	}
	actionCreate := ActionCreate{
		Type:        requestData["type"].(string),
		Description: requestData["description"].(string),
		Payload:     payload,
	}
	request := ActionCreateRequest{
		Action: actionCreate,
	}

	jsonData, err := json.Marshal(request)
	if err != nil {
		log.Fatal(fmt.Sprintf("Error: %s", err))
	}

	baseURL := baseURL()
	url := fmt.Sprintf(actionCreatePath, baseURL, requestData["application_id"])

	if strings.HasPrefix(url, "https") {
		if verify := os.Getenv("WATCHMAN_BOT_SSL_VERIFY"); verify == "1" {
			rootCertificates, _ := x509.SystemCertPool()
			if rootCertificates == nil {
				rootCertificates = x509.NewCertPool()
			}
			if _, err := os.Stat(localCertificateFile); os.IsNotExist(err) {
				log.Println("Custom certificate file doesn't exist")
			} else {
				log.Println("Custom certificate file found; loading it")
				certificates, err := ioutil.ReadFile(localCertificateFile)
				if err != nil {
					log.Fatalf("Failed to append %q to RootCAs: %v", localCertificateFile, err)
				}
				if ok := rootCertificates.AppendCertsFromPEM(certificates); !ok {
					log.Println("No certificates appended, using system certificates only")
				}
			}
			tlsConfig = &tls.Config{
				InsecureSkipVerify: false,
				RootCAs:            rootCertificates,
			}
			tr = &http.Transport{TLSClientConfig: tlsConfig}
			client = &http.Client{Transport: tr}
		} else {
			tlsConfig = &tls.Config{
				InsecureSkipVerify: true,
			}
			tr = &http.Transport{TLSClientConfig: tlsConfig}
			client = &http.Client{Transport: tr}
		}
	} else {
		client = &http.Client{}
	}

	httpRequest, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatal(fmt.Sprintf("Error: %s", err))
	}

	httpRequest.Header.Add("Accept", "application/json")
	httpRequest.Header.Add("Content-Type", "application/json")
	httpRequest.Header.Add("Authorization", fmt.Sprintf("Bearer %s", authorizationBearer()))
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
