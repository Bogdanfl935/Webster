package com.webster.msauth.token;

import javax.crypto.SecretKey;

import org.springframework.stereotype.Component;

import io.jsonwebtoken.JwtBuilder;
import io.jsonwebtoken.JwtParserBuilder;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;

@Component
public class JwtSecurity {
	private static final SignatureAlgorithm SIGNATURE_ALGORITHM = SignatureAlgorithm.HS512;
	private static final SecretKey SECRET_KEY = Keys.secretKeyFor(SIGNATURE_ALGORITHM);

	public JwtBuilder signBuiltToken(JwtBuilder builtToken) {
		return builtToken.signWith(SECRET_KEY, SIGNATURE_ALGORITHM);
	}

	public JwtParserBuilder setTokenParserKey(JwtParserBuilder parser) {
		return parser.setSigningKey(SECRET_KEY);
	}
}
