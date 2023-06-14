package utils

import (
	"os"
	"os/user"
	"strconv"

	"github.com/apsdehal/go-logger"
)

func CreatePid(log *logger.Logger, pid int, path string) error {
	f, err := os.Create(path)
	if err != nil {
		log.ErrorF("Could not create file %s", path)
		return err
	}
	defer f.Close()

	_, err = f.WriteString(strconv.Itoa(pid))
	if err != nil {
		log.ErrorF("Could not write pid to file: %s", path)
		return err
	}

	log.DebugF("Created pidfile: %s", path)
	return nil
}

func RemovePid(log *logger.Logger, path string) error {
	if !FileExists(path) {
		log.Debug("PID doesn't exist")
		return nil
	}

	err := os.Remove(path)
	if err != nil {
		log.WarningF("Could not remove file: %s", path)
		return err
	}
	return nil
}

func FileExists(path string) bool {
	if _, err := os.Stat(path); os.IsNotExist(err) {
		return false
	} else {
		return true
	}
}

func GetUserHome() (string, error) {
	usr, err := user.Current()
	if err != nil {
		return "", err
	}
	return usr.HomeDir, nil
}

// ExitGracefully - is needed for writing the log bcs the logger library doesn't support filestreams (:facepalm:)
func ExitGracefully(exitCode int, config *Config) {
	if !config.Debug {
		f, err := os.OpenFile(config.Logfile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			panic(err)
		}
		if _, err := f.Write(config.Logs.Bytes()); err != nil {
			panic(err)
		}
		defer f.Close()
	}

	os.Exit(exitCode)
}
