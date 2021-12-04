package com.webster.msauth.exception;

import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public enum AuthExceptionMessage {
	USERNAME_NOT_FOUND("No account associated with username exists"), 
	USERNAME_ALREADY_TAKEN("Username has already been taken"),
	ACCOUNT_NOT_CONFIRMED("Email address has not yet been confirmed"),
	ACCOUNT_ALREADY_CONFIRMED("Email address has already been confirmed"),
	INVALID_USERNAME_OR_PASSWORD("Invalid username or password provided"),
	INVALID_ACCESS_TOKEN_PROVIDED("Invalid access token provided"),
	TAMPERED_ACCESS_TOKEN_PROVIDED("Access token signature does not match"),
	MALFORMED_ACCESS_TOKEN_PROVIDED("Access token provided could not be decoded"),
	INVALID_REFRESH_TOKEN_PROVIDED("Invalid refresh token provided"),
	NO_PREFIX_PROVIDED_ACCESS_TOKEN("No token type prefix provided");

	@NotNull
	@Getter
	private String errorMessage;
}
