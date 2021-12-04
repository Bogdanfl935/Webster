package com.webster.msauth.jwt;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.junit.Assume.assumeTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.doReturn;

import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Random;

import javax.crypto.SecretKey;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;
import org.postgresql.util.Base64;

import com.webster.msauth.models.CustomUserDetails;
import com.webster.msauth.token.JwtConfig;
import com.webster.msauth.token.JwtHandle;
import com.webster.msauth.token.JwtScopeClaim;
import com.webster.msauth.token.JwtSecurity;

import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.JwtBuilder;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.JwtParserBuilder;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import io.jsonwebtoken.security.SignatureException;

@ExtendWith(MockitoExtension.class)
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class TokenHandleTest {
	@Mock
	private JwtConfig tokenConfig;
	@Spy
	private JwtSecurity tokenSecurity;
	@Mock
	private CustomUserDetails customUserDetails;
	private Long expiration;

	@InjectMocks
	private JwtHandle tokenHandle;

	@BeforeAll
	void setUp() {
		tokenHandle = new JwtHandle();
	}

	@BeforeEach
	void setUpIndividually() {
		expiration = 100000L;
		given(tokenConfig.getTokenIssuer()).willReturn("Webster MsAuth");
		given(customUserDetails.getUsername()).willReturn("Valid-Email@Webster.uk.co");
	}

	@Test
	void verificationSuccessTokenIsValidForActuallyValidToken() {
		// Given
		String token = tokenHandle.createJsonWebToken(customUserDetails, expiration, JwtScopeClaim.ACCESS);

		// When & Then
		assertThat(tokenHandle.isValidJwt(token, JwtScopeClaim.ACCESS)).isTrue();
	}

	@Test
	void verificationFailForExpiredToken() throws InterruptedException {
		// Given
		expiration = 1L;
		String token = tokenHandle.createJsonWebToken(customUserDetails, expiration, JwtScopeClaim.ACCESS);

		// When & Then
		Thread.sleep(2);
		assertThatThrownBy(() -> tokenHandle.isValidJwt(token, JwtScopeClaim.ACCESS)).isInstanceOf(ExpiredJwtException.class);
	}

	@RepeatedTest(value = 3)
	void verificationFailForTokenWithDifferentSecretKey() {
		// Given
		String token = tokenHandle.createJsonWebToken(customUserDetails, expiration, JwtScopeClaim.ACCESS);

		// When
		byte[] bytes = new byte[512];
		new Random().nextBytes(bytes);
		doAnswer(invocation -> invocation.getArgument(0, JwtParserBuilder.class).setSigningKey(bytes))
				.when(tokenSecurity).setTokenParserKey(any(JwtParserBuilder.class));

		// Then
		assertThatThrownBy(() -> tokenHandle.isValidJwt(token, JwtScopeClaim.ACCESS)).isInstanceOf(SignatureException.class);
	}

	@Test
	void verificationSuccessTokenIsInvalidForTokenWithDifferentIssuer() {
		// Given
		String token = tokenHandle.createJsonWebToken(customUserDetails, expiration, JwtScopeClaim.ACCESS);

		// When
		doReturn(tokenConfig.getTokenIssuer() + "Suffix").when(tokenConfig).getTokenIssuer();

		// Then
		assertThat(tokenHandle.isValidJwt(token, JwtScopeClaim.ACCESS)).isFalse();
	}

	@ParameterizedTest()
	@EnumSource(SignatureAlgorithm.class)
	void verificationFailForTamperedHeaderToken(SignatureAlgorithm alternativeSignAlg) {
		SignatureAlgorithm signAlg = SignatureAlgorithm.HS256;
		/* Algorithm must be different otherwise test is not meaningful */
		assumeTrue(alternativeSignAlg != signAlg);

		// Given
		byte[] bytes = new byte[512];
		new Random().nextBytes(bytes);
		SecretKey key = Keys.hmacShaKeyFor(bytes);

		// When
		doAnswer(invocation -> invocation.getArgument(0, JwtBuilder.class).signWith(key, signAlg)).when(tokenSecurity)
				.signBuiltToken(any(JwtBuilder.class));
		doAnswer(invocation -> invocation.getArgument(0, JwtParserBuilder.class).setSigningKey(key)).when(tokenSecurity)
				.setTokenParserKey(any(JwtParserBuilder.class));
		String token = tokenHandle.createJsonWebToken(customUserDetails, expiration, JwtScopeClaim.ACCESS);
		String tamperedHeader = Base64
				.encodeBytes(String.format("{\"alg\":\"%s\"}", alternativeSignAlg.toString()).getBytes());
		String tamperedToken = token.replaceFirst(".+?\\.", tamperedHeader + ".");

		// Then
		assertThatThrownBy(() -> tokenHandle.isValidJwt(tamperedToken, JwtScopeClaim.ACCESS)).isInstanceOf(JwtException.class);
	}

	@RepeatedTest(value = 3)
	void verificationFailForTamperedPayloadToken() throws NoSuchAlgorithmException {
		// Given
		String token = tokenHandle.createJsonWebToken(customUserDetails, expiration, JwtScopeClaim.ACCESS);

		String base64JwtChars = "0123456789abcdefghijklmnopqrstuvwxyz=-_ABCDEFGHIJKLMNOPQRSTUVWXYZ";
		SecureRandom secureRandom = SecureRandom.getInstanceStrong();
		String[] tokenSection = token.split("\\.");
		tokenSection[1] = secureRandom.ints(tokenSection[1].length(), 0, base64JwtChars.length())
				.mapToObj(i -> base64JwtChars.charAt(i))
				.collect(StringBuilder::new, StringBuilder::append, StringBuilder::append).toString();
		String tamperedWithToken = String.join(".", tokenSection);

		// When & Then
		assertThatThrownBy(() -> tokenHandle.isValidJwt(tamperedWithToken, JwtScopeClaim.ACCESS)).isInstanceOf(SignatureException.class);
	}

}
