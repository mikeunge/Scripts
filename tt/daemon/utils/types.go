package utils

import "bytes"

type Config struct {
	Pidfile string
	Logfile string
	Debug   bool
	Logs    *bytes.Buffer
}
