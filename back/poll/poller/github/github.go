package github

import (
	"encoding/json"
	"errors"
	"github.com/mitchellh/mapstructure"
	"io/ioutil"
	"net/http"
	"poll/logging"
	"poll/parse"
	"poll/utils"
)

type Repos struct {
	Name string `json:"name,omitempty"`
}

func getRepos(userId string) ([]string, error) {
	github, err := parse.GetGithubToken(userId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req, err := http.NewRequest("GET", "https://api.github.com/user/repos", nil)
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

	var list []Repos
	if err := json.Unmarshal(body, &list); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	var names []string
	for _, item := range list {
		names = append(names, item.Name)
	}

	logging.INFO.Println("We get Repo List !")
	return names, nil
}

type create struct {
	Names []string `json:"names"`
	Total int `json:"total"`
	Diff []string `json:"repos,omitempty"`
}

func createRepo(area parse.Area) {
	names, err := getRepos(area.UserId)
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
	logging.INFO.Println("Data for action create repo is update !")
	if store.Total < len(names) { // means a playlist was create
		logging.INFO.Println("Poller found something, go send to TRIGGER service")
		utils.Sender("github", area.Id, create{Diff: diff})
	}
}

func Handler(area parse.Area) {
	switch area.Actions.Id {
	case "github-create-repo":
		createRepo(area)
		break
	case "github-add-collab":
		addCollab(area)
		break
	case "github-new-invits":
		newInvites(area)
		break
	default:
		logging.ERROR.Println("Error we don't know action...")
		break
	}
}