package gincharacter

import (
	"IPADictionaryAPI/common"
	"IPADictionaryAPI/component"
	"IPADictionaryAPI/modules/character/characterbiz"
	"IPADictionaryAPI/modules/character/charactermodel"
	"IPADictionaryAPI/modules/character/characterstorage"
	"github.com/gin-gonic/gin"
	"net/http"
)

func CreateCharacter(appCtx component.AppContext) gin.HandlerFunc {

	return func(c *gin.Context) {
		var data charactermodel.CharacterCreate
		if err := c.ShouldBind(&data); err != nil {
			panic(common.ErrInvalidRequest(err))
		}
		//requester := c.MustGet(common.CurrentUser).(common.Requester)
		//data.OwnerId = requester.GetUserId()

		store := characterstorage.NewSQLStore(appCtx.GetMainDBConnection())
		biz   := characterbiz.NewCreateCharacterBiz(store)

		if err := biz.CreateCharacter(c.Request.Context(), &data); err != nil {
			panic(err)
		}

		data.GenUID(common.DbTypeCharacter)
		c.JSON(http.StatusOK, common.SimpleSuccessResponse(data.FakeId.String()))
	}
}