package com.webster.msauth.exception;

import javax.validation.constraints.NotNull;

public enum AuthExceptionMessage {
	USERNAME_NOT_FOUND("Username %s does not exist"), 
	USERNAME_ALREADY_TAKEN("Username %s is already taken"),
	ACCOUNT_NOT_CONFIRMED("Email address %s has not yet been confirmed"),
	ACCOUNT_ALREADY_CONFIRMED("Email address %s has already been confirmed"),
	INVALID_USERNAME_OR_PASSWORD("Invalid username or password provided"),
	INVALID_ACCESS_TOKEN_PROVIDED("Invalid access token provided"),
	TAMPERED_ACCESS_TOKEN_PROVIDED("Access token signature does not match"),
	MALFORMED_ACCESS_TOKEN_PROVIDED("Access token provided could not be decoded"),
	INVALID_REFRESH_TOKEN_PROVIDED("Invalid refresh token provided"),
	NO_PREFIX_PROVIDED_ACCESS_TOKEN("No token type prefix provided for token %s");

	private String errorMessage;
	private String errorParameter;

	private AuthExceptionMessage(String errorMessage) {
		this.errorMessage = errorMessage;
		this.errorParameter = new String();
	}

	public String getErrorMessage() {
		return String.format(errorMessage, errorParameter);
	}

	public void setErrorParameter(@NotNull String errorParameter) {
		this.errorParameter = errorParameter;
	}
}
