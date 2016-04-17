package football_crawler

import (
	"fmt"
	"regexp"
)

func main() {
	var reg string
	var input string
	var compiler *regexp.Regexp

	for {
		fmt.Print("Input regular expression: ")
		fmt.Scanln(&reg)
		fmt.Print("Input string: ")
		fmt.Scanln(&input)

		compiler, _ = regexp.Compile(input)
		match := compiler.FindAllString(input, 2)
		fmt.Println(match)
	}
}
