package com.webster.msauth.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.UNAUTHORIZED)
public class InvalidUsernameException extends RuntimeException {
	private static final long serialVersionUID = -4940600589672641185L;

	public InvalidUsernameException(String msg) {
		super(msg);
	}

	public InvalidUsernameException(String msg, Throwable cause) {
		super(msg, cause);
	}
}