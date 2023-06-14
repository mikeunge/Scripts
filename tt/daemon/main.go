package main

import (
	"bytes"
	"fmt"
	"os"
	"os/signal"
	"strings"
	"syscall"

	"github.com/mikeunge/Scripts/tt/utils"

	"github.com/apsdehal/go-logger"
	"github.com/mikeunge/Scripts/tt/core"
)

var (
	log    *logger.Logger
	config *utils.Config
)

func init() {
	var err error
	config = &utils.Config{
		Pidfile: "/tmp/tt_daemon.pid",
		Logfile: "/tmp/tt_daemon.log",
	}

	for i := 0; i < len(os.Args); i++ {
		if strings.ToLower(os.Args[i]) == "debug" {
			config.Debug = true
			break
		}
	}

	if config.Debug {
		log, err = logger.New("tt_daemon", 1, os.Stdout)
		log.SetLogLevel(logger.DebugLevel)
		log.SetFormat("%{time:2006-02-01 15:04:05} %{filename}:%{line} - [%{level}] %{message}")
	} else {
		// stream logs to file
		config.Logs = new(bytes.Buffer)
		log, err = logger.New("tt_daemon", 0, config.Logs)
		log.SetLogLevel(logger.WarningLevel)
		log.SetFormat("%{time:2006-02-01 15:04:05} - [%{level}] %{message}")
	}

	if err != nil {
		fmt.Printf("An error occured while initializing, exting.\n%+v", err)
		os.Exit(1)
	}
}

func main() {
	if core.DaemonIsRunning(config.Pidfile) {
		log.Warning("There is already an instance running, aborting.")
		utils.ExitGracefully(0, config)
	}

	var pid = os.Getpid()
	err := utils.CreatePid(log, pid, config.Pidfile)
	if err != nil {
		err = utils.RemovePid(log, config.Pidfile)
		if err != nil {
			log.ErrorF("Could not cleanup pidfile! %+v", err)
		}
		utils.ExitGracefully(7, config)
	}

	// catch SIGETRM or SIGINTERRUPT
	cancelChan := make(chan os.Signal, 1)
	signal.Notify(cancelChan, syscall.SIGTERM, syscall.SIGINT)

	// start the actual daemon
	go func() {
		log.InfoF("Startin daemon...")
		log.InfoF("Daemon running with PID: %d", pid)
		core.Start(log, config)
	}()

	// catch kill signal & cleanup
	sig := <-cancelChan
	log.WarningF("Caught signal %v", sig)
	core.Stop(log, config)
}
