package stackoverflow

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

type user struct {
	DisplayName string `json:"display_name,omitempty"`
}

type users struct {
	Items []user `json:"items,omitempty"`
	Total int64 `json:"total,omitempty"`
}

func getName(userId string) (string, error) {
	stack, err := parse.GetStackToken(userId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return "", err
	}
	req, err := http.NewRequest("GET", "https://api.stackexchange.com/2.2/me", nil)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return "", err
	}
	q := req.URL.Query()
	q.Add("key", "QOg*bwIzDO1YjIrbKzVGNQ((")
	q.Add("site", "stackoverflow")
	q.Add("access_token", stack.AccessToken)
	q.Add("filter", "default")
	req.URL.RawQuery = q.Encode()

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		logging.ERROR.Println("Error:", err)
		return "", err
	}

	if resp.StatusCode != 200 {
		logging.ERROR.Println("StackOverflow service occurred an error... ", resp.Status)
		return "", errors.New(resp.Status)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		logging.ERROR.Println("Error when try to read body...\n", err)
		return "", err
	}

	var list users
	if err := json.Unmarshal(body, &list); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return "", err
	}

	if len(list.Items) == 0 {
		logging.WARNING.Println("Warning no user for stack overflow ...")
		return "", errors.New("No user for stack overflow ...")
	}

	var name string
	name = list.Items[0].DisplayName

	logging.INFO.Println("We get display name stack overflow !")
	return name, nil
}

type create struct {
	Name string `json:"name,omitempty"`
}


func changeName(area parse.Area) {
	displayName, err := getName(area.UserId)
	if err != nil {
		return
	}

	if area.Actions.Data == nil {
		logging.INFO.Println("Data for action create playlist is empty !")
		area.Actions.Data = create{
			Name: displayName,
		}
		_ = parse.UpdateData(area.Id, area)
		return
	}

	var store create
	if err := mapstructure.Decode(area.Actions.Data, &store); err != nil {
		logging.ERROR.Println(err)
		return
	}

	if store.Name == displayName {
		return
	}

	area.Actions.Data = create{
		Name: displayName,
	}
	_ = parse.UpdateData(area.Id, area)
	logging.INFO.Println("Data for action display name stackOverflow is update !")
	if area.IsActif { // means a playlist was create
		logging.INFO.Println("Poller found something, go send to TRIGGER service")
		utils.Sender( "stackoverflow", area.Id, nil)
	}
}
