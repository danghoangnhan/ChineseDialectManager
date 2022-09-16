package dictionarybiz

import (
	"IPADictionaryAPI/modules/dictionary/dictionarymodel"
	"context"
)

type CreateDictionaryStore interface {
	Create(ctx context.Context, data *dictionarymodel.DictionaryCreate) error
}
type createDictionaryBiz struct {
	store CreateDictionaryStore
}
func NewCreateDictionaryBiz(store CreateDictionaryStore) *createDictionaryBiz {
	return &createDictionaryBiz{store: store}
}
func (biz *createDictionaryBiz) CreateDictionary(ctx context.Context, data *dictionarymodel.DictionaryCreate) error {

	//if err := data.Validate(); err != nil {
	//	return err
	//}
	err := biz.store.Create(ctx, data)
	return err
}