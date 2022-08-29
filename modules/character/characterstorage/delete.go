package characterstorage

import (
	"IPADictionaryAPI/common"
	"IPADictionaryAPI/modules/character/charactermodel"
	"context"
)

func (s *sqlStore) SoftDeleteData(ctx context.Context, id int, ) error {
	db := s.db
	if error := db.Table(charactermodel.Character{}.TableName()).
		Where("id = ?", id).
		Updates(map[string]interface{}{"status": 0,}).
		Error; error != nil {
		return common.ErrDB(error)
	}
	return nil
}