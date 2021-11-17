package com.webster.msauth.controller;

import static org.junit.Assume.assumeTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.doReturn;

import java.security.SecureRandom;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Optional;
import java.util.stream.Stream;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.boot.autoconfigure.jdbc.DataSourceTransactionManagerAutoConfiguration;
import org.springframework.boot.autoconfigure.orm.jpa.HibernateJpaAutoConfiguration;
import org.springframework.boot.test.autoconfigure.web.reactive.AutoConfigureWebTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.web.reactive.server.WebTestClient;

import com.webster.msauth.constants.EndpointConstants;
import com.webster.msauth.constants.ExternConfigValidationConstants;
import com.webster.msauth.constants.ValidationConstants;
import com.webster.msauth.dto.LoginUserDTO;
import com.webster.msauth.dto.RefreshTokenDTO;
import com.webster.msauth.dto.RegisterUserDTO;
import com.webster.msauth.models.RefreshToken;
import com.webster.msauth.models.User;
import com.webster.msauth.repository.RefreshTokenRepository;
import com.webster.msauth.repository.UserRepository;
import com.webster.msauth.token.JwtSecurity;
import com.webster.msauth.token.OpaqueTokenHandle;

import io.jsonwebtoken.JwtBuilder;
import io.jsonwebtoken.SignatureAlgorithm;
import net.minidev.json.JSONObject;
import net.minidev.json.parser.JSONParser;
import net.minidev.json.parser.ParseException;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@EnableAutoConfiguration(exclude = { DataSourceAutoConfiguration.class,
		DataSourceTransactionManagerAutoConfiguration.class, HibernateJpaAutoConfiguration.class })
@AutoConfigureWebTestClient
class AuthenticationControllerTest {
	@Autowired
	private PasswordEncoder passwordEncoder;
	@MockBean
	private UserRepository userRepositoryMock;
	@MockBean
	private RefreshTokenRepository refreshTokenRepositoryMock;
	@MockBean
	private User userMock;
	@SpyBean
	private JwtSecurity tokenSecuritySpy;
	@Autowired
	private WebTestClient webClient;

	@Nested
	@TestInstance(TestInstance.Lifecycle.PER_CLASS)
	class RegistrationTest {
		@BeforeEach
		public void setUp() {
			doReturn(Optional.ofNullable(null)).when(userRepositoryMock).findByUsername(any(String.class));
			doAnswer(invocation -> invocation.getArgument(0, User.class)).when(userRepositoryMock)
					.save(any(User.class));
		}

		@Test
		public void registration400BadRequestForNoBody() {
			webClient.post().uri(EndpointConstants.REGISTRATION).contentType(MediaType.APPLICATION_JSON).exchange()
					.expectStatus().isBadRequest();
		}

		@Test
		public void registration400BadRequestForEmptyBody() {
			webClient.post().uri(EndpointConstants.REGISTRATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new RegisterUserDTO()).exchange().expectStatus().isBadRequest();
		}

		@ParameterizedTest
		@NullAndEmptySource
		@MethodSource
		public void registration400BadRequestForUsernameConstraintViolation(String email) {
			webClient.post().uri(EndpointConstants.REGISTRATION).contentType(MediaType.APPLICATION_JSON).bodyValue(
					new RegisterUserDTO(email, TestConstants.VALID_PASSWORD_ONE, TestConstants.VALID_PASSWORD_ONE))
					.exchange().expectStatus().isBadRequest();
		}

		@ParameterizedTest
		@NullAndEmptySource
		@MethodSource
		public void registration400BadRequestForPasswordConstraintViolation(String password) {
			webClient.post().uri(EndpointConstants.REGISTRATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new RegisterUserDTO(TestConstants.VALID_EMAIL_ADDRESS, password, password)).exchange()
					.expectStatus().isBadRequest();
		}

