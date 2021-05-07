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
	"strings"
)

type Game struct {
	Id string `json:"id,omitempty"`
	Name string `json:"name,omitempty"`
	BoxArtUrl string `json:"box_art_url,omitempty"`
	Seen bool `json:"seen"`
}

type Pagination struct {
	Cursor string `json:"cursor,omitempty"`
}

type TopParam struct {
	Contain string `json:"contain,omitempty"`
}

type Games struct {
	Data []Game `json:"data,omitempty"`
	Pagination  Pagination `json:"pagination,omitempty"`
}

func getTopGames(userId string) ([]Game, error) {
	twitch, err := parse.GetTwitchToken(userId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req, err := http.NewRequest("GET", "https://api.twitch.tv/helix/games/top", nil)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	q := req.URL.Query()
	q.Add("first", "30")
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
		logging.ERROR.Println("Twitch service occurred an error... ", resp.Status)
		return nil, errors.New(resp.Status)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		logging.ERROR.Println("Error when try to read body...\n", err)
		return nil, err
	}

	var games Games
	if err := json.Unmarshal(body, &games); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	return games.Data, nil
}

func getParamTop(params []interface{}) *TopParam {
	var topParam TopParam

	for _, param := range params {
		myMap := param.(map[string]interface{})
		if myMap["title-contain"] != nil {
			topParam.Contain = myMap["title-contain"].(string)
		}
	}

	return &topParam
}

type top struct {
	Top []Game `json:"top,omitempty"`
}

func topGame(area parse.Area) {
	games, err := getTopGames(area.UserId)
	if err != nil {
		return
	}

	if area.Actions.Data == nil {
		area.Actions.Data = top{
			Top: games,
		}
		_ = parse.UpdateData(area.Id, area)
	}

	parm := getParamTop(area.Actions.Parameters)

	var store top
	if err := mapstructure.Decode(area.Actions.Data, &store); err != nil {
		logging.ERROR.Println(err)
		return
	}

	var toReturn []Game
	for i, game := range games {
		seen := false
		for _, save := range store.Top {
			if save.Id == game.Id && save.Name == game.Name {
				seen = save.Seen
			}
		}

		if strings.Contains(game.Name, parm.Contain) && !seen {
			toReturn = append(toReturn, game)
		}
		games[i].Seen = true
	}

	area.Actions.Data = top{
		Top: games,
	}
	_ = parse.UpdateData(area.Id, area)
	if len(toReturn) > 0 && area.IsActif {
		logging.INFO.Println("Poller found something, go send to TRIGGER service")
		utils.Sender( "twitch", area.Id, nil)
	}
}