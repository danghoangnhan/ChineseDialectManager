package dictionarymodel

import "IPADictionaryAPI/common"

type Dictionary struct {
	common.SQLModel `json:",inline"`
	DictionaryID int
	DictionaryName string
}

type DictionaryCreate struct {
	common.SQLModel `json:",inline"`
	DictionaryID int
	DictionaryName string
}