package com.webster.msauth.service;

import java.util.concurrent.TimeUnit;

import javax.validation.constraints.NotNull;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.webster.msauth.dto.AuthorizationResponse;
import com.webster.msauth.token.JwtHandle;
import com.webster.msauth.token.JwtScopeClaim;
import com.webster.msauth.token.JwtValidator;

@Service
public class AuthorizationService {
	@Autowired
	private JwtHandle tokenHandle;
	@Autowired
	private JwtValidator tokenValidator;

	public AuthorizationResponse validate(@NotNull String rawToken, JwtScopeClaim scopeClaim) {
		String token = tokenValidator.stripTokenPrefix(rawToken);
		/* If token is invalid, an exception will be thrown */
		tokenValidator.validate(token, scopeClaim);

		Long accessTokenExpiration = TimeUnit.MILLISECONDS
				.toSeconds(tokenHandle.getJwtExpiration(token).getTime() - System.currentTimeMillis());
		return new AuthorizationResponse(accessTokenExpiration, tokenHandle.getJwtSubject(token));
	}

}
