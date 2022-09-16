package characterbiz

import (
	"IPADictionaryAPI/modules/character/charactermodel"
	"context"
)

type CreateCharacterStore interface {
	Create(ctx context.Context, data *charactermodel.CharacterCreate) error
}
type createCharacterBiz struct {
	store CreateCharacterStore
}
func NewCreateCharacterBiz(store CreateCharacterStore) *createCharacterBiz {
	return &createCharacterBiz{store: store}
}
func (biz *createCharacterBiz) CreateCharacter(ctx context.Context, data *charactermodel.CharacterCreate) error {
	if err := data.Validate(); err != nil {
		return err
	}
	err := biz.store.Create(ctx, data)
	return err
}