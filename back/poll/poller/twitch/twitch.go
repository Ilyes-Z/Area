package twitch

import (
	"poll/logging"
	"poll/parse"
)

func Handler(area parse.Area) {
	switch area.Actions.Id {
	case "twitch-stream-actif":
		actifStream(area)
		break
	case "twitch-follower-user":
		moduloFan(area)
		break
	case "twitch-top-games":
		topGame(area)
		break
	default:
		logging.ERROR.Println("Error we don't know action...")
		break
	}
}