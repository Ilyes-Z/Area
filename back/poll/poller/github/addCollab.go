package github

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/mitchellh/mapstructure"
	"io/ioutil"
	"net/http"
	"poll/logging"
	"poll/parse"
	"poll/utils"
)

type Collab struct {
	Login string `json:"login"`
}

func getCollab(userId, owner, repo string) ([]string, error) {
	github, err := parse.GetGithubToken(userId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req, err := http.NewRequest("GET", fmt.Sprintf("https://api.github.com/repos/%s/%s/collaborators", owner, repo), nil)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req.Header.Add("Authorization", "token " + github.AccessToken)
	req.Header.Add("Accept", "application/vnd.github.v3+json")
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		logging.ERROR.Println("Error:", err)
		return nil, err
	}

	if resp.StatusCode != 200 {
		logging.ERROR.Println("Github service occurred an error... ", resp.Status)
		return nil, errors.New(resp.Status)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		logging.ERROR.Println("Error when try to read body...\n", err)
		return nil, err
	}

	var list []Collab
	if err := json.Unmarshal(body, &list); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	var collabs []string
	for _, item := range list {
		collabs = append(collabs, item.Login)
	}

	logging.INFO.Println("We get Repo List !")
	return collabs, nil
}

type CollabParam struct {
	Repos string `json:"repo,omitempty"`
	Owner string `json:"owner,omitempty"`
}

func getParamCollab(params []interface{}) *CollabParam {
	var collabParam CollabParam

	for _, param := range params {
		myMap := param.(map[string]interface{})
		if myMap["repo-name"] != nil {
			collabParam.Repos = myMap["repo-name"].(string)
		}
		if myMap["owner-name"] != nil {
			collabParam.Owner = myMap["owner-name"].(string)
		}
	}

	return &collabParam
}

func addCollab(area parse.Area) {
	param := getParamCollab(area.Actions.Parameters)
	names, err := getCollab(area.UserId, param.Owner, param.Repos)
	if err != nil {
		return
	}

	if area.Actions.Data == nil {
		logging.INFO.Println("Data for action create repo is empty !")
		area.Actions.Data = create{
			Names: names,
			Total: len(names),
		}
		_ = parse.UpdateData(area.Id, area)
		return
	}

	var store create
	if err := mapstructure.Decode(area.Actions.Data, &store); err != nil {
		logging.ERROR.Println(err)
		return
	}
	diff := utils.Difference(store.Names, names)
	if len(diff) == 0 {
		return
	}

	area.Actions.Data = create{
		Names: names,
		Total: len(names),
	}
	_ = parse.UpdateData(area.Id, area)
	logging.INFO.Println("Data for action add collab is update !")
	if store.Total < len(names) { // means a playlist was create
		logging.INFO.Println("Poller found something, go send to TRIGGER service")
		utils.Sender("github", area.Id, nil)
	}
}