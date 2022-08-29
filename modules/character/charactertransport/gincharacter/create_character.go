package gincharacter

import (
	"IPADictionaryAPI/common"
	"IPADictionaryAPI/component"
	"IPADictionaryAPI/modules/character/charactermodel"
	"github.com/gin-gonic/gin"
	"net/http"
)

func CreateCharacter(appCtx component.AppContext) gin.HandlerFunc {

	return func(c *gin.Context) {
		var data charactermodel.CharacterCreate
		if err := c.ShouldBind(&data); err != nil {
			panic(common.ErrInvalidRequest(err))
		}
		requester := c.MustGet(common.CurrentUser).(common.Requester)
		data.OwnerId = requester.GetUserId()

		store := characterstorag.NewSQLStore(appCtx.GetMainDBConnection())
		biz   := housebiz.NewCreateHouseBiz(store)

		if err := biz.CreateHouse(c.Request.Context(), &data); err != nil {
			panic(err)
		}

		data.GenerateUID(common.DbTypeRestaurant)
		c.JSON(http.StatusOK, common.SimpleSuccessResponse(data.FakeId.String()))
	}
}