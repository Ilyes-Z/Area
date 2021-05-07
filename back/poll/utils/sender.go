package utils

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"poll/logging"
)

func Sender(areaType, areaId string, toSend interface{}) {
	data := make(map[string]interface{})
	data["data"] = toSend
	payloadBuf := new(bytes.Buffer)
	_ = json.NewEncoder(payloadBuf).Encode(data)
	req, err := http.NewRequest("POST", fmt.Sprintf("http://trigger:6060/%s/%s/", areaType, areaId), payloadBuf)
	if err != nil {
		logging.ERROR.Println(err.Error())
		return
	}
	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{}
	_, err = client.Do(req)
	if err != nil {
		logging.ERROR.Println("Error:", err)
		return
	}

	logging.INFO.Printf("Service %s, was send to the trigger with id: %s !\n", areaType, areaId)
}
