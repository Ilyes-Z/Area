package twitch

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

type Stream struct {
	Id string `json:"id,omitempty"`
	UserId string `json:"user_id,omitempty"`
	UserLogin string `json:"user_login,omitempty"`
}

type Streams struct {
	Data []Stream `json:"data,omitempty"`
}


func getActifStream(userId string, streamers []string) ([]string, error) {
	twitch, err := parse.GetTwitchToken(userId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req, err := http.NewRequest("GET", "https://api.twitch.tv/helix/streams", nil)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	q := req.URL.Query()
	for _, streamer := range streamers {
		q.Add("user_login", streamer)
	}
	req.URL.RawQuery = q.Encode()
	req.Header.Add("Authorization", "Bearer "+twitch.AccessToken)
	req.Header.Add("Client-Id", twitch.ClientId)
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

	var list Streams
	if err := json.Unmarshal(body, &list); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	var names []string
	for _, item := range list.Data {
		names = append(names, item.UserLogin)
	}

	return names, nil
}

type actifStreamer struct {
	Streamers []string `json:"streamers"`
	Total int `json:"total"`
	Actifs []string `json:"actifs,omitempty"`
}

func checkActif(area parse.Area, actifs []string) {
	if area.Actions.Data == nil {
		logging.INFO.Println("Data for action create playlist is empty !")
		area.Actions.Data = actifStreamer{
			Streamers: actifs,
			Total: len(actifs),
		}
		utils.Sender( "twitch", area.Id, actifStreamer{Actifs: actifs})
		_ = parse.UpdateData(area.Id, area)
		return
	}

	var store actifStreamer
	if err := mapstructure.Decode(area.Actions.Data, &store); err != nil {
		logging.ERROR.Println(err)
		return
	}
	diff := utils.Difference(store.Streamers, actifs)
	if len(diff) == 0 {
		return
	}

	area.Actions.Data = actifStreamer{
		Streamers: actifs,
		Total: len(actifs),
	}
	_ = parse.UpdateData(area.Id, area)
	logging.INFO.Println("Data for action streamer actif is update !")
	if store.Total < len(actifs) && area.IsActif { // means a playlist was create
		logging.INFO.Println("Poller found something, go send to TRIGGER service")
		utils.Sender( "twitch", area.Id, actifStreamer{Actifs: diff})
	}
}

func actifStream(area parse.Area) {
	for _, param := range area.Actions.Parameters {
		f := param.(map[string]interface{})
		if f["streamer-list"] != nil {
			var list []string
			for _, item := range f["streamer-list"].([]interface{}) {
				list = append(list, item.(string))
			}

			actif, err := getActifStream(area.UserId, list)
			if err != nil {
				continue
			}
			checkActif(area, actif)
		}

	}
}