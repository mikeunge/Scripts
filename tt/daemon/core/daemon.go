package core

import (
	"github.com/mikeunge/Scripts/tt/utils"

	"github.com/apsdehal/go-logger"
	"github.com/godbus/dbus/v5"
)

func handleSignal(log *logger.Logger, signals []interface{}) {
	/*
	 * Signal meaning:
	 *  - signal == true => screen got locked
	 *  - signal == false => screen got unlocked
	 *  - signal == emtpy => nothing
	 */

	if len(signals) == 0 {
		log.Debug("Received empty signal")
		return
	}

	if len(signals) > 1 {
		log.WarningF("Received too many signals, %d - %+v", len(signals), signals)
		return
	}

	var signal = signals[0]
	if signal == true {
		log.Debug("Screen got locked")
		PauseTimetrace(log)
	} else if signal == false {
		log.Debug("Screen got unlocked")
		ResumeTimetrace(log)
	} else {
		log.NoticeF("Not expected signal, %+v", signal)
	}
}

func Start(log *logger.Logger, config *utils.Config) {
	conn, err := dbus.ConnectSessionBus()
	if err != nil {
		log.CriticalF("Failed to connect to session bus: %+v", err)
		utils.ExitGracefully(1, config)
	}
	defer conn.Close()

	if err = conn.AddMatchSignal(
		dbus.WithMatchObjectPath("/org/gnome/ScreenSaver"),
		dbus.WithMatchInterface("org.gnome.ScreenSaver"),
		dbus.WithMatchSender("org.gnome.ScreenSaver"),
	); err != nil {
		log.CriticalF("Fatal error occured while matching DBus signals: %+v", err)
		utils.ExitGracefully(1, config)
	}

	c := make(chan *dbus.Signal, 10)
	conn.Signal(c)
	for v := range c {
		handleSignal(log, v.Body)
	}
}

func Stop(log *logger.Logger, config *utils.Config) {
	log.Info("Stopping daemon...")
	utils.RemovePid(log, config.Pidfile)
	log.DebugF("Removed pidfile: %s", config.Pidfile)
	utils.ExitGracefully(0, config)
}

func DaemonIsRunning(path string) bool {
	return utils.FileExists(path)
}
