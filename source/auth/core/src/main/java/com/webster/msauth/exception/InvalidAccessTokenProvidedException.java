package com.webster.msauth.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.UNAUTHORIZED)
public class InvalidAccessTokenProvidedException extends RuntimeException  {
	private static final long serialVersionUID = -6199244105456453871L;

	public InvalidAccessTokenProvidedException(String msg) {
		super(msg);
	}

	public InvalidAccessTokenProvidedException(String msg, Throwable cause) {
		super(msg, cause);
	}
}
