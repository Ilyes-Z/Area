package stackoverflow

import (
	"poll/logging"
	"poll/parse"
)

func Handler(area parse.Area) {
	switch area.Actions.Id {
	case "stackoverflow-change-name":
		changeName(area)
		break
	default:
		logging.ERROR.Println("Error we don't know action...")
		break
	}
}