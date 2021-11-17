package com.webster.msauth.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.FORBIDDEN)
public class AccountAlreadyConfirmedException extends RuntimeException {
	private static final long serialVersionUID = -4444581246899909520L;

	public AccountAlreadyConfirmedException(String msg) {
		super(msg);
	}

	public AccountAlreadyConfirmedException(String msg, Throwable cause) {
		super(msg, cause);
	}
}
