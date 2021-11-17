package com.webster.msnotification.controller;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.times;

import java.io.IOException;

import javax.mail.Message;
import javax.mail.MessagingException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.test.autoconfigure.web.reactive.AutoConfigureWebTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.reactive.server.WebTestClient;

import com.webster.msnotification.constants.EndpointConstants;
import com.webster.msnotification.dto.EmailContentDTO;
import com.webster.msnotification.dto.EmailTokenDTO;
import com.webster.msnotification.handle.MailHandle;
import com.webster.msnotification.renderer.HtmlMailContentRenderer;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@EnableAutoConfiguration
@AutoConfigureWebTestClient
class EmailNotificationController200Test {
	@SpyBean
	private HtmlMailContentRenderer htmlMailContentRenderer;
	@Captor
	private ArgumentCaptor<String> endpointCaptor;
	@Captor
	private ArgumentCaptor<EmailContentDTO> emailContentDtoCaptor;
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
	public void endpointRequest200OKForValidEmailTokenDTO(String endpoint) throws MessagingException, IOException {
		// When
		webClient.post().uri(endpoint).contentType(MediaType.APPLICATION_JSON)
				.bodyValue(new EmailTokenDTO(TestConstants.VALID_TOKEN, TestConstants.VALID_EMAIL_ADDRESS)).exchange()
				.expectStatus().isOk();

		Mockito.verify(htmlMailContentRenderer).renderContent(endpointCaptor.capture(), any(String.class));
		Mockito.verify(mailHandle).composeMimeMessage(emailContentDtoCaptor.capture());

		Document htmlDocument = Jsoup.parse(emailContentDtoCaptor.getValue().getContent());
		Elements links = htmlDocument.select(HtmlTestConstants.LINK);

		// Then
		Mockito.verify(mailHandle, times(1)).sendMessage(any(Message.class));
		assertThat(links.first().attr(HtmlTestConstants.LINK_HREF)).isEqualTo(endpointCaptor.getValue());
	}
}
