package spotify

import (
	"poll/logging"
	"poll/parse"
)

func Handler(area parse.Area) {
	switch area.Actions.Id {
	case "spotify-create-playlist":
		createPlaylist(area)
		break
	case "spotify-current-track":
		getCurrentTrack(area)
		break
	case "spotify-follow-artist":
		followArtist(area)
		break
	default:
		logging.ERROR.Println("Error we don't know action...")
		break
	}
}