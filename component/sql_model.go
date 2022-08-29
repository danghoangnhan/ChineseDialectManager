package component

import "time"

type SQLModel struct {
	Id        int         `json:"-" gorm:"column:id;"`
	//FakeId    *UID        `json:"id" gorm:"-"`
	Status    int         `json:"status" gorm:"column:status;"`
	CreateAt  *time.Time  `json:"status" gorm:"column:created_at;"`
	UpdateAt  *time.Time  `json:"status" gorm:"column:updated_at;"`
}

//func (s *SQLModel) GenerateUID(dbType int)  {
//	uid := NewUID(uint32(s.Id),dbType,1)
//	s.FakeId = &uid
//}