		@Test
		public void registration400BadRequestForUnmatchingPasswords() {
			webClient.post().uri(EndpointConstants.REGISTRATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new RegisterUserDTO(TestConstants.VALID_EMAIL_ADDRESS, TestConstants.VALID_PASSWORD_ONE,
							TestConstants.VALID_PASSWORD_TWO))
					.exchange().expectStatus().isBadRequest();
		}

		@Test
		public void registration201CreatedForValidUserInputUsernameNotYetTaken() {
			webClient.post().uri(EndpointConstants.REGISTRATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new RegisterUserDTO(TestConstants.VALID_EMAIL_ADDRESS, TestConstants.VALID_PASSWORD_ONE,
							TestConstants.VALID_PASSWORD_ONE))
					.exchange().expectStatus().isCreated();
		}

		@Test
		public void registration409ConflictForValidUserInputUsernameAlreadyTaken() {
			doReturn(Optional.ofNullable(userMock)).when(userRepositoryMock).findByUsername(any(String.class));
			webClient.post().uri(EndpointConstants.REGISTRATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new RegisterUserDTO(TestConstants.VALID_EMAIL_ADDRESS, TestConstants.VALID_PASSWORD_TWO,
							TestConstants.VALID_PASSWORD_TWO))
					.exchange().expectStatus().isEqualTo(HttpStatus.CONFLICT);
		}

		private Stream<String> registration400BadRequestForPasswordConstraintViolation() {
			return Stream.of(TestConstants.INVALID_PASSWORD_TOO_SHORT, TestConstants.INVALID_PASSWORD_TOO_LONG,
					TestConstants.INVALID_PASSWORD_HAS_WHITESPACE, TestConstants.INVALID_PASSWORD_HAS_ALPHABET_SEQUENCE,
					TestConstants.INVALID_PASSWORD_HAS_NUMERIC_SEQUENCE,
					TestConstants.INVALID_PASSWORD_HAS_QWERTY_SEQUENCE, TestConstants.INVALID_ONE_CHARACTER_CONSTRAINT,
					TestConstants.INVALID_TWO_CHARACTERS_CONSTRAINT);
		}

		private Stream<String> registration400BadRequestForUsernameConstraintViolation() {
			return Stream.of(TestConstants.INVALID_EMAIL_TOO_SHORT, TestConstants.INVALID_EMAIL_TOO_LONG,
					TestConstants.INVALID_EMAIL_NO_AT, TestConstants.INVALID_EMAIL_HAS_WHITESPACE,
					TestConstants.INVALID_EMAIL_FORBIDDEN_CHARACTERS);
		}
	}

	@Nested
	class AuthenticationTest {
		@BeforeEach
		public void setUp() {
			doAnswer(invocation -> {
				doReturn(invocation.getArgument(0, String.class)).when(userMock).getUsername();
				return Optional.of(userMock);
			}).when(userRepositoryMock).findByUsername(any(String.class));
			doAnswer(invocation -> invocation.getArgument(0, User.class)).when(userRepositoryMock)
					.save(any(User.class));
			doAnswer(invocation -> invocation.getArgument(0, RefreshToken.class)).when(refreshTokenRepositoryMock)
					.save(any(RefreshToken.class));
		}

		@Test
		public void authentication400BadRequestForNoBody() {
			webClient.post().uri(EndpointConstants.AUTHENTICATION).contentType(MediaType.APPLICATION_JSON).exchange()
					.expectStatus().isBadRequest();
		}

		@Test
		public void authentication400BadRequestForEmptyBody() {
			webClient.post().uri(EndpointConstants.AUTHENTICATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new LoginUserDTO()).exchange().expectStatus().isBadRequest();
		}

		@ParameterizedTest
		@NullAndEmptySource
		public void authentication400BadRequestForMissingOrBlankUsername(String username) {
			webClient.post().uri(EndpointConstants.AUTHENTICATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new LoginUserDTO(username, TestConstants.VALID_PASSWORD_ONE)).exchange().expectStatus()
					.isBadRequest();
		}

