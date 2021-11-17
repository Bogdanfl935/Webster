package com.webster.msauth.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.UNAUTHORIZED)
public class InvalidRefreshTokenProvidedException extends RuntimeException {
	private static final long serialVersionUID = 5822092819152880859L;

	public InvalidRefreshTokenProvidedException(String msg) {
		super(msg);
	}

	public InvalidRefreshTokenProvidedException(String msg, Throwable cause) {
		super(msg, cause);
	}
}
