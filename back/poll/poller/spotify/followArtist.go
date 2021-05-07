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
)

type Artist struct {
	Name string `json:"name"`
	Uri string `json:"uri"`
}

type Cursor struct {
	After string `json:"after"`
}

type Artists struct {
	Items []Artist `json:"items"`
	Cursor Cursor `json:"cursor"`
	Total int `json:"total"`
}

type dataSpotify struct {
	Artists Artists `json:"artists"`
}

func getArtist(userId, cursor string) ([]Artist, error) {
	spotify, err := parse.GetSpotifyToken(userId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}

	var list []Artist
	var data dataSpotify
	data.Artists.Total = 1000
	for len(list) < data.Artists.Total {
		req, err := http.NewRequest("GET", "https://api.spotify.com/v1/me/following", nil)
		if err != nil {
			logging.ERROR.Println(err.Error())
			return nil, err
		}

		q := req.URL.Query()
		if len(data.Artists.Cursor.After) > 0 {
			q.Add("after", data.Artists.Cursor.After)
		}
		q.Add("type", "artist")
		req.URL.RawQuery = q.Encode()

		req.Header.Add("Authorization", "Bearer "+spotify.AccessToken)
		req.Header.Add("Accept", "application/json")
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

		var toAdd dataSpotify
		if err := json.Unmarshal(body, &toAdd); err != nil {
			logging.ERROR.Println("Error when try to transform body...\n", err)
			return nil, err
		}
		data.Artists.Total = toAdd.Artists.Total
		list = append(list, toAdd.Artists.Items...)
	}

	logging.INFO.Println("We get Artist List !")
	return list, nil
}

type saveData struct {
	Artists []Artist `json:"artists,omitempty"`
}

func followArtist(area parse.Area) {
	list, err := getArtist(area.UserId, "")
	if err != nil {
		return
	}

	if area.Actions.Data == nil {
		logging.INFO.Println("Data for action create playlist is empty !")
		area.Actions.Data = saveData{
			Artists: list,
		}
		_ = parse.UpdateData(area.Id, area)
		return
	}

	var store saveData
	if err := mapstructure.Decode(area.Actions.Data, &store); err != nil {
		logging.ERROR.Println(err)
		return
	}

	var listStore []string
	var listUpdate []string
	for _, artist := range store.Artists {
		listStore = append(listStore, artist.Name)
	}

	for _, artist := range list {
		listUpdate = append(listUpdate, artist.Name)
	}

	diff := utils.Difference(listStore, listUpdate)
	if len(diff) == 0 {
		return
	}

	area.Actions.Data = saveData{
		Artists: list,
	}
	_ = parse.UpdateData(area.Id, area)
	logging.INFO.Println("Data for action create playlist is update !")
	if len(store.Artists) < len(list) && area.IsActif { // means a playlist was create
		logging.INFO.Println("Poller found something, go send to TRIGGER service")
		utils.Sender( "spotify", area.Id, nil)
	}
}