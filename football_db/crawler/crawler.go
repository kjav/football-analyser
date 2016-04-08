package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

// http://www.whoscored.com/Matches/614052/Live is the match for
// Eveton vs Manchester
const match_address = "http://www.whoscored.com/Matches/"

// the max id we get
const max_id = 100000
const num_workers = 5

// function that get the bytes of the match id from the website
func match_fetch(matchid int) {
	url := fmt.Sprintf("%s%d/Live", match_address, matchid)

	resp, err := http.Get(url)
	if err != nil {
		fmt.Println(err)
		return
	}

	// if we sucessfully got a response, store the
	// body in memory
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
		return
	}

	// write the body to memory
	pwd, _ := os.Getwd()
	filepath := fmt.Sprintf("%s/match_data/%d", pwd, matchid)
	err = ioutil.WriteFile(filepath, body, 0644)
	if err != nil {
		fmt.Println(err)
		return
	}
}

// data type to send to the workers,
// last means this job is the last one
// matchid is the match id to be fetched
// a matchid of -1 means don't fetch a match
type job struct {
	last    bool
	matchid int
}

func create_worker(jobs chan job) {
	for {
		next_job := <-jobs
		if next_job.matchid != -1 {
			match_fetch(next_job.matchid)
		}
		if next_job.last {
			return
		}
	}
}

func main() {
	// do the eveton match as a reference
	match_fetch(614052)

	var joblist [num_workers]chan job
	var v int

	for i := 0; i < num_workers; i++ {
		job_chan := make(chan job)
		joblist[i] = job_chan
		go create_worker(job_chan)
	}
	for i := 0; i < max_id; i = i + num_workers {
		for index, c := range joblist {
			if i+index < max_id {
				v = i + index
			} else {
				v = -1
			}
			c <- job{false, v}
		}
	}
	for _, c := range joblist {
		c <- job{true, -1}
	}
}
