package com.webster.msauth.token;

import java.util.Date;
import java.util.NoSuchElementException;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Positive;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtBuilder;
import io.jsonwebtoken.JwtParserBuilder;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.RequiredTypeException;

@Service
public class JwtHandle {
	public static final String DEFAULT_TOKEN_TYPE = "Bearer";

	@Autowired
	private JwtConfig tokenConfig;
	@Autowired
	private JwtSecurity tokenSecurity;

	public String createJsonWebToken(@NotNull UserDetails userDetails, @Positive Long expirationInMilisec,
			JwtScopeClaim scopeClaim) {
		Date issuedAt = new Date();
		JwtBuilder builtToken = Jwts.builder().setSubject(userDetails.getUsername()).setIssuedAt(issuedAt)
				.setIssuer(tokenConfig.getTokenIssuer())
				.setExpiration(new Date(issuedAt.getTime() + expirationInMilisec))
				.claim(JwtScopeClaim.SCOPE_CLAIM, scopeClaim.getScope());
		return tokenSecurity.signBuiltToken(builtToken).compact();
	}

	public boolean isValidJwt(@NotNull String token, @NotNull JwtScopeClaim scopeClaim) {
		/*
		 * If token is ill formated or invalid, parsing of the JWT will throw an
		 * exception
		 */
		String issuer = getJwtIssuer(token);
		JwtScopeClaim parsedClaim = null;
		try {
			parsedClaim = JwtScopeClaim.getAssociatedScope(getJwtClaim(token, JwtScopeClaim.SCOPE_CLAIM));
		} catch (NoSuchElementException | RequiredTypeException exception) {
			// Parsed claim remains null
		}

		return scopeClaim.equals(parsedClaim) && issuer.equals(tokenConfig.getTokenIssuer());
	}

	public String getJwtSubject(String token) {
		Claims extractedClaims = extractJwtClaims(token);
		return extractedClaims.getSubject();
	}

	public Date getJwtExpiration(String token) {
		Claims extractedClaims = extractJwtClaims(token);
		return extractedClaims.getExpiration();
	}

	public Date getJwtIssuedAt(String token) {
		Claims extractedClaims = extractJwtClaims(token);
		return extractedClaims.getIssuedAt();
	}

	public String getJwtIssuer(String token) {
		Claims extractedClaims = extractJwtClaims(token);
		return extractedClaims.getIssuer();
	}

	public String getJwtClaim(String token, String claim) {
		Claims extractedClaims = extractJwtClaims(token);
		return extractedClaims.get(claim, String.class);
	}

	private Claims extractJwtClaims(@NotNull String token) {
		JwtParserBuilder parser = Jwts.parserBuilder();
		return tokenSecurity.setTokenParserKey(parser).build().parseClaimsJws(token).getBody();
	}
}
