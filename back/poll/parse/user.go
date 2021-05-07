package parse

import (
	"encoding/json"
	"errors"
	"io/ioutil"
	"net/http"
	"poll/logging"
)

type Spotify struct {
	AccessToken  string `json:"access_token,omitempty"`
	RefreshToken string `json:"refresh_token,omitempty"`
	Connected    bool   `json:"connected"`
	AuthRequired bool   `json:"auth_required"`
}

type Github struct {
	AccessToken  string `json:"access_token,omitempty"`
	Connected    bool   `json:"connected"`
	AuthRequired bool   `json:"auth_required"`
}

type Reddit struct {
	AccessToken  string `json:"access_token,omitempty"`
	RefreshToken string `json:"refresh_token,omitempty"`
	Connected    bool   `json:"connected"`
	AuthRequired bool   `json:"auth_required"`
}

type Discord struct {
	AccessToken  string `json:"access_token,omitempty"`
	RefreshToken string `json:"refresh_token,omitempty"`
	Connected    bool   `json:"connected"`
	AuthRequired bool   `json:"auth_required"`
}

type Twitch struct {
	AccessToken  string `json:"access_token,omitempty"`
	RefreshToken string `json:"refresh_token,omitempty"`
	ClientId     string `json:"client_id,omitempty"`
	Connected    bool   `json:"connected"`
	AuthRequired bool   `json:"auth_required"`
}

type StackOverflow struct {
	AccessToken string `json:"access_token,omitempty"`
}

type AuthService struct {
	Spotify       Spotify       `json:"Spotify,omitempty"`
	Github        Github        `json:"Github,omitempty"`
	Reddit        Reddit        `json:"Reddit,omitempty"`
	Discord       Discord       `json:"Discord,omitempty"`
	Twitch        Twitch        `json:"Twitch,omitempty"`
	StackOverflow StackOverflow `json:"Stackoverflow"`
}

type User struct {
	Id          string      `json:"objectId,omitempty"`
	AuthService AuthService `json:"auth_service,omitempty"`
}

func GetStackToken(userId string) (*StackOverflow, error) {
	req, err := http.NewRequest("GET", "http://parse-server:1337/parse/users/"+userId, nil)
	if err != nil {
		logging.ERROR.Println("Error:", err)
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

	var user User
	if err := json.Unmarshal(body, &user); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	return &user.AuthService.StackOverflow, nil
}

func GetTwitchToken(userId string) (*Twitch, error) {
	req, err := http.NewRequest("GET", "http://parse-server:1337/parse/users/"+userId, nil)
	if err != nil {
		logging.ERROR.Println("Error:", err)
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

	var user User
	if err := json.Unmarshal(body, &user); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	return &user.AuthService.Twitch, nil
}

func GetDiscordToken(userId string) (*Discord, error) {
	req, err := http.NewRequest("GET", "http://parse-server:1337/parse/users/"+userId, nil)
	if err != nil {
		logging.ERROR.Println("Error:", err)
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

	var user User
	if err := json.Unmarshal(body, &user); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	return &user.AuthService.Discord, nil
}

func GetSpotifyToken(userId string) (*Spotify, error) {
	req, err := http.NewRequest("GET", "http://parse-server:1337/parse/users/"+userId, nil)
	if err != nil {
		logging.ERROR.Println("Error:", err)
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

	var user User
	if err := json.Unmarshal(body, &user); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	return &user.AuthService.Spotify, nil
}

func GetGithubToken(userId string) (*Github, error) {
	req, err := http.NewRequest("GET", "http://parse-server:1337/parse/users/"+userId, nil)
	if err != nil {
		logging.ERROR.Println("Error:", err)
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

	var user User
	if err := json.Unmarshal(body, &user); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	return &user.AuthService.Github, nil
}

func GetRedditToken(userId string) (*Reddit, error) {
	req, err := http.NewRequest("GET", "http://parse-server:1337/parse/users/"+userId, nil)
	if err != nil {
		logging.ERROR.Println("Error:", err)
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

	var user User
	if err := json.Unmarshal(body, &user); err != nil {
		logging.ERROR.Println("Error when try to transform body...\n", err)
		return nil, err
	}

	return &user.AuthService.Reddit, nil
}
