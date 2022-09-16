package main

import (
	"IPADictionaryAPI/component"
	"IPADictionaryAPI/modules/character/charactertransport/gincharacter"
	"IPADictionaryAPI/modules/dictionary/dictionarytransport/gindictionary"
	"github.com/gin-gonic/gin"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"log"
	"net/http"
	"os"
)

func main(){

	dsn := os.Getenv("DBConnectionStr")
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})

	if err != nil {
		log.Fatalln(err)
	}

	if err := runService(db); err != nil {
		log.Fatalln(err)
	}

}

func runService(db *gorm.DB) error {

	r := gin.Default()
	appCtx := component.NewAppContext(db)
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})
	characters := r.Group("/words")
	{
		characters.POST("",gincharacter.CreateCharacter(appCtx))
	}
	dictionaries := r.Group("/dictionaries")
	{
		dictionaries.POST("",gindictionary.CreateDictionary(appCtx))
	}
	return r.Run()
}