package twitch

import (
	"encoding/json"
	"errors"
	"io/ioutil"
	"net/http"
	"poll/logging"
	"poll/parse"
	"poll/utils"
)

type Streamer struct {
	Id string `json:"id,omitempty"`
	Login string `json:"login,omitempty"`
}

type Streamers struct {
	Data []Streamer `json:"data,omitempty"`
}


func getStreamersId(userId string, streamers []string) ([]string, error) {
	twitch, err := parse.GetTwitchToken(userId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req, err := http.NewRequest("GET", "https://api.twitch.tv/helix/users", nil)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	q := req.URL.Query()
	for _, streamer := range streamers {
		q.Add("login", streamer)
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

	var list Streamers
	if err := json.Unmarshal(body, &list); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	var ids []string
	for _, item := range list.Data {
		ids = append(ids, item.Id)
	}

	return ids, nil
}

type countFan struct {
	Total int `json:"total,omitempty"`
}

func getUserFan(userId, id string) (int, error) {
	twitch, err := parse.GetTwitchToken(userId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return 0, err
	}
	req, err := http.NewRequest("GET", "https://api.twitch.tv/helix/users/follows", nil)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return 0, err
	}
	q := req.URL.Query()
	q.Add("to_id", userId)
	req.URL.RawQuery = q.Encode()
	req.Header.Add("Authorization", "Bearer "+twitch.AccessToken)
	req.Header.Add("Client-Id", twitch.ClientId)
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		logging.ERROR.Println("Error:", err)
		return 0, err
	}

	if resp.StatusCode != 200 {
		logging.ERROR.Println("Spotify service occurred an error... ", resp.Status)
		return 0, errors.New(resp.Status)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		logging.ERROR.Println("Error when try to read body...\n", err)
		return 0, err
	}

	var total countFan
	if err := json.Unmarshal(body, &total); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return 0, err
	}

	return total.Total, nil
}

type streamFan struct {
	Id string `json:"id,omitempty"`
	Total int `json:"total,omitempty"`
}

func checkFan(area parse.Area, streamers []string, modulo int) {
	for _, streamer := range streamers{
		fan, err := getUserFan(area.Id, streamer)
		if err != nil {
			continue
		}

		if (fan > 0 && fan % modulo == 0) && area.IsActif { // means a playlist was create
			logging.INFO.Println("Poller found something, go send to TRIGGER service")
			utils.Sender("twitch", area.Id, streamFan{Id: streamer, Total: fan})
		}
	}
}

func moduloFan(area parse.Area) {
	streamers := area.Actions.Parameters[0].(map[string]interface{})
	f := area.Actions.Parameters[1].(map[string]interface{})
	if streamers["streamer-list"] != nil {
		var list []string
		for _, item := range streamers["streamer-list"].([]interface{}) {
			list = append(list, item.(string))
		}

		var modulo int
		if f["modulo-number"] != nil {
			modulo = f["modulo-number"].(int)
		}


		ids, err := getStreamersId(area.UserId, list)
		if err != nil {
			return
		}
		checkFan(area, ids, modulo)
	}
}
