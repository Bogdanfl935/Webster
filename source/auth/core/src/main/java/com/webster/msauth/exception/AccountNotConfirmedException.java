package com.webster.msauth.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.FORBIDDEN)
public class AccountNotConfirmedException extends RuntimeException {
	private static final long serialVersionUID = -8628415303039071434L;
	
	public AccountNotConfirmedException(String msg) {
		super(msg);
	}

	public AccountNotConfirmedException(String msg, Throwable cause) {
		super(msg, cause);
	}
}
