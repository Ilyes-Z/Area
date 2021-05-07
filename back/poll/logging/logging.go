package logging

import (
	"log"
	"os"
)

var (
	INFO *log.Logger
	WARNING *log.Logger
	ERROR *log.Logger
)

func init() {
	INFO = log.New(os.Stdout, "INFO:", log.Ldate|log.Ltime|log.Lshortfile)
	WARNING = log.New(os.Stdout, "WARNING:", log.Ldate|log.Ltime|log.Lshortfile)
	ERROR = log.New(os.Stdout, "ERROR:", log.Ldate|log.Ltime|log.Lshortfile)
}
