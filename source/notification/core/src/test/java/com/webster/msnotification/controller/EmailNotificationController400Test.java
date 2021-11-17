package com.webster.msnotification.controller;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doNothing;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

import javax.mail.Message;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.test.autoconfigure.web.reactive.AutoConfigureWebTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.reactive.server.WebTestClient;

import com.webster.msnotification.constants.EndpointConstants;
import com.webster.msnotification.dto.EmailTokenDTO;
import com.webster.msnotification.handle.MailHandle;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@EnableAutoConfiguration
@AutoConfigureWebTestClient
class EmailNotificationController400Test {
	@SpyBean
	private MailHandle mailHandle;
	@Autowired
	private WebTestClient webClient;

	@BeforeEach
	void setUp() throws Exception {
		doNothing().when(mailHandle).sendMessage(any(Message.class));
	}

	@ParameterizedTest
	@ValueSource(strings = { EndpointConstants.EMAIL_CONFIRMATION, EndpointConstants.EMAIL_PASSWORD_RESET })
	public void endpointRequest400BadRequestForNoBody(String endpoint) {
		webClient.post().uri(endpoint).contentType(MediaType.APPLICATION_JSON).exchange().expectStatus().isBadRequest();
	}

	@ParameterizedTest
	@ValueSource(strings = { EndpointConstants.EMAIL_CONFIRMATION, EndpointConstants.EMAIL_PASSWORD_RESET })
	public void endpointRequest400BadRequestForEmpty(String endpoint) {
		webClient.post().uri(endpoint).contentType(MediaType.APPLICATION_JSON).exchange().expectStatus().isBadRequest();
	}

	@ParameterizedTest
	@MethodSource
	public void endpointRequest400BadRequestForRecipientConstraintViolation(String endpoint, String email) {
		webClient.post().uri(endpoint).contentType(MediaType.APPLICATION_JSON)
				.bodyValue(new EmailTokenDTO(TestConstants.VALID_TOKEN, email)).exchange().expectStatus()
				.isBadRequest();
	}

	@ParameterizedTest
	@MethodSource
	public void endpointRequest400BadRequestForTokenConstraintViolation(String endpoint, String token) {
		webClient.post().uri(endpoint).contentType(MediaType.APPLICATION_JSON)
				.bodyValue(new EmailTokenDTO(token, TestConstants.VALID_EMAIL_ADDRESS)).exchange().expectStatus()
				.isBadRequest();
	}

	private static Stream<Arguments> endpointRequest400BadRequestForRecipientConstraintViolation() {
		List<String> invalidEmailList = List.of(TestConstants.INVALID_EMAIL_TOO_SHORT,
				TestConstants.INVALID_EMAIL_TOO_LONG, TestConstants.INVALID_EMAIL_NO_AT,
				TestConstants.INVALID_EMAIL_HAS_WHITESPACE, TestConstants.INVALID_EMAIL_FORBIDDEN_CHARACTERS);
		List<String> endpointList = EmailNotificationController400Test.getEndpointsList();
		List<Arguments> argumentList = new ArrayList<Arguments>();

		/* Special edge cases */
		for (String endpoint : endpointList) {
			argumentList.add(Arguments.of(endpoint, TestConstants.NULL));
			argumentList.add(Arguments.of(endpoint, TestConstants.EMPTY));
		}

		for (String email : invalidEmailList) {
			for (String endpoint : endpointList) {
				argumentList.add(Arguments.of(endpoint, email));
			}
		}
		return argumentList.stream();
	}

	private static Stream<Arguments> endpointRequest400BadRequestForTokenConstraintViolation() {
		List<String> endpointList = EmailNotificationController400Test.getEndpointsList();
		List<Arguments> argumentList = new ArrayList<Arguments>();

		/* Special edge cases */
		for (String endpoint : endpointList) {
			argumentList.add(Arguments.of(endpoint, TestConstants.NULL));
			argumentList.add(Arguments.of(endpoint, TestConstants.EMPTY));
		}
		return argumentList.stream();
	}

	private static List<String> getEndpointsList() {
		return List.of(EndpointConstants.EMAIL_CONFIRMATION, EndpointConstants.EMAIL_PASSWORD_RESET);
	}

}
