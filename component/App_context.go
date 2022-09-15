package component

import (
	"gorm.io/gorm"
)

type AppContext interface {
	GetMainDBConnection() *gorm.DB
	SecretKey() string
}


type appCtx struct {
	db          *gorm.DB
}

func (ctx *appCtx) SecretKey() string {
	panic("implement me")
}

func NewAppContext(db *gorm.DB) *appCtx {
	return &appCtx{
		db: db,
	}
}

func (ctx *appCtx) GetMainDBConnection() *gorm.DB {
	return ctx.db
}
