package com.webster.msauth.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

import lombok.NoArgsConstructor;

@ResponseStatus(HttpStatus.NOT_FOUND)
@NoArgsConstructor
public class JwtScopeClaimConversionFailException extends RuntimeException {
	private static final long serialVersionUID = 2029769846864519890L;

	public JwtScopeClaimConversionFailException(String msg) {
		super(msg);
	}

	public JwtScopeClaimConversionFailException(String msg, Throwable cause) {
		super(msg, cause);
	}
}
