package main

import (
	"IPADictionaryAPI/component"
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
	products := r.Group("/products")
	{
		products.POST("", ginproduct.CreateProduct(appCtx))
		products.GET("/:id", ginproduct.GetProduct(appCtx))
		products.GET("", ginproduct.ListProduct(appCtx))
		products.PATCH("/:id", ginproduct.UpdateProduct(appCtx))
		products.DELETE("/:id", ginproduct.DeleteProduct(appCtx))
	}
	return r.Run()
}