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

type playlist struct {
	Id string `json:"id"`
}

type playlists struct {
	Items []playlist `json:"items,omitempty"`
	Total int64 `json:"total,omitempty"`
}

func getPlaylists(userId string) ([]string, error) {
	spotify, err := parse.GetSpotifyToken(userId)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return nil, err
	}
	req, err := http.NewRequest("GET", "https://api.spotify.com/v1/me/playlists", nil)
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

	var list playlists
	if err := json.Unmarshal(body, &list); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	var names []string
	for _, item := range list.Items {
		names = append(names, item.Id)
	}

	logging.INFO.Println("We get Playlist List !")
	return names, nil
}

type create struct {
	Names []string `json:"names,omitempty"`
	Total int `json:"total,omitempty"`
	Diff []string `json:"playlists"`
}

func createPlaylist(area parse.Area) {
	names, err := getPlaylists(area.UserId)
	if err != nil {
		return
	}

	if area.Actions.Data == nil {
		logging.INFO.Println("Data for action create playlist is empty !")
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
	logging.INFO.Println("Data for action create playlist is update !")
	if store.Total < len(names) && area.IsActif { // means a playlist was create
		logging.INFO.Println("Poller found something, go send to TRIGGER service")
		utils.Sender( "spotify", area.Id, create{Diff: diff})
	}
}