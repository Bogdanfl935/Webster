package com.webster.msnotification.handle;

import javax.mail.Authenticator;
import javax.mail.PasswordAuthentication;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Positive;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.webster.msnotification.constants.ExternConfigConstants;

import lombok.Getter;

@Component
public class MailSessionConfig {
	@Value(ExternConfigConstants.MAIL_SESSION_HOST)
	@NotNull
	@Getter
	private String host;
	@Value(ExternConfigConstants.MAIL_SESSION_PORT)
	@NotNull
	@Getter
	@Positive
	private Integer port;
	@Value(ExternConfigConstants.MAIL_SESSION_USERNAME)
	@NotNull
	private String username;
	@Value(ExternConfigConstants.MAIL_SESSION_PASSWORD)
	@NotNull
	private String password;

	public Authenticator getAuthenticator() {
		return new Authenticator() {
			protected PasswordAuthentication getPasswordAuthentication() {
				return new PasswordAuthentication(username, password);
			}
		};
	}
}
