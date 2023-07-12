package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"math/rand"
	"os"
	"os/exec"
	"os/user"
	"path/filepath"
	"strings"

	"github.com/akamensky/argparse"
	"github.com/apsdehal/go-logger"
)

const (
	appName        = "better-cowsay"
	appDescription = "A better way of using cowsay."
	appVersion     = "1.0.1"
	appAuthor      = "@mikeunge"
)

var (
	DEBUG      bool   = false
	ConfigFile string = "~/.config/better-cowsay.json"
	Cowfile    string = ""
	log        *logger.Logger
)

type Config struct {
	Cowfiles string `json:"cowfiles"`
}

func serializePath(path string) string {
	var sPath string
	usr, _ := user.Current()
	dir := usr.HomeDir
	if path == "~" || path == "$HOME" {
		sPath = dir
	} else if strings.HasPrefix(path, "~/") || strings.HasPrefix(path, "$HOME/") {
		sPath = filepath.Join(dir, path[2:])
	} else {
		sPath = path
	}
	return sPath
}

func pathExistsAndIsFile(path string) (bool, bool) {
	if info, err := os.Stat(path); os.IsNotExist(err) {
		return false, false
	} else {
		return true, !info.IsDir()
	}
}

func configParser(configpath string) (Config, error) {
	var config Config
	exists, isFile := pathExistsAndIsFile(configpath)
	if !(exists && isFile) {
		return config, fmt.Errorf("config not found: %s", configpath)
	}

	data, err := ioutil.ReadFile(configpath)
	if err != nil {
		return config, fmt.Errorf("error when reading config: %+v", err)
	}

	err = json.Unmarshal(data, &config)
	if err != nil {
		return config, fmt.Errorf("error while parsing: %+v, please make sure the file is correctly formatted (json)", err)
	}

	return config, nil
}

func getCowfile(path string) (string, error) {
	files, err := ioutil.ReadDir(path)
	if err != nil {
		return "", err
	}

	var s []string
	var filename string
	for _, file := range files {
		if !file.IsDir() && strings.HasSuffix(file.Name(), ".cow") {
			if len(Cowfile) > 0 && file.Name() == Cowfile {
				log.InfoF("found %s in %s, selecting this cowfile!", file.Name(), path)
				return fmt.Sprintf("%s/%s", path, file.Name()), nil
			}
			s = append(s, file.Name())
		} else {
			log.NoticeF("%s is not a cowfile", file.Name())
		}
	}

	idx := rand.Intn(len(s) - 0)
	filename = s[idx]

	log.NoticeF("found %d cowfiles", len(s))
	log.WarningF("didn't find %s in %s", Cowfile, path)
	log.InfoF("the chosen one: %s", filename)

	return fmt.Sprintf("%s/%s", path, filename), nil
}

func cowsayExists() error {
	var stdout bytes.Buffer
	var stderr bytes.Buffer
	cmd := exec.Command("which", "cowsay")

	// change the std.err & std.out to a buffer to cacpture the output from which
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err := cmd.Run()
	if err != nil {
		return fmt.Errorf(fmt.Sprint(err) + ": " + stderr.String())
	}
	log.Notice("cowsay exists")
	return nil
}

func cowsay(cowfile string) {
	err := cowsayExists()
	if err != nil {
		log.Error(err.Error())
		log.Fatal("could not find cowsay as executable, please make sure it is installed and available in $PATH")
	}

	// get piped input
	stdin, err := io.ReadAll(os.Stdin)
	if err != nil {
		log.FatalF("an error occured while reading stdin, error: %s", err.Error())
	}

	cmd := exec.Command("cowsay", "-f", cowfile, "-W", "100", string(stdin))
	cmd.Stdout = os.Stdout
	cmd.Stderr = io.Discard // fuck the error, we catch it anyways

	err = cmd.Run()
	if err != nil {
		log.FatalF("execution failed, %s", err.Error())
	}
}

func init() {
	parser := argparse.NewParser(appName, "A better way of using cowsay.")

	version := parser.Flag("v", "version", &argparse.Options{Required: false, Help: "Prints the version"})
	debug := parser.Flag("d", "debug", &argparse.Options{Required: false, Help: "Enable debug logging"})
	config := parser.String("c", "config", &argparse.Options{Required: false, Help: "Specify the configuration path"})
	filename := parser.String("f", "filename", &argparse.Options{Required: false, Help: "Specify the cowfile name"})

	err := parser.Parse(os.Args)
	if err != nil {
		fmt.Println(parser.Usage(err))
	}

	if *version {
		fmt.Printf("v%s\n", appVersion)
		os.Exit(0)
	}
	if *debug {
		DEBUG = true
	}

	if DEBUG {
		log, err = logger.New("cowsay", 1, os.Stdout)
		log.SetFormat("%{time:2006-02-01 15:04:05} %{filename}:%{line} - [%{level}] %{message}")
	} else {
		log, err = logger.New("cowsay", 0, io.Discard)
	}
	if err != nil {
		panic(err)
	}

	if len(*config) >= 1 {
		p := serializePath(*config)
		exists, isFile := pathExistsAndIsFile(p)
		if exists && isFile {
			ConfigFile = p
		} else {
			log.ErrorF("config not found: %s, using default", p)
		}
	} else {
		ConfigFile = serializePath(ConfigFile)
	}
	if len(*filename) >= 1 {
		n := strings.Split(*filename, ".")
		if len(n) == 1 || n[len(n)-1] != "cow" {
			Cowfile = *filename + ".cow"
			log.InfoF("added cow extension to %s", *filename)
		} else {
			Cowfile = *filename
		}
		log.NoticeF("looking for %s", Cowfile)
	}
}

func main() {
	c, err := configParser(ConfigFile)
	if err != nil {
		log.Fatal(err.Error())
	}
	// Serialize paths if needed
	c.Cowfiles = serializePath(c.Cowfiles)

	cowfile, err := getCowfile(c.Cowfiles)
	if err != nil {
		log.Errorf("something went wrong, are there any cowfiles? (error: %+v)", err.Error())
	}
	log.InfoF("loading: %s", cowfile)

	cowsay(cowfile)
	os.Exit(0)
}
