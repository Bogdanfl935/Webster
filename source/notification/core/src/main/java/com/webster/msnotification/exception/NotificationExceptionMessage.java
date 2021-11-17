package com.webster.msnotification.exception;

import javax.validation.constraints.NotNull;

import lombok.Setter;

public enum NotificationExceptionMessage {
	EMAIL_DELIVERY_FAILED("Could not deliver email notification to %s");
	
	private String errorMessage;
	@Setter
	@NotNull
	private String errorParameter;

	private NotificationExceptionMessage(String errorMessage) {
		this.errorMessage = errorMessage;
		this.errorParameter = new String();
	}

	public String getErrorMessage() {
		return String.format(errorMessage, errorParameter);
	}
}
