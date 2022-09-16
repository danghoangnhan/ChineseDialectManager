package gindictionary

import (
	"IPADictionaryAPI/common"
	"IPADictionaryAPI/component"
	"IPADictionaryAPI/modules/dictionary/dictionarybiz"
	"IPADictionaryAPI/modules/dictionary/dictionarymodel"
	"IPADictionaryAPI/modules/dictionary/dictionarystorage"
	"github.com/gin-gonic/gin"
	"net/http"
)

func CreateDictionary(ctx component.AppContext) gin.HandlerFunc{
	return func(c *gin.Context) {
		var data dictionarymodel.DictionaryCreate
		if err := c.ShouldBind(&data); err != nil {
			panic(common.ErrInvalidRequest(err))
		}

		store := dictionarystorage.NewSQLStore(ctx.GetMainDBConnection())
		biz   := dictionarybiz.NewCreateDictionaryBiz(store)

		if err := biz.CreateDictionary(c.Request.Context(), &data); err != nil {panic(err)}
		data.GenUID(common.DbTypeDictionary)
		c.JSON(http.StatusOK, common.SimpleSuccessResponse(data.FakeId.String()))
	}
}