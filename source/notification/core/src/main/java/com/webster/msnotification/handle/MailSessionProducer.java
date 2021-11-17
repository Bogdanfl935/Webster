package com.webster.msnotification.handle;

import java.util.Properties;

import javax.mail.Session;

import org.springframework.stereotype.Component;

import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@Component
@RequiredArgsConstructor
public class MailSessionProducer {
	@NonNull
	private MailSessionConfig mailSessionConfig;

	public Session produceSession() {
		Properties props = new Properties();
		
		props.put("mail.smtp.host", mailSessionConfig.getHost());
		props.put("mail.smtp.ssl.trust", mailSessionConfig.getHost());
		props.put("mail.smtp.auth", true);
		props.put("mail.smtp.starttls.enable", true);
		props.put("mail.smtp.port", mailSessionConfig.getPort());

		return Session.getDefaultInstance(props, mailSessionConfig.getAuthenticator());
	}
}
