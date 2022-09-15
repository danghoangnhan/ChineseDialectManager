package charactermodel

import (
	"IPADictionaryAPI/common"
	"strings"
)

const EntityName = "Character"

type Character struct {
	Symbol 	string
	Sound 	string
	Tone	string
	Ipa 	string
	DictionaryID int
}
type CharacterCreate struct {
	Symbol 	string
	Sound 	string
	Tone	string
	Ipa 	string
}

type CharacterUpdate struct {
	Symbol 	string
	Sound 	string
	Tone	string
	Ipa 	string
}

func (Character) TableName() string {
	return EntityName
}
func (CharacterUpdate) TableName() string {
	return Character{}.TableName()
}
func (CharacterCreate) TableName() string {
	return Character{}.TableName()
}

func (character *CharacterCreate)  Validate() error{

	character.Symbol 	= 	strings.TrimSpace(character.Symbol)
	character.Sound 	= 	strings.TrimSpace(character.Sound)
	character.Tone 		= 	strings.TrimSpace(character.Tone)
	character.Ipa 		= 	strings.TrimSpace(character.Ipa)

	if len(character.Symbol) == 0 {
		return ErrSymbolCannotBeEmpty
	}
	if len(character.Sound) == 0 {
		return ErrSoundCannotBeEmpty
	}
	if len(character.Tone) == 0 {
		return ErrToneCannotBeEmpty
	}
	if len(character.Ipa) == 0 {
		return ErrIpaCannotBeEmpty
	}
	return nil
}
func (character *CharacterUpdate) Validate() error {

	character.Symbol 	= 	strings.TrimSpace(character.Symbol)
	character.Sound 	= 	strings.TrimSpace(character.Sound)
	character.Tone 		= 	strings.TrimSpace(character.Tone)
	character.Ipa 		= 	strings.TrimSpace(character.Ipa)

	if len(character.Symbol) == 0 {
		return ErrSymbolCannotBeEmpty
	}
	if len(character.Sound) == 0 {
		return ErrSoundCannotBeEmpty
	}
	if len(character.Tone) == 0 {
		return ErrToneCannotBeEmpty
	}
	if len(character.Ipa) == 0 {
		return ErrIpaCannotBeEmpty
	}
	return nil
}
var (
	ErrSymbolCannotBeEmpty 	= common.NewCustomError(nil, "character's symbol can't be blank", "ErrSymbolCannotBeEmpty")
	ErrSoundCannotBeEmpty 	= common.NewCustomError(nil, "character's sound can't be blank", 	"ErrSoundCannotBeEmpty")
	ErrToneCannotBeEmpty 	= common.NewCustomError(nil, "character's tone can't be blank", 	"ErrToneCannotBeEmpty")
	ErrIpaCannotBeEmpty 	= common.NewCustomError(nil, "character's ipa can't be blank", 	"ErrIpaCannotBeEmpty")

)
func (character *Character) Mask(isAdminOrOwner bool)  {
	character.GenerateUID(common.DbTypeRestaurant)
}
