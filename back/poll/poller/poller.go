package poller

import (
	"poll/logging"
	"poll/parse"
	"poll/poller/discord"
	"poll/poller/github"
	"poll/poller/reddit"
	"poll/poller/spotify"
	"poll/poller/stackoverflow"
	"poll/poller/twitch"
	"time"
)

func handleArea(area parse.Area) {
	switch area.Services.TriggerId {
	case "pXJSDNBC0q": // Spotify
		spotify.Handler(area)
		break
	case "bIGSDNTH0u": // Github
		github.Handler(area)
		break
	case "brGdDeTHIu": // Reddit
		reddit.Handler(area)
		break
	case "PvAPuOIELm": // Discord
		discord.Handler(area)
		break
	case "trWdCHTHIu": // Twitch
		twitch.Handler(area)
		break
	case "BsUIQasnQU": //StackOverflow
		stackoverflow.Handler(area)
		break
	default:
		logging.ERROR.Println("Error unknown Service id !")
		break
	}
}

func Poller() {
	for {
		logging.INFO.Println("Getting list AREA")
		areas, err := parse.GetListAction()
		if err != nil {
			logging.WARNING.Println("Something wrong we stop and call again parse")
			continue
		}

		logging.INFO.Printf("We handle list of %d AREA!\n", len(areas))
		for _, area := range areas {
			handleArea(area)
		}
		logging.INFO.Println("All AREA is done, go next !")
		time.Sleep(10 * time.Second)
	}
}
