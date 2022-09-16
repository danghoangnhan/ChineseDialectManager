package dictionarystorage

import (
	"IPADictionaryAPI/common"
	"IPADictionaryAPI/modules/dictionary/dictionarymodel"
	"context"
)

func (s *sqlStore) Create(ctx context.Context, data *dictionarymodel.DictionaryCreate) error {
	db := s.db
	if err := db.Create(data).Error; err != nil {
		return common.ErrDB(err)
	}
	return nil
}