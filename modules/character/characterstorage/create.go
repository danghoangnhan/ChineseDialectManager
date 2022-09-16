package characterstorage

import (
	"IPADictionaryAPI/common"
	"IPADictionaryAPI/modules/character/charactermodel"
	"context"
)

func (s *sqlStore) Create(ctx context.Context, data *charactermodel.CharacterCreate) error {
	db := s.db
	if err := db.Create(data).Error; err != nil {
		return common.ErrDB(err)
	}
	return nil
}