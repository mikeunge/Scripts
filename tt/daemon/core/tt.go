package core

import (
	"io"
	"os/exec"

	"github.com/apsdehal/go-logger"
)

func PauseTimetrace(log *logger.Logger) error {
	cmd := exec.Command("tt", "pause")
	cmd.Stdout = io.Discard
	cmd.Stderr = io.Discard

	err := cmd.Run()
	if err != nil {
		log.CriticalF("tt - Execution failed, %+v", err)
		return err
	}
	return nil
}

func ResumeTimetrace(log *logger.Logger) error {
	cmd := exec.Command("tt", "resume")
	cmd.Stdout = io.Discard
	cmd.Stderr = io.Discard

	err := cmd.Run()
	if err != nil {
		log.CriticalF("tt - Execution failed, %+v", err)
		return err
	}
	return nil
}
