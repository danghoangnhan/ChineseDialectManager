package main

import (
	"IPADictionaryAPI/modules/character/charactermodel"
	"encoding/csv"
	"fmt"
	"os"
)

func main() {
	file, err := os.Open("/home/danieldu/Downloads/data.csv")
	if err != nil {
		fmt.Println(err)
	}
	reader := csv.NewReader(file)
	records, _ := reader.ReadAll()
	var characterList []charactermodel.Character
	for index, record := range records{
		characterList = append(characterList, charactermodel.Character{})
	}
	fmt.Println(records)
}