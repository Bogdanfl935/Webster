package com.webster.msauth.token;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.webster.msauth.exception.AuthExceptionMessage;
import com.webster.msauth.exception.InvalidAccessTokenProvidedException;
import com.webster.msauth.exception.NoPrefixProvidedForAccessToken;

import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.io.DecodingException;
import io.jsonwebtoken.security.SignatureException;

@Component
public class JwtValidator {
	@Autowired
	private JwtHandle tokenHandle;
	
	public String stripTokenPrefix(String rawToken) {
		String tokenPrefix = String.format("%s ", JwtHandle.DEFAULT_TOKEN_TYPE);

		if (!rawToken.startsWith(tokenPrefix)) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.NO_PREFIX_PROVIDED_ACCESS_TOKEN;
			exceptionMessage.setErrorParameter(rawToken);
			throw new NoPrefixProvidedForAccessToken(exceptionMessage.getErrorMessage());
		}

		return rawToken.replace(tokenPrefix, "");
	}
	
	public String validate(String token) {
		String validationErrorMessage = attemptValidation(token);

		if (validationErrorMessage != null) {
			throw new InvalidAccessTokenProvidedException(validationErrorMessage);
		}
		
		return tokenHandle.getJwtSubject(token);
	}

	private String attemptValidation(String token) {
		String exceptionMessage = null;

		try {
			if (!tokenHandle.isValidJwt(token)) {
				exceptionMessage = AuthExceptionMessage.INVALID_ACCESS_TOKEN_PROVIDED.getErrorMessage();
			}
		} catch (SignatureException exception) {
			exceptionMessage = AuthExceptionMessage.TAMPERED_ACCESS_TOKEN_PROVIDED.getErrorMessage();
		} catch (DecodingException exception) {
			exceptionMessage = AuthExceptionMessage.MALFORMED_ACCESS_TOKEN_PROVIDED.getErrorMessage();
		} catch (JwtException exception) {
			exceptionMessage = exception.getMessage();
		}

		return exceptionMessage;
	}
}