		@Test
		public void authentication400BadRequestForUsernameConstraintViolation() {
			webClient.post().uri(EndpointConstants.AUTHENTICATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new LoginUserDTO(TestConstants.INVALID_EMAIL_TOO_LONG, TestConstants.VALID_PASSWORD_ONE))
					.exchange().expectStatus().isBadRequest();
		}

		@Test
		public void authentication400BadRequestForPasswordConstraintViolation() {
			webClient.post().uri(EndpointConstants.AUTHENTICATION).contentType(MediaType.APPLICATION_JSON).bodyValue(
					new LoginUserDTO(TestConstants.VALID_EMAIL_ADDRESS, TestConstants.INVALID_PASSWORD_TOO_LONG))
					.exchange().expectStatus().isBadRequest();
		}

		@ParameterizedTest
		@NullAndEmptySource
		public void authentication400BadRequestForMissingOrBlankPassword(String password) {
			webClient.post().uri(EndpointConstants.AUTHENTICATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new LoginUserDTO(TestConstants.VALID_EMAIL_ADDRESS, password)).exchange().expectStatus()
					.isBadRequest();
		}

		@Test
		public void authentication401UnauthorizedForInexistentUsername() {
			doReturn(Optional.ofNullable(null)).when(userRepositoryMock).findByUsername(any(String.class));

			webClient.post().uri(EndpointConstants.AUTHENTICATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new LoginUserDTO(TestConstants.VALID_EMAIL_ADDRESS, TestConstants.VALID_PASSWORD_TWO))
					.exchange().expectStatus().isUnauthorized();
		}

		@Test
		public void authentication401UnauthorizedForBadCredentials() {
			doReturn(passwordEncoder.encode(TestConstants.VALID_PASSWORD_ONE)).when(userMock).getPassword();

			webClient.post().uri(EndpointConstants.AUTHENTICATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new LoginUserDTO(TestConstants.VALID_EMAIL_ADDRESS, TestConstants.VALID_PASSWORD_TWO))
					.exchange().expectStatus().isUnauthorized();
		}

