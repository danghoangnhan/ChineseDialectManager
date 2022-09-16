package common

const (
	DbTypeCharacter		= 1
	DbTypeDictionary	= 2
)

const CurrentUser = "user"

type Requester interface {
	GetUserId() int
	GetEmail() string
	GetRole() string
}