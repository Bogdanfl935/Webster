package com.webster.msnotification.constants;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor(access = AccessLevel.PRIVATE)
public enum EmailTarget {
	CONFIRMATION(EmailConstants.ACCOUNT_CONFIRMATION_SUBJECT, RenderingConstants.EMAIL_CONFIRMATION_FILENAME),

	PASSWORD_RESET(EmailConstants.PASSWORD_RESET_SUBJECT, RenderingConstants.EMAIL_PASSWORD_RESET_FILENAME);

	@Getter
	private final String emailSubject;
	@Getter
	private final String emailContentTemplatePath;
}
