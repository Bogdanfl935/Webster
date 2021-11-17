package com.webster.msnotification.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
public class EmailDeliveryException extends RuntimeException {
	private static final long serialVersionUID = -3648775292026553320L;

	public EmailDeliveryException(String msg) {
		super(msg);
	}

	public EmailDeliveryException(String msg, Throwable cause) {
		super(msg, cause);
	}
}
