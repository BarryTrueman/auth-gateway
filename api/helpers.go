package authgateway

import (
	"errors"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/dgrijalva/jwt-go"
	"github.com/golang-jwt/jwt/v4"
)

const (
	tokenExpirationTime = 30 * time.Minute
	jwtSecretKey      = "your_secret_key_here"
)

func GenerateToken(claims jwt.MapClaims) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(jwtSecretKey))
}

func ValidateToken(tokenString string) (jwt.MapClaims, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, errors.New("unexpected signing method")
		}
		return []byte(jwtSecretKey), nil
	})
	if err != nil {
		return nil, err
	}
	if claims, ok := token.Claims.(jwt.MapClaims); !ok {
		return nil, errors.New("token contains unexpected claims")
	}
	return claims, nil
}

func ExtractToken(r *http.Request) string {
	tokenString := r.Header.Get("Authorization")
	if !strings.HasPrefix(tokenString, "Bearer ") {
		return ""
	}
	return tokenString[7:]
}

func jwtError(err error) error {
	return fmt.Errorf("jwt error: %w", err)
}