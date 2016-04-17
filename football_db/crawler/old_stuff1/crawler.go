package main

import (
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"net/http"
	"regexp"
)

// take a URL of the form:
// http://www.whoscored.com/Matches/{MATCH_ID}/Live
// e.g http://www.whoscored.com/Matches/614052/Live is the match for
// Eveton vs Manchester
// and return a pointer to the body of the GET request or an error
func GetRequestMatch(matchid int) ([]byte, error) {
	const match_address = "http://www.whoscored.com/Matches/"

	url := fmt.Sprintf("%s%d/Live", match_address, matchid)

	resp, err := http.Get(url)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}

	// if we sucessfully got a response, store the
	// body in memory
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}
	return body, nil

}

//const a = `var b = ".*"`
const a = `var b.*";for`

var numberRegex *regexp.Regexp

// take a request body and find the number in it
// it has a bunch of crap in it then "var b = "the number we want""
func GetNumberFromRequest(body string) string {
	unprocessed := numberRegex.FindString(body)
	return unprocessed[7 : len(unprocessed)-5]
}

// take a string of numbers and decode them to the string
func DecodeNumber(num string) string {
	data, _ := (hex.DecodeString(num))
	return string(data)
}

func init() {
	numberRegex, _ = regexp.Compile(a)
}

func main() {
	fmt.Println("Crawler starting.....")

	vbody, err := GetRequestMatch(614052)
	body := string(vbody)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(body)

	numString := GetNumberFromRequest(body)
	fmt.Println(numString)

	fmt.Println(DecodeNumber(numString))
}
