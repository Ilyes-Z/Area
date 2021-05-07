package spotify

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

type Artiste struct {
	Name string `json:"name,omitempty"`
	Id string `json:"id,omitempty"`
}

type TrackInfo struct {
	Name string `json:"name,omitempty"`
	Artists []Artiste `json:"artists,omitempty"`
}

type CurrentTrack struct {
	Item TrackInfo `json:"item,omitempty"`
}

type TrackParam struct {
	Name string `json:"name,omitempty"`
	ArtisteName string `json:"artiste_name,omitempty"`
}

func searchCurrentTrack(area parse.Area) (*CurrentTrack, error) {
	spotify, err := parse.GetSpotifyToken(area.UserId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req, err := http.NewRequest("GET", "https://api.spotify.com/v1/me/player/currently-playing", nil)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req.Header.Add("Authorization", "Bearer " + spotify.AccessToken)
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

	var track CurrentTrack
	if err := json.Unmarshal(body, &track); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	logging.INFO.Println("We get Current Track !")
	return &track, nil
}

func getParamTrack(params []interface{}) *TrackParam {
	var trackParam TrackParam

	for _, param := range params {
		myMap := param.(map[string]interface{})
		if myMap["track-title"] != nil {
			trackParam.Name = myMap["track-title"].(string)
		}
		if myMap["artists-track"] != nil {
			trackParam.ArtisteName = myMap["artists-track"].(interface{}).(string)
		}
	}

	return &trackParam
}

func getCurrentTrack(area parse.Area) {
	track, err := searchCurrentTrack(area)
	if err != nil {
		return
	}

	if !area.IsActif {
		return
	}

	data := area.Actions.Data
	area.Actions.Data = track
	_ = parse.UpdateData(area.Id, area)

	params := getParamTrack(area.Actions.Parameters)
	if strings.ToLower(params.Name) != strings.ToLower(track.Item.Name) || strings.ToLower(params.ArtisteName) != strings.ToLower(track.Item.Artists[0].Name) {
		return
	}

	var store CurrentTrack
	if err := mapstructure.Decode(data, &store); err != nil {
		logging.ERROR.Println(err)
		return
	}

	if strings.ToLower(store.Item.Name) == strings.ToLower(track.Item.Name) && strings.ToLower(store.Item.Artists[0].Name) == strings.ToLower(track.Item.Artists[0].Name) {
		return
	}

	logging.INFO.Println("Data for action create playlist is update !")
	logging.INFO.Println("Poller found something, go send to TRIGGER service")
	utils.Sender( "spotify", area.Id, TrackInfo{})
}