		@Test
		public void authentication200OKForCorrectCredentials() {
			String password = TestConstants.VALID_PASSWORD_ONE;
			doReturn(passwordEncoder.encode(password)).when(userMock).getPassword();

			webClient.post().uri(EndpointConstants.AUTHENTICATION).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new LoginUserDTO(TestConstants.VALID_EMAIL_ADDRESS, password)).exchange().expectStatus()
					.isOk().expectBody().jsonPath("$.accessToken").exists().jsonPath("$.refreshToken").exists();
		}
	}

	@Nested
	class AuthorizationTest {
		private String tokenType;
		private String accessToken;

		@BeforeEach
		public void setUp() throws ParseException {
			JSONObject response = makeSuccessfulLoginPOSTRequest();
			tokenType = getValueOf("type", response);
			accessToken = getValueOf("accessToken", response);
		}

		@Test
		public void authorization400BadRequestForMissingHeader() {
			webClient.post().uri(EndpointConstants.AUTHORIZATION).contentType(MediaType.APPLICATION_JSON).exchange()
					.expectStatus().isBadRequest();
		}

		@Test
		public void authorization400BadRequestForMissingAccessTokenTypePrefix() {
			webClient.post().uri(EndpointConstants.AUTHORIZATION).contentType(MediaType.APPLICATION_JSON)
					.header(EndpointConstants.AUTHORIZATION_HEADER, accessToken).exchange().expectStatus()
					.isBadRequest();
		}

		@Test
		public void authorization401UnauthorizedForModifiedAccessTokenHeader() throws ParseException {
			String algorithmHeaderKey = "alg";
			String[] tokenPieces = accessToken.split("\\.");

			assumeTrue(tokenPieces.length == 3);

			JSONObject jsonObject = (JSONObject) new JSONParser(JSONParser.MODE_JSON_SIMPLE)
					.parse(Base64.getUrlDecoder().decode(tokenPieces[0]));

			SignatureAlgorithm currentAlg = SignatureAlgorithm.forName(jsonObject.getAsString(algorithmHeaderKey));
			List<SignatureAlgorithm> allAlgs = Arrays.asList(SignatureAlgorithm.values());
			Collections.shuffle(allAlgs);

			SignatureAlgorithm alternativeAlg = allAlgs.stream()
					.filter(alg -> !alg.getValue().equals(currentAlg.getValue())
							&& alg.getFamilyName().equals(currentAlg.getFamilyName()))
					.findFirst().get();

			jsonObject.put(algorithmHeaderKey, alternativeAlg);
			String modifiedHeader = Base64.getUrlEncoder().encodeToString(jsonObject.toJSONString().getBytes());
			String modifiedToken = String.format("%s.%s.%s", modifiedHeader, tokenPieces[1], tokenPieces[2]);

			webClient.post().uri(EndpointConstants.AUTHORIZATION).contentType(MediaType.APPLICATION_JSON)
					.header(EndpointConstants.AUTHORIZATION_HEADER, String.format("%s %s", tokenType, modifiedToken))
					.exchange().expectStatus().isUnauthorized();
		}

		@Test
		public void authorization401UnauthorizedForModifiedAccessTokenPayload() throws ParseException {
			String expirationPayloadKey = "exp";
			String[] tokenPieces = accessToken.split("\\.");

			assumeTrue(tokenPieces.length == 3);

			JSONObject jsonObject = (JSONObject) new JSONParser(JSONParser.MODE_JSON_SIMPLE)
					.parse(Base64.getUrlDecoder().decode(tokenPieces[1]));

			Date modifiedExpiration = new Date(System.currentTimeMillis() + 10000000);
			jsonObject.put(expirationPayloadKey, modifiedExpiration.getTime());

			String modifiedPayload = Base64.getUrlEncoder().encodeToString(jsonObject.toJSONString().getBytes());
			String modifiedToken = String.format("%s.%s.%s", tokenPieces[0], modifiedPayload, tokenPieces[2]);

			webClient.post().uri(EndpointConstants.AUTHORIZATION).contentType(MediaType.APPLICATION_JSON)
					.header(EndpointConstants.AUTHORIZATION_HEADER, String.format("%s %s", tokenType, modifiedToken))
					.exchange().expectStatus().isUnauthorized();
		}

		@Test
		public void authorization401UnauthorizedForExpiredAccessToken() throws InterruptedException, ParseException {
			doAnswer(invocation -> {
				invocation.getArguments()[0] = invocation.getArgument(0, JwtBuilder.class).setExpiration(new Date());
				return invocation.callRealMethod();
			}).when(tokenSecuritySpy).signBuiltToken(any(JwtBuilder.class));

			String rapidExpirationAccessToken = getValueOf("accessToken", makeSuccessfulLoginPOSTRequest());
			Thread.sleep(5);

			webClient.post().uri(EndpointConstants.AUTHORIZATION).contentType(MediaType.APPLICATION_JSON)
					.header(EndpointConstants.AUTHORIZATION_HEADER,
							String.format("%s %s", tokenType, rapidExpirationAccessToken))
					.exchange().expectStatus().isUnauthorized();
		}

		@Test
		public void authorization200OKForValidAccessToken() {
			webClient.post().uri(EndpointConstants.AUTHORIZATION).contentType(MediaType.APPLICATION_JSON)
					.header(EndpointConstants.AUTHORIZATION_HEADER, String.format("%s %s", tokenType, accessToken))
					.exchange().expectStatus().isOk();
		}
	}

	@Nested
	class RefreshmentTest {
		@Test
		public void refreshment400BadRequestForNoBody() {
			webClient.post().uri(EndpointConstants.REFRESHMENT).contentType(MediaType.APPLICATION_JSON).exchange()
					.expectStatus().isBadRequest();
		}

		@Test
		public void refreshment400BadRequestForEmptyBody() {
			webClient.post().uri(EndpointConstants.REFRESHMENT).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new RefreshTokenDTO()).exchange().expectStatus().isBadRequest();
		}

		@ParameterizedTest
		@NullAndEmptySource
		public void refreshment400BadRequestForMissingOrBlankRefreshToken(String refreshToken) {
			webClient.post().uri(EndpointConstants.REFRESHMENT).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new RefreshTokenDTO(refreshToken)).exchange().expectStatus().isBadRequest();
		}

		@Test
		public void refreshment400BadRequestForRefreshTokenTooLong() {
			SecureRandom randomSecurer = new SecureRandom();
			byte[] byteArray = new byte[ValidationConstants.REFRESH_TOKEN_MAX_LENGTH + 1];
			randomSecurer.nextBytes(byteArray);
			String refreshToken = Base64.getEncoder().encodeToString(byteArray);

			webClient.post().uri(EndpointConstants.REFRESHMENT).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new RefreshTokenDTO(refreshToken)).exchange().expectStatus().isBadRequest();
		}

		@Test
		public void refreshment401UnauthorizedForInexistentRefreshToken() {
			SecureRandom randomSecurer = new SecureRandom();
			byte[] byteArray = new byte[OpaqueTokenHandle.OPAQUE_TOKEN_BYTE_LENGTH];
			randomSecurer.nextBytes(byteArray);
			String refreshToken = Base64.getEncoder().encodeToString(byteArray);

			doReturn(Optional.ofNullable(null)).when(refreshTokenRepositoryMock).findById(refreshToken);

			webClient.post().uri(EndpointConstants.REFRESHMENT).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new RefreshTokenDTO(refreshToken)).exchange().expectStatus().isUnauthorized();
		}

		@Test
		public void refreshment200ForValidRefreshToken() throws ParseException {
			JSONObject response = makeSuccessfulLoginPOSTRequest();
			String refreshToken = getValueOf("refreshToken", response);

			doReturn(Optional.of(new RefreshToken(refreshToken, TestConstants.VALID_EMAIL_ADDRESS)))
					.when(refreshTokenRepositoryMock).findById(refreshToken);
			doAnswer(invocation -> {
				doReturn(invocation.getArgument(0, String.class)).when(userMock).getUsername();
				return Optional.of(userMock);
			}).when(userRepositoryMock).findByUsername(any(String.class));
			doReturn(new String()).when(userMock).getPassword();
			doReturn(List.of()).when(userMock).getRoles();

			webClient.post().uri(EndpointConstants.REFRESHMENT).contentType(MediaType.APPLICATION_JSON)
					.bodyValue(new RefreshTokenDTO(refreshToken)).exchange().expectStatus().isOk();
		}
	}

	private JSONObject makeSuccessfulLoginPOSTRequest() throws ParseException {
		doAnswer(invocation -> {
			doReturn(invocation.getArgument(0, String.class)).when(userMock).getUsername();
			return Optional.of(userMock);
		}).when(userRepositoryMock).findByUsername(any(String.class));
		doAnswer(invocation -> invocation.getArgument(0, User.class)).when(userRepositoryMock).save(any(User.class));
		doAnswer(invocation -> invocation.getArgument(0, RefreshToken.class)).when(refreshTokenRepositoryMock)
				.save(any(RefreshToken.class));

		String password = TestConstants.VALID_PASSWORD_ONE;
		doReturn(passwordEncoder.encode(password)).when(userMock).getPassword();

		String response = new String(
				webClient.post().uri(EndpointConstants.AUTHENTICATION).contentType(MediaType.APPLICATION_JSON)
						.bodyValue(new LoginUserDTO(TestConstants.VALID_EMAIL_ADDRESS, password)).exchange()
						.expectBody().returnResult().getResponseBody());

		JSONParser parser = new JSONParser(JSONParser.MODE_JSON_SIMPLE);
		JSONObject jsonObject = (JSONObject) parser.parse(response);

		return jsonObject;
	}

	private String getValueOf(String key, JSONObject jsonObject) {
		return (String) jsonObject.entrySet().stream().filter(entry -> entry.getKey().equals(key)).findFirst().get()
				.getValue();
	}
}
