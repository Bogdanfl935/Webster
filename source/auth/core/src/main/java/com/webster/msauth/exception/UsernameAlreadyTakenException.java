package com.webster.msauth.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.CONFLICT)
public class UsernameAlreadyTakenException extends RuntimeException {
	private static final long serialVersionUID = 4257066131525011116L;

	public UsernameAlreadyTakenException(String msg) {
		super(msg);
	}

	public UsernameAlreadyTakenException(String msg, Throwable cause) {
		super(msg, cause);
	}
}
