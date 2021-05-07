package discord

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

type Guild struct {
	Id             string        `json:"id,omitempty"`
	Name           string        `json:"name,omitempty"`
	Icon           string        `json:"icon,omitempty"`
	Owner          bool          `json:"owner,omitempty"`
	Permissions    int64         `json:"permissions,omitempty"`
	Features       []interface{} `json:"features,omitempty"`
	PermissionsNew string        `json:"permissions_new,omitempty"`
}

func getServerIds(userId string) ([]string, error) {
	discord, err := parse.GetDiscordToken(userId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req, err := http.NewRequest("GET", "https://discord.com/api/users/@me/guilds", nil)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req.Header.Add("Authorization", "Bearer "+discord.AccessToken)
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		logging.ERROR.Println("Error:", err)
		return nil, err
	}

	if resp.StatusCode != 200 {
		logging.ERROR.Println("Spotify service occurred an error... ", resp.Status)
		return nil, errors.New(resp.Status)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		logging.ERROR.Println("Error when try to read body...\n", err)
		return nil, err
	}

	var list []Guild
	if err := json.Unmarshal(body, &list); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	var names []string
	for _, item := range list {
		names = append(names, item.Id)
	}

	return names, nil
}

type create struct {
	Ids []string `json:"ids,omitempty"`
	Total int `json:"total,omitempty"`
	Diff []string `json:"diff"`
}

func newServer(area parse.Area) {
	ids, err := getServerIds(area.UserId)
	if err != nil {
		return
	}

	if area.Actions.Data == nil {
		logging.INFO.Println("Data for action create server is empty !")
		area.Actions.Data = create{
			Ids: ids,
			Total: len(ids),
		}
		_ = parse.UpdateData(area.Id, area)
		return
	}

	var store create
	if err := mapstructure.Decode(area.Actions.Data, &store); err != nil {
		logging.ERROR.Println(err)
		return
	}
	diff := utils.Difference(store.Ids, ids)
	if len(diff) == 0 {
		return
	}

	area.Actions.Data = create{
		Ids: ids,
		Total: len(ids),
	}
	_ = parse.UpdateData(area.Id, area)
	logging.INFO.Println("Data for action create service is update !")
	if store.Total < len(ids) && area.IsActif { // means a playlist was create
		logging.INFO.Println("Poller found something, go send to TRIGGER service")
		utils.Sender( "discord", area.Id, create{Diff: diff})
	}
}

func Handler(area parse.Area) {
	switch area.Actions.Id {
	case "discord-new-server":
		newServer(area)
		break
	default:
		logging.ERROR.Println("Error we don't know action...")
		break
	}
}