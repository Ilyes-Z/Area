package parse

import (
	"bytes"
	"encoding/json"
	"errors"
	"io/ioutil"
	"net/http"
	"poll/logging"
)

type Action struct {
	Id         string        `json:"id"`
	Data       interface{}   `json:"data,omitempty"`
	Parameters []interface{} `json:"parameters,omitempty"`
}

type Services struct {
	TriggerId  string `json:"trigger,omitempty"`
	ReactionId string `json:"reaction,omitempty"`
}

type Area struct {
	Id       string   `json:"objectId,omitempty"`
	Services Services `json:"services,omitempty"`
	UserId   string   `json:"user_id,omitempty"`
	IsActif  bool     `json:"is_actif,omitempty"`
	Actions  Action   `json:"trigger,omitempty"`
}

type Result struct {
	Areas []Area `json:"results"`
}

func UpdateData(id string, area Area) error {
	area.Id = ""
	payloadBuf := new(bytes.Buffer)
	_ = json.NewEncoder(payloadBuf).Encode(area)
	req, err := http.NewRequest("PUT", "http://parse-server:1337/parse/classes/Area/"+id, payloadBuf)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return err
	}
	req.Header.Add("X-Parse-Application-Id", "")
	req.Header.Add("X-Parse-REST-API-Key", "")
	req.Header.Add("Content-Type", "application/json")
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		logging.ERROR.Println("Error:", err)
		return err
	}

	if resp.StatusCode != 200 {
		logging.ERROR.Println(resp.Status)
		return err
	}

	return nil
}

func GetListAction() ([]Area, error) {
	req, err := http.NewRequest("GET", "http://parse-server:1337/parse/classes/Area", nil)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req.Header.Add("X-Parse-Application-Id", "")
	req.Header.Add("X-Parse-REST-API-Key", "")
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		logging.ERROR.Println("Error:", err)
		return nil, err
	}

	if resp.StatusCode != 200 {
		logging.ERROR.Println(resp.Status)
		return nil, errors.New("Something wrong with parse: " + resp.Status)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		logging.ERROR.Println("Error when try to read body...\n", err)
		return nil, err
	}

	var list Result
	if err := json.Unmarshal(body, &list); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	return list.Areas, nil
}
