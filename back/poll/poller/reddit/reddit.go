package reddit

import (
	"encoding/json"
	"errors"
	"github.com/mitchellh/mapstructure"
	"io/ioutil"
	"net/http"
	"poll/logging"
	"poll/parse"
)

type Data struct {
	Dist int `json:"dist,omitempty"`
}

type Resp struct {
	Data Data `json:"data,omitempty"`
}

func getMessagesSent(userId string) (int, error) {
	token, err := parse.GetRedditToken(userId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return 0, err
	}
	req, err := http.NewRequest("GET", "https://oauth.reddit.com/message/unread", nil)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return 0, err
	}
	req.Header.Add("Authorization", "Bearer "+token.AccessToken)
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		logging.ERROR.Println("Error:", err)
		return 0, err
	}

	if resp.StatusCode != 200 {
		logging.ERROR.Println("Reddit service occurred an error... ", resp.Status)
		return 0, errors.New(resp.Status)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		logging.ERROR.Println("Error when try to read body...\n", err)
		return 0, err
	}

	var reddit Resp
	if err := json.Unmarshal(body, &reddit); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return 0, err
	}

	logging.INFO.Println("We get number of message sent !")
	return reddit.Data.Dist, nil
}

type create struct {
	Total int `json:"total"`
}

func sendNewMessage(area parse.Area) {
	sent, err := getMessagesSent(area.UserId)
	if err != nil {
		return
	}

	if area.Actions.Data == nil {
		logging.INFO.Println("Data for action send message is empty !")
		area.Actions.Data = create{
			Total: sent,
		}
		_ = parse.UpdateData(area.Id, area)
		return
	}

	var store create
	if err := mapstructure.Decode(area.Actions.Data, &store); err != nil {
		logging.ERROR.Println(err)
		return
	}

	area.Actions.Data = create{
		Total: sent,
	}
	_ = parse.UpdateData(area.Id, area)
	logging.INFO.Println("Data for action create repo is update !")
	if store.Total != sent { // means a playlist was create
		logging.INFO.Println("Poller Reddit found something, go send to TRIGGER service")
		// send to trigger!
	}
}

func Handler(area parse.Area) {
	switch area.Actions.Id {
	case "reddit-sent-new-message":
		sendNewMessage(area)
		break
	default:
		logging.ERROR.Println("Error we don't know action...")
		break
	}
}